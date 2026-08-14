# Worldsmith, the World Codex Librarian

An AI skill for building and maintaining a homebrew tabletop RPG world, where **you** stay the sole author of what is true.

Worldsmith keeps your setting as plain markdown files a game master can actually read at the table. It looks facts up rather than trusting its own memory, and it writes nothing into your world without your explicit approval. It brainstorms when you ask. It does not promote a proposal into a fact. Any game, any system, any genre.

## What it does

- **Never invents world facts on its own.** Every claim it makes is labeled as established (with a citation), inferred, or proposed. Only you can promote a proposal to canon.
- **Attaches an invention receipt to prose.** When it writes read-aloud text or a faction summary, it lists every new name, number, and implication in it, so nothing gets smuggled in while you are reading for flavor.
- **Refuses to guess numbers.** Distances, dates, populations, travel times. Invented numbers propagate and quietly corrupt a setting, so it says "not established" and offers options instead.
- **Catches drift and hands you the options.** Spellings, dates, and contradictions, including when you are the one contradicting yourself. It never picks a winner.
- **Writes pages a GM can run.** Each page opens with what you read to players, not with a block of metadata. Player-facing material and GM secrets are separated by a heading, and handouts are built from the safe side.
- **Records what you dictate.** The facts you make up mid-session are the ones your players remember and the only ones nobody writes down. Worldsmith walks you through filing them.
- **Audits the world** for broken links, confusable names, timeline problems, orphaned entries, and drift from your own stated premise.

## Quick start

Download **`SKILL.md`** and add it as a skill.

- **Claude**: Settings, then Capabilities, then Skills, then upload the file.
- **ChatGPT**: Skills, then Create, then Upload.
- **Anything else that reads markdown**: paste it in as instructions. All of the discipline lives in the prose, and there is nothing to install.

Then say something like *"I want to start a new setting"* or *"what do I have established about Threl?"* and the Librarian will take it from there. On a new world it will ask how you want your files organized before creating anything.

## How a world is arranged

Four files are always named, and Worldsmith creates them on the first run:

| File | Holds |
|---|---|
| `WORLD.md` | The premise, the tone, the rules that never bend, and what this world is NOT. |
| `STYLE.md` | Name examples, sound patterns, canonical spellings, what you have ruled out, and how pages are written. |
| `CANON-INDEX.md` | The register. One line per entry saying which page holds which facts. It carries no facts of its own. |
| `CANON-LOG.md` | An append-only record of what was established, when, and where it came from. |

Everything else is yours to arrange. Worldsmith asks where you want things shelved and records your answer at the top of the register, so it reads your layout instead of assuming one.

## What changed in v2

v1 shipped a Python script and a multi-file skill folder. **Both are gone.** Worldsmith is now a single markdown file with no software in it at all. If you were using v1, the old files are still in this repository's history and nothing you built with them is lost, but they are no longer maintained.

Three problems in v1 drove the rewrite:

**The canon index had become a copy of the world.** v1 marked load-bearing facts with `(!)` and gathered every marked fact into the index. In practice almost every fact gets marked, so the index grew into a second, competing copy of the setting, wrong the moment a page was edited and silently so. In one real world it reached 57 KB for 47 entries, and 65 percent of it was duplicated fact text.

The index is now a register: one line per entry carrying a name, its variant spellings, and a link. It says where a fact lives and never holds the fact. The same world's register is 9.9 KB. Nothing in the procedure is proportional to the size of the world any more, so a thousand entries behave like a hundred.

**Every update meant regenerating that index.** A rebuild step is a step that can be skipped, and an index that quietly lags a session behind is worse than none, because it looks current. The register is now written one row at a time, in the same step as the page it points to. There is nothing to rebuild, so there is nothing to skip.

**The files read like database records.** v1 pages opened with a dozen lines of technical header followed by identically stamped bullets, and linked entries by id, so a sentence read `[[plc-rivkah-9]] lies north of [[plc-benk]]`. Those links also resolve to nothing in Obsidian unless the filenames are id-shaped. Pages now open with a one-line identity and a **Read to Players** section, link by display name, and keep provenance in a dated change log instead of on every bullet.

## Checking facts without checking everything

The obvious way to prevent contradictions is to verify every statement against the world. That is unusably slow, and most of what gets verified is not a fact.

Worldsmith checks by class of statement instead. Four classes drift: **names**, **numbers**, **relations** between entries, and anything that would bend a hard rule. Mood, description, dialogue, and pacing are not checked, because they are not facts. The check happens at the moment of writing a claim rather than as a sweep before the conversation starts.

## What it is protecting against

Two failures, both of which feel fine in the moment.

**Drift by amnesia.** The model forgets what you established months ago and contradicts it, and you find out at the table in front of your players.

**Drift by accretion.** The model is fluent and generous. It names the river. It decides the empire fell three centuries ago because the sentence needed a number. None of it was asked for, all of it sounds right, and a tired GM accepts it. Six sessions later the setting belongs to the model. This one is invisible while it is happening, which is why it needs structure rather than good intentions.

## Contents

```
SKILL.md      the skill, everything in one file
README.md     this file
LICENSE       CC BY 4.0
```

## License

**Worldsmith** by **QuothGM**, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use it, change it, run games with it, sell what you make with it. Keep the credit line. If you improve it, I would like to hear about it.
