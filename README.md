# SponsorProof

**Intelligent verification of sponsored-content commitments.**

Brands and creators can agree a brief and still disagree about what the delivered content communicates. SponsorProof turns that brief, the exact submitted evidence, and the assessment into a shared, inspectable contract record.

- Python Intelligent Contract on GenLayer Studionet.
- Immutable campaign requirements and commit-pinned public UTF-8 snapshots.
- SHA-256 integrity checks, deterministic URL/disclosure checks, and AI consensus for paraphrased product messages.
- Per-message evidence quotes, decision hashes, append-only review history, one challenge, and approval by both parties.
- Responsive frontend with live contract reads and verified transaction tracking.
- No escrow, payments, tokens, reach estimates, ownership claims, posting-time judgments, or video analysis.

## Try it

Public website and final verified address are recorded in [DEPLOYMENT.md](docs/DEPLOYMENT.md). [EVIDENCE.md](docs/EVIDENCE.md) records real transaction outcomes. [SUBMISSION.md](docs/SUBMISSION.md) contains submission text and the integration caveat.

**Signing is a manual Studio handoff.** GenLayer Studio's built-in wallet does not expose a cross-origin signer. The frontend prepares the exact function arguments and opens the deployed contract in Studio. Sign there with a built-in account using **Normal (Full Consensus)**, then paste the transaction hash into SponsorProof. The app decodes the real calldata and checks the target contract, signer, method, arguments, and consensus mode before monitoring pending → accepted → finalized or failed. It never asks for a private key and never invokes MetaMask. This is genuine live read/receipt integration, but it is **not one-click frontend transaction submission**. Do not describe it as such.

## How to use

1. Open Studio and copy a built-in account's full address. Set that address in SponsorProof. Address entry is a reference, not a wallet connection.
2. Create a campaign: give it a unique ID, nominate a creator address, and commit 1–5 product messages, an exact HTTPS link, and a disclosure.
3. Sign the prepared `create_campaign` in Studio. Link its hash to track it.
4. As the nominated creator, submit an immutable `.txt` snapshot URL, its SHA-256, and the original source reference.
5. Either party can request a review. Validators independently fetch the snapshot, agree its bytes, and assess the messages.
6. Either party can challenge once with a reason and replacement evidence. Earlier reviews remain visible and approvals reset.
7. Both parties accept the latest decision hash with `finalize_delivery`. The contract records `FINALIZED` only after both approvals; no funds move.

Requirements and all evidence are public. Use distinct brand/creator accounts for a real two-party demonstration; the contract also allows a self-test with one account in both roles.

## Evidence and verdicts

V1 deliberately supports a narrow reproducible evidence format: `https://raw.githubusercontent.com/OWNER/REPO/40_HEX_COMMIT/path.txt`, maximum 16,000 bytes, valid UTF-8. Links are exact whitespace-delimited URL tokens. Put the required URL on its own line. Disclosure matching is case-insensitive with word boundaries. A message marked MET must contain a literal quotation present in the snapshot.

| Verdict | Rule |
| --- | --- |
| FULFILLED | All checks MET |
| PARTIAL | At least one MET and at least one MISSING |
| NOT_FULFILLED | All checks MISSING |
| INCONCLUSIVE | Any UNCERTAIN check, inaccessible/invalid evidence, or hash mismatch |

Malformed AI output or consensus failure fails the transaction and preserves earlier committed state. The model cannot directly choose the aggregate verdict. The deterministic contract computes it from the validated checks.

**A hash authenticates bytes, not the provenance of a social post.** HTTPS authenticates the snapshot host. Commit pinning fixes the submitted bytes. The original source URL is self-reported and is not independently proven to match the original post. Synthetic fixtures are prominently labeled. A FULFILLED result means only that the snapshot communicates the committed text requirements; it does not prove the factual truth of those claims.

## Run locally

Requires Node 22+ and Python 3.12+. The exact JavaScript dependencies are locked.

```sh
npm ci
npm test
npm run build
npm run dev
```

Additional GenLayer verification:

```sh
python -m pip install genvm-linter==0.11.0 genlayer-test==0.29.2
python /path/to/genvm-lint check contracts/sponsorproof.py
python scripts/direct-test.py
```

`npm test` runs mocked contract state-machine/adversarial logic tests and frontend receipt/lifecycle tests. `scripts/direct-test.py` loads the actual pinned v0.2.16 GenLayer SDK with mocked web/LLM calls; it checks runtime API compatibility, storage, review, and finalization. These local tests do not claim real AI consensus. Live evidence is recorded separately.

## Contract API

| Function | Authorization | Effect |
| --- | --- | --- |
| `create_campaign(id, title, creator, requirements_json)` | Caller becomes brand | Locks requirements |
| `submit_delivery(id, url, sha256, source_url)` | Nominated creator | Locks initial evidence |
| `review_delivery(id)` | Either party | Fetches, hashes and assesses evidence |
| `challenge_review(id, reason, url, sha256, source_url)` | Either party; once | Preserves decision and submits new evidence |
| `finalize_delivery(id, decision_hash)` | Either party | Approves latest hash; both approvals finalize |
| `get_campaign(id)` | Public | JSON record with entire history |
| `list_campaigns(offset, limit)` | Public | Paginated IDs; maximum 50 per call |

State path: CREATED → SUBMITTED → REVIEWED → optional CHALLENGED → REVIEWED → FINALIZED. A challenge can occur while one party has accepted; it clears all approvals. There is no automatic timeout settlement: withholding acceptance can leave a campaign unresolved. This prevents unilateral settlement in V1.

## Architecture

`contracts/sponsorproof.py` is standalone with an immutable runner dependency. JSON strings in typed `TreeMap` storage keep the public ABI simple. Fetching runs in a strict equivalence block. Semantic evaluation runs in a separate comparative block over the agreed bytes; storage is not accessed within nondeterministic callbacks. Validator assessment must agree on each ordered status and material conclusions.

`src/chain.js` uses the official `genlayer-js` SDK for reads and receipt tracking. The UI handles numeric Studio statuses, array leader receipts, execution reverts, transport failures, pending timeouts, and resume without duplicate writes. Transaction plans and hashes are saved locally. No key material is stored or collected.

## Continued development

Next: an audited Studio wallet bridge or an explicitly selected signed-wallet integration for direct writes; signed creator/platform provenance attestations; approved source adapters; durable archival receipts; independent adversarial AI evaluation; and deployment to a production-like signed network. Escrow requires a separate security design and is intentionally absent.

See [SECURITY.md](SECURITY.md) for trust boundaries and [TESTING.md](docs/TESTING.md) for verification scope.
