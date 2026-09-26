import unittest
from content_workflow import build,approve
S={'kind':'product','name':'Sample','sources':{'s':'Synthetic document'},'claims':[{'text':'A sample fact.','source_id':'s'}]}
class TestWorkflow(unittest.TestCase):
    def test_supported(self):self.assertEqual(build(S,{'audience':'people'},'inform','web')['state'],'HUMAN_REVIEW')
    def test_unsourced(self):self.assertEqual(build({**S,'sources':{}},{'audience':'people'},'inform','web')['state'],'QA_FAILED')
    def test_missing_id(self):self.assertRaises(ValueError,build,{**S,'claims':[{'text':'x'}]},{'audience':'people'},'inform','web')
    def test_unknown_kind(self):self.assertRaises(ValueError,build,{**S,'kind':'unknown'},{'audience':'people'},'inform','web')
    def test_unknown_channel(self):self.assertRaises(ValueError,build,S,{'audience':'people'},'inform','unknown')
    def test_human_gate(self):self.assertRaises(ValueError,approve,build(S,{'audience':'people'},'inform','web'),'')
    def test_approval(self):self.assertEqual(approve(build(S,{'audience':'people'},'inform','web'),'Human')['state'],'APPROVED')
    def test_long_x_draft_fails_without_silent_truncation(self):
        source={**S,'claims':[{'text':'a'*280+' FINAL_CLAIM_END','source_id':'s'}]}
        draft=build(source,{'audience':'people'},'inform','x')
        self.assertEqual(draft['state'],'QA_FAILED')
        self.assertFalse(draft['checks']['length_ok'])
        self.assertIn('FINAL_CLAIM_END',draft['draft'])
        self.assertRaises(ValueError,approve,draft,'Human')
if __name__=='__main__':unittest.main()
