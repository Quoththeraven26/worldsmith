# Entity schema

Every canon entity is one markdown file with YAML frontmatter and a fixed set of sections. The rigidity is deliberate: predictable structure is what makes retrieval, auditing, and player-safe export possible without reading everything.

## Frontmatter

```yaml
---
id: fac-ashen-covenant        # required, unique, <type-prefix>-<slug>
name: The Ashen Covenant      # required, the canonical display name
type: faction                 # required, see types below
status: canon                 # required: canon | provisional | proposed | retired
secrecy: mixed                # public | mixed | gm-only
aliases: [The Covenant, the ash-priests]
tags: [religion, antagonist, northern-reach]
links: [reg-thornmarch, npc-solene-var, evt-the-sundering]
created: 2026-08-13
updated: 2026-08-13
---
```

**Type prefixes.** `reg-` region · `plc-` place · `fac-` faction · `npc-` character · `cul-` culture or people · `pwr-` power · `evt-` event · `itm-` item · `crt-` creature · `sys-` system · `cmp-` campaign · `ses-` session.

The taxonomy is deliberately free of setting assumptions. `powers` holds whatever this world treats as a force above ordinary people — gods, patrons, ancestors, a company, an ideology, a machine. `systems` holds whatever it runs on that ours does not — magic, technology, ritual, psionics, the rules of the anomaly. `cultures` holds peoples, whether the difference between them is biological, historical, or invented. A world that needs none of these leaves those shelves empty, which is information in itself.

**status** is the canon gate made durable. `proposed` means the AI or worldbuilder floated it and nobody committed — proposed files live in `proposals/`, never in `canon/`. `provisional` means the worldbuilder committed it but reserves the right to change it; it hasn't survived play yet. `canon` means it's true and changing it is a retcon. `retired` means it was true and no longer is — keep the file, note what replaced it, because retired facts explain player memories.

**secrecy** drives handout generation. `gm-only` files never contribute a word to `handouts/`.

## Sections

```markdown
# The Ashen Covenant

> One-sentence identity. This line is what lands in CANON-INDEX.md, so make it load-bearing.

## Established facts
- Founded during the Sundering (812) to hold Kellamar Pass. [session 4 prep]
- Led by a council of seven called the Ash Table; the seventh seat is empty. [session 4 prep]
- Collects the salt tithe from every caravan crossing the pass. [table, session 9]

## Player knowledge
What the party has actually learned, and what they believe that is wrong.
- Know: the Covenant controls the pass and taxes it.
- Believe (false): that the tithe funds the kingdom.

## GM only
Secrets, true causes, planned reveals. Never exported.

## Relationships
- Holds [[reg-kellamar-pass]] against [[fac-crown-levy]].
- [[npc-solene-var]] sits at the Ash Table.

## Open questions
- Why is the seventh seat empty? (see OPEN-QUESTIONS.md #14)

## Change log
- 2026-08-13 — created (session 4 prep)
- 2026-08-20 — salt tithe added after table improvisation, session 9
```

Not every type needs every section — a creature rarely has player-knowledge nuance — but keep the ones that apply and delete the rest rather than leaving empty headings, which read as "nothing established" when they mean "not written yet."

## Invariants

Start a fact's bullet with `(!)` when it constrains other facts — dates, hard limits, who holds what, anything a later contradiction would ripple through:

```markdown
- (!) Occurred 214 years before the present day. [worldbuilding, 2026-05-02]
- Pass-country stories say the sky burned in a single night. [worldbuilding]
```

`reindex` gathers every `(!)` fact, plus `WORLD.md`'s hard rules, into the Invariants section at the top of `CANON-INDEX.md`. That section is read at the start of every session, so marking a fact as an invariant is how a worldbuilder makes it impossible to forget. Mark sparingly — an invariant list of eighty items is a list nobody reads.

## Facts, one per line

Each bullet under `## Established facts` should be a single checkable claim with a bracketed source. One fact per line is what makes contradiction-hunting and diffing tractable; a paragraph of prose hides three claims and a mood inside one blob.

Sources worth recording: `[session N prep]`, `[table, session N]`, `[worldbuilding, 2026-08-13]`, `[from worldbuilder's original notes]`. Provenance answers "can I change this?" — a fact improvised at the table and witnessed by players is much more expensive to retcon than one written in prep and never used.

## Cross-references

Reference other entities in body text with `[[id]]` or `[[Display Name]]`. The audit script resolves these against the index, so `[[...]]` is what turns prose into a checkable link graph. Plain mentions are fine in flavor text; use `[[...]]` whenever the connection is a fact.

Keep `links:` in frontmatter as the *structural* relationships (what this entity is part of, allied with, ruled by) and let `[[...]]` carry the incidental ones.

## Bidirectional discipline

When entity A gains a fact about entity B, B's file gets the mirror fact. One-way links are the main way parts of a world become unreachable — a beautifully detailed NPC nobody can find because only one obscure file mentions them.

## Type-specific notes

**Place** — add `## Getting there` (routes, travel time), `## Who runs it`, `## What can be got here`. Travel times are numbers and therefore never invented silently.

**Character** — add `## Voice` (speech pattern, a signature phrase) and `## What they want`. Both are what makes an NPC playable at 9pm on a Tuesday.

**Event** — add `date:` to frontmatter using the world's own calendar, plus `## Disputed accounts` if in-world sources disagree, which is usually more interesting than a single official history.

**Power** — add `## What devotion looks like` and `## What their adherents get`. Both are player-facing and both are rules-adjacent, whatever the power actually is.

**Culture** — separate what is inherited from what is learned; conflating the two is both a worldbuilding weakness and a table-level problem.

**System** — state plainly what it can do, what it cannot, what it costs, and who is permitted to use it. These four answers do more work at the table than any amount of cosmology.
