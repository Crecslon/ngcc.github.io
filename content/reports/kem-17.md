<!-- synced from ngcc1/kem-17/report.md -->
Candidate: HEP-QC
Family: Code-based (quasi-cyclic)
Scope: Reference implementation, all four parameter sets
Archive: [HEP-QC.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/HEP-QC.zip) (SHA-256: `3780991127f49b6397b4182d32b35ab7a6359bf825a707e90df0f809beeb3790`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Publicly reproducible secret keys

Key generation draws from a file-scope SHAKE-256 PRNG context that is never initialized by the KEM wrapper. The API-provided seeded DRNG is declared but never consumed. Each fresh process therefore begins from the same zero-initialized state and generates the same key pair.

Fresh-process tests with different API seeds produced identical public and secret keys for `hep-qc-1`, `hep-qc-3`, `hep-qc-5`, and `hep-qc-7`.

An attacker recovers a victim's secret key by starting a fresh process and invoking the submitted key-generation API once. No code-based cryptanalysis is required. The resulting secret key decapsulates the victim's ciphertexts, completely breaking the claimed KEM confidentiality.

The wrapper must initialize its PRNG from the supplied DRNG for every independent key-generation operation and must not rely on zero-initialized global state.

## Reproducing

Build the candidate and the reproducer, then run:

```sh
make -C api harness && make -C tools && make -C kem-17
tools/ngcc_attack keygen-fresh kem-17/lib/libhep-qc-1.so 0x01   # repeat with a different seed
```

`tools/reproduce.sh` runs this together with every other reported
finding and its controls. See `tools/README.md`.
