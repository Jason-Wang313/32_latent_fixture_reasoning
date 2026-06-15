# Reviewer Attacks

1. Attack: This is just POMDP state estimation. Response: concede the framing and argue that the fixture graph is the useful robotics abstraction and action interface.
2. Attack: The evaluation is synthetic. Response: true; the paper is a final full-scale synthetic mechanism study, not a hardware performance claim.
3. Attack: Fixture categories are hand-designed. Response: yes; the contribution is the state/action interface and stress-test structure, not learned taxonomy discovery.
4. Attack: Active perception can already choose probes. Response: this paper ties probe residuals directly to release-action selection, wrong-release damage, and abstention.
5. Attack: Contact-rich manipulation already models constraints. Response: the distinction is whether the constraint cause is visible and specified or latent and inferred from action outcomes.
6. Attack: An unseen fixture can be confidently misclassified. Response: true; this is why the v3 suite includes unknown fixtures, guarded abstention, action-menu misspecification, and over-abstention controls.
7. Attack: Abstention can make the robot useless. Response: true; abstention is reported separately, and over-abstaining guard is included as a negative control.
8. Attack: The oracle is unrealistic. Response: true; it is an upper reference used to diagnose whether the bottleneck is inference/action coverage rather than the fixture abstraction itself.
9. Attack: Free objects should not require fixture reasoning. Response: true; the free-fixture control prevents the paper from rewarding methods that always suspect hidden constraints.
10. Attack: The final numbers may not transfer to real assemblies. Response: true; the transfer claim requires hardware calibration and is explicitly left as future work.
