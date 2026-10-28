# Security and trust boundaries

SponsorProof is a Studionet prototype, not a payment or legal adjudication system.

## What is enforced

Immutable requirements, creator/party address checks, fixed state transitions, maximum one challenge, bounded text/array inputs, commit-pinned HTTPS raw text URLs, expected SHA-256, independent validator fetching, constrained verdict vocabulary, real substring citations for MET messages, deterministic aggregation, decision-hash-bound approvals, and review history retention.

## What remains unproven

Original-post provenance, account ownership on a social platform, publication/deletion time, audience reach, impressions, engagement, factual product claims, content outside the text snapshot, images, video, and commercial authenticity. The source reference is self-reported. A fabricated public snapshot can satisfy a text brief; it cannot establish a real campaign. Both parties must judge provenance before accepting.

## Wallet boundary

Studio signs with its own built-in browser-local wallet. SponsorProof cannot access that signer. Address entry is not authentication. Users sign in Studio and link hashes; the frontend decodes and validates the target, signer, calldata, and Full Consensus mode. It never requests private keys, recovery phrases, or MetaMask permissions. Do not paste secrets into contract arguments. Studio is a resettable development environment, not a production trust anchor.

## AI and public data

Requirements and snapshots are untrusted data. Prompts explicitly reject embedded instructions and require evidence quotes. Comparative consensus reduces single-model dependence, but validators and models can share biases and can agree on a wrong classification. Substring checks prove quote presence, not relevance; relevance remains an AI judgment. No claim is made that prompt injection is solved. The adversarial fixture is public; mocked offline tests do not demonstrate live prompt-injection resistance.

Raw GitHub commit URLs reduce mutable-page disagreement and SSRF exposure. Availability is not guaranteed, including removal of a repository or commit. The contract fetcher catches HTTP/UTF-8 failures and returns INCONCLUSIVE. Model/schema errors fail the transaction. Input byte limits are checked after fetching; V1 does not control upstream transfer size before the HTTP response is returned.

## Settlement and availability

No assets are held or transferred. Either party may withhold acceptance indefinitely. Challenges are bounded to avoid endless review loops. A final decision is immutable at the application level, but the Studio host's upgrade/admin capabilities and network resets remain part of the development-environment trust model. No production security audit has been performed.

Report a reproducible issue through the repository, omitting credentials and private campaign data.
