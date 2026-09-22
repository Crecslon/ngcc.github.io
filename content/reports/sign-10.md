<!-- synced from ngcc1/sign-10/report.md -->
Candidate: Facto-DSA
Family: Multivariate (cubic factorisation)
Archive: [Facto-DSA.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/Facto-DSA.zip) (SHA-256: `b3de38fcc2d92ce83290d17cb250dde61f95d3326a49ada36fad3c578f2fc509`)

## sign-10-1: The hidden zero subspace has an unpriced algebraic recovery path

Severity: High
Status: Lead
Layer: Design
Affected: Facto-DSA-128, -256, and -512 security estimates
Discovery: Non-trivial
Exploitation: Full-size costs are extrapolated; approximately 2^55, 2^96, and 2^185 under the observed solving-degree model
Credit: Kris Kwiatkowski <contact@amongbytes.com>
Date: 2026-09-22

The specification prices recovery of one nonzero vector in `K2 = ker(L2)` as an unstructured `q^n` search. But `K2` is an `n`-dimensional linear subspace contained in the zero locus of the public homogeneous cubic map. A random `(n+1)`-dimensional linear subspace of the `2n`-dimensional ambient space must meet `K2` nontrivially. Restricting the public map to it therefore gives `m` cubic equations in `n` affine variables with a guaranteed rational solution, which can be attacked algebraically rather than by guessing ambient points.

The submitted `build_public_key()` directly constructs `Q(L1*z)+R(L2*z)`, multiplies it by `Y=L2*z`, and applies the public output map `T`, confirming that the source has the structure used by the attack. The supplied specification-derived implementation reproduces the submitted parameter sizes and signing behavior, and confirms at full dimensions that `K2` has dimension `n` and the public map vanishes on it. Public-key-only reduced experiments recover the exact secret `K2` for `n=5,6,7`; the `n=7` instance reached solving degree 8 and completed in about 349 seconds in this review. Reduced `s=1` experiments then recover the coordinate separation, hidden quadratic space, symmetriser, and an equivalent triangular central map.

If solving degree remains `n+1`, the specification's own cubic-linear-algebra model gives `3*log2(binomial(2n+1,n+1))`, or approximately 55.3, 96.2, and 184.9 bits. This is not yet a confirmed submitted-size break: the degree pattern is extrapolated, Facto-DSA-128 has the less-overdetermined `s=6` shape, no full-size solve was run, and the final rational-normal-curve/GRS container identification needed for a working forgery was not implemented. The result nevertheless invalidates treating `q^n` search as the only structural recovery model and warrants a new full-scale algebraic analysis.

### Reproducing

The specification-derived attack code was submitted in [ngcc-harness PR #3](https://github.com/ngcc-dev/ngcc-harness/pull/3).

```sh
make -C sign-10/cryptanalysis
make -C sign-10/cryptanalysis test

# Optional larger reduced instance; about six minutes on the audit host.
sign-10/cryptanalysis/build/attack1 7 12 1 12
```
