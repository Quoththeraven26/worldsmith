# Worldsmith — the World Codex Librarian

An AI skill for building and maintaining a homebrew tabletop RPG world, where **you** stay the sole author of what is true.

Worldsmith stores your setting as plain markdown files, keeps a canon index it rereads at the start of every session rather than trusting its own memory, and refuses to write anything into canon without your explicit approval. It brainstorms freely. It does not promote a proposal into a fact. Any game, any system, any genre.

## What it does

- **Never invents world facts on its own.** Every claim it makes is labeled as established (with a file citation), inferred, or proposed. Only you can promote a proposal to canon.
- **Attaches an invention receipt to prose.** When it writes read-aloud text or a faction summary, it lists every new name, number, and implication in it, so nothing gets smuggled in while you are reading for flavor.
- **Refuses to guess numbers.** Distances, dates, populations, travel times. Invented numbers propagate and quietly corrupt a setting, so it says "not established" and offers options instead.
- **Catches contradictions and hands you the options.** Including when you are the one contradicting yourself. It never picks a winner.
- **Harvests what happened at the table.** The facts you improvise mid-session are the ones your players remember and the only ones nobody wrote down. Worldsmith walks you through filing them.
- **Separates player-facing from GM-only**, and checks handouts for leaks before you print them.
- **Audits the world** for broken references, duplicate ids, confusable names, timeline problems, and drift from your own stated premise.

## Quick start

**Claude** — download `worldsmith-single-file.md`, rename it `SKILL.md`, and add it as a skill. Or use the `skill/` folder as-is for the multi-file version, which loads less into context at a time.

**ChatGPT** — Skills → Create → Upload, using `worldsmith-single-file.md` renamed to `SKILL.md`. A single-file skill with `name` and `description` frontmatter is valid, which is what this is.

**Anything else that reads markdown** — paste the file in as instructions. All of the discipline lives in the prose; the Python is a convenience, not a dependency.

Then say something like *"I want to start a new setting"* or *"what do I have established about Threl?"* and the Librarian will take it from there.

## The optional tool

`skill/scripts/worldsmith.py` scaffolds worlds and entity files, regenerates the canon index, runs mechanical consistency checks, and searches canon. Python 3.8+, standard library only, nothing to install.

```bash
python3 worldsmith.py init ~/my-world
python3 worldsmith.py new --type faction --name "The Ashen Covenant"
python3 worldsmith.py reindex
python3 worldsmith.py audit
```

Everything it does can be done by hand. Appendix E of the single-file edition explains how.

## What it is protecting against

Two failures, both of which feel fine in the moment.

**Drift by amnesia.** The model forgets what you established months ago and contradicts it, and you find out at the table in front of your players.

**Drift by accretion.** The model is fluent and generous. It names the river. It decides the empire fell three centuries ago because the sentence needed a number. None of it was asked for, all of it sounds right, and a tired GM accepts it. Six sessions later the setting belongs to the model. This one is invisible while it is happening, which is why it needs structure rather than good intentions.

## Contents

```
worldsmith-single-file.md    everything in one file — start here
skill/SKILL.md               the instructions
skill/references/            entity schema, elicitation, audit playbook, session play
skill/scripts/worldsmith.py  the optional tool
LICENSE                      CC BY 4.0 (prose) + MIT (code)
```

## License

**Worldsmith** by **QuothGM**. Prose under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); `worldsmith.py` under the MIT License. Use it, change it, run games with it, sell what you make with it. Keep the credit line. If you improve it, I would like to hear about it.
