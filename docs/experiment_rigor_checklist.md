# Experiment Rigor Checklist

- [x] Main simulator is `scripts/recover_paper32.py`.
- [x] Main run uses 2,000 deterministic seeds.
- [x] Baselines include geometry-only, reactive-failure, and latent-fixture policies.
- [x] Main metrics include success, collisions, wrong fixture actions, steps, return, and belief confidence.
- [x] V2 stress attacks taxonomy misspecification.
- [x] V2 stress reports forced known-taxonomy failure and guarded abstention.
- [ ] No hardware validation.
- [ ] No high-fidelity physical simulator.
- [ ] No learned fixture taxonomy.
- [ ] No POMDP or active-perception baseline implementation.
- [ ] No measured tactile sensor noise or calibration procedure.

Decision: mechanism evidence only; terminal state is workshop-only / strong-revise.
