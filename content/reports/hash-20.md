<!-- synced from ngcc1/hash-20/report.md -->
Candidate: MOZI
Scope: Reference implementation, MOZI-384 and MOZI-512
Archive: orig/hash-20/orig.zip (SHA-256: `f68c6b73ff4ac064e6bb8a9b74c4bd8a929594c3c48c89e1a65941e03676ea30`)
Severity: High
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## The 384-bit digest is a prefix of the 512-bit digest

For the 24-bit message hex `616263` (`abc`), MOZI-384 returns:

`f3aa50e4542947c662f18092b6b4079e489192491a8f13b49ebd108352e49d1da81e938795a675a409083fce63f2eb1f`

MOZI-512 returns that exact 48-byte value followed by:

`69444aab68ec23d14f909ef4ce1b9b63`

For every message shorter than 1024 bits, both variants initialize the same zero state, inject identical padded bytes at the same offset, and apply the same 20-round permutation. The digest length or variant identifier is never absorbed; only the amount returned to the caller differs.

The two functions therefore lack cross-variant domain separation and cannot be treated as independent hashes. No explicit specification claim of cross-profile independence was located, so this is reported as a confirmed composition defect rather than a collision-resistance claim violation.
