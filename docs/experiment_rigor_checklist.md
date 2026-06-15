# Experiment Rigor Checklist

- [x] Detailed v3 execution plan exists before substantive edits: `docs/full_scale_execution_plan.md`.
- [x] Full-scale runner exists: `scripts/run_full_scale_fixture_suite.py`.
- [x] The suite covers 8 fixture families.
- [x] The suite covers 10 regimes.
- [x] The suite compares 12 policies.
- [x] The suite uses 80 deterministic seeds per family/regime/method.
- [x] The suite represents 12,288,000 fixture-reasoning decisions.
- [x] Baselines include geometry-only, reactive-after-failure, nearest fixture, generic latent classifier, random probing, and over-abstention.
- [x] Stronger methods include posterior belief, guarded abstention, active probing, sequential diagnosis, POMDP-style belief, and oracle fixture knowledge.
- [x] Stress tests include unknown fixtures, partial action menus, high damage cost, sensor bias, ambiguous residuals, sequential fixtures, limited probes, and free-fixture controls.
- [x] Metrics include success, damage, wrong release, abstention, probes, utility, oracle gap, and win rate.
- [x] Outputs include seed metrics, aggregate metrics, summary JSON, representative trace, manuscript tables, and vector figures.
- [x] The final manuscript is 26 pages and includes explicit limitations.
- [ ] No hardware validation.
- [ ] No high-fidelity physical simulator.
- [ ] No learned fixture taxonomy.
- [ ] No measured tactile sensor calibration.

Decision: final full-scale synthetic mechanism evidence. The paper is substantially stronger than v2, but it remains bounded to synthetic evaluation.
