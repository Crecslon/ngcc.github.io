<!-- synced from ngcc1/sign-01/report.md -->
Candidate: Aigis-Sig+
Family: Lattice (Module-LWE/SIS, Fiat-Shamir)
Scope: Reference implementation, all three parameter sets
Archive: [Aigis-Sig+.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/Aigis-Sig%2B.zip) (SHA-256: `88242576a3ae8f9d090b0c9045020f04ee9b5ae828e01b839f25267959e9c7ea`)
Severity: High
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Trivial signature malleability violates SUF-CMA

The packed hint has a variable meaningful length inside a fixed-size signature buffer. Verification decodes the meaningful portion but does not require a unique, canonical encoding of the remaining bytes.

Changing a sampled unused packed-hint bit in a valid signature produces a different byte string that still verifies for the same public key and message. No secret key or signing operation is needed to construct the second signature.

This does not by itself forge a signature for a new message, so it is not an EUF-CMA break. It does directly violate the specification's strong-unforgeability claim, because an attacker transforms one valid signature into a distinct valid signature on the same message.

The decoder must reject noncanonical hint encodings and require every unused byte or bit to have its unique prescribed value.

## Reproduction

`security/ngcc_security sign-01/lib/libAigis-sig1.so sig-signature-flip`
