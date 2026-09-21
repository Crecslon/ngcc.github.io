<!-- synced from ngcc1/sign-07/report.md -->
Candidate: CS
Family: Lattice (Module-LWE, Fiat-Shamir)
Scope: Reference implementation, all three parameter sets
Archive: [CS.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/CS.zip) (SHA-256: `c790d31cd4a288990f3d692381ed721a06641938a02dfc2e0435b7d323475cef`)
Severity: High
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Trivial signature malleability violates SUF-CMA

The signature contains a fixed-size rANS encoding area and an encoded byte count. `sigDecode` consumes only the indicated meaningful bytes and does not require the unused tail to be zero or otherwise canonical.

Changing the last unused signature byte produces a distinct signature that continues to verify for the same public key and message. This transformation needs neither the secret key nor a signing query beyond the original valid signature.

The result is not a new-message forgery and therefore does not alone violate EUF-CMA. It directly violates the submitted strong-unforgeability claim, which forbids producing a second accepted signature for an already signed message.

Verification must enforce a unique encoding, including the complete fixed-size tail.

## Reproduction

`security/ngcc_security sign-07/lib/libCS-128.so sig-signature-flip`
