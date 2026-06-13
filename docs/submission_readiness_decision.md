# Submission Readiness Decision

Decision: workshop-only / strong-revise.

## Why Not Submit-Ready

- Evidence is a toy simulator with synthetic residuals.
- The fixture taxonomy and release-action menu are hand-coded.
- V2 shows the mechanism fails on an out-of-taxonomy cable-tie fixture unless the robot abstains.
- There is no hardware validation or high-fidelity assembly simulation.
- There is no comparison to POMDP, active-perception, tactile-inference, or contact-rich manipulation baselines.

## Why Not Kill

- The latent-fixture variable is a clear robotics abstraction tied directly to safe action choice.
- The positive toy result cleanly shows why visible geometry alone is incomplete for hidden fixtures.
- The v2 stress makes the taxonomy boundary explicit rather than hiding it.
- The narrowed claim is useful as a mechanism note.

## Required Next Work

- Evaluate on real or high-fidelity hidden-fixture manipulation tasks.
- Learn or calibrate fixture prototypes and unknown-fixture thresholds.
- Compare against POMDP and active-perception baselines.
- Add a diagnostic workflow for out-of-taxonomy abstentions.
