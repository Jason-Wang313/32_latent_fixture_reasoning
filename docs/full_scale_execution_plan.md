# Paper32 Full-Scale Execution Plan

## Current Claim

Paper32 argues that robots should infer hidden fixtures and supports from manipulation outcomes, not only from visible geometry. The v2 paper has a positive known-taxonomy toy result and a negative out-of-taxonomy cable-tie stress. The strong v3 version should keep that honesty while scaling the evidence: latent fixture reasoning helps when the fixture taxonomy and release-action menu cover the true cause; abstention and further diagnosis are necessary when the residual is out of taxonomy.

## Gaps To Close

1. The existing experiment has one toy residual model and three policies.
2. Fixture types are hand-coded and few.
3. Probe sequencing is minimal.
4. Out-of-taxonomy handling is only one cable-tie stress.
5. There are no families of assemblies, sensor modalities, or noise regimes.
6. There are no calibrated baselines such as POMDP-style belief update, active probing, nearest-prototype with abstention, or generic latent-state classifiers.
7. The manuscript is far below the 25-page final threshold.
8. The docs still describe a compact v2 mechanism artifact.

## Target Full-Scale Experiment

Create `scripts/run_full_scale_fixture_suite.py` using only the Python standard library. Write outputs to `results/full_scale/` and figures to `figures/full_scale/`. Use RAM-light expected rollouts for the full grid and explicit representative traces for a small number of cases.

Target scale:

- 8 assembly/fixture families
- 10 regimes
- 12 policies
- 80 deterministic seeds
- 160 represented probe/action decisions per seed
- 12,288,000 represented fixture-reasoning decisions

## Fixture / Assembly Families

1. `visible_free_vs_hidden_bolt`: visible geometry appears free, but bolts constrain motion.
2. `latch_under_occlusion`: latch state is hidden behind occluding geometry.
3. `adhesive_patch`: thermal or peel response reveals adhesive support.
4. `hidden_stop_channel`: a stop blocks one direction but allows reorientation.
5. `cable_tie_unknown`: out-of-taxonomy flexible restraint requiring abstention.
6. `magnetic_fixture`: holding force resembles adhesive but releases differently.
7. `dual_fixture`: two simultaneous fixtures require sequential diagnosis.
8. `fixture_absent_control`: no hidden fixture; direct action should often win.

## Regimes

1. `low_noise_known_taxonomy`: favorable calibrated case.
2. `high_noise_known_taxonomy`: noisy residuals within taxonomy.
3. `limited_probe_budget`: few reversible probes before commitment.
4. `high_damage_cost`: wrong release actions are expensive.
5. `ambiguous_residuals`: prototypes overlap.
6. `out_of_taxonomy`: unknown fixture appears.
7. `partial_action_menu`: true fixture is known but correct release action is unavailable.
8. `sensor_bias`: residual calibration is shifted.
9. `sequential_fixture`: more than one hidden constraint is active.
10. `free_fixture_control`: fixture absent or safely free.

## Policies / Baselines

1. `geometry_only`: assumes visible geometry is complete.
2. `reactive_after_failure`: commits, observes failure, then retries.
3. `nearest_fixture`: nearest prototype without abstention.
4. `latent_fixture_posterior`: posterior over known fixture taxonomy.
5. `guarded_abstention`: posterior plus unknown detector.
6. `active_probe_selection`: chooses next probe to disambiguate fixtures.
7. `sequential_diagnosis`: diagnoses and releases multiple fixtures.
8. `pomdp_style_belief`: value-of-information baseline over probes and releases.
9. `generic_latent_classifier`: predicts latent class without action semantics.
10. `oracle_fixture`: knows true fixture family and release action.
11. `over_abstaining_guard`: safe but refuses too often.
12. `random_probe_policy`: randomized diagnostic baseline.

## Metrics

For each seed-level row record:

- success
- damage/collision
- wrong release actions
- abstentions
- probes used
- release attempts
- diagnostic steps
- belief confidence
- unknown score / distance to known taxonomy
- return / utility
- family, regime, method, and seed

For aggregates record means, standard errors, win rates, abstention rates, damage rates, and utility gaps to the oracle.

## Ablations And Stress Tests

1. Known-taxonomy success under low/high residual noise.
2. Out-of-taxonomy cable-tie/magnetic/flexible restraint detection.
3. Probe budget sweep.
4. Damage-cost sweep.
5. Unknown-threshold calibration.
6. Action-menu misspecification.
7. Sequential multi-fixture diagnosis.
8. Free-fixture negative control where direct action should work.

## Figures And Tables

Generate manuscript-ready artifacts:

- `full_scale_scale.tex`: families, regimes, methods, seeds, steps, decisions.
- `full_scale_main_performance.tex`: main method comparison.
- `full_scale_family_summary.tex`: family-level winners and damage rates.
- `full_scale_regime_winners.tex`: regime-level winners.
- `full_scale_unknown_controls.tex`: unknown fixture, over-abstention, action-menu misspecification, and free control.
- `damage_by_method.pdf`: damage/wrong-release rates.
- `success_abstention_pareto.pdf`: success versus abstention/damage tradeoff.
- `regime_winner_phase.pdf`: utility winner by regime.
- `representative_trace.csv`: explicit probe/action trace.

## Manuscript Expansion Strategy

Rewrite `main.tex` into a v3 final full-scale manuscript:

1. Keep the v2 boundary: latent fixture reasoning needs taxonomy/action coverage or abstention.
2. Add the v3 marker and 12,288,000-decision scale.
3. Expand related work around POMDPs, active tactile probing, assembly fixtures, contact-rich manipulation, support relation reasoning, and world models.
4. Formalize fixture variables, residuals, probe actions, release actions, unknown detection, and utility.
5. Report main results, unknown controls, sequential fixture failures, and free-fixture controls.
6. Add appendices for residual models, policies, metrics, calibration, hardware fixture protocols, claim boundaries, failure catalog, and reviewer attacks.

The final rendered PDF must be at least 25 pages. Extra length must come from real content: experimental scale, ablations, detailed interpretations, limitations, hardware protocols, and reproducibility.

## RAM-Light Execution Strategy

- Use expected seed-level rollouts for the full grid.
- Store only seed summaries and aggregate summaries.
- Store one explicit representative trace.
- Generate small vector PDFs directly with the standard library.
- Keep all artifacts in the repo until final acceptance.
- Do not copy to Downloads until the final 25+ page manuscript passes verification.

## Final Acceptance Checklist

Paper32 is not final until all of the following are true:

- `docs/full_scale_execution_plan.md` exists before substantive edits.
- Full-scale runner completes reproducibly.
- Generated outputs exist in `results/full_scale/`.
- Generated figures exist in `figures/full_scale/`.
- Manuscript renders to at least 25 pages.
- PDF text contains `v3 final full-scale` and `12,288,000`.
- Build log has no fatal LaTeX errors, unresolved references, undefined citations, or overfull boxes.
- Canonical PDF is copied only to `C:/Users/wangz/Downloads/32.pdf`.
- Local `main.pdf` is removed after final build.
- Docs and status files describe v3, not stale v2 results.
- Commit is pushed and local HEAD matches upstream.
