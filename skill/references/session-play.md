# Session prep, play, and harvest

Play is where a world proves itself and where it changes fastest. The loop that keeps canon and table in sync: prep from canon → run → harvest back into canon.

## Prep

Prep is retrieval plus a small amount of clearly-marked new material. Everything invented during prep gets an invention receipt and enters as `status: provisional` until it survives contact with players.

Write to `play/sessions/<date>-s<N>.md`:

```markdown
---
id: ses-2026-08-20-s12
campaign: cmp-the-salt-road
date: 2026-08-20
status: prepped        # prepped | run | harvested
---

# Session 12 prep

## Where we left off
Two or three sentences. Pull from session 11's notes, not memory.

## What the party wants
Their stated goals, per player if they differ. Prep aimed at what they said
they'd do survives contact far better than prep aimed at where you want them.

## Canon in play tonight
Links to every entity they can plausibly reach, with the one line each and the
two or three facts most likely to come up. This is the quick-reference the worldbuilder
actually reads mid-scene, so keep it scannable — a wall of lore is unusable at
the table.
- [[plc-threl]] — toll town on the pass. Salt tithe. Marda runs the north gate.
- [[npc-solene-var]] — wants the seventh seat filled. Lying about why.

## Scenes
Not a script. For each: where, who, what's at stake, what changes if the party
does nothing, and how it can go wrong in an interesting way.

## Ready to improvise
Names, a rumor or two, one complication — pre-generated so table improvisation
draws from prepared material instead of blank panic. Everything here is
provisional and unnamed in canon until used.

## Open threads to touch
From OPEN-QUESTIONS.md — questions this session could answer through play,
which is the best way to answer them.
```

## During play

If the worldbuilder is running with assistance live, the priorities invert: speed beats completeness, and retrieval beats generation. Answer with the cited fact and nothing else. Keep a running list of anything improvised at the table — this list is the harvest queue, and capturing it in the moment costs seconds while reconstructing it later costs the fact entirely.

## Harvest

The most valuable and most skipped step. Facts created at the table are the ones players remember and the ones most likely to be contradicted later, because they're the only ones nobody wrote down.

After a session:

1. **Ask what happened**, briefly. What did the party do, what did they learn, what did the worldbuilder make up on the spot? If there are running notes, read them first and ask only about gaps.
2. **List the new facts.** Same format as an invention receipt, but reversed — these are already true because they were said out loud at a table. The question isn't whether to accept them, it's how to file them.
3. **Sort them.** New entity, new fact on an existing entity, or a player belief (which is a fact about the *players*, not the world, and belongs under `## Player knowledge` — including the false ones, which are the most important to track).
4. **Check for conflicts.** Table improvisation contradicts prep regularly. Run the conflict protocol; often the table version wins simply because players witnessed it.
5. **Commit** with source `[table, session N]`. That provenance marks these facts as expensive to retcon.
6. **Update player knowledge** across every entity the party learned about, and note what they concluded that's wrong. Tracked misconceptions are among a worldbuilder's best tools.
7. **Update open questions.** Close what play answered. Add the ones play created — usually the good ones, since they come with player investment already attached.
8. Mark the session file `status: harvested`, then `reindex` so the next session opens on a current index.

## Handouts

Generate from `## Player knowledge` only. Never from `## GM only`, and never from `## Established facts` directly, since those include things the party hasn't learned.

Write in an in-world voice when it fits — a broadsheet, a merchant's letter, a page torn from a ledger — and let in-world sources be wrong in characterful ways. A handout that is merely accurate reads like a wiki entry; one written by somebody with an agenda is a clue.

Before delivering, reread it against the GM-only sections of every entity it touches, and check what the *omissions* reveal. Then save to `handouts/` and run the audit's secrecy check.
