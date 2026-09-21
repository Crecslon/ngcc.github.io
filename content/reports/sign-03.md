<!-- synced from ngcc1/sign-03/report.md -->
Candidate: CEDRUS+C
Family: Hash-based (stateless)
Scope: Reference implementation, all eight parameter sets
Archive: [cedrus+c.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/cedrus%2Bc.zip) (SHA-256: `a31de849cf0a0703a4e57decbdf4d97b100d00dc74756feaded2c04a7593e110`)
Severity: Critical
Discovery: Trivial
Exploitation: Low-query adaptive signature accumulation
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Hypertree index collapse causes repeated few-time keys

Every submitted `hash_sm3.c` parses the message digest and then assigns `*tree = 0` instead of decoding the hypertree index. The implementation therefore discards the 64- to 67-bit tree selection required by the specification and repeatedly uses only bottom-layer addresses.

An additional missing-parentheses defect in `SPX_BOTTOM_TREE_HEIGHT` makes the leaf mask retain two fewer bits than intended. The resulting numbers of reachable bottom FORS/WOTS addresses are only 4, 64, 8, 64, 16, 128, 32, and 128 for 160f, 160s, 256f, 256s, 384f, 384s, 512f, and 512s. Thus the initially observed 16-key collapse in 160f is actually a four-address collapse.

A same-key experiment with 100 CEDRUSC-160f signatures produced exactly four bottom authentication paths, with multiplicities 23, 25, 26, and 26. The specification models FORS-instance reuse with a probability near `1/2^h`; the implementation instead repeats few-time FORS and associated WOTS keys after only a handful of signatures.

This invalidates the submitted concrete-security analysis and enables low-query leaf accumulation and signature reuse attacks. The tree index must be decoded from the digest and every height macro must be parenthesized before use in masks.
