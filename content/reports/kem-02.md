<!-- synchronized report: kem-02/report.md -->
Candidate: Amoeba
Family: Lattice-based (Ring-LWE)
Archive: [Amoeba.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/Amoeba.zip) (SHA-256: `719c438a30cccd72c9d83da4b5150fee0c55351f2c13e7a66fd61bf653ca5c24`)

## kem-02-1: The FO check compares only every fourth ciphertext byte

Severity: High
Status: Confirmed
Layer: Implementation
Affected: All five Amoeba reference parameter sets
Discovery: Trivial
Exploitation: Reported full Amoeba-576 key recovery in approximately 30,000 decapsulation queries
Credit: Jinnuo Li
Date: 2026-09-22
Original source: [NGCC PKC Forum report](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/JB6IBZZUEVGTMM2SF6WK5PIYW7ESSPYT/)

Jinnuo Li reported the attack in the [NGCC PKC Forum](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/JB6IBZZUEVGTMM2SF6WK5PIYW7ESSPYT/). Amoeba's Fujisaki--Okamoto decapsulation re-encrypts the decoded message, but `cmp()` advances its byte index by four. Amoeba-576 consequently checks only 262 of 1,047 ciphertext bytes; changes in the other 785 bytes cannot trigger implicit rejection. The same source defect appears in every submitted parameter set.

This exposes a plaintext-checking primitive of the type developed by Das in [ePrint 2026/1682](https://eprint.iacr.org/2026/1682): unchecked ciphertext coefficients can be swept across decoding thresholds to obtain linear information about the reused Ring-LWE secret. Li reports recovering the secret keys for all ten official Amoeba-576 KAT vectors in about `3*10^4` decapsulation queries per key. We independently confirmed the incomplete predicate and the attack class, but have not independently reproduced Li's Amoeba-specific end-to-end key-recovery code. The attack also requires an application-level accept/reject signal under a reused KEM key; implicit rejection alone returns a pseudorandom-looking key in both branches.

The fix is to compare the complete ciphertext in constant time. A full-byte comparison is also required by the scheme's stated FO construction and IND-CCA2 argument.

### Reproducing

```sh
make -C kem-02 exploit
```

The source-level witness verifies the vulnerable loop in all five trees, enumerates the 262 checked positions for Amoeba-576, and exercises checked and unchecked mutation controls.
