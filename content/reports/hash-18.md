<!-- synced from ngcc1/hash-18/report.md -->
Candidate: MEGASCON
Family: Symmetric (sponge)
Archive: [Megascon.zip](https://www.niccs.org.cn/niccs/Proposal/Cryptographic%20Hash%20Algorithms/Round%201%20candidates/Megascon.zip) (SHA-256: `70d0796942e60a1ddd25ad2332dbfe2755052825c301e9585167c90c1fa09d3d`)

## hash-18-1: The 384-bit digest is a prefix of the 512-bit digest

Severity: High
Layer: Design
Affected: Reference implementation, MEGASCON-384 and MEGASCON-512
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

For the 24-bit message hex `616263` (`abc`), MEGASCON-384 returns:

`12a06f59d0c531c20cf4efad19195ba328c2aa92e8ef76b344f7084b98cc88a913f71388bb289e33b76accc9966d7cf4`

MEGASCON-512 returns that exact 48-byte value followed by:

`907761161784fcce7082995b14ee6036`

For every message shorter than 1024 bits, both variants initialize the same zero state, inject identical padded bytes at the same offset, and apply the same 15-round permutation. The digest length or variant identifier is never absorbed; only the amount returned to the caller differs.

The two functions therefore lack cross-variant domain separation and cannot be treated as independent hashes. No explicit specification claim of cross-profile independence was located, so this is reported as a confirmed composition defect rather than a collision-resistance claim violation.

### Reproducing

Build the candidate and the reproducer, then run:

```sh
make -C api harness && make -C tools && make -C hash-18
tools/ngcc_attack hash-prefix hash-18/lib/libMEGASCON-384.so hash-18/lib/libMEGASCON-512.so
```

`tools/reproduce.sh` runs this together with the other supported runtime
witnesses and their controls. See `tools/README.md`.
