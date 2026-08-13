# Audit playbook

An audit is a checkup, not a correction pass. Report findings as questions with options; the worldbuilder decides what's a bug. A surprising number of apparent contradictions are deliberate mysteries, in-world propaganda, unreliable narrators, or things the worldbuilder already has plans for — and "fixing" one of those silently does more damage than the inconsistency ever would.

Run in two passes: the script for what machines are good at, then judgment for what they aren't.

## Pass 1 — mechanical

```bash
python3 scripts/worldsmith.py audit
python3 scripts/worldsmith.py audit --json   # if you want to process results
```

Covers: missing or malformed frontmatter, duplicate ids, near-duplicate names, unresolved `[[references]]`, entities missing from `CANON-INDEX.md`, an index that is stale relative to the canon files, one-way links, `gm-only` content appearing in `handouts/`, files with no established facts, and leftover TODO markers.

A stale index is the highest-priority finding even though it looks clerical: everything the skill knows about the world in the next session comes through that file.

## Pass 2 — judgment

The script can't read meaning. These checks need you.

**Direct contradictions.** Two facts that can't both be true. Most often found where two entities describe the same relationship from opposite sides. Read entity pairs that link to each other, not just single files.

**Timeline coherence.** Dates against lifespans, reign lengths, travel times, construction times, and generational math. A character who witnessed an event 200 years ago in a world where humans live 80 years is either a mistake or the most interesting thing in the setting — ask which.

**Scale and plausibility.** A city of 200,000 needs farmland, water, and a way to move grain. An army of 30,000 needs a payroll and a supply line. A three-day journey needs to match the map. These don't need real-world realism, but they need internal consistency, and numbers invented separately are the most common source of quiet nonsense.

**Consequence gaps.** A big established fact with no visible effects. If magic can raise the dead cheaply, inheritance law is strange. If the empire fell fifty years ago, someone alive remembers being a citizen. Flag the fact and ask what it changed — this is usually where the best unwritten material is hiding.

**Tone and premise violations.** Check content against `WORLD.md`'s pillars and its "what this world is not." Drift here is gradual and rarely noticed from inside: a grim survival setting quietly acquiring a whimsical thieves' guild over six sessions.

**Naming drift.** Names that don't match `STYLE.md`'s phonology, or two cultures whose names have converged. Also near-collisions that will confuse players at the table — Kessine and Kellamar in the same region is a table problem regardless of whether it's a canon problem.

**Entity drift.** Compare an entity's current facts to its one-line identity and its earliest change-log entries. A faction that started as desperate smugglers and is now a shadow government may have grown, or may have been quietly rewritten by accumulation. Ask.

**Orphans and dead ends.** Entities nothing links to, mysteries with no planted clues, open questions that have gone stale, foreshadowing that never landed. These are opportunities more than errors.

**Secrecy hygiene.** Beyond the script's text matching: does any player-facing document *imply* a GM-only fact? Does a handout's omission give something away?

**Play readiness.** For anywhere the party might go soon: is there a name, a sensory detail, someone to talk to, and something to want? A canon entry that can't be run is not yet finished.

## Reporting

Group by severity, lead with what actually threatens a session, and keep it short enough to read. For each finding:

> **Timeline — Solene Var's age.** `npc-solene-var` says she sat at the founding of the Ash Table (812). `evt-the-sundering` puts that 214 years ago. Humans in this setting live a normal span (`WORLD.md`).
> Options: (a) she's not human or not entirely, (b) it's a different Solene — a line of them, (c) the founding date moves, (d) intentional, leave it.

Never batch-fix. Even obvious typo-level corrections get confirmed, because "obvious" and "load-bearing" overlap more than they should in a homebrew setting.

## Cadence

- Before a session — targeted audit of what the party can reach this week.
- After a harvest — check the newly canonized table material against everything it touched.
- Every couple of months — a full pass, including tone and entity drift, which only show up over time.
