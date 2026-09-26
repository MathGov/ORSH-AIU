"""Audit the curated files; optionally audit all files in the original ZIP."""
from pathlib import Path
import argparse,json,hashlib,zipfile
R=Path(__file__).resolve().parents[1]
EXPECTED='bc739d957ccd57a40d1c30c438ec2c4ab998d17c3b2e79f3dd6651b209b26d94'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=Path);a=p.parse_args()
 inv=json.loads((R/'provenance/source-inventory.json').read_text(encoding='utf-8'))
 assert inv['archive_sha256']==EXPECTED
 actual={p.relative_to(R/'publication').as_posix() for p in (R/'publication').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 assert actual==set(inv['included']),('Unexpected/missing curated files',actual^set(inv['included']))
 for name,digest in inv['included'].items():assert sha((R/'publication'/name).read_bytes())==digest,name
 manifest=json.loads((R/'publication/MANIFEST_SHA256.json').read_text(encoding='utf-8'))['files']
 for name,digest in manifest.items():assert {**inv['included'],**inv['archive_only']}[name]==digest,name
 report={'curated_files':len(actual),'original_manifest_entries':len(manifest),'curated_hashes_match':True}
 if a.archive:
  assert sha(a.archive.read_bytes())==EXPECTED,'Original ZIP hash differs'
  with zipfile.ZipFile(a.archive) as z:
   assert z.testzip() is None
   members={n.removeprefix('ORSH_AIU_v1_8/') for n in z.namelist() if not n.endswith('/')}
   assert members==set(inv['included'])|set(inv['archive_only'])
   for n,h in {**inv['included'],**inv['archive_only']}.items():assert sha(z.read('ORSH_AIU_v1_8/'+n))==h,n
  report.update(original_archive_verified=True,original_files=len(members))
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
