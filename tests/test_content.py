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
if __name__=='__main__':unittest.main()
