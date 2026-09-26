"""Typeset canonical equation-bearing Markdown directly through XeLaTeX.
Does not use the DOCX/LibreOffice export whose delimiters failed in an older edition.
"""
from pathlib import Path
import argparse,subprocess,json,hashlib,shutil

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('markdown',type=Path,nargs='+');a=p.parse_args();r=a.root.resolve()
 for md in a.markdown:
  md=md.resolve();stem=md.stem;work=r/'typesetting'/stem;work.mkdir(parents=True,exist_ok=True)
  tex=work/(stem+'.tex');header=r/'typesetting/header.tex'
  cmd=['pandoc',str(md),'-f','markdown+autolink_bare_uris-implicit_figures','-t','latex','-s','--resource-path',str(md.parent),'-V','documentclass:article','-V','papersize:a4','-V','geometry:margin=21mm','-V','fontsize:10pt','-V','colorlinks:false','-V','urlcolor:black','-H',str(header),'--lua-filter',str(r/'typesetting/codewrap.lua'),'-o',str(tex)]
  res=subprocess.run(cmd,cwd=md.parent,capture_output=True,text=True);(work/'pandoc.log').write_text(res.stdout+res.stderr);res.check_returncode()
  # All figure references resolve from the canonical source's own directory.
  src=tex.read_text();src=src.replace('../figures/','../../figures/');tex.write_text(src)
  for k in range(2):
   q=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(work),str(tex)],cwd=work,capture_output=True,text=True)
   (work/f'compile_{k+1}.txt').write_text(q.stdout+q.stderr)
   if q.returncode:print((q.stdout+q.stderr)[-3500:]);q.check_returncode()
  pdf=work/(stem+'.pdf');shutil.copy2(pdf,md.with_suffix('.pdf'))
  warnings=[x for x in (work/(stem+'.log')).read_text(errors='replace').splitlines() if any(y in x for y in ('Overfull','Missing character','Warning:'))]
  out={'source':str(md.relative_to(r)),'source_sha256':hashlib.sha256(md.read_bytes()).hexdigest(),'engine':'XeLaTeX from canonical Markdown','warnings':warnings}
  (r/'verification'/f'{stem}_pdf_build.json').write_text(json.dumps(out,indent=2));print(stem,'PDF built',len(warnings),'warnings',flush=True)
if __name__=='__main__':main()
