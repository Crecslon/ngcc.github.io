<!-- synced from ngcc1/hash-17/report.md -->
Candidate: MasterCube
Family: Symmetric (sponge, AndRX permutation)
Archive: [MasterCube.zip](https://www.niccs.org.cn/niccs/Proposal/Cryptographic%20Hash%20Algorithms/Round%201%20candidates/MasterCube.zip) (SHA-256: `1f9773b8ece90152a6a9adc632a7112c9afc670a5d28b7f1e9ac111e5eea8f13`)

## hash-17-1: Trivial collisions at every rate boundary

Severity: Critical
Status: Confirmed
Layer: Implementation
Affected: Reference implementation, all three parameter sets
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

The following collision was verified against MasterCube-512:

- Input 1: 958 one bits, encoded in 120 bytes of `ff` with length 958 bits
- Input 2: 959 one bits, encoded in the same buffer with length 959 bits

Both produce:

`847a067d6eb9078d5c3ce3e3f08fbfd3a1488eb6e89909144db1a76d5fcb9a097fef21b4927bb6fe0a1bb2769ef0f249734550c1e8acfa0023a1281d12131bf6`

The implementation attempts to apply `pad10*1` in a single rate block. When the message length is `r-1 mod r`, only one bit remains. The opening and closing delimiter bits are ORed into the same position instead of emitting the additional block required by the specification.

Consequently, for any prefix `P` of length `r-2 mod r`, the implementation gives `H(P) = H(P || 1)`. The same defect was reproduced at 702/703 bits for MasterCube-768 and 446/447 bits for MasterCube-1024. It directly violates the claimed 256-, 384-, and 512-bit collision strengths and is an implementation error rather than an attack on the specified permutation.

### Reproducing

Build the candidate and the reproducer, then run:

```sh
make -C api harness && make -C tools && make -C hash-17
tools/ngcc_attack hash-collide-rate hash-17/lib/libMasterCube-512.so 959
```

`tools/reproduce.sh` runs this together with the other supported runtime
witnesses and their controls. See `tools/README.md`.
