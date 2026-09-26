#!/usr/bin/env python3
"""Portable content/package checks. Does not replace visual or scientific review."""
from pathlib import Path
import argparse,hashlib,json,zipfile,subprocess
from lxml import etree
from build_documents import signature,NS

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mc(x):
 if isinstance(x,dict):return int(x.get('t')=='Math')+sum(mc(v) for v in x.values())
 if isinstance(x,list):return sum(mc(v) for v in x)
 return 0

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--report',type=Path);a=ap.parse_args();r=a.root.resolve();checks=[]
 def add(name,val):checks.append({'check':name,'passed':bool(val)})
 for bpath in sorted((r/'verification/build').glob('*_build.json')):
  b=json.loads(bpath.read_text());md=r/b['markdown'];dx=md.with_suffix('.docx')
  add(md.name+':source',sha(md)==b['markdown_sha256']);add(md.name+':ordered_content',signature(dx)==b['blocks'])
  ast=json.loads(subprocess.check_output(['pandoc',str(md),'-f','markdown-implicit_figures','-t','json']))
  with zipfile.ZipFile(dx) as z:
   add(dx.name+':zip_integrity',z.testzip() is None);e=etree.fromstring(z.read('word/document.xml'))
   add(dx.name+':native_math_count',len(e.xpath('//m:oMath',namespaces=NS))==mc(ast)==b['math_objects'])
   add(dx.name+':table_borders',all(t.xpath('./w:tblPr/w:tblBorders',namespaces=NS) for t in e.xpath('//w:tbl',namespaces=NS)))
 for path,h in json.loads((r/'pilot/PRE_EXECUTION_RECEIPT.json').read_text())['files'].items():add(path+':pre_execution_hash',sha(r/path)==h)
 manifest=r/'MANIFEST_SHA256.json'
 if manifest.exists():
  entries=json.loads(manifest.read_text())['files']
  if isinstance(entries,dict):entries=[{'path':p,'sha256':h} for p,h in entries.items()]
  for entry in entries:
   p=r/entry['path'];add(entry['path']+':manifest',p.is_file() and sha(p)==entry['sha256'])
 out={'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'limitations':'Structural and hash checks only. Not a semantic proof, Word application test, visual review or scientific validation.'}
 if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(out,indent=2))
 print(json.dumps({k:out[k] for k in ['passed','failed','limitations']},indent=2))
 if out['failed']:raise SystemExit(1)
if __name__=='__main__':main()
