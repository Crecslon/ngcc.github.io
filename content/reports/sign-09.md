<!-- synchronized report: sign-09/report.md -->
Candidate: DOVE
Family: Multivariate (Double Oil-and-Vinegar)
Archive: [DOVE.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/DOVE.zip) (SHA-256: `19169e545f6a6fd90b844b0deb72db81b5eb73c136873d1dae113c2c39d1c6e0`)

## sign-09-1: The 256-bit SM3 state caps forgery security at 128 bits

Severity: Critical
Status: Confirmed
Layer: Design
Affected: DOVE-256 and DOVE-512, both classic and pkc_skc variants
Discovery: Moderate
Exploitation: Approximately 2^128 SM3 compression evaluations and one signing query
Credit: Dariia Porechna ([dariolina](https://github.com/dariolina))
Date: 2026-09-22
Original source: [GitHub issue #9](https://github.com/ngcc-dev/ngcc-harness/issues/9)

Further extension to the existing analysis… Dariia Porechna observed in the [original submission, GitHub issue #9](https://github.com/ngcc-dev/ngcc-harness/issues/9), that the inert signature salt gives a new-message forgery, not only signature malleability. The specified and implemented verification target is `pseudoXOF(msg || seed_pk)`; the signature's salt is never read by the verifier. The XOF produces each output block as `SM3(msg || seed_pk || BE32(counter))` using SM3's 256-bit Merkle--Damgard state.

Find two distinct 64-byte messages `B` and `B'` for which the first compression produces the same chaining state. This is a generic collision search with expected cost about `2^128`. For every XOF counter, both computations then continue from that same state with the identical `seed_pk`, counter, padding, and encoded length. Consequently all target bytes match, independent of whether DOVE requests 96 bytes or 216 bytes. A signature requested for `B` therefore verifies unchanged for the previously unsigned message `B'`, directly violating the EUF-CMA claim.

The attack caps classical forgery security at 128 bits, far below the specification's Table 5 minima of 263 and 522 bits for DOVE-256 and DOVE-512. DOVE-128 is not below its claimed 128-bit classical target through this attack; generic quantum collision search also remains above its stated 80-bit quantum target. Appending the salt after the attacker-controlled message would not stop this fixed-prefix collision. Preventing this security cap for the larger sets requires a target hash construction with a sufficiently wider internal state.

No `2^128` collision search was attempted. The structural validator checks all four submitted classic/pkc_skc source copies, confirms that signing and verification hash `msg || seed_pk`, confirms that verification ignores the salt, and traces every XOF block to the 256-bit SM3 state and big-endian counter.

### Reproducing

```sh
make -C sign-09 exploit
```
