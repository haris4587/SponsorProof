# Project Explorer submission

## Project name
SponsorProof

## Tagline
Intelligent verification of sponsored-content commitments.

## Description
SponsorProof helps brands and creators resolve disagreement about whether delivered sponsored text communicates an agreed campaign brief. A Python GenLayer Intelligent Contract commits required product messages, an exact link, and an advertising disclosure. Validators independently retrieve a commit-pinned public text snapshot, verify its SHA-256, and assess paraphrased product messages through comparative AI consensus. Deterministic code checks links, disclosures, evidence quotes, permissions, state transitions, and the aggregate verdict.

Results are FULFILLED, PARTIAL, NOT_FULFILLED, or INCONCLUSIVE. Each review retains an evidence hash, agreement hash, decision hash, and per-message findings. Either party can challenge once with replacement evidence. Both parties must accept the latest decision hash before application finalization. The prototype never releases payments.

## Why this needs GenLayer
Natural-language product messages cannot be checked reliably by exact-string matching. SponsorProof combines independent semantic assessment with deterministic integrity and lifecycle rules, preserving a shared decision trail rather than trusting a single centralized AI service.

## Links
- Repository: https://github.com/haris4587/SponsorProof
- Public app: https://sponsorproof.keenbasil9.chatgpt.site
- Network, verified contract address and deployment transaction: [DEPLOYMENT.md](DEPLOYMENT.md)
- Demonstrated transactions and screenshots: [EVIDENCE.md](EVIDENCE.md)

## Interaction disclosure — include this in the submission
The website reads the deployed contract and verifies/tracks real transactions using the official GenLayer SDK. Signing uses a manual handoff to GenLayer Studio's built-in wallet. The website prepares exact arguments, the user signs in Studio, and the website verifies the resulting hash against the intended contract, signer, method, arguments, and Full Consensus mode. It does not provide one-click direct writes from the website or claim to connect to Studio's private signing key. If Project Explorer requires direct frontend submission, this requirement remains unmet until GenLayer provides a signer bridge or a separate signing integration is explicitly accepted.

## Evidence limitations — include this in the submission
The demo is synthetic and publicly labeled. Hashes authenticate snapshot bytes, not the provenance of an original social post. Original source references are self-reported. V1 does not prove publication time, account ownership, reach, engagement, video, or the truth of product claims. This is a Studionet prototype, not a production security-audited settlement system.

## Categories
Intelligent Contracts · AI Consensus · Creator Economy · Evidence Verification · Dispute Workflow

## Roadmap
Signed platform/creator provenance; immutable archive attestations; audited direct signing; expanded source adapters; production-like network validation; independent adversarial evaluation. Payment/escrow is a separate future security design.

No Project Explorer form or public promotional post has been submitted automatically. These materials are for review and submission by the project owner.
