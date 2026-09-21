<!-- synced from ngcc1/hash-20/report.md -->
Candidate: MOZI
Family: Symmetric (sponge)
Archive: [Mozi.zip](https://www.niccs.org.cn/niccs/Proposal/Cryptographic%20Hash%20Algorithms/Round%201%20candidates/Mozi.zip) (SHA-256: `f68c6b73ff4ac064e6bb8a9b74c4bd8a929594c3c48c89e1a65941e03676ea30`)

## hash-20-1: For short messages, the 384-bit digest is a prefix of the 512-bit digest

Severity: Medium
Status: Confirmed
Layer: Design
Affected: Specified construction and reference implementation, MOZI digest and XOF profiles
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

For the 24-bit message hex `616263` (`abc`), MOZI-384 returns:

`f3aa50e4542947c662f18092b6b4079e489192491a8f13b49ebd108352e49d1da81e938795a675a409083fce63f2eb1f`

MOZI-512 returns that exact 48-byte value followed by:

`69444aab68ec23d14f909ef4ce1b9b63`

For every message shorter than 1024 bits, both variants initialize the same zero state, inject identical padded bytes at the same offset, and apply the same 20-round permutation. The digest length or variant identifier is never absorbed; only the amount returned to the caller differs.

The two functions therefore lack cross-variant domain separation and cannot be treated as independent hashes. No explicit specification claim of cross-profile independence was located, so this is reported as a confirmed composition defect rather than a collision-resistance claim violation.

The same missing domain separation affects the XOF profiles. On the audited short messages, the 384- and 512-profile 256-bit XOF outputs are equal, while shorter outputs are prefixes of the longer XOF streams. This follows from the normative zero initialization, common padding and permutation, and `MSB_l` output rule; it is not only a wrapper artifact.

### Reproducing

Build the candidate and the reproducer, then run:

```sh
make -C api harness && make -C tools && make -C hash-20
tools/ngcc_attack hash-prefix hash-20/lib/libMOZI-384.so hash-20/lib/libMOZI-512.so
```

`tools/reproduce.sh` runs this together with the other supported runtime
witnesses and their controls. See `tools/README.md`.
