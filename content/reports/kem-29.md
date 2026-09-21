<!-- synced from ngcc1/kem-29/report.md -->
Candidate: Polar-KEM
Family: Lattice (polar-code-defined)
Scope: Reference implementation, all three parameter sets
Archive: [Polar-KEM.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/Polar-KEM.zip) (SHA-256: `3ae9d4f1a717fb473e76447014d585cd5d14fe38728f02b1a044cc6a2d03e16d`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## The submission ships a complete public-key-only break

The submission's own shipped functions provide the complete attack. `polarkem_recover_message(pk, ct, mu)` and `polarkem_derive_valid_secret(mu, ct, ss)` are declared in `polarkem_ct.h` and implemented in the submitted reference source. They recover the encapsulated message and derive the exact shared secret using only public inputs.

The frozen specification does not have this defect: it defines the public key as the disguised basis `B_pk = O * B_red`, keeps the orthogonal transformation `O` in the secret key, and requires decapsulation to apply `O^-1` before decoding. The submitted implementation does not implement that construction. Instead, `polarkem_recover_message` expands a signed permutation from the seed at `pk + POLARKEM_PK_SEED_OFFSET`, making the implementation's decoding transform public. Secret-key material is consulted only to derive the fallback secret for invalid ciphertexts.

Independent execution against the three built libraries called `polarkem_recover_message(pk, ct, mu)` followed by `polarkem_derive_valid_secret(mu, ct, ss)`. The result exactly matched the encapsulator's 16-, 32-, and 64-byte secrets for PolarKEM-128, PolarKEM-256, and PolarKEM-512 without supplying any secret-key bytes.

Anyone observing a public key and ciphertext can therefore recover the session key by calling code shipped by the candidate. This is a total break of the submitted implementation at every level, but it is not an attack on the secret-isometry construction described by the specification.

## Reproducing

Build the candidate and the reproducer, then run:

```sh
make -C api harness && make -C tools && make -C kem-29
python3 kem-29/reproduce_public_recovery.py
```

`tools/reproduce.sh` runs this together with every other reported
finding and its controls. See `tools/README.md`.
