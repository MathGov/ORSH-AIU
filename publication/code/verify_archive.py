#!/usr/bin/env python3
"""Verify every entry and detect unlisted files in a clean extracted release."""
import argparse,hashlib,json
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();root=a.root.resolve()
 manifest=json.loads((root/'MANIFEST_SHA256.json').read_text());bad=[]
 for name,digest in manifest['files'].items():
  file=root/name
  if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=digest:bad.append(name)
 actual={str(x.relative_to(root)) for x in root.rglob('*') if x.is_file() and '__pycache__' not in x.parts}
 allowed=set(manifest['files'])|{'MANIFEST_SHA256.json','SHA256SUMS.txt'}
 extra=sorted(actual-allowed);missing=sorted(allowed-actual)
 print(json.dumps({'entries':len(manifest['files']),'mismatches':bad,'unlisted':extra,'missing':missing},indent=2))
 if bad or extra or missing:raise SystemExit(1)
if __name__=='__main__':main()
