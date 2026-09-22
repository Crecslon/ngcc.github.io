<!-- synced from ngcc1/kem-36/report.md -->
Candidate: TRIKE
Family: Code-based
Archive: [TRIKE.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/TRIKE.zip) (SHA-256: `03956a13fde3d402513bfcf9942f2b04fd23e98b01a3dc52b48938b9c89fe4d6`)

## kem-36-1: The specified TRIKE decoder rejects every tested honest ciphertext

Severity: High
Status: Confirmed
Layer: Design
Affected: TRIKE specification; all four implementations use a different rule
Discovery: Trivial
Exploitation: Trivial correctness failure for the specified algorithm
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

TRIKE's PDF defines the bit-flipping threshold as `max(Tnow,T′)`, repeats that return value in Algorithm 8, and explains that the decoder uses the larger threshold. Every submitted implementation instead computes `min(Tnow,T′)`.

The difference is decisive. In a paired whole-KEM test where the libraries differed only in this expression, the shipped `min` decoder recovered 1,000/1,000 honest TRIKE-2 shared secrets. The literal PDF `max` decoder recovered 0/1,000: the API still returned success, but every derived shared secret was wrong. Hence the specified scheme is nonfunctional, while the implementation and its KATs instantiate a materially different decoder. Any DFR claim must identify and analyze the actual rule.

### Reproducing

```sh
make -C kem-36 lib/libTRIKE-2.so
python3 security/trike_threshold_differential.py --trials 1000
```

The script builds an isolated copy with the literal PDF expression and compares both complete KEMs on identical deterministic trials.
