<!-- synchronized report: sign-22/report.md -->
Candidate: Rhyme
Family: Lattice-based
Archive: [Rhyme.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/Rhyme.zip) (SHA-256: `7b509d21c6674bc23751b8743cb7c2a4a07ee295fafe04e2fa95c0613160bdfd`)

## sign-22-1: The implemented message representative caps forgery security at 256 bits

Severity: Critical
Status: Confirmed
Layer: Implementation
Affected: Rhyme-SHAKE-384/-512 and Rhyme-SM3-384/-512 reference implementations; specification leaves the hash length undefined
Discovery: Trivial
Exploitation: Approximately 2^256 hash evaluations
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

Rhyme uses the unsalted message binding `mu = H_gen(pk, M)`. The SHAKE and SM3 implementations for the 384- and 512-bit sets all fix `mu` at 64 bytes, enabling a generic collision-and-signature-transfer attack in about `2^256` evaluations, below each set's claim.

The PDF specifies the construction but never defines the output length of `H_gen`. The implementation ceiling is confirmed, but the omission prevents calling the 64-byte length a clean normative parameter.

### Reproducing

```sh
python3 security/design_parameter_audit.py
```

The `sign-22-1` check verifies the normative message-binding algorithm on
physical PDF pages 29–32 and 50–51 and the source digest constant.

## sign-22-2: The implementation expands the complete key pair from a 256-bit root

Severity: Critical
Status: Confirmed
Layer: Implementation
Affected: Rhyme-SHAKE-384/-512 and Rhyme-SM3-384/-512 reference implementations; specification leaves the root length undefined
Discovery: Trivial
Exploitation: Approximately 2^256 key-generation trials
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

The affected Rhyme-384 and Rhyme-512 implementations expand each entire key pair from one 32-byte root. The generated public-key support is therefore at most `2^256`; generic root enumeration and public-key matching recovers the corresponding signing key.

The normative algorithm denotes the root length by `rho_0` but never assigns `rho_0` in its parameter table. This is both an implementation security ceiling and a specification omission.

### Reproducing

```sh
python3 security/design_parameter_audit.py
```

The `sign-22-2` check verifies the normative KeyGen algorithm on physical PDF
pages 29 and 50–51 and the source root constant.

## sign-22-3: Rhyme-SM3 omits the specified doubled-width parity mask

Severity: Medium
Status: Confirmed
Layer: Implementation
Affected: Reference and optimized Rhyme-SM3-128, -256, -384, and -512; the SHAKE implementations are controls
Discovery: Moderate
Exploitation: Valid signatures give noisy linear equations in the secret parity; key recovery or forgery not demonstrated
Credit: Yijian Liu, with AI assistance
Date: 2026-09-28
Original source: [Liu's PKC Forum post](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/32MEEUHEHAW2TQD74RYHELHXNBUJKU5I/)

Algorithm 6 samples `X'` from `D_Z,sigma` but requires the independent masking noise `e_bottom` to come from `D_Z,2sigma`. Theorem 4.3 says that the doubled width is essential to make its parity statistically close to uniform and uses an identical `D_Z,2sigma` sample in the simulator. Every submitted SM3 signer instead calls the ordinary `SampleGauss` for both values (`src/sign.c:333–334`); that function always uses the `rhyme_cdt_g` table (`src/sampler.c:175–181`). Both the reference and optimized trees are affected. The SHAKE trees contain the missing separate `SampleGaussE`/`rhyme_cdt_e` path and provide a direct control.

Reducing a valid signature modulo two removes the `2 B' X'` term. The rejection sampler's offset has the challenge's parity, so the remaining public relation is

`z_bottom mod 2 = s_tail * c + e_bottom mod 2`.

Exact evaluation of the submitted CDT gives `E[(-1)^e]` equal to `6.3322e-4`, `4.8828e-4`, `4.1941e-4`, and `3.7652e-4` for the four SM3 levels. Thus signatures carry secret-dependent noisy parity equations, and Theorem 4.3's parity-masking argument and stated `2sigma` condition—and the later bounds that invoke them—do not apply to the submitted SM3 implementations. This report does not claim an efficient decoder for those equations, a signing-key recovery, or a forgery; that boundary keeps the finding at Medium.

Use the specified doubled-width sampler/table for `e_bottom`, retaining the already distinct nonce/domain used by the SM3 signer, and re-evaluate the complete transcript distribution. The submitted SHAKE implementation provides a working model for the separate sampler.

### Reproducing

```sh
python3 sign-22/reproduce_sm3_parity_bias.py
```

The script checks both implementation trees, confirms the SHAKE control, and computes the four exact CDT parity biases.

An optional accepted-transcript experiment generates and verifies 25,000 deterministic Rhyme-SM3-128 signatures, then scores the predicted parity relation over 25.6 million bottom-response coefficients:

```sh
sh sign-22/reproduce_sm3_parity_runtime.sh
```

The checked run measured bias `7.025e-4`, versus the exact raw-CDT value `6.3322e-4`; a zero-vector wrong predictor measured `-1.028125e-4`. It takes about two minutes on this host.
