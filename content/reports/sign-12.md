<!-- synced from ngcc1/sign-12/report.md -->
Candidate: Galas
Scope: Reference implementation, all submitted parameter sets
Archive: orig/sign-12/orig.zip (SHA-256: `98d57af868fa10d74b2c0656e565aa14a42ff902646d6fc440ffb7355b75342c`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Publicly reproducible signing keys

The signing wrapper constructs a private DRNG but does not seed it from the API-provided `drng_algorithm`. Unless a non-API test helper is called, it initializes that generator with 32 zero bytes.

Independent fresh-process tests against Galas-160F generated identical public and secret keys in separate processes. The same implementation pattern is shared by the submitted Galas instances.

An attacker recovers the signing key by running the public key-generation implementation from its initial state. The advertised hard relation is irrelevant because the victim and attacker deterministically generate the same secret key.

Key generation must obtain its seed exclusively from the initialized API DRNG and must not provide a zero-seed production default.

## Reproduction

`python3 security/run_low_hanging.py --wave all --candidate sign-12 --check sig-fresh-keygen --workers 1 --timeout 60`
