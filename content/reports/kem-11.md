<!-- synced from ngcc1/kem-11/report.md -->
Candidate: COMPASS-KEM
Family: Lattice-based
Archive: [COMPASS-KEM.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/COMPASS-KEM.zip) (SHA-256: `8fc838488ac0849d4c6afd161f8b9742c7a8b9a330bc3b79df70ced7e2d1d5e2`)

## kem-11-1: The Level-5 implementation uses a 256-bit key-generation root

Severity: High
Layer: Implementation
Affected: COMPASS-KEM-512 reference implementation and specification
Discovery: Trivial
Exploitation: Approximately 2^256 key-generation trials
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

The COMPASS-KEM specification sets `n=512` and defines both the initial key-generation seed and the shared key as `n`-bit values. The submitted COMPASS-KEM-512 implementation instead fixes `SYMBYTES` and `SSBYTES` at 32 bytes.

The entire IND-CPA key pair is a deterministic function of one 256-bit `coins` value. There are therefore at most `2^256` generated public keys: enumerate the root, regenerate the public key, and compare it with the target to recover the corresponding secret key. The KEM output independently has at most 256 bits of delivered-key capacity.

This is an implementation/specification conformance break. The normative algorithms request 512-bit values; the submitted Level-5 code retains 256-bit constants.

### Reproducing

```sh
python3 security/design_parameter_audit.py
```

The check verifies the Level-5 source constants and deterministic expansion against physical PDF pages 9, 12, and 16.
