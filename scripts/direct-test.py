from pathlib import Path
from gltest.direct import VMContext, deploy_contract, create_address
import json,hashlib
vm=VMContext()
url='https://raw.githubusercontent.com/haris4587/SponsorProof/'+'a'*40+'/fixtures/fulfilled.txt'
text=Path('fixtures/fulfilled.txt').read_bytes()
with vm.activate():
    contract=deploy_contract(Path('contracts/sponsorproof.py'),vm)
    vm.sender=create_address('0x'+'1'*40)
    creator=str(vm.sender)
    print('sender',creator)
    contract.create_campaign('direct-demo','Direct runtime test',creator,json.dumps({'messages':['Keeps drinks cold for 24 hours'], 'link':'https://example.com/aster','disclosure':'#ad'}))
    contract.submit_delivery('direct-demo',url,hashlib.sha256(text).hexdigest(),'https://example.com/post')
    vm.mock_web(url,{'status':200,'headers':{},'body':text})
    vm.mock_llm('.*',json.dumps({'checks':[{'status':'MET','quote':'keeps drinks cold for 24 hours','reason':'Explicit statement'}]}))
    contract.review_delivery('direct-demo')
    c=json.loads(contract.get_campaign('direct-demo'))
    print(c['reviews'])
    assert c['reviews'][-1]['verdict']=='FULFILLED'
    contract.finalize_delivery('direct-demo',c['reviews'][-1]['decision_hash'])
    assert json.loads(contract.get_campaign('direct-demo'))['state']=='FINALIZED'
print('DIRECT SDK RUNTIME PASS')
