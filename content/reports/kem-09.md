<!-- synced from ngcc1/kem-09/report.md -->
Candidate: CheetahKEM
Family: Lattice (Ring/Module-LWE)
Scope: Reference implementation, all four parameter sets
Archive: [CheetahKEM.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/CheetahKEM.zip) (SHA-256: `fc321e46bac9c387535e2053bed560eac3d3cd88ba9bebc154f5bf68dd47dcd1`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Partial rejection mask leaks the candidate shared secret

The decapsulator ORs ciphertext-byte differences into an arbitrary nonzero byte and then uses its negation directly as a selection mask. Negating a nonzero byte produces `0xff` only when that byte is `0x01`; other values select a bitwise mixture of the valid candidate key and the rejection key.

For all four parameter sets, changing ciphertext byte 1 by `0x80` produced a rejection output retaining all seven low bits of every byte of the valid shared secret. Byte 0 is not a universal witness: at the 128- and 256-bit levels it produces only a partial mixture, while it works at the 384- and 512-bit levels. The permanent `kem-reject-mask` test reproduced a byte-1 witness for every tested key generation.

An IND-CCA attacker modifies the challenge ciphertext and compares the retained bit positions with the challenge key. For a real challenge they agree; for a random challenge the false-match probability is negligible. This is a direct distinguisher against all four claimed IND-CCA instances.

The fix is to normalize every nonzero comparison result to an all-ones mask before selecting between the candidate and rejection secrets.

## Reproduction

`security/ngcc_security kem-09/lib/libCheetah128.so kem-reject-mask`
