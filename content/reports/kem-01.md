<!-- synced from ngcc1/kem-01/report.md -->
Candidate: Aigis-Enc+
Scope: Reference implementation, all three parameter sets
Archive: orig/kem-01/orig.zip (SHA-256: `1c053133175cd189fd9f0e058bde684168f55a6fc3871de2a755404a08990186`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Ineffective implicit rejection breaks IND-CCA security

Changing a ciphertext bit frequently leaves the decapsulated shared secret unchanged. An exhaustive sweep of Aigis-enc1 found that 5,632 of 7,168 single-bit ciphertext changes return the original shared secret. The same defect was reproduced in the other two parameter sets.

`mkem_dec` writes the candidate valid secret to the output before checking the re-encrypted ciphertext. On failure, the intended constant-time replacement writes into the wrong buffer, leaving the already-returned candidate secret untouched. Rejection is therefore ineffective.

An attacker given a challenge ciphertext and candidate challenge key can modify the ciphertext, decapsulate it through the allowed CCA oracle, and compare the result with the candidate key. Retention identifies the real encapsulated key and provides a direct IND-CCA distinguisher. This violates the claimed IND-CCA security at every submitted level.

## Reproduction

`security/ngcc_security kem-01/lib/libAigis-enc1.so kem-ciphertext-flip`
