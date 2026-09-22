<!-- synchronized report: sign-32/report.md -->
Candidate: UVW
Family: Multivariate (F3)
Archive: [UVW signature.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/UVW%20signature.zip) (SHA-256: `bbfa8dad5ee57083578b50b9937e773e6158f72646e825da3d3265cc00cb1294`)

## sign-32-1: Every signature is accepted

Severity: Critical
Status: Confirmed
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

## sign-32-2: An all-zero signature crashes two verifier instances

Severity: High
Status: Confirmed
Layer: Implementation
Affected: UVW-128 and UVW-256 reference implementations
Discovery: Trivial
Exploitation: Unauthenticated denial of service
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

Direct verifier calls with a correctly sized all-zero signature crash the UVW-128 and UVW-256 implementations while deserializing or processing the malformed response. Signature verification is normally exposed to unauthenticated input, so this is a remotely triggerable denial of service independent of the universal-forgery return-value error in `sign-32-1`.

The unconditional-success wrapper hides ordinary nonzero verification results, but it cannot make a memory fault safe. Verification must validate every decoded length, index, and object before use and return rejection for malformed encodings.

### Reproducing

Run either affected instance through the guarded verifier driver:

```sh
tools/ngcc_attack sig-accept-all sign-32/lib/libUVW-128.so
```

Its verdict records `all-zero signature CRASHED the verifier` instead of a normal rejection. UVW-512 did not reproduce this crash and is not included in this finding.
