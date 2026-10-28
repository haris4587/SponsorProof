# Deployment

- Network: GenLayer **Studionet** (hosted Studio development sandbox), chain ID **61999**.
- RPC: `https://studio.genlayer.com/api`.
- Public app: https://sponsorproof.keenbasil9.chatgpt.site
- Final contract: [`0x57Edf2573acFDba8F9D6e712DF12B96A94633236`](https://explorer-studio.genlayer.com/address/0x57Edf2573acFDba8F9D6e712DF12B96A94633236)
- Deployment transaction: [`0x081b826980021321b0cabaed8d2628b5096c52f9577b8a01faeda1f683abe565`](https://explorer-studio.genlayer.com/tx/0x081b826980021321b0cabaed8d2628b5096c52f9577b8a01faeda1f683abe565).
- Studio import: https://studio.genlayer.com/?import-contract=0x57Edf2573acFDba8F9D6e712DF12B96A94633236
- Demo campaign ID: `aster-launch-demo`.
- Runtime: GenVM `v0.2.16`, `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.
- JavaScript SDK: `genlayer-js@1.1.8`, locked with `package-lock.json`.

The deployment and all demonstrated writes were signed using **GenLayer Studio's built-in accounts**, with **Normal (Full Consensus)** selected. No MetaMask integration or copied private keys were used. The exact deployed source is `contracts/sponsorproof.py`; its SHA-256 and byte comparison are in [verification.json](verification.json).

The frontend is a Vite static build. `src/deployment.json` records its configured network, address, deployment transaction, demo ID and immutable fixture commit. It performs live SDK reads and decoded receipt/lifecycle verification. Writes use a **manual Studio signing handoff**; see README. Merely entering an address never signs a transaction or connects a wallet.

## Reproduce without redeploying

```sh
npm ci
npm test
npm run build
node scripts/live.mjs inspect
node scripts/live.mjs read aster-launch-demo
node scripts/collect-evidence.mjs
```

The evidence collector only reads existing transactions and contract state. It does not deploy or send writes.

## Deployment procedure for changed contract source only

1. Run the mocked tests, actual SDK direct smoke, and GenVM lint/semantic validation.
2. Import `contracts/sponsorproof.py` in Studio. Keep Normal (Full Consensus), select a built-in account, and deploy once.
3. Wait for FINALIZED and verify successful execution, not only consensus acceptance.
4. Read the deployment transaction's `data.contract_code`, decode it, and compare byte for byte with the source file.
5. Update `src/deployment.json` only with verified values. Rebuild, publish the same source state, and perform public browser QA.

Do not redeploy unchanged source. The original deployment at `0x3Bf1Bfb70c385f7dE54A4D9c3272bFbb8186cEA9` is **superseded**. Live testing caught an HTTP response-field mismatch between newer docs and the pinned stable SDK. The corrected release uses the stable SDK's `Response.status` and explicit JSON model output. [superseded-transactions.ndjson](superseded-transactions.ndjson) retains that history; it is not claimed as successful semantic verification.

Studionet availability and persisted state can change or reset. No production deployment or security audit is claimed.
