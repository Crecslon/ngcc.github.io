<!-- synced from ngcc1/kex-02/report.md -->
Candidate: AFS-KEX
Scope: Uniform-API reference wrappers, all three parameter sets
Archive: orig/kex-02/orig.zip (SHA-256: `7d902107b74870e512c84da82c6bfb386633ca864ddc7df2f7b0b183511f983a`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial after later long-term-key compromise
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## The ephemeral key is generated once as long-term state

The specification requires fresh AFS ephemeral key material for each session and claims completed-session forward secrecy after later compromise of long-term keys.

The uniform wrapper instead generates `seed_e` and calls the ephemeral key generator inside `kex_init_self`. It embeds the resulting `pk_e/sk_e` into the composite public and secret keys returned as the party's long-term material and stores `seed_e` in the persistent state. Later pass functions reuse that material and never generate a fresh per-session ephemeral key.

Reusing an initialized party therefore reuses the contribution on which the forward-secrecy argument depends. A later compromise of the returned composite long-term secret also reveals the supposedly ephemeral secret used by earlier sessions, directly invalidating the submitted PFS claim.

Ephemeral AFS keys must be generated for each protocol execution, kept outside long-term key serialization, and erased when the session completes.
