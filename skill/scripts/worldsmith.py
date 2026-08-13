#!/usr/bin/env python3
"""worldsmith - scaffolding, indexing and mechanical consistency checks for a
homebrew TTRPG world stored as markdown files.

Standard library only. Run from the world root, or pass --root.

    worldsmith.py init <path>
    worldsmith.py new --type faction --name "The Ashen Covenant"
    worldsmith.py reindex
    worldsmith.py audit [--json]
    worldsmith.py find "kellamar"

Part of the Worldsmith skill by QuothGM. MIT licensed.
"""

import argparse
import difflib
import json
import os
import re
import sys
from datetime import date

# Genre-neutral taxonomy. These names carry no assumptions about setting or
# system: "powers" covers gods, patrons, corporations or cosmic forces, and
# "systems" covers magic, technology, psionics or whatever the strange runs on.
TYPES = {
    "region": "reg", "place": "plc", "faction": "fac", "character": "npc",
    "culture": "cul", "power": "pwr", "event": "evt", "item": "itm",
    "creature": "crt", "system": "sys", "campaign": "cmp", "session": "ses",
}
TYPE_DIRS = {
    "region": "canon/regions", "place": "canon/places",
    "faction": "canon/factions", "character": "canon/characters",
    "culture": "canon/cultures", "power": "canon/powers",
    "event": "canon/events", "item": "canon/items",
    "creature": "canon/creatures", "system": "canon/systems",
    "campaign": "play/campaigns", "session": "play/sessions",
}
STATUSES = ("canon", "provisional", "proposed", "retired")
PLAY_STATUSES = ("prepped", "run", "harvested")
REQUIRED = ("id", "name", "type", "status")

# --------------------------------------------------------------------------- io

def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def parse_frontmatter(text):
    """Minimal YAML-subset parser: scalars, inline lists, and block lists."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw, body = text[3:end], text[end + 4:]
    data, key = {}, None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith("- ") and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(line.split("- ", 1)[1].strip().strip("\"'"))
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [v.strip().strip("\"'") for v in inner.split(",") if v.strip()]
        elif val == "":
            data[key] = []
        else:
            data[key] = val.strip("\"'")
    return data, body


def canon_files(root):
    out = []
    for base in ("canon", "play", "proposals"):
        d = os.path.join(root, base)
        for dirpath, _, names in os.walk(d):
            for n in sorted(names):
                if n.endswith(".md"):
                    out.append(os.path.join(dirpath, n))
    return out


def load_entities(root):
    ents = []
    for path in canon_files(root):
        try:
            text = open(path, encoding="utf-8").read()
        except OSError:
            continue
        fm, body = parse_frontmatter(text)
        rel = os.path.relpath(path, root)
        ents.append({"path": rel, "fm": fm, "body": body, "text": text})
    return ents


def summary_line(body):
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("> "):
            return line[2:].strip()
    return ""


def sections(body):
    """Return {heading_lower: text} for '## ' sections (any heading level)."""
    out, cur, buf = {}, None, []
    for line in body.splitlines():
        m = re.match(r"^#{2,3}\s+(.+)$", line)
        if m:
            if cur:
                out[cur] = "\n".join(buf)
            cur, buf = m.group(1).strip().lower(), []
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf)
    return out

# ------------------------------------------------------------------------ init

WORLD_MD = """# {name}

> One or two sentences: the pitch you'd give a friend deciding whether to play.

## Form and system
What kind of world this is, and what game is being run in it.
-

## Tone pillars
What the table should feel. These are constraints, not decoration.
-

## The strange thing

What is true here that would not be true in an ordinary world of this kind?
Bullets here become invariants too.

-

## Hard rules

Things that are always true and never get quietly bent. Every bullet here
becomes an invariant in CANON-INDEX.md, so keep prose out of the list.

-

## What this world is NOT

Forms, tropes, tones, and content ruled out. Every future proposal gets
checked against this list, so be blunt.

