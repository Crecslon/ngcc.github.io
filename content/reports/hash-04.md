<!-- synced from ngcc1/hash-04/report.md -->
Candidate: CHAMP
Family: Symmetric (Cayley graph / matrix products)
Archive: [CHAMP.zip](https://www.niccs.org.cn/niccs/Proposal/Cryptographic%20Hash%20Algorithms/Round%201%20candidates/CHAMP.zip) (SHA-256: `8953f95618236d8d86191992b10e3580ae74520c28a36a715c2fc8bea2a9e8c1`)

## hash-04-1: Fixed-length outputs occupy only one determinant fiber

Severity: Medium
Status: Confirmed
Layer: Design
Affected: CHAMP-512 and CHAMP-1024 construction and reference implementation
Discovery: Non-trivial
Exploitation: Generic birthday scales at most approximately 2^192 and 2^384 if the walk mixes
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

CHAMP hashes a bit string by multiplying two public `2 x 2` matrices. Both generators have determinant 2, so every message of a fixed bit length `n` has determinant `2^n`. All fixed-length outputs therefore lie in one determinant fiber of size exactly `p(p^2-1)`, approximately `p^3`, rather than the full approximately `p^4` matrix space.

An invertible output encoding cannot enlarge that image. The nominal 512- and 1024-bit outputs consequently have at most approximately 384 and 768 bits of fixed-length image entropy, with generic birthday scales no greater than approximately `2^192` and `2^384` if the walk mixes. This does not contradict the specification's explicit unequal-length theorem, but it probably contradicts a natural 256/512-bit same-length collision-strength interpretation.

## hash-04-2: Projective positive-word collision lead for CHAMP-512

Severity: Low
Status: Lead
Layer: Design
Affected: CHAMP-512 construction
Discovery: Non-trivial
Exploitation: Approximately 2^64 for CHAMP-512 (heuristic, not yet instantiated)
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

Because `p = 7 mod 8`, 2 is a square. Scaling both generators by the inverse square root of 2 normalizes them into `SL2` without changing equal-length collisions. The exact generators satisfy `det(AB-BA)=2`, so they have no shared projective eigenline.

The Mullan-Tsaban general-generator heuristic then suggests positive-word collisions in approximately `sqrt(p)` work, around `2^64` for CHAMP-512. Its proven special case does not directly apply because `det(A-B)=-5`, so this remains a probable attack lead rather than a demonstrated collision. It should not be described as confirmed until instantiated against the exact generators.
