<!-- synced from ngcc1/sign-06/report.md -->
Candidate: COMPASS-SIG
Family: Lattice-based
Archive: [COMPASS-SIG.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/COMPASS-SIG.zip) (SHA-256: `ce88066506fe9b58c300b3ca51462c7a8350484d88ad5b8a9c9f17b5152ca820`)

## sign-06-1: The specified message representative caps forgery security at 256 bits

Severity: High
Layer: Design
Affected: COMPASS-SIG-512 specification and reference implementation
Discovery: Trivial
Exploitation: Approximately 2^256 hash evaluations
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

COMPASS-SIG-512 claims 512-bit classical security and binds the message through the unsalted value `mu = H(pk || m)`, instantiated as 64 bytes. A generic collision in this fixed 512-bit representative costs about `2^256` evaluations.

An attacker finds two messages that collide under the target public key, obtains a signature on one, and transfers it to the other. This specification-level construction therefore cannot provide 512-bit classical EUF-CMA security regardless of the lattice parameters.

### Reproducing

```sh
python3 security/design_parameter_audit.py
```

The `sign-06-1` check verifies the construction on physical PDF pages 5 and
8–10 and the submitted Level-5 constants.

## sign-06-2: The implementation expands the entire key pair from a 256-bit root

Severity: High
Layer: Implementation
Affected: COMPASS-SIG-512 reference implementation and specification
Discovery: Trivial
Exploitation: Approximately 2^256 key-generation trials
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

The COMPASS-SIG specification requires an `n`-bit KeyGen seed and sets `n=512` at Level 5. The implementation instead draws one 32-byte root and deterministically expands the complete key pair from it.

The generated public-key support is at most `2^256`; exhaustive root enumeration and public-key matching recovers a target signing key in at most that many trials. This second issue is an implementation/specification conformance break.

### Reproducing

```sh
python3 security/design_parameter_audit.py
```

The `sign-06-2` check verifies the KeyGen seed on physical PDF pages 7 and 13
and the submitted Level-5 constants.
