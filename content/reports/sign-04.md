<!-- synchronized report: sign-04/report.md -->
Candidate: CEDRUS-alpha
Family: Hash-based
Archive: [cedrus-alpha.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/cedrus-%CE%B1.zip) (SHA-256: `b90559ca94bda0130420f91fa52eeb242063a57188c766037c1b234ec3af563b`)

## sign-04-1: The 160-bit WOTS implementation authenticates only 128 bits

Severity: Medium
Status: Confirmed
Layer: Implementation
Affected: CEDRUSALPHA-160s and CEDRUSALPHA-160f, reference and optimized implementations
Discovery: Trivial
Exploitation: Reduces the relevant WOTS second-preimage target from 160 to 128 bits
Credit: shiyuan (NGCC PKC Forum sender)
Date: 2026-09-22
Original source: [NGCC PKC Forum report](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/S5GGRLD7YZQQRH2VPPYET2GWYTHFWKXR/)

Shiyuan reported the defect in the [NGCC PKC Forum](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/S5GGRLD7YZQQRH2VPPYET2GWYTHFWKXR/). The specification converts the complete `n`-byte WOTS message to an integer. In both 160-bit implementations, however, `WOTS_UINT_WORDS` is `SPX_N/8 = 2`, and `chain_lengths()` loads only two eight-byte words. Bytes 16 through 19 of every FORC or child-XMSS root are ignored by WOTS signing and verification.

The implementation therefore authenticates only a 128-bit prefix at these layers, contradicting the stated 160-bit classical strength. This is not an immediate signature-bit malleability: exploiting it in the full hypertree still requires finding a lower-layer result with the same authenticated prefix. The submitted `2^128` second-preimage estimate is the justified cap; the forum post's separate `2^64` collision figure does not by itself give a `2^64` signature forgery.

### Reproducing

```sh
make -C sign-04 exploit
```

The first control calls the submitted `chain_lengths()` and `wots_pk_from_sig()` on two 20-byte inputs that differ in all trailing 32 bits and obtains identical outputs.

## sign-04-2: FORC chain addresses are truncated to eight bits

Severity: Medium
Status: Confirmed
Layer: Implementation
Affected: All eight CEDRUSALPHA parameter sets, reference and optimized implementations
Discovery: Trivial
Exploitation: Address and secret-key aliases; a complete full-scheme forgery is not demonstrated
Credit: shiyuan (NGCC PKC Forum sender)
Date: 2026-09-22
Original source: [NGCC PKC Forum report](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/DZLVOKPTO2KZTN76AGZ2SST2T5ZCIUB7/)

Shiyuan reported the defect in the [NGCC PKC Forum](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/DZLVOKPTO2KZTN76AGZ2SST2T5ZCIUB7/). The specification assigns a full 32-bit `chainAddr` with domain `0..k*2^a-1`. The implementation writes the value only to address byte 27, so indices congruent modulo 256 generate identical PRF and FORC-chain inputs. The intended `k*2^a` leaf secrets consequently draw from at most 256 distinct values inside a fixed FORC address context.

This invalidates the specification's independence model and aliases leaves both within and across FORC trees. It does not establish the forum post's coupon-collector claim: ordinary signatures select fresh FORC contexts through their hypertree address, so observations from different contexts cannot be pooled as the same 256 keys without a separate address-reuse attack. A complete adaptive forgery exploiting the aliases remains to be constructed.

### Reproducing

```sh
make -C sign-04 exploit
```

The second control links the submitted address code and SM3 PRF and confirms that indices 0 and 256 produce identical 32-byte addresses and identical secret values.

## sign-04-3: Specified and implemented hash instantiations are incompatible

Severity: Low
Status: Confirmed
Layer: Implementation
Affected: All eight CEDRUSALPHA parameter sets, reference and optimized implementations
Discovery: Trivial
Exploitation: Cross-implementation verification failure; no cryptographic attack demonstrated
Credit: shiyuan (NGCC PKC Forum sender)
Date: 2026-09-22
Original source: [NGCC PKC Forum report](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/3PASZVC2PGWVNXMF7K5T7S2KZ2RZRZLX/)

Shiyuan documented the mismatch in the [NGCC PKC Forum](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/3PASZVC2PGWVNXMF7K5T7S2KZ2RZRZLX/). Specification Section 1.11 pads `PK.seed` to one 64-byte SM3 block, uses the 22-byte compressed address `ADRS^c`, and includes `PK.seed` in `PRF(PK.seed,SK.seed,ADRS)`. The code instead hashes `SPX_N` bytes of `PK.seed` followed by the full 32-byte address, while `prf_addr()` hashes only `SK.seed || ADRS` and receives no public seed.

Thus a conforming implementation of the PDF cannot reproduce the submitted keys, signatures, or verification results. The discrepancy also removes the specified public-seed domain separation from secret-value generation, but no cross-key attack follows from that omission alone.

### Reproducing

```sh
pdftotext -layout sign-04/sign-04-spec.pdf - | grep -A8 'pad the PK.seed'
sed -n '12,30p' sign-04/Implementations/Reference_Implementation/CEDRUSALPHA-160s/hash_sm3.c
sed -n '12,24p' sign-04/Implementations/Reference_Implementation/CEDRUSALPHA-160s/thash_sm3_simple.c
```
