# Reviewer Attacks

1. Attack: This is just POMDP state estimation. Response: the paper should explicitly concede the POMDP framing and argue for the fixture graph as the useful robotics abstraction.
2. Attack: The toy benchmark is too small. Response: true; the paper is a mechanism note and needs richer validation before a full conference claim.
3. Attack: Fixture categories are hand-designed. Response: yes; the contribution is the state/action interface, not learned taxonomy discovery.
4. Attack: Active perception can already choose probes. Response: many active perception systems choose information-gathering views; this work ties probe residuals directly to release-action selection.
5. Attack: Contact-rich manipulation already has constraints. Response: the difference is whether the constraint cause is observed or latent and only revealed through action outcomes.
6. Attack: An unseen fixture type will be confidently misclassified as a known one. Response: true. The v2 cable-tie stress makes this failure explicit; safe behavior is abstention or additional diagnosis, not a successful release.
