"""Offline contract logic tests. Mock web/AI/consensus; not a GenVM substitute."""
import unittest, types, sys, json, importlib.util, hashlib
from pathlib import Path
from types import SimpleNamespace as NS

B = '0x' + '1'*40
C = '0x' + '2'*40
O = '0x' + '3'*40
URL = 'https://raw.githubusercontent.com/haris4587/SponsorProof/' + 'a'*40 + '/fixtures/fulfilled.txt'
TEXT = '#ad\nAster keeps drinks cold for 24 hours. Reusable steel, leak-proof design.\nhttps://example.com/aster\n'
REQ = {'messages':['Keeps drinks cold for 24 hours','Made from reusable steel','Leak-proof design'], 'link':'https://example.com/aster','disclosure':'#ad'}
class Generic:
    def __class_getitem__(cls, args): return cls
mod=types.ModuleType('genlayer')
gl=NS(vm=NS(UserError=Exception), Contract=object, public=NS(write=lambda f:f,view=lambda f:f), message=NS(sender_address=B))
mod.gl=gl; mod.TreeMap=Generic; mod.DynArray=Generic
sys.modules['genlayer']=mod
spec=importlib.util.spec_from_file_location('contract',Path(__file__).parents[1]/'contracts/sponsorproof.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class ContractTests(unittest.TestCase):
    def setUp(self):
        gl.message.sender_address=B
        self.c=m.SponsorProof(); self.c.campaigns={}; self.c.campaign_ids=[]
        self.body=TEXT.encode(); self.status=200; self.semantic=['MET']*3
        gl.nondet=NS(web=NS(get=lambda url:NS(body=self.body,status_code=self.status)),exec_prompt=self.prompt)
        gl.eq_principle=NS(strict_eq=lambda f:f(),prompt_comparative=lambda f,**kw:f())
        self.c.create_campaign('test-001','Aster launch',C,json.dumps(REQ))
    def prompt(self,prompt):
        return json.dumps({'checks':[{'status':s,'quote':'Aster' if s=='MET' else '', 'reason':'Supported' if s=='MET' else 'Not supported'} for s in self.semantic]})
    def submit(self, sha=None):
        gl.message.sender_address=C
        self.c.submit_delivery('test-001',URL,sha or hashlib.sha256(self.body).hexdigest(),'https://example.com/post')
    def review(self):
        self.submit(); self.c.review_delivery('test-001'); return self.get()
    def get(self): return json.loads(self.c.get_campaign('test-001'))
    def test_fulfilled(self): self.assertEqual(self.review()['reviews'][-1]['verdict'],'FULFILLED')
    def test_partial(self):
        self.semantic=['MET','MISSING','MISSING']; self.assertEqual(self.review()['reviews'][-1]['verdict'],'PARTIAL')
    def test_uncertain(self):
        self.semantic=['UNCERTAIN']*3; self.assertEqual(self.review()['reviews'][-1]['verdict'],'INCONCLUSIVE')
    def test_none(self):
        self.body=b'Nothing promised here'; self.semantic=['MISSING']*3; self.assertEqual(self.review()['reviews'][-1]['verdict'],'NOT_FULFILLED')
    def test_wrong_hash(self):
        self.submit('0'*64); self.c.review_delivery('test-001'); self.assertEqual(self.get()['reviews'][0]['error'],'Evidence hash mismatch')
    def test_http_error(self):
        self.status=404; self.assertEqual(self.review()['reviews'][0]['verdict'],'INCONCLUSIVE')
    def test_oversized(self):
        self.body=b'x'*16001; self.assertEqual(self.review()['reviews'][0]['verdict'],'INCONCLUSIVE')
    def test_invalid_utf8(self):
        self.body=b'\xff'; self.assertEqual(self.review()['reviews'][0]['verdict'],'INCONCLUSIVE')
    def test_empty(self):
        self.body=b' '; self.assertEqual(self.review()['reviews'][0]['verdict'],'INCONCLUSIVE')
    def test_link_suffix(self):
        self.body=TEXT.replace('https://example.com/aster','https://example.com/aster.evil').encode(); self.assertEqual(self.review()['reviews'][0]['checks'][0]['status'],'MISSING')
    def test_disclosure_boundary(self):
        self.body=TEXT.replace('#ad','#advertisement').encode(); self.assertEqual(self.review()['reviews'][0]['checks'][1]['status'],'MISSING')
    def test_duplicate(self):
        with self.assertRaises(Exception): self.c.create_campaign('test-001','Again',C,json.dumps(REQ))
    def test_submit_permissions(self):
        with self.assertRaises(Exception): self.c.submit_delivery('test-001',URL,'0'*64,'https://example.com')
    def test_review_permissions(self):
        self.submit(); gl.message.sender_address=O
        with self.assertRaises(Exception): self.c.review_delivery('test-001')
    def test_ordering(self):
        with self.assertRaises(Exception): self.c.review_delivery('test-001')
    def test_locked_delivery(self):
        self.submit()
        with self.assertRaises(Exception): self.submit()
    def test_two_party_finalize(self):
        self.review(); h=self.get()['reviews'][0]['decision_hash']
        self.c.finalize_delivery('test-001',h); self.assertEqual(self.get()['state'],'REVIEWED')
        gl.message.sender_address=B; self.c.finalize_delivery('test-001',h); self.assertEqual(self.get()['state'],'FINALIZED')
        with self.assertRaises(Exception): self.c.challenge_review('test-001','A new challenge',URL,'0'*64,'https://example.com')
    def test_stale_hash(self):
        self.review()
        with self.assertRaises(Exception): self.c.finalize_delivery('test-001','0'*64)
    def test_duplicate_approval(self):
        self.review(); h=self.get()['reviews'][0]['decision_hash']; self.c.finalize_delivery('test-001',h)
        with self.assertRaises(Exception): self.c.finalize_delivery('test-001',h)
    def test_challenge_preserves_history(self):
        self.review(); old=self.get()['reviews'][0]
        self.c.finalize_delivery('test-001',old['decision_hash'])
        self.c.challenge_review('test-001','Please assess corrected public text',URL,hashlib.sha256(self.body).hexdigest(),'https://example.com/post')
        self.assertEqual(self.get()['approvals'],[])
        self.c.review_delivery('test-001'); c=self.get(); self.assertEqual(c['reviews'][0],old); self.assertEqual(len(c['reviews']),2)
        with self.assertRaises(Exception): self.c.challenge_review('test-001','Third attempt not allowed',URL,'0'*64,'https://example.com')
    def test_citation_rejects_hallucination(self):
        with self.assertRaises(Exception): m.validate_assessment(json.dumps({'checks':[{'status':'MET','quote':'invented','reason':'x'}]}),['message'],TEXT)
    def test_met_needs_quote(self):
        with self.assertRaises(Exception): m.validate_assessment(json.dumps({'checks':[{'status':'MET','quote':'','reason':'x'}]}),['message'],TEXT)
    def test_invalid_model_output(self):
        for raw in ['{}','not json','{"checks":[{"status":"FULFILLED"}]}']:
            with self.assertRaises(Exception): m.validate_assessment(raw,['message'],TEXT)
    def test_snapshot_restrictions(self):
        for url in ['http://localhost/x.txt',URL.replace('a'*40,'main'),URL+'?x=1',URL.replace('fixtures','../fixtures'),URL.replace('raw.githubusercontent.com','evil.com')]:
            with self.assertRaises(Exception): m.snapshot_url(url)
    def test_pagination(self):
        self.assertEqual(self.c.list_campaigns(0,10),['test-001'])
        with self.assertRaises(Exception): self.c.list_campaigns(-1,2)
    def test_hash_reproducible(self):
        self.review(); r=self.get()['reviews'][0]; h=r.pop('decision_hash'); self.assertEqual(m.digest(m.encode(r)),h)
if __name__=='__main__': unittest.main()
