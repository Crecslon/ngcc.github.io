<!-- synced from ngcc1/sign-33/report.md -->
Candidate: VDOO
Family: Multivariate (UOV family)
Scope: Reference implementation, all three parameter sets
Archive: [VDOO.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/VDOO.zip) (SHA-256: `4b7bb0f15388b395b9308ae480f25622105a734f0ab4a6bd16398438c4b9752a`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Publicly reproducible signing keys

The implementation declares the API-provided `drng_algorithm` but never reads it. Key generation instead uses a second file-local global DRNG object that is never initialized by the shared-library wrapper and therefore starts from zero-initialized process memory.

Independent fresh-process tests with different API seeds generated identical VDOO public and secret keys. The result was directly reproduced against the built VDOO-256 library and the same RNG wiring is used by all submitted levels.

An attacker recovers the victim's secret signing key by starting a fresh process and invoking key generation once. No multivariate cryptanalysis is required.

All key-generation randomness must be derived from the initialized API DRNG; the uninitialized private generator must be removed or explicitly and securely seeded.

## Reproducing

Build the candidate and the reproducer, then run:

```sh
make -C api harness && make -C tools && make -C sign-33
tools/ngcc_attack keygen-fresh sign-33/lib/libvdoo_128.so 0x01
tools/ngcc_attack keygen-fresh sign-33/lib/libvdoo_128.so 0x99   # same key digest
```

`tools/reproduce.sh` runs this together with every other reported
finding and its controls. See `tools/README.md`.