-

## Scale of play
Where the campaign starts and how big the map that matters is.
-
"""

STYLE_MD = """# Style

## Names the GM already likes
-

## Phonology by culture
Sounds, syllable shapes, and common endings, derived from the names above.
-

## Vocabulary
Words and registers that fit this world:
Words that don't (period slips, tonal misfits, borrowed jargon):

## Prose register
How lore and read-aloud text should sound.
-
"""

OPEN_MD = """# Open questions

The queue of things the world hasn't answered yet. Brainstorming pulls from
here so it has somewhere to start; play answers these better than prep does.

| # | Question | Touches | Blocking play? | Status |
|---|----------|---------|----------------|--------|
"""

LOG_MD = """# Canon log

Append-only. What was established, when, and where it came from. Provenance is
what later tells you whether a fact is safe to change.

| Date | Established | Source |
|------|-------------|--------|
"""


def cmd_init(args):
    root = os.path.abspath(args.path)
    name = args.name or os.path.basename(root).replace("-", " ").title()
    for d in set(TYPE_DIRS.values()) | {"handouts", "proposals"}:
        os.makedirs(os.path.join(root, d), exist_ok=True)
    files = {
        "WORLD.md": WORLD_MD.format(name=name),
        "STYLE.md": STYLE_MD,
        "OPEN-QUESTIONS.md": OPEN_MD,
        "CANON-LOG.md": LOG_MD,
        "CANON-INDEX.md": "# Canon index\n\n_Run `worldsmith.py reindex` to populate._\n",
    }
    for fn, content in files.items():
        p = os.path.join(root, fn)
        if not os.path.exists(p):
            open(p, "w", encoding="utf-8").write(content)
    print("Initialized world at %s" % root)
    print("Next: fill in WORLD.md through the seed interview. Do not pre-populate canon.")
    return 0

# ------------------------------------------------------------------------- new

ENTITY_TMPL = """---
id: {id}
name: {name}
type: {type}
status: {status}
secrecy: {secrecy}
aliases: []
tags: []
links: []
created: {today}
updated: {today}
---

# {name}

> One-sentence identity. This line goes into CANON-INDEX.md.

## Established facts
- 

## Player knowledge

## GM only

## Relationships

## Open questions

