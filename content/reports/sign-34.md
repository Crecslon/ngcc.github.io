<!-- synced from ngcc1/sign-34/report.md -->
Candidate: YuanYang.DSA
Family: Lattice-based (NTRU hash-and-sign)
Archive: [YuanYang.DSA.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/YuanYang.DSA.zip) (SHA-256: `1eb45f24ad8f7ff25db923479c6500f273aee8b2470d76339030fed8d96b5b31`)

## sign-34-1: Wrong perturbation covariance leaks secret-basis information

Severity: High
Status: Confirmed
Layer: Implementation
Affected: YuanYang.DSA-512, -1024, and -2048 reference implementations
Discovery: Non-trivial
Exploitation: Key-dependent transcript distinguisher from a few thousand signatures; complete key recovery not demonstrated
Credit: Kris Kwiatkowski <contact@amongbytes.com>
Date: 2026-09-22

The specification represents the NTRU basis vectors as columns and requires perturbation covariance `Sigma_p = sigma^2 I - B_hat B_hat^*`. The implementation's `sigma_p_set_slot()` instead subtracts `B_hat^* B_hat`, the Gram matrix of those basis vectors. Since the two matrix products differ for this non-normal basis, the intended cancellation fails and leaves secret-dependent variance and cross-covariance in every signature.

For each Fourier slot, the diagonal leakage predicts `Var(s1)=sigma_eff^2-|g|^2+|F_hat|^2` and the opposite deviation in `Var(s2)`. The off-diagonal covariance combines with that difference to expose an approximation to the slotwise ratio `f/g`. The public-data reproducer decodes only published signature bytes and never reads the secret key. On an independently generated YuanYang-512 key, 4,000 signatures produced a 7.4-sigma dispersion and a 2.23-fold slot-variance spread; a spherical control produced 1.0 sigma and a 1.08-fold spread. The faulty source is byte-identical across all three parameter sets.

This confirms substantial key-dependent leakage and invalidates the claimed spherical-transcript simulation. It does not yet recover `(f,g)` or forge a signature: the proposed final rank-one module-lattice recovery has not been implemented, and the observed ratio estimate retains a systematic error floor. The implementation must subtract `B_hat B_hat^*`, and the repaired sampler must be revalidated statistically.

### Reproducing

The public-data reproducer was submitted in [ngcc-harness PR #3](https://github.com/ngcc-dev/ngcc-harness/pull/3).

```sh
make -C sign-34 exploit
sign-34/reproduce_transcript_leak sign-34/lib/libyuanyang-512.so 4000
```

The same run prints the `sign-34-2` packing witness; its 4,000-signature count
is needed by the `sign-34-1` statistical test, not by this encoding check.

## sign-34-2: Non-injective public-key packing creates key aliases

Severity: Medium
Status: Confirmed
Layer: Implementation
Affected: YuanYang.DSA-512, -1024, and -2048 public-key encodings
Discovery: Moderate
Exploitation: Trivial transformation of an aliasable packed block
Credit: Kris Kwiatkowski <contact@amongbytes.com>
Date: 2026-09-22

The implementation packs four coefficients as a fixed-width radix-`q` integer but never rejects integers at least `q^4`. Decoding uses repeated reduction modulo `q`, so adding `q^4` to any block with sufficient encoding slack changes the byte string while recovering exactly the same four coefficients.

For the 512, 1024, and 2048 sets, the block widths are 46, 49, and 52 bits and unused codeword fractions are approximately 25.70%, 28.38%, and 22.71%. The boundary words `0` and `q^4` decode to the same coefficient tuple in every set. The runtime witness alters an actual YuanYang-512 public key and confirms that its bytes differ while the same signature verifies under both encodings.

This is not an EUF-CMA forgery, because the mathematical public key is unchanged. It breaks canonical key identity and can defeat systems that fingerprint, pin, compare, or hash serialized public keys. Decoding must reject each packed block unless it is strictly below `q^4`, or re-encode and compare the complete public-key byte string.

### Reproducing

The encoding witness was submitted in [ngcc-harness PR #3](https://github.com/ngcc-dev/ngcc-harness/pull/3).

```sh
make -C sign-34 exploit
sign-34/reproduce_transcript_leak sign-34/lib/libyuanyang-512.so 4000
```
