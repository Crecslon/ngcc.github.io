<!-- synced from ngcc1/sign-33/report.md -->
Candidate: VDOO
Family: Multivariate (UOV family)
Archive: [VDOO.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/VDOO.zip) (SHA-256: `4b7bb0f15388b395b9308ae480f25622105a734f0ab4a6bd16398438c4b9752a`)

## sign-33-1: Publicly reproducible signing keys

Severity: Critical
Layer: Implementation
Affected: Reference implementation, all three parameter sets
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

The implementation declares the API-provided `drng_algorithm` but never reads it. Key generation instead uses a second file-local global DRNG object that is never initialized by the shared-library wrapper and therefore starts from zero-initialized process memory.

Independent fresh-process tests with different API seeds generated identical VDOO public and secret keys. The result was directly reproduced against the built VDOO-256 library and the same RNG wiring is used by all submitted levels.

An attacker recovers the victim's secret signing key by starting a fresh process and invoking key generation once. No multivariate cryptanalysis is required.

All key-generation randomness must be derived from the initialized API DRNG; the uninitialized private generator must be removed or explicitly and securely seeded.

### Reproducing

Build the candidate and the reproducer, then run:

```sh
make -C api harness && make -C tools && make -C sign-33
tools/ngcc_attack keygen-fresh sign-33/lib/libvdoo_128.so 0x01
tools/ngcc_attack keygen-fresh sign-33/lib/libvdoo_128.so 0x99   # same key digest
```

`tools/reproduce.sh` runs this together with the other supported runtime
witnesses and their controls. See `tools/README.md`.

## sign-33-2: A 256-bit implementation prehash limits forgery security to 128 bits

Severity: Critical
Layer: Implementation
Affected: VDOO-512 reference wrapper and specification
Discovery: Trivial
Exploitation: Approximately 2^128 hash evaluations
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

The VDOO-512 wrapper first hashes every arbitrary-length message to a 32-byte digest and passes only that digest to the specified signing transform. Two messages with the same inner digest therefore produce the same signing input. A generic birthday search costs about `2^128` hash evaluations; after obtaining a signature on one colliding message, the attacker transfers it unchanged to the other.

The specification types its message hash as mapping directly to the MQ target space and does not clearly require this 32-byte truncation. This finding is therefore an implementation/specification conformance break, not a clean property of the normative VDOO design.

### Reproducing

```sh
python3 security/design_parameter_audit.py
```

The `sign-33-2` check traces the 32-byte wrapper prehash in the Level-5 source.

## sign-33-3: The Level-5 proof contains a 128-bit salt term

Severity: High
Layer: Design
Affected: VDOO Level-5 specification and proof
Discovery: Trivial
Exploitation: Proof gap; not by itself a concrete forgery
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

The VDOO specification fixes the salt at 16 bytes for Level 5. Its own EUF-CMA bound contains the term `(q_s+q_h)q_s 2^-128`: it is already `2^-127` for one signing and one hash query and becomes order one around `2^64` signing queries.

This is a specification-level parameter and proof gap: the stated reduction cannot substantiate 512-bit EUF-CMA security. It is not, by itself, a concrete forgery and is reported separately from `sign-33-2`.

### Reproducing

```sh
python3 security/design_parameter_audit.py
```

The `sign-33-3` check verifies the normative salt length and the corresponding
term in the submitted EUF-CMA bound.
