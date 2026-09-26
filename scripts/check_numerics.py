"""Fresh bounded checks without writing into frozen publication artifacts."""
from pathlib import Path
import subprocess,tempfile,json,sys,os
R=Path(__file__).resolve().parents[1];P=R/'publication'
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONUTF8='1')
sys.path.insert(0,str(P/'code'))
from replay_reviewer import compare
with tempfile.TemporaryDirectory(prefix='orsh-check-') as temp:
 out=Path(temp)
 for script,args in [('validate_factorial.py',['--out',str(out/'checks.json')]),('analyze_factorial.py',['--out',str(out/'analysis')])]:
  res=subprocess.run([sys.executable,str(P/'code'/script),'--root',str(P),*args],capture_output=True,text=True,encoding='utf-8',env=os.environ)
  if res.returncode:print(res.stdout,res.stderr);res.check_returncode()
 original=json.loads((P/'data/factorial_analysis/analysis.json').read_text(encoding='utf-8'))
 fresh=json.loads((out/'analysis/analysis.json').read_text(encoding='utf-8'))
 errors=compare(original,fresh);assert not errors,errors
 checks=json.loads((out/'checks.json').read_text(encoding='utf-8'));assert checks['failed']==0
 print(json.dumps({'selected_method_checks':checks['passed'],'factorial_analysis_matches':True,'comparison_rtol':1e-8,'comparison_atol':1e-10,'scope':checks['scope']},indent=2))
