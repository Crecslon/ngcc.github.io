<!-- synced from ngcc1/hash-09/report.md -->
Candidate: Eijen
Scope: Reference implementation, all five parameter sets
Archive: orig/hash-09/orig.zip (SHA-256: `5e2581d905b9a3d3a8c34c76ed73213c77da970a15cc6b3b26b2bb086b93e3f4`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Trivial collisions in all Eijen implementations

The following collision was verified against Eijen-256:

- Input 1: empty string, length 0 bits
- Input 2: hex `00`, length 7 bits (seven zero bits)

Both produce:

`6f13fcc5cb0edcc73d8129c78913b663b5c6040fa0e2e8c4819d16b0ffda051d`

The bit length is essential: hex `00` with length 8 bits is a different message.

The collision is caused by an implementation bug, not by the specified construction. The specification requires injective `pad10*` padding, `M || 1 || 0^k`. Eijen processes message bits MSB-first, so the padding byte following a byte-aligned message must begin with `0x80`.

Instead, the byte-aligned path writes `0x01`. The partial-byte path correctly computes `0x80 >> partial_bits`; after seven explicit zero bits, this also produces `0x01`. The two distinct messages therefore have identical padded representations.

More generally, for every byte-aligned message `M`, `H(M) = H(M || 0^7)`. The defect affects all five submitted parameter sets. Replacing `0x01` with `0x80` in the byte-aligned padding path removes this collision. The implementation violates the specification's collision-resistance claims, but the defect is not inherent in the specified design.

## Reproduction

`security/ngcc_security hash-09/lib/libEijen-256.so hash-zero-padding`