## Change log
- {today} — created
"""


def cmd_new(args):
    root = os.path.abspath(args.root)
    t = args.type.lower()
    if t not in TYPES:
        print("Unknown type %r. Known: %s" % (t, ", ".join(sorted(TYPES))), file=sys.stderr)
        return 2
    slug = slugify(args.name)
    eid = "%s-%s" % (TYPES[t], slug)
    d = os.path.join(root, TYPE_DIRS[t])
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, slug + ".md")
    if os.path.exists(path) and not args.force:
        print("Already exists: %s" % os.path.relpath(path, root), file=sys.stderr)
        return 1
    open(path, "w", encoding="utf-8").write(ENTITY_TMPL.format(
        id=eid, name=args.name, type=t, status=args.status,
        secrecy=args.secrecy, today=date.today().isoformat()))
    print(os.path.relpath(path, root))
    return 0

# --------------------------------------------------------------------- reindex

INVARIANT_RE = re.compile(r"^\s*[-*]\s*\(!\)\s*(.+)$")


def newest_source_mtime(root):
    newest = 0.0
    for p in canon_files(root) + [os.path.join(root, f) for f in ("WORLD.md", "STYLE.md")]:
        ap = p if os.path.isabs(p) else os.path.join(root, p)
        if os.path.exists(ap):
            newest = max(newest, os.path.getmtime(ap))
    return newest


def cmd_reindex(args):
    root = os.path.abspath(args.root)
    ents = load_entities(root)
    world_name = "the world"
    hard_rules, invariants = [], []

    wp = os.path.join(root, "WORLD.md")
    if os.path.exists(wp):
        wtext = open(wp, encoding="utf-8").read()
        m = re.search(r"(?m)^#\s+(.+)$", wtext)
        if m:
            world_name = m.group(1).strip()
        wsecs = sections(wtext)
        for head in ("hard rules", "the strange thing"):
            for line in wsecs.get(head, "").splitlines():
                if not re.match(r"^\s*[-*]\s+\S", line):
                    continue  # only real bullets; instructional prose is skipped
                s = line.strip().lstrip("-*").strip()
                if s:
                    hard_rules.append((s, "WORLD.md"))

    for e in ents:
        facts = sections(e["body"]).get("established facts", "")
        for line in facts.splitlines():
            m = INVARIANT_RE.match(line)
            if m:
                invariants.append((m.group(1).strip(), e["path"]))

    by_type = {}
    for e in ents:
        by_type.setdefault(e["fm"].get("type", "untyped"), []).append(e)

    L = ["# Canon index — %s" % world_name, "",
         "_Generated by `worldsmith.py reindex` on %s. %d entities._" % (
             date.today().isoformat(), len(ents)), "",
         "This file is the entry point to the world. Read it at the start of every",
         "session before saying anything about this setting. It is regenerated from",
         "the canon files, so it is never the place to edit a fact — edit the file",
         "it came from and reindex.", ""]

    L += ["## Invariants", "",
          "Load-bearing facts. Changing one of these is a retcon with consequences",
          "across the setting, not an edit. Mark a fact as an invariant by starting",
          "its bullet with `(!)` in the entity file.", ""]
    if hard_rules or invariants:
        for text, src in hard_rules + invariants:
            L.append("- %s  _(%s)_" % (text, src))
    else:
        L.append("_None recorded yet._")
    L.append("")

    L += ["## Entity register", ""]
    for t in sorted(by_type):
        L += ["### %s" % t.title(), "",
              "| Name | id | Status | Identity | Also called | File |",
              "|------|----|--------|----------|-------------|------|"]
        for e in sorted(by_type[t], key=lambda x: x["fm"].get("name", x["path"])):
            fm = e["fm"]
            al = fm.get("aliases", []) or []
            L.append("| %s | `%s` | %s | %s | %s | `%s` |" % (
                fm.get("name", "?"), fm.get("id", "?"), fm.get("status", "?"),
                summary_line(e["body"]).replace("|", "/")[:110],
                ", ".join(str(a) for a in al)[:50], e["path"]))
        L.append("")

    op = os.path.join(root, "OPEN-QUESTIONS.md")
    if os.path.exists(op):
        rows = [l for l in open(op, encoding="utf-8").read().splitlines()
                if l.strip().startswith("|") and "open" in l.lower()]
        L += ["## Open questions (unanswered)", ""]
        L += rows[:20] if rows else ["_None._"]
        L.append("")

    cl = os.path.join(root, "CANON-LOG.md")
    if os.path.exists(cl):
        rows = [l for l in open(cl, encoding="utf-8").read().splitlines()
                if l.strip().startswith("|") and not set(l) <= set("|- ")]
        rows = [r for r in rows if not r.lower().startswith("| date")]
        if rows:
            L += ["## Most recent canon changes", "",
                  "| Date | Established | Source |", "|------|-------------|--------|"]
            L += rows[-8:]
            L.append("")

    open(os.path.join(root, "CANON-INDEX.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    legacy = os.path.join(root, "INDEX.md")
    if os.path.exists(legacy):
        os.remove(legacy)
    print("Indexed %d entities, %d invariants -> CANON-INDEX.md" % (
        len(ents), len(hard_rules) + len(invariants)))
    return 0

# ----------------------------------------------------------------------- audit

def cmd_audit(args):
    root = os.path.abspath(args.root)
    ents = load_entities(root)
    findings = []

    def add(sev, kind, msg, where=""):
        findings.append({"severity": sev, "check": kind, "message": msg, "file": where})

    ids, names = {}, {}
    for e in ents:
        fm, p = e["fm"], e["path"]
        for f in REQUIRED:
            if not fm.get(f):
                add("high", "frontmatter", "missing required field '%s'" % f, p)
        st = fm.get("status")
        if p.startswith("play"):
            if st and st not in PLAY_STATUSES:
                add("low", "frontmatter",
                    "session status %r not one of %s" % (st, ", ".join(PLAY_STATUSES)), p)
        elif st and st not in STATUSES:
            add("medium", "frontmatter", "status %r not one of %s" % (st, ", ".join(STATUSES)), p)
        if p.startswith("canon") and st == "proposed":
            add("high", "canon-gate",
                "status 'proposed' inside canon/ — proposals belong in proposals/ until committed", p)
        eid = fm.get("id")
        if eid:
            if eid in ids:
                add("high", "duplicate-id", "id %r also used by %s" % (eid, ids[eid]), p)
            ids[eid] = p
        nm = fm.get("name")
        if nm:
            names.setdefault(nm.lower(), []).append((nm, p))
        secs = sections(e["body"])
        facts = secs.get("established facts", "")
        if p.startswith("canon") and not [l for l in facts.splitlines()
                                          if l.strip().lstrip("- ").strip()]:
            add("low", "empty", "no established facts recorded yet", p)
        if re.search(r"\bTODO\b|\bTBD\b|\?{3,}", e["text"]):
            add("low", "todo", "contains TODO/TBD marker", p)

    # near-duplicate names
    keys = sorted(names)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if a != b and difflib.SequenceMatcher(None, a, b).ratio() > 0.85:
                add("low", "name-collision",
                    "%r and %r are easy to confuse at the table" % (names[a][0][0], names[b][0][0]),
                    "%s / %s" % (names[a][0][1], names[b][0][1]))

    name_to_id = {}
    for e in ents:
        fm = e["fm"]
        if fm.get("name") and fm.get("id"):
            name_to_id[fm["name"].lower()] = fm["id"]
            for al in fm.get("aliases", []) or []:
                name_to_id[str(al).lower()] = fm["id"]

    # link + wiki-reference resolution, and one-way links
    link_graph = {}
    for e in ents:
        fm, p = e["fm"], e["path"]
        eid = fm.get("id")
        outs = set()
        for target in fm.get("links", []) or []:
            outs.add(target)
            if target not in ids:
                add("medium", "broken-link", "links: -> %r resolves to nothing" % target, p)
        for ref in re.findall(r"\[\[([^\]]+)\]\]", e["body"]):
            ref = ref.strip()
            if ref in ids:
                outs.add(ref)
            elif ref.lower() in name_to_id:
                outs.add(name_to_id[ref.lower()])
            else:
                add("medium", "broken-ref", "[[%s]] matches no entity id, name or alias" % ref, p)
        if eid:
            link_graph[eid] = outs
    play_ids = {e["fm"].get("id") for e in ents if e["path"].startswith("play")}
    for src, outs in link_graph.items():
        if src in play_ids:
            continue  # session notes point at canon; canon does not point back
        for dst in outs:
            if dst in play_ids:
                continue
            if dst in link_graph and src not in link_graph[dst]:
                add("low", "one-way-link",
                    "%s references %s but %s never references back" % (src, dst, dst),
                    ids.get(src, ""))

    # index freshness
    idx_path = os.path.join(root, "CANON-INDEX.md")
    if os.path.exists(idx_path):
        idx = open(idx_path, encoding="utf-8").read()
        for eid, p in ids.items():
            if eid not in idx:
                add("medium", "stale-index", "%s is not in CANON-INDEX.md — run reindex" % eid, p)
        if newest_source_mtime(root) > os.path.getmtime(idx_path) + 1:
            add("medium", "stale-index",
                "canon files changed after the index was built — run reindex", "CANON-INDEX.md")
    else:
        add("high", "stale-index",
            "CANON-INDEX.md missing — run reindex before doing anything else", "")

    # secrecy: gm-only material appearing in handouts
    secret_lines, secret_names = set(), []
    for e in ents:
        gm = sections(e["body"]).get("gm only", "")
        for line in gm.splitlines():
            t = line.strip().lstrip("-*# ").strip()
            if len(t) > 40:
                secret_lines.add(re.sub(r"\s+", " ", t.lower()))
        if str(e["fm"].get("secrecy", "")).lower() == "gm-only" and e["fm"].get("name"):
            secret_names.append((e["fm"]["name"], e["path"]))
    hdir = os.path.join(root, "handouts")
    if os.path.isdir(hdir):
        for dirpath, _, fns in os.walk(hdir):
            for fn in fns:
                hp = os.path.join(dirpath, fn)
                rel = os.path.relpath(hp, root)
                try:
                    htxt = re.sub(r"\s+", " ", open(hp, encoding="utf-8", errors="ignore").read().lower())
                except OSError:
                    continue
                for s in secret_lines:
                    if s in htxt:
                        add("high", "secrecy-leak", "handout repeats GM-only text: %r" % s[:70], rel)
                for nm, src in secret_names:
                    if nm.lower() in htxt:
                        add("high", "secrecy-leak",
                            "handout names gm-only entity %r (%s)" % (nm, src), rel)

    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["check"], f["file"]))
    if args.json:
        print(json.dumps({"entities": len(ents), "findings": findings}, indent=2))
        return 0
    print("Audited %d entities. %d findings.\n" % (len(ents), len(findings)))
    cur = None
    for f in findings:
        if f["severity"] != cur:
            cur = f["severity"]
            print("== %s ==" % cur.upper())
        print("  [%s] %s%s" % (f["check"], f["message"], ("  (%s)" % f["file"]) if f["file"] else ""))
    if not findings:
        print("No mechanical problems found. The judgment pass is still worth doing:")
        print("see the audit playbook (references/audit-playbook.md, or Appendix C")
        print("of the single-file edition): timeline, scale, tone, entity drift.")
    else:
        print("\nThese are mechanical findings only. Do not fix them unilaterally —")
        print("several are usually deliberate. Report them to the GM with options.")
    return 0

# ------------------------------------------------------------------------ find

def cmd_find(args):
    root = os.path.abspath(args.root)
    term = args.term.lower()
    hits = 0
    for e in load_entities(root):
        lines = e["text"].splitlines()
        matched = [(i, l) for i, l in enumerate(lines) if term in l.lower()]
        if not matched:
            continue
        hits += 1
        print("\n--- %s  [%s / %s]" % (e["path"], e["fm"].get("name", "?"),
                                       e["fm"].get("status", "?")))
        for i, l in matched[:8]:
            heading = ""
            for j in range(i, -1, -1):
                if lines[j].startswith("#"):
                    heading = lines[j].lstrip("# ").strip()
                    break
            print("  %-22s | %s" % (heading[:22], l.strip()[:110]))
    if not hits:
        print("No canon file contains %r." % args.term)
        print("That may mean it isn't established, or it's filed under another name.")
        print("Try spelling variants and partial words before concluding anything.")
    return 0

# ------------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="world root (default: cwd)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init"); p.add_argument("path"); p.add_argument("--name")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("new")
    p.add_argument("--type", required=True); p.add_argument("--name", required=True)
    p.add_argument("--status", default="provisional", choices=list(STATUSES))
    p.add_argument("--secrecy", default="mixed", choices=["public", "mixed", "gm-only"])
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new)

    sub.add_parser("reindex").set_defaults(func=cmd_reindex)

    p = sub.add_parser("audit"); p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("find"); p.add_argument("term")
    p.set_defaults(func=cmd_find)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
