<!-- synced from ngcc1/kex-02/report.md -->
Candidate: AFS-KEX
Family: Lattice (Module-LWE AKE)
Scope: Uniform-API reference wrappers, all three parameter sets
Archive: [AFS-KEX.zip](https://www.niccs.org.cn/niccs/Proposal/Public-Key%20Cryptographic%20Algorithms/Round%201%20candidates/AFS-KEX.zip) (SHA-256: `7d902107b74870e512c84da82c6bfb386633ca864ddc7df2f7b0b183511f983a`)
Severity: Critical
Discovery: Trivial
Exploitation: Trivial after later long-term-key compromise
Credit: Markku-Juhani O. Saarinen <markku-juhani.saarinen@tuni.fi>, with AI assistance
Date: 2026-09-21

## The ephemeral key is generated once as long-term state

The specification requires fresh AFS ephemeral key material for each session and claims completed-session forward secrecy after later compromise of long-term keys.

The uniform wrapper instead generates `seed_e` and calls the ephemeral key generator inside `kex_init_self`. It embeds the resulting `pk_e/sk_e` into the composite public and secret keys returned as the party's long-term material and stores `seed_e` in the persistent state. Later pass functions reuse that material and never generate a fresh per-session ephemeral key.

This gives a direct completed-session key-recovery attack. A passive attacker records `m1 = ct_B` and the `ct_A` prefix of `m2`. After the session completes, compromise of the two API long-term secret keys exposes `csk_B` and `csk_A` in their first halves. The attacker decapsulates the recorded ciphertexts to recover `K_B` and `K_A`, then computes the public session KDF `XOF(K_B || K_A)`. The result is the exact erased session key. No cryptanalysis or search is required.

Ephemeral AFS keys must be generated for each protocol execution, kept outside long-term key serialization, and erased when the session completes.

## Reproducing

```sh
make -C kex-02 exploit
kex-02/reproduce_pfs_break
kex-02/reproduce_pfs_break_c256
kex-02/reproduce_pfs_break_c512
```

The three drivers complete honest C128, C256, and C512 exchanges, erase both session-state buffers, and recover each session key using only the recorded first two flights and the subsequently compromised API long-term keys. They also check that the true static-key halves alone do not recover the key.

```text
ATTACK kex-pfs-recovery AFS_KEX_C128 CONFIRMED recorded m1/m2 plus later API long-term-key compromise recovered erased session key 1218217aea48c0aee27983653641600a (static-only control differs)
ATTACK kex-pfs-recovery AFS_KEX_C256 CONFIRMED recorded m1/m2 plus later API long-term-key compromise recovered erased session key 40076703841413297c9105f888a439d48f6015ab23774c9539b3ce6e19eeff5e (static-only control differs)
ATTACK kex-pfs-recovery AFS_KEX_C512 CONFIRMED recorded m1/m2 plus later API long-term-key compromise recovered erased session key 12033302a024a20f0d4498daafdc87c3c91d7c9b7479be51280d1cacf286a0b9eab8d3593771c3260f60eaf02cdc4101b3828a0e4d9ebc3bbe742aee77830a1f (static-only control differs)
```
