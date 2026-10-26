# When the Metric Lies: Artifacts

Artifacts for the paper

> Seyed Ali Alavi, Mohaddeseh Jahanabadi, Dustin Dannenhauer.
> **When the Metric Lies: Silent Evaluation Failures in RL Exploration.**
> TAE (Trust-AI-Eval) Workshop: Can We Trust AI Evaluation?, NeurIPS 2026.

The paper documents four evaluation failures from one reinforcement-learning
exploration project in Dungeon Crawl Stone Soup (DCSS), all under a
pre-registered protocol, and analyzes how a rate whose denominator depends on
the agent's own behavior can reverse a ranking of agents.

This folder contains the one simulation from the paper and the four frozen
coverage reference files whose SHA-256 hashes the paper cites as H1 to H4.
These files are extracted from a larger private research project.

## Contents

```
demo/rate_inversion_demo.py   simulation from the section "Rates with behavior-dependent denominators"
references/                   the four frozen coverage reference files (v1 to v4)
verify_references.py          recomputes and checks the SHA-256 of the four reference files
```

Both scripts use only the Python standard library. They were tested with
Python 3.13.

## The rate inversion demo

`demo/rate_inversion_demo.py` simulates two agents with no RL and no game.
Discovery grows sublinearly in steps (`N = c * S**ALPHA`, `ALPHA < 1`) and an
episode can end early when the agent dies. Agent A is better on both axes: it
discovers more per unit of exploration and survives longer. The script shows
that A wins on cells discovered per episode but loses on cells per step.
`ALPHA` is a parameter of the simulation, not a measured value.

Run:

```
python demo/rate_inversion_demo.py
```

Expected output (deterministic, fixed seed):

```
alpha=0.463  cap=5000  episodes=10000  seed=12345

agent         cells/ep  steps/ep  deaths  cells/step
A (better)       571.9    4405.4    2223      0.1298
B (worse)        261.5    1810.6    9227      0.1444

count says A beats B by +118.7%
rate  says A beats B by -10.1%

The ranking inverts. Nothing is mis-implemented: both ratios are
computed correctly. The denominator is a function of the behaviour
being scored, so the better agent is charged for the steps it
survived to take.
```

The `cells/step` column is the pooled rate: total cells divided by total
steps over all episodes.

## The coverage reference files

The primary coverage metric (P1 in the paper) divides the cells an agent
discovered on a map by a fixed reference set of cells for that map. Each
reference file holds that denominator for the 30 evaluation map seeds. For
each seed it is the union of passable cells observed across confirmed
evaluation episodes, so it is a lower bound on the reachable floor.

| Version | Paper | File | Built from |
|---|---|---|---|
| v1 | H1 | `eval_reference_union.json` | 219 episodes |
| v2 | H2 | `eval_reference_union_v2_20260818.json` | 384 episodes |
| v3 | H3 | `eval_reference_union_v3_20260819.json` | 515 episodes |
| v4 | H4 | `eval_reference_union_v4_20260822.json` | 625 episodes |

v3 is the denominator used for the main evaluation campaign. v4 was rebuilt
after a further 110 episodes and has the same cell set as v3 on all 30 seeds
(40,072 passable cells in total). Its hash differs from v3 only because the
build metadata differs.

Each file is a JSON object with build metadata (`written_utc`, `source`,
`kind`, `built_from`, `episodes_used`, `episodes_skipped_unconfirmed`,
`patterns`) and two maps from seed number to a cell set: `reference`, built
from passable cells, which is the denominator, and `reference_other_key`,
the same union built from all cells the agents saw (`known`). Each seed entry
has `cells` (a list of `[x, y]` coordinates), `size` (the number of cells),
`built_from` and `contributing_agents` (the agent types whose episodes
contributed).

## Verifying the reference files

Run:

```
python verify_references.py
```

Expected output:

```
OK       v1 (H1)  eval_reference_union.json
         expected 7ca04545ed124960072574751babbfdf6271f961dfb159f39f9733ef207ddf40
         actual   7ca04545ed124960072574751babbfdf6271f961dfb159f39f9733ef207ddf40
OK       v2 (H2)  eval_reference_union_v2_20260818.json
         expected 1ff27271a429a94ad42c734bf8504ffe1e563497f75ccfc5b29938240182e641
         actual   1ff27271a429a94ad42c734bf8504ffe1e563497f75ccfc5b29938240182e641
OK       v3 (H3)  eval_reference_union_v3_20260819.json
         expected e7146ced6e8d317e5971da30ad70150d45459203a01a486d069fcd59e362c6a6
         actual   e7146ced6e8d317e5971da30ad70150d45459203a01a486d069fcd59e362c6a6
OK       v4 (H4)  eval_reference_union_v4_20260822.json
         expected 4b364bfff47a58d81126afe5f5389ea365ab2e8e4085cf9fe5cde37540dc0376
         actual   4b364bfff47a58d81126afe5f5389ea365ab2e8e4085cf9fe5cde37540dc0376

All 4 reference files match.
```

The script exits with status 0 if all four files match and 1 otherwise.

The hashes are computed over the exact bytes of each file, which use CRLF
line endings. If a file was checked out with converted line endings, its hash
will not match. Download the files without line-ending conversion.

## License

The whole folder, code and data, is released under the MIT License. See
`LICENSE`. Copyright (c) 2026 Seyed Ali Alavi, Mohaddeseh Jahanabadi, Dustin
Dannenhauer.
