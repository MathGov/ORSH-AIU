#!/usr/bin/env python3
"""Build the v1.8 reading guide and merged reading copy; embed cover fonts with XeLaTeX."""
from pathlib import Path
import argparse, json, subprocess
import fitz

PARTS = [
 ('Frame-Aligned Records', 'v0.5', 'manuscripts/Frame_Aligned_Records_v0_5.pdf', 'Methods, proofs and inference safeguards'),
 ('Supplementary Information', 'v1.2', 'supplement/Frame_Aligned_Records_Supplement_v1_2.pdf', 'Calculations, run catalogue and reproducibility'),
 ('Post-injection Results', 'v1.2', 'pilot/Post_Injection_Results_v1_2.pdf', 'Original pilot and separate review-stage extensions'),
 ('P01 Protocol', 'v1.3', 'protocols/P01_Post_Injection_Protocol_v1_3.pdf', 'Reader edition of the frozen executed specification'),
 ('Absolute Infinite Union', 'v1.4', 'manuscripts/Absolute_Infinite_Union_v1_4.pdf', 'Philosophical hypothesis and evidence-bridge assessment')]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();r=a.root.resolve()
 work=r/'typesetting/collection_cover';work.mkdir(parents=True,exist_ok=True)
 start=2;items=[]
 for title,version,path,description in PARTS:
  with fitz.open(r/path) as doc: n=doc.page_count
  items.append(dict(title=title,version=version,path=path,description=description,start=start,end=start+n-1,pages=n));start+=n
 rows='\n'.join(f"\\textbf{{{x['title']}}} & {x['version']} & {x['start']}-{x['end']} \\\\ \n\\multicolumn{{3}}{{@{{}}p{{166mm}}@{{}}}}{{\\small {x['description']}}} \\\\[3mm]" for x in items)
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{fontspec}
\setmainfont{Noto Sans}
\usepackage{array,booktabs,hyperref}
\hypersetup{pdftitle={ORSH / AIU v1.8: Collected Reading Copy},pdfauthor={James McGaughran},pdfsubject={Finalized specialist-review reading copy}}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{10pt}
\begin{document}
{\small RESEARCH PORTFOLIO / SPECIALIST-REVIEW EDITION}\par
\vspace{5mm}
{\Huge\bfseries ORSH / AIU}\par
{\Large Collected Reading Copy\quad v1.8}\par
\vspace{2mm}
\textbf{Open Relational Substrate Hypothesis}\newline
\textbf{Absolute Infinite Union}

James McGaughran\newline
MathGov / RippleLogic Research Program\newline
26 September 2026

\vspace{3mm}
\textbf{Contents and suggested reading order}

\begin{tabular}{@{}p{101mm}p{21mm}r@{}}
\toprule
Document & Version & Pages \\
\midrule
''' + rows + r'''
\bottomrule
\end{tabular}

\vspace{3mm}
The methods paper and philosophical inquiry are separate manuscripts. The
supplement, results log and protocol support review; they are not additional
independent discoveries.

\textbf{Release boundary.} Complete for specialist criticism, not a certification
of scientific novelty, journal acceptance, recovered spacetime or a conscious
substrate. Author declarations and any public deposit remain separate actions.

\textbf{Same versions, traceable finalization.} The manifest and finalization
record identify these corrected files. Original experiment inputs and their
pre-execution records remain unchanged. Earlier release files are preserved as
historical material, not competing current editions.
\end{document}
'''
 p=work/'collection_cover.tex';p.write_text(tex,encoding='utf-8')
 for i in (1,2):
  q=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',p.name],cwd=work,capture_output=True,text=True)
  (r/'verification'/f'collection_cover_compile_{i}.txt').write_text(q.stdout+q.stderr)
  if q.returncode:raise RuntimeError((q.stdout+q.stderr)[-2500:])
 out=fitz.open();toc=[]
 with fitz.open(p.with_suffix('.pdf')) as d:
  if d.page_count!=1:raise RuntimeError('Cover must remain one page')
  out.insert_pdf(d)
 toc.append([1,'Contents and release scope',1])
 for x in items:
  offset=out.page_count
  with fitz.open(r/x['path']) as d:
   subtoc=d.get_toc();out.insert_pdf(d)
  toc.append([1,x['title']+' '+x['version'],offset+1])
  for level,title,page in subtoc:
   if page>0:toc.append([level+1,title,offset+page])
 out.set_toc(toc);out.set_metadata({'title':'ORSH / AIU v1.8: Collected Reading Copy','author':'James McGaughran','subject':'Finalized specialist-review release; manuscript versions retained','creator':'Canonical Markdown / XeLaTeX / PyMuPDF'})
 out.save(r/'ORSH_AIU_v1_8_Collected_Reading_Copy.pdf',garbage=4,deflate=True)
 report={'cover_pages':1,'components':items,'total_pages':out.page_count,'bookmarks':len(toc),'pdfa_status':'Not certified; cover fonts embedded, but font embedding alone is not PDF/A conformance.'}
 (r/'verification/collection_build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
