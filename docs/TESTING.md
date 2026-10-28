# Verification scope

- 26 offline Python state-machine/adversarial tests: all verdict rules, permissions, ordering, duplicate submissions/IDs/approvals, immutable evidence URLs, invalid UTF-8, size bounds, empty evidence, HTTP errors, hash mismatch, exact link spoofing, disclosure boundaries, invented citations, malformed model output, stale hashes, challenge history, and two-party finalization.
- 13 JavaScript tests: accepted versus finalized, finalized execution failure, canceled/undetermined transactions, polling, transport error, timeout/resume, numeric Studio status, missing execution proof, known SHA-256 vector, account/hash validation, decoded receipt matching, and rejection of unrelated/leader-only receipts.
- GenVM linter 0.11.0: AST lint and semantic validation; 7 public methods, 5 write and 2 view.
- Actual pinned SDK direct-mode smoke: mocked HTTP/AI, real SDK and storage; create → submit → assess → finalize. This caught the stable SDK's `Response.status` API and JSON response type before release deployment.
- Vite production build.
- Browser QA and live network transaction evidence are recorded in EVIDENCE.md.

Local mocks are intentionally isolated from the real SDK in the unittest process. Direct-mode smoke runs in a fresh Python process. Neither replaces live GenVM/consensus verification. Review outcomes in EVIDENCE.md are factual observations, not promises of AI accuracy.

The direct smoke explicitly selects the public GenVM release `v0.2.16` when loading SDK artifacts. This avoids the test harness auto-selecting an unavailable release candidate. Development dependency security fixes are locked; `npm audit` reported zero vulnerabilities after updating Vite to 7.3.7.
