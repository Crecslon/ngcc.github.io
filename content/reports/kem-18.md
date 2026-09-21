<!-- synced from ngcc1/kem-18/report.md -->
Candidate: LoongKEM
Family: Lattice (LWE)
Scope: Reference implementation, all four parameter sets
Archive: [LoongKEM.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/LoongKEM.zip) (SHA-256: `a6e5070647a40e7de1bf6e5b085dc1d6423c003a409864fdb303d87f881cec0b`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Partial rejection mask leaks the candidate shared secret

The decapsulator ORs ciphertext-byte differences into an arbitrary nonzero byte and negates that byte directly to form a selection mask. Except for the value `0x01`, this does not produce the required `0xff` mask. Invalid-ciphertext output is consequently a bitwise mixture of the candidate and fallback keys.

For all four parameter sets, changing ciphertext byte 1 by `0x80` produced an output retaining all seven low bits of every byte of the valid shared secret. Byte 0 is not a universal witness: at the 128- and 256-bit levels it produces only a partial mixture, while it works at the 384- and 512-bit levels. The byte-1 result was reproduced across ten independent key generations per parameter set.

An attacker modifies the IND-CCA challenge ciphertext and compares the retained positions with the challenge key. Agreement distinguishes the real key from a random key with overwhelming probability. This directly violates the claimed IND-CCA security of all four instances.

The comparison result must be normalized to a Boolean and expanded to exactly `0x00` or `0xff` before key selection.

## Reproduction

`security/ngcc_security kem-18/lib/libLoong128.so kem-reject-mask`
