<!-- synced from ngcc1/sign-15/report.md -->
Candidate: MORNING-ATLAS
Family: Lattice (Module-LWR, Fiat-Shamir)
Scope: Reference API and supplied KAT, all four parameter sets
Archive: [MORNING-ATLAS.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/MORNING-ATLAS.zip) (SHA-256: `c796b106a7d43b2b3d6110ec2be426aa321cc7336f39a2cc027b2d6e8b4cc8c1`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Returned-length error causes an out-of-bounds heap disclosure

`sig_get_sn_len_bytes()` advertises a `CRYPTO_BYTES`-byte output buffer. `sig_sign()` writes exactly that detached signature, but returns `CRYPTO_BYTES + message_length` as though it had also appended the message. A caller that allocates the advertised size and serializes the returned length reads beyond the allocation.

The submitters' own KAT does exactly this. In its first records, the out-of-bounds `Sn` field contains allocator bytes followed by 41, 45, 40, and 41 bytes of the adjacent 64-byte KAT seed for the 128-, 192-, 256-, and 512-bit instances. From record 3 onward it includes all 64 seed bytes. That seed deterministically generates the KAT key material.

The KAT format also prints `Seed` and `SK` as separate fields, so these published vectors do not newly expose an otherwise secret value. They nevertheless provide a concrete demonstration that trusting the candidate's returned length discloses adjacent heap data; in another caller the adjacent object may be private. This is a critical API/memory-disclosure defect, distinct from the cryptographic malleability below.

## Trivial hint-padding malleability violates SUF-CMA

The signature decoder stops after the cumulative number of encoded hint indices but does not require the remaining fixed-size hint slots to be canonical. Verification compares only the decoded algebraic values and ignores changes in those unused slots.

For each of `lwrdsa128`, `lwrdsa192`, `lwrdsa256`, and `lwrdsa512`, flipping the high bit of the final unused hint-index byte in a valid signature produced a different byte string that still verified for the same message and public key.

The attack needs only one ordinary valid signature. It does not forge a new message and therefore does not by itself violate EUF-CMA, but it directly violates the specification's SUF-CMA claim.

Verification must reject any noncanonical unused hint slot and enforce all stated hint-weight and ordering constraints. The separate KAT heap over-read and ATLAS-192 parameter shortfall are documented in `security_findings.md` and are not needed for this attack.
