<!-- synced from ngcc1/sign-18/report.md -->
Candidate: Origami
Family: MPC-in-the-head
Archive: [Origami.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/Origami.zip) (SHA-256: `e34f18832e968681dd0c51ce0d4b29d80e01ad29daa83dfb805718b76fdffa80`)

## sign-18-1: A fixed 512-bit message prehash caps forgery security at 256 bits

Severity: High
Layer: Design
Affected: Origami-512 specification and reference implementation
Discovery: Trivial
Exploitation: Approximately 2^256 hash evaluations
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

Origami-512 claims 512-bit classical security but first compresses every message with a fixed 64-byte `H_msg`. It only then derives the randomized target from `target || H_msg(message) || salt`.

A generic collision in `H_msg` costs about `2^256` evaluations. Once two messages share that prehash, every later salt produces the same signing target for both, so a signature requested on one message transfers to the other. Adding the salt after the short prehash does not repair the collision.

The construction and length are explicit in both the PDF and source, making this a specification-level design break of the advertised 512-bit classical EUF-CMA level.

### Reproducing

```sh
python3 security/design_parameter_audit.py
```

The check verifies physical PDF pages 14–16 and 50–52 and the submitted 64-byte digest constant.
