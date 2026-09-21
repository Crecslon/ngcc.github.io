<!-- synced from ngcc1/sign-25/report.md -->
Candidate: SQIsign2D2
Scope: Level2-eff uncompressed reference implementation
Archive: orig/sign-25/orig.zip (SHA-256: `cf635de5eebbdeb7b2212e84f349da4ca878889e0a4a59b463d0c8cdfdb8eeab`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Verifier accepts modified messages and an all-zero signature

The Level2-eff uncompressed verifier accepted a valid signature after the first message byte was changed. It also accepted a full-length all-zero signature. Both results were reproduced through the submitted shared-library API using the advertised key and signature lengths.

The uncompressed verification path computes a message-dependent challenge but does not enforce all of the protocol's required point and response checks. Several stronger checks are absent or commented out, and the remaining codomain/nonzero tests are insufficient.

An attacker can submit an all-zero signature for a message without making any signing query, or reuse a signature with a modified message. This is a direct universal-style forgery against the affected instance and violates the specification's EUF-CMA theorem.

The verifier must implement every specified validation condition and reject zero or malformed decoded responses before performing protocol verification.

## Reproduction

`security/ngcc_security sign-25/lib/libSQISign2Dsquare-Level2-eff_uncompressed.so sig-zero`
