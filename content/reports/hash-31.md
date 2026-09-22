<!-- synchronized report: hash-31/report.md -->
Candidate: The ZC-DMC Hash Function
Family: Symmetric (feed-forward sponge)
Archive: [ZC-DMC.zip](https://www.niccs.org.cn/niccs/Proposal/Cryptographic%20Hash%20Algorithms/Round%201%20candidates/ZC-DMC.zip) (SHA-256: `b6da323d388d3411b882228152f25626999502b8c246cc0c9b64a0a9d72eaaac`)

## hash-31-1: Cross-domain distinguisher between ZC-1536-512 and ZC-1536-768

Severity: Medium
Status: Lead
Layer: Design
Affected: Specified ZC-DMC-1536-512 and ZC-DMC-1536-768 construction
Discovery: Moderate
Exploitation: Moderate
Credit: Tsinghua Hash Lab <cuihr26@mails.tsinghua.edu.cn>
Date: 2026-09-22
Original source: [CryptHashForum report](https://list.niccs.org.cn/archives/list/crypthashforum@list.niccs.org.cn/message/CVL24T5A4ILSD6V2GACF73MENNFQC3JB/)

The two instances share the same 1536-bit permutation and zero initial state, while moving the rate/capacity feed-forward boundary. A three-block synchronization construction in the specification makes the final states agree in their leading 704 bits; fixing a removable four-bit suffix accommodates the mandatory `M || 01 || 10*1` padding. Consequently the first 64-bit squeeze blocks are equal, an event with probability `2^-64` for independent random functions.

This is a cross-profile distinguisher, not a same-instance collision. The message gives the construction and its probability but no concrete messages, and we have not yet generated an implementation-level witness; the report therefore remains a Lead.
