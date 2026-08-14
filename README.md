# Worldsmith

A skill for building and maintaining a homebrew tabletop RPG world as markdown files, for use with Claude, ChatGPT, or any assistant that reads markdown instructions.

Version 2. Single file, no dependencies, no software.

## Contents

```
SKILL.md      the skill, 6,000 words
README.md     this file
LICENSE       CC BY 4.0
```

## Installation

Download `SKILL.md` and add it as a skill.

- Claude: Settings, Capabilities, Skills, Upload.
- ChatGPT: Skills, Create, Upload.
- Other tools: paste the file contents in as instructions.

The file carries `name` and `description` frontmatter, which is what makes it a valid skill on both platforms. The `description` field controls when the skill triggers without being named.

## What the skill does

It applies six behaviors. Each is a rule in the file, not a feature of a program.

**Classifies every claim.** Anything the assistant says about the world is labeled as established (written on a page, cited), inferred (follows from established facts, not itself written down), or proposed (invented). Only the worldbuilder promotes a proposal to canon.

**Attaches an invention receipt to generated prose.** After writing read-aloud text or a summary, it lists every new proper noun, number, and implication introduced in that text, and asks which to keep.

**Refuses to supply unestablished numbers.** Distances, dates, populations, prices, travel times, and counts are read from a page or reported as not established.

**Reports drift rather than correcting it.** Spelling variants, conflicting figures, and contradictions are reported with the pages cited and two or three lettered options. No fix is applied without confirmation.

**Separates player-facing content from GM content** by heading, and generates handouts from everything above the `GM secrets` heading.

**Audits on request** for row and page count mismatches, unresolved links, near-duplicate names, one-way relations, secret leakage, timeline arithmetic, scale, and drift from the world's stated premise.

## Files the skill uses

Four filenames are fixed. The skill creates them on first run.

| File | Contents |
|---|---|
| `WORLD.md` | Premise, tone pillars, hard rules, and what the world is not. The Hard rules section is the invariant list, hand-curated and capped at about 25 lines. |
| `STYLE.md` | Name examples grouped by what they name, the letter and syllable patterns those names follow, canonical spellings of any word with variants, names and words ruled out, and the page writing rules. |
| `CANON-INDEX.md` | The register. One row per entity. Carries no facts. |
| `CANON-LOG.md` | Append-only. Date, what was established, and its source. |

Folder structure is not fixed. The skill asks how the worldbuilder wants entries shelved, records the answer at the top of `CANON-INDEX.md`, and reads it there in later sessions.

## Page format

```markdown
---
type: place
status: canon
aliases: [Leabu]
updated: 2026-08-14
---

# Leahbu 4

*One sentence of identity. This line is copied into the register.*

## Read to Players
## What is established
## Full Description
## Connections
## GM secrets
## Change log
```

`type` is one of region, place, faction, character, culture, power, event, item, creature, system, campaign, session, and determines which shelf the page sits on.

`status` is `canon`, `provisional`, `proposed`, or `retired`.

`aliases` holds every other name the entity goes by, including misspellings that have appeared. This is what makes a search for a variant find the page.

Facts under `What is established` are one checkable claim per line. Provenance is recorded in the change log rather than on each bullet, with one exception: facts created at the table are marked inline, because they are more expensive to retcon.

Links use display names (`[[Rivkah 9]]`), not identifiers. Filenames are the display name lowercased with spaces converted to hyphens and apostrophes dropped, so links resolve in Obsidian and similar tools.

## The register

```markdown
| Name | Also | Type | What it is | Page |
|---|---|---|---|---|
| Leahbu 4 | Leabu | place | A habitable moon in the Rivkah System. | [[Leahbu 4]] |
```

Grouped by type, alphabetical within each group, one row per entity, no wrapping. The `What it is` column is the page's identity sentence and nothing more.

The register is written by hand, one row at a time, in the same step as the page it points to. There is no regeneration step.

Read behavior by size:

| Entries | Behavior |
|---|---|
| Up to ~150 | Can be read whole |
| 150 to 400 | Searched by name; one type section read when browsing |
| Over 400 | Split into one file per type |

No operation is proportional to the size of the world. Adding an entity is one appended row. Looking one up is one search.

## Fact checking

Verifying every statement against the world is too slow to use, and most of what would be verified is not a fact. The skill checks by class of statement instead. Four classes are checked:

1. Names, searched against the register in one pass per passage rather than once per name.
2. Numbers, read from the page that owns them.
3. Relations between entities, checked on both pages.
4. Statements that would contradict a hard rule in `WORLD.md`.

Mood, sensory detail, description, dialogue, adjectives, and pacing are not checked. The check runs at the point of making a claim, not as a pass before the conversation begins.

## Changes in version 2

Version 1 shipped a multi-file skill folder and `worldsmith.py`. Both have been removed. The old files remain in this repository's commit history.

**The canon index no longer holds facts.** Version 1 marked load-bearing facts with `(!)` and gathered every marked fact into the index. In use, most facts get marked. In one world of 47 entries the index reached 57 KB, of which 65 percent was fact text duplicated from the pages, meaning the index disagreed with a page as soon as that page was edited. The index is now a register carrying only names, aliases, type, an identity sentence, and a link. The same world's register is 9.9 KB.

**The `(!)` marker has been removed.** Load-bearing facts are promoted by hand into `WORLD.md` under Hard rules, against a cap of about 25 lines.

**There is no reindex step.** Version 1 regenerated the index after each commit, which could be skipped and which produced an index that looked current while lagging a session behind. The register row is now written in the same step as the page.

**Links use display names.** Version 1 linked by identifier (`[[plc-rivkah-9]]`) while naming files by slug (`rivkah-9.md`), so links resolved to nothing in Obsidian.

**Page layout changed.** Version 1 pages opened with eight frontmatter fields followed by fact bullets each carrying a source stamp. Version 2 pages carry four frontmatter fields and open with an identity sentence and a `Read to Players` section.

**Handout sourcing changed.** Version 1 generated handouts from a `Player knowledge` section. Version 2 generates from every section except `GM secrets`.

## License

Worldsmith by QuothGM, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution required. Commercial use permitted.
