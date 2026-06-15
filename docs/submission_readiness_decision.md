# Submission Readiness Decision

Decision: final full-scale synthetic mechanism paper; not a hardware-validated main empirical robotics paper.

## Why This Is Now Submission-Hardened

- The manuscript is 26 pages and contains a full v3 argument rather than a short toy note.
- The evaluation covers 8 fixture families, 10 regimes, 12 policies, 80 seeds, and 12,288,000 represented decisions.
- The paper includes geometry-only, nearest known-taxonomy, guarded abstention, active probing, sequential diagnosis, POMDP-style belief, oracle, random probing, and over-abstention comparisons.
- The stress tests include unknown fixtures, partial action menus, high damage cost, sensor bias, sequential fixtures, limited probes, ambiguous residuals, and free controls.
- The manuscript reports separate success, damage, wrong-release, abstention, probe, utility, and oracle-gap metrics.
- The final PDF is verified at `C:/Users/wangz/Downloads/32.pdf`.

## Remaining Boundary

- The evidence is synthetic.
- Fixture families and residual models are hand-designed.
- There is no hardware validation.
- There is no learned taxonomy or measured tactile calibration.
- The POMDP-style baseline is synthetic and not a full solver over a real robot task.

## Final Supported Claim

Latent fixture variables are useful action-selecting state abstractions for hidden-constraint manipulation, but only when taxonomy coverage, unknown detection, probe safety, release-action availability, and abstention are reported honestly.
