<!-- synchronized report: kem-40/report.md -->
Candidate: YuanYang.KEM
Family: Lattice (NTRU)
Archive: [YuanYang.KEM.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/YuanYang.KEM.zip) (SHA-256: `fe1bf3d78272bb79048e7d456819160324c6140206798cb77a22c2babcfdcf4a`)

## kem-40-1: Encryption discards the specified error polynomial

Severity: Medium
Status: Confirmed
Layer: Implementation
Affected: Reference implementation, all three parameter sets
Discovery: Trivial
Exploitation: Security-proof gap; no complete attack demonstrated
Credit: Yijian Liu (archive sender `Yijian_Liu`)
Date: 2026-09-22
Original source: [NGCC PKC Forum report](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/FXRFQBH243BPG4XMEBKRPWCAQVGINRWF/)

Algorithm 3 specifies `c_bar = h*s + e + m*p^-1 mod q`, and the IND-CPA proof invokes decisional Ring-LWE for `(h, h*s+e)`. Every submitted `yy_encrypt` samples both `s` and `e`, but computes the ciphertext from `h*s` and the encoded message without ever reading `e` again.

This confirms Yijian Liu's [mailing-list report](https://list.niccs.org.cn/archives/list/pkcforum@list.niccs.org.cn/message/FXRFQBH243BPG4XMEBKRPWCAQVGINRWF/). The shipped ciphertext distribution is not the distribution analyzed by the proof or the failure calculation. Omitting `e` is not by itself a demonstrated message-recovery attack—classical NTRU encryption can use a single ephemeral short polynomial—but the submitted implementation cannot claim the stated Ring-LWE reduction without a new analysis.

### Reproducing

```sh
python3 kem-40/reproduce_unused_error.py
```

The static witness checks all three independent implementation copies and fails unless `e` is sampled and then absent from the remainder of `yy_encrypt`.
