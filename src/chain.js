import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
export const RPC = 'https://studio.genlayer.com/api';
export const EXPLORER = 'https://explorer-studio.genlayer.com';
export const addressOK = value => /^0x[0-9a-fA-F]{40}$/.test(value || '');
export const hashOK = value => /^[0-9a-f]{64}$/.test(value || '');
export const txURL = hash => `${EXPLORER}/tx/${hash}`;
export function makeClient(address) {
  // Explicit JSON-RPC account object prevents implicit window.ethereum use.
  // Studionet is an unsigned sandbox; an address is NOT proof of ownership.
  return createClient({ chain: studionet, ...(address ? {account:{address,type:'json-rpc'}} : {}) });
}
export function classifyReceipt(tx) {
  const status = String(tx.statusName || tx.status || '').toUpperCase();
  const leader = Array.isArray(tx.consensus_data?.leader_receipt) ? tx.consensus_data.leader_receipt[0] : tx.consensus_data?.leader_receipt;
  const execution = String(tx.execution_result || tx.executionResult || leader?.execution_result || '').toUpperCase();
  if (['CANCELED','CANCELLED','UNDETERMINED'].includes(status)) return 'failed';
  if (execution && !['SUCCESS','0'].includes(execution)) return 'failed';
  if (status === 'FINALIZED' && ['SUCCESS','0'].includes(execution)) return 'finalized';
  if (status === 'ACCEPTED') return 'accepted';
  return 'pending';
}
export async function trackTransaction(client, hash, update, {attempts=120, delay=2500, sleep=ms=>new Promise(r=>setTimeout(r,ms))}={}) {
  for (let i=0; i<attempts; i++) {
    const receipt = await client.getTransaction({hash});
    const stage = classifyReceipt(receipt);
    update(stage,receipt);
    if (stage==='failed') throw new Error(`Transaction failed: ${receipt.execution_result || receipt.status}`);
    if (stage==='finalized') return receipt;
    await sleep(delay);
  }
  throw new Error('Still pending. Resume tracking the saved hash; do not submit again.');
}
export async function sha256(text) {
  return [...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text)))].map(x=>x.toString(16).padStart(2,'0')).join('');
}
