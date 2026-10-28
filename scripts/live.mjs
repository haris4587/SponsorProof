import fs from 'node:fs';
import {makeClient,trackTransaction,classifyReceipt} from '../src/chain.js';
import config from '../src/deployment.json' with {type:'json'};
const brand='0xcD1305217298eB7a99696EEAB7f5a46b9dE2E441';
const client=makeClient(brand);
if(process.argv[2]==='inspect'){
 const tx=await client.getTransaction({hash:config.deploymentTransaction});
 const source=Buffer.from(tx.data.contract_code,'base64');
 console.log({status:tx.statusName,execution:tx.consensus_data?.leader_receipt?.[0]?.execution_result,sourceMatches:source.equals(fs.readFileSync('contracts/sponsorproof.py')),leaderOnly:tx.leader_only});
}else if(process.argv[2]==='read'){
 console.log(await client.readContract({address:config.contract,functionName:'get_campaign',args:[process.argv[3]]}));
}else if(process.argv[2]==='tx'){
 const tx=await client.getTransaction({hash:process.argv[3]});console.log(JSON.stringify({status:tx.statusName,stage:classifyReceipt(tx),execution:tx.consensus_data?.leader_receipt?.[0]?.execution_result,receipt:tx.consensus_data?.leader_receipt?.[0]?.result,consensus:tx.last_round},null,2));
}
