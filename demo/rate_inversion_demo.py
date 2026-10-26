"""Minimal demonstration that a per-step rate can invert a ranking.

Accompanies "When the Metric Lies", Section "Rates with behavior-dependent
denominators". No DCSS, no RL, no dependencies beyond the standard library:
    python rate_inversion_demo.py

The simulation encodes three assumptions:
  1. discovery is front-loaded, so cumulative novelty grows sublinearly in
     steps, N(s) = c * s**ALPHA with ALPHA < 1;
  2. episodes can end early, on the agent's own account;
  3. the better explorer also survives longer -- stipulated below, not
     derived, and the condition that turns 1 and 2 into an inversion.

Agent A is STRICTLY BETTER than agent B on both axes: it discovers more per
unit of exploration (larger c) and it survives longer (smaller per-step death
hazard). The count metric says so. The per-step rate says the opposite.
Raising A's c far enough, with 1 and 2 untouched and A still better on both
axes, restores the correct ranking: the inversion holds in a window.

ALPHA is a parameter of this simulation, not a measurement.
"""

import random

ALPHA = 0.463      # front-loading exponent; stipulated, see docstring
CAP = 5000         # step cap per episode
EPISODES = 10_000  # per agent
SEED = 12345

#                     discovery scale   per-step death hazard
AGENTS = {"A (better)": (12.0, 0.00005),
          "B (worse)":  (9.0,  0.00050)}


def run(c, hazard, rng):
    """One episode. Returns (cells discovered, steps taken)."""
    steps = CAP
    for s in range(1, CAP + 1):
        if rng.random() < hazard:      # died: episode truncates here
            steps = s
            break
    return c * steps ** ALPHA, steps


def main():
    print(f"alpha={ALPHA}  cap={CAP}  episodes={EPISODES}  seed={SEED}\n")
    print(f"{'agent':<12}{'cells/ep':>10}{'steps/ep':>10}{'deaths':>8}{'cells/step':>12}")
    results = {}
    for name, (c, hazard) in AGENTS.items():
        rng = random.Random(SEED)      # same stream per agent: paired comparison
        cells = steps = deaths = 0
        for _ in range(EPISODES):
            n, s = run(c, hazard, rng)
            cells += n
            steps += s
            deaths += (s < CAP)
        rate = cells / steps           # pooled ratio; Case 4 used mean-of-ratios
        results[name] = (cells / EPISODES, steps / EPISODES, deaths, rate)
        print(f"{name:<12}{cells/EPISODES:>10.1f}{steps/EPISODES:>10.1f}"
              f"{deaths:>8}{rate:>12.4f}")

    (ca, _, _, ra), (cb, _, _, rb) = results["A (better)"], results["B (worse)"]
    print(f"\ncount says A beats B by {100*(ca-cb)/cb:+.1f}%")
    print(f"rate  says A beats B by {100*(ra-rb)/rb:+.1f}%")
    print("\nThe ranking inverts. Nothing is mis-implemented: both ratios are")
    print("computed correctly. The denominator is a function of the behaviour")
    print("being scored, so the better agent is charged for the steps it")
    print("survived to take.")


if __name__ == "__main__":
    main()
