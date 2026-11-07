from pathlib import Path
import hashlib, importlib.util, itertools, json
from decimal import Decimal, localcontext
root=Path.cwd()
base=root/'experiments/E-261103-04-s5-genus-ladder-9-faces/results'
checker=base/'recovery-review/independent.py'
spec=importlib.util.spec_from_file_location('auxiliary_independent', checker)
check=importlib.util.module_from_spec(spec); spec.loader.exec_module(check)
candidate=base/'intermediate-om-realization-review/roest_vigh-g1.candidate.json'
data=json.loads(candidate.read_text())
saved_input=base/'intermediate-om-realization/roest_vigh-g1-hinge-warm.input.json'
expected=json.loads(saved_input.read_text())
chi={tuple(map(int,k.split(','))):v for k,v in expected['chi'].items()}
assert data['links']=={str(i):v for i,v in enumerate(expected['links'])}
assert len(data['planes'])==8 and all(type(v) is int for row in data['planes'] for v in row)
def signs(planes):
 h=planes+[[0,0,0,1]]
 return {q:(lambda d:(d>0)-(d<0))(check.det([h[i] for i in q])) for q in itertools.combinations(range(9),4)}
reports={}
for name,planes in [('original',data['planes'])]+[(str(scale),[[int((Decimal(v)/sum(Decimal(x)**2 for x in row[:3]).sqrt()*Decimal(scale)).to_integral_value()) for v in row] for row in data['planes']]) for scale in ()]:
 assert signs(planes)==chi
 reports[name]=check.check({'planes':planes,'links':data['links']},[16,24,8,0])
with localcontext() as ctx:
 ctx.prec=80
 for scale in (10**9,10**12):
  planes=[]
  for row in data['planes']:
   length=sum(Decimal(v)**2 for v in row[:3]).sqrt()
   planes.append([int((Decimal(v)*Decimal(scale)/length).to_integral_value()) for v in row])
  assert signs(planes)==chi
  reports[str(scale)]=check.check({'planes':planes,'links':data['links']},[16,24,8,0])
print(json.dumps({'verdict':'ACCEPT','evidence':'PROVED-1; standalone exact rational checks, no human review or verify_all reproduction','candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(checker.read_bytes()).hexdigest(),'input_sha256':hashlib.sha256(saved_input.read_bytes()).hexdigest(),'signs_compared':len(chi),'sign_mismatches':0,'rounding':'Original integer candidate, plus normal-normalized integer rescaling at 1e9 and 1e12; Decimal precision80, round-half-even. Not a second rounding of raw optimizer output.','reports':reports,'ladder_exact_imported':False},indent=2,default=str))
