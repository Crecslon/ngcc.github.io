<!-- synchronized report: hash-32/report.md -->
Candidate: ZC-EDMC
Family: Symmetric (sponge)
Archive: [ZC-EDMC.zip](https://www.niccs.org.cn/niccs/Proposal/Cryptographic%20Hash%20Algorithms/Round%201%20candidates/ZC-EDMC.zip) (SHA-256: `235157f178c0ec885dad4062ee232cdc0d16e95474f05c6f93038fd951ca3712`)

## hash-32-1: The specified and implemented ZC-EDMC mappings differ

Severity: Low
Status: Confirmed
Layer: Design
Affected: All six ZC-EDMC parameter sets
Discovery: Trivial
Exploitation: Trivial
Credit: Cryptanalysts001, Institute of Software, Chinese Academy of Sciences <yufei2021@iscas.ac.cn>
Date: 2026-09-22
Original source: [CryptHashForum report](https://list.niccs.org.cn/archives/list/crypthashforum@list.niccs.org.cn/message/6BKFT5FXW3PL3ZXWNQFTLEIQOJSXZTWK/)

The construction prose and Algorithm 3 define the compression mapping with two different six-round halves, `h(g(X) xor (0^r || X_c))`. A displayed equation instead uses `h(h(X) xor ...)`, and the reference implementation invokes the same last-six-round function twice. It therefore implements the displayed equation rather than Algorithm 3.

The submitted permutation constants introduce a second deterministic mismatch: rounds 5--7 and 9--11 of the code's twelve-round schedule are permuted relative to the specification table. The submitters independently modeled the code schedule and reproduced its KATs, and report that changing the inner call from `h` to `g` changes all 22 tested digests for each of the six instances. This is an interoperability and analysis-target defect, not a demonstrated collision or preimage attack.

### Reproducing

The local checker verifies both calls in every reference instance and the exact submitted constant schedule:

```sh
make -C hash-32 reproduce-forum
```
