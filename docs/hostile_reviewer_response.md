# Hostile Reviewer Response

## Likely Rejection

This is POMDP-style hidden-state inference in a synthetic fixture simulator. The fixture taxonomy, residual model, probe model, and release-action menu are hand-designed. There is no hardware validation, so the reported numbers cannot be treated as real-robot performance.

## Honest Response

We agree with the boundary. The contribution is not new general hidden-state estimation, unknown-fixture discovery, or a hardware benchmark. The contribution is a robotics-specific mechanism claim: a latent fixture variable is a useful action interface because it connects physical residuals to release actions, further probes, and abstention.

The v3 suite is designed to make this claim hard to overstate. It includes 8 fixture families, 10 regimes, 12 policies, 80 seeds, and 12,288,000 represented decisions. It includes unknown fixtures, partial action menus, sensor bias, sequential fixtures, and free controls. It reports abstention separately from success. It also includes negative controls: nearest known-taxonomy classification remains damaging, and over-abstention is safe but unproductive.

## Best Defense

- Geometry-only manipulation is unsafe in the suite: 24.0% success and 68.9% damage.
- Nearest known-taxonomy reasoning improves success but remains brittle: 31.6% success and 60.6% damage.
- Guarded abstention improves the safety tradeoff: 44.0% success and 33.3% damage, while explicitly paying 28.1% abstention.
- Active probing improves deployable success by selecting action-relevant probes.
- Oracle fixture knowledge reaches 93.1% success and 0.3% damage, showing that fixture-aware release selection has high potential if inference and menu coverage improve.

## Required Upgrade Beyond This Paper

- Validate on hardware or a high-fidelity assembly simulator.
- Learn or calibrate fixture prototypes and unknown thresholds from measured residuals.
- Include measured false-commit rates for unknown fixtures.
- Compare against a full POMDP or active tactile perception implementation on real tasks.
- Add recovery workflows where abstention triggers useful human assistance, tool changes, or additional safe probing.
