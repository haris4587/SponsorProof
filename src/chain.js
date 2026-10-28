import {sha256 as hashBytes} from 'viem';
import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
export const RPC = 'https://studio.genlayer.com/api';
export const EXPLORER = 'https://explorer-studio.genlayer.com';
export const addressOK = value => /^0x[0-9a-fA-F]{40}$/.test(value || '');
export const hashOK = value => /^[0-9a-f]{64}$/.test(value || '');
export const txURL = hash => `${EXPLORER}/tx/${hash}`;
export function makeClient() {
  // Read/receipt client only. Studio signs on its own origin.
  return createClient({ chain: studionet });
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
    if (stage==='failed') {
      const leader = Array.isArray(receipt.consensus_data?.leader_receipt) ? receipt.consensus_data.leader_receipt[0] : receipt.consensus_data?.leader_receipt;
      throw new Error(`Transaction failed: ${receipt.txExecutionResultName || receipt.execution_result || leader?.execution_result || receipt.statusName || receipt.status}`);
    }
    if (stage==='finalized') return receipt;
    await sleep(delay);
  }
  throw new Error('Still pending. Resume tracking the saved hash; do not submit again.');
}
export function sha256Bytes(bytes) { return hashBytes(new Uint8Array(bytes)).slice(2); }
export async function sha256(text) { return sha256Bytes(new TextEncoder().encode(text)); }

export function validateLinkedTransaction(tx, plan, decode) {
  const recipient = tx.to_address || tx.recipient || tx.to;
  const sender = tx.from_address || tx.sender;
  if (String(recipient).toLowerCase() !== plan.contract.toLowerCase()) throw Error('Transaction targets a different contract');
  if (String(sender).toLowerCase() !== plan.account.toLowerCase()) throw Error('Transaction was signed by a different account');
  const call = decode(Uint8Array.from(tx.data?.calldata?.raw || []));
  if (call.get('method') !== plan.method || JSON.stringify(call.get('args')) !== JSON.stringify(plan.args)) throw Error('Transaction arguments do not match the prepared action');
  if (tx.leader_only === true || (tx.execution_mode && tx.execution_mode !== 'normal' && tx.execution_mode !== 'NORMAL')) throw Error('Use Normal Full Consensus in Studio');
  return true;
}
