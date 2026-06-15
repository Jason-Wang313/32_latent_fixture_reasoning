# Submission Attack Log

Updated: 2026-06-15

## Attack Rounds

1. Closest-prior attack: POMDPs, contact-rich manipulation, active perception, and fixture-aware planning already cover much of the conceptual area. Response: keep the novelty to an interpretable fixture variable tied directly to release actions.
2. Evidence attack: the v2 experiment is a toy simulator with synthetic residuals. Response: expand to a v3 suite with 8 families, 10 regimes, 12 policies, 80 seeds, and 12,288,000 represented decisions.
3. Taxonomy attack: the fixture classes and release actions are hand-coded. Response: keep the claim synthetic and bounded; add unknown-fixture, partial-action-menu, sensor-bias, and oracle-gap analyses.
4. Unknown-fixture attack: unseen fixtures may be forced into known labels. Response: nearest known-taxonomy classification remains damaging; guarded abstention reduces damage but pays explicit abstention cost.
5. Abstention attack: a safe robot can become useless. Response: report abstention separately and include over-abstaining guard as a negative control.
6. Free-control attack: the suite may reward always suspecting hidden constraints. Response: include a fixture-absent family and free-fixture regime.
7. Sequential-fixture attack: one release may expose another fixture. Response: include dual-fixture family and sequential-fixture regime.
8. Artifact attack: stale local PDFs can be mistaken for final PDFs. Response: canonical build copies only the final accepted PDF to Downloads and removes local `main.pdf`.

## V3 Outcome

The paper is now a final full-scale synthetic mechanism paper. It is stronger
than the v2 compact mechanism artifact because it has broad stress tests,
substantive controls, full artifact outputs, and a 26-page final manuscript.
It still does not claim hardware validation or learned taxonomy discovery.
