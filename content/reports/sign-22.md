<!-- synced from ngcc1/sign-22/report.md -->
Candidate: Rhyme
Family: Lattice-based
Archive: [Rhyme.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/Rhyme.zip) (SHA-256: `7b509d21c6674bc23751b8743cb7c2a4a07ee295fafe04e2fa95c0613160bdfd`)

## sign-22-1: The implemented message representative caps forgery security at 256 bits

Severity: High
Layer: Implementation
Affected: Rhyme-512 reference implementation and specification
Discovery: Trivial
Exploitation: Approximately 2^256 hash evaluations
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

Rhyme-512 claims 512-bit classical security and uses the unsalted message binding `mu = H_gen(pk, M)`. Its implementation fixes `mu` at 64 bytes, enabling a generic collision-and-signature-transfer attack in about `2^256` evaluations.

The PDF specifies the construction but never defines the output length of `H_gen`. The implementation ceiling is confirmed, but the omission prevents calling the 64-byte length a clean normative parameter.

### Reproducing

```sh
python3 security/design_parameter_audit.py
```

The `sign-22-1` check verifies the normative message-binding algorithm on
physical PDF pages 29–32 and 50–51 and the source digest constant.

## sign-22-2: The implementation expands the complete key pair from a 256-bit root

Severity: High
Layer: Implementation
Affected: Rhyme-512 reference implementation and specification
Discovery: Trivial
Exploitation: Approximately 2^256 key-generation trials
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

Rhyme-512 expands its entire key pair from one 32-byte root. The generated public-key support is therefore at most `2^256`; generic root enumeration and public-key matching recovers the corresponding signing key.

The normative algorithm denotes the root length by `rho_0` but never assigns `rho_0` in its parameter table. This is both an implementation security ceiling and a specification omission.

### Reproducing

```sh
python3 security/design_parameter_audit.py
```

The `sign-22-2` check verifies the normative KeyGen algorithm on physical PDF
pages 29 and 50–51 and the source root constant.
