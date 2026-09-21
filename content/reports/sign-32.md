<!-- synced from ngcc1/sign-32/report.md -->
Candidate: UVW
Family: Multivariate (F3)
Archive: [UVW signature.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/UVW%20signature.zip) (SHA-256: `bbfa8dad5ee57083578b50b9937e773e6158f72646e825da3d3265cc00cb1294`)

## sign-32-1: Every signature is accepted

Severity: Critical
Layer: Implementation
Affected: Reference implementation, all three parameter sets
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

The internal `uvw_verify` routine computes the intended verification predicate. The API wrapper converts that result to `0` or `-1`, stores it in a local variable, and then unconditionally returns `0`.

Consequently, invalid signatures, modified messages, and arbitrary full-length signature buffers are reported as valid by all three submitted reference instances. No cryptanalysis or signing query is required.

This permits universal forgery through the submitted API and directly violates the claimed EUF-CMA security.

The wrapper must return the computed verification result rather than an unconditional success value. Tests must include invalid signatures and modified messages, not only valid KAT signatures.

### Reproducing

Build the candidate and the reproducer, then run:

```sh
make -C api harness && make -C tools && make -C sign-32
tools/ngcc_attack sig-accept-all sign-32/lib/libUVW-128.so
```

`tools/reproduce.sh` runs this together with the other supported runtime
witnesses and their controls. See `tools/README.md`.
