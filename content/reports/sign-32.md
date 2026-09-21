<!-- synced from ngcc1/sign-32/report.md -->
Candidate: UVW
Scope: Reference implementation, all three parameter sets
Archive: orig/sign-32/orig.zip (SHA-256: `bbfa8dad5ee57083578b50b9937e773e6158f72646e825da3d3265cc00cb1294`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## Every signature is accepted

The internal `uvw_verify` routine computes the intended verification predicate. The API wrapper converts that result to `0` or `-1`, stores it in a local variable, and then unconditionally returns `0`.

Consequently, invalid signatures, modified messages, and arbitrary full-length signature buffers are reported as valid by all three submitted reference instances. No cryptanalysis or signing query is required.

This permits universal forgery through the submitted API and directly violates the claimed EUF-CMA security.

The wrapper must return the computed verification result rather than an unconditional success value. Tests must include invalid signatures and modified messages, not only valid KAT signatures.
