<!-- synchronized report: sign-25/report.md -->
Candidate: SQIsign2D2
Family: Isogeny
Archive: [SQIsign2D2.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/SQIsign2D2.zip) (SHA-256: `cf635de5eebbdeb7b2212e84f349da4ca878889e0a4a59b463d0c8cdfdb8eeab`)

## sign-25-1: Verifier verdict is decided by stale stack contents

Severity: Critical
Status: Confirmed
Layer: Implementation
Affected: Level2-eff uncompressed reference implementation
Discovery: Trivial
Exploitation: Trivial
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

The Level2-eff uncompressed verifier accepts a full-length all-zero signature, and
accepts a valid signature after the message is changed, when either is verified after
another verification in the same process. The same all-zero signature is rejected when
the stack below the verifier is overwritten first. The verdict is therefore not a
function of the signature.

`protocols_verif_internal` is compiled with `-DNDEBUG`, which removes the point-order
and codomain `assert`s that the verification path relies on, and several further checks
are commented out in the shipped source. For a malformed signature the dim-2 isogeny
chain leaves its codomain partly unwritten, and the final j-invariant comparison then
reads whatever the previous call left on the stack. Two independent tests confirm the
mechanism: overwriting the stack between calls, and rebuilding the instance with
`-ftrivial-auto-var-init=zero`, each make both forgeries reject.

`-DNDEBUG` is the candidate's own default release configuration: the shipped sqisign
Makefiles set `BUILD ?= release` and `RELEASE_CFLAGS := -O2 -DNDEBUG`. The harness mirrors
that default; it did not introduce the assert removal.

A verifier normally processes signatures one after another, so the accepting state is
the ordinary one: an attacker can submit an all-zero signature for a message of their
choice without making any signing query. Acceptance depends on process state rather
than on the attacker's input, which makes the behaviour unpredictable rather than safe.
The compressed instance built from the same tree is unaffected.

All eight uncompressed submitted instances were tested with the same primed-versus-
scrubbed witness. Only Level2-eff uncompressed accepted the forged input; the other
seven rejected it in both states, as did the compressed Level2-eff control. The unsafe
assert-as-validation pattern is shared source, but demonstrated acceptance is therefore
scoped to Level2-eff uncompressed.

The verifier must initialise every value its decision reads, enforce the specified point,
order and codomain conditions unconditionally rather than through `assert`, and reject
zero or malformed decoded responses before protocol verification.

### Reproducing

Build the candidate and the reproducer, then run:

```sh
make -C api harness && make -C tools && make -C sign-25
tools/ngcc_attack sig-uninit-verdict sign-25/lib/libSQISign2Dsquare-Level2-eff_uncompressed.so
```

The check verifies one all-zero signature twice, once after a genuine verification and
once after overwriting the stack, and reports the two verdicts. The compressed instance
is run as a control and rejects both. `tools/reproduce.sh` runs this together with the
other supported runtime witnesses and their controls. See `tools/README.md`.
