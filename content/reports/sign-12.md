<!-- synced from ngcc1/sign-12/report.md -->
Candidate: Galas
Family: Symmetric (MPC/VOLE-in-the-Head)
Archive: [Galas Signature.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/Galas%20Signature.zip) (SHA-256: `98d57af868fa10d74b2c0656e565aa14a42ff902646d6fc440ffb7355b75342c`)

## sign-12-1: Publicly reproducible signing keys

Severity: Critical
Layer: Implementation
Affected: Reference implementation, all submitted parameter sets
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

The signing wrapper constructs a private DRNG but does not seed it from the API-provided `drng_algorithm`. Unless a non-API test helper is called, it initializes that generator with 32 zero bytes.

Independent fresh-process tests against Galas-160F generated identical public and secret keys in separate processes. The same implementation pattern is shared by the submitted Galas instances.

An attacker recovers the signing key by running the public key-generation implementation from its initial state. The advertised hard relation is irrelevant because the victim and attacker deterministically generate the same secret key.

Key generation must obtain its seed exclusively from the initialized API DRNG and must not provide a zero-seed production default.

### Reproducing

Build the candidate and the reproducer, then run:

```sh
make -C api harness && make -C tools && make -C sign-12
tools/ngcc_attack keygen-determinism sign-12/lib/libGalas-160S.so
```

`tools/reproduce.sh` runs this together with the other supported runtime
witnesses and their controls. See `tools/README.md`.
