"""Synthetic content workflow with evidence and human review gates."""
import json
from pathlib import Path

KINDS={'brand','product','personal-ip','store'}
CHANNELS={'web','x','email'}
def build(source:dict,persona:dict,intent:str,channel:str)->dict:
    if source.get('kind') not in KINDS or channel not in CHANNELS or not intent.strip():raise ValueError('INVALID_INPUT')
    if not source.get('claims') or not persona.get('audience'):raise ValueError('MISSING_EVIDENCE')
    claims=[c for c in source['claims'] if c.get('source_id') and c.get('text')]
    if len(claims)!=len(source['claims']):raise ValueError('UNSOURCED_CLAIM')
    body=f"For {persona['audience']}: {source['name']} — "+' '.join(c['text'] for c in claims)
    if channel=='x':body=body[:280]
    checks={'supported':all(c['source_id'] in source.get('sources',{}) for c in claims),'length_ok':len(body)<=280 if channel=='x' else len(body)<=2000,'human_review':False}
    return {'kind':source['kind'],'persona':persona['audience'],'intent':intent,'channel':channel,'draft':body,'citations':[c['source_id'] for c in claims],'checks':checks,'state':'HUMAN_REVIEW' if all([checks['supported'],checks['length_ok']]) else 'QA_FAILED','synthetic_unverified':True}
def approve(item:dict,reviewer:str)->dict:
    if item['state']!='HUMAN_REVIEW' or not reviewer.strip():raise ValueError('HUMAN_GATE_REQUIRED')
    item['checks']['human_review']=True;item['state']='APPROVED';item['reviewer']=reviewer;return item
def main():
    sample=json.loads(Path('examples/source.json').read_text());out=build(sample,{'audience':'fictional operations team'},'explain sample feature','web')
    Path('output').mkdir(exist_ok=True);Path('output/draft.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
