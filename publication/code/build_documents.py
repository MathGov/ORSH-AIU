#!/usr/bin/env python3
"""One Markdown source per manuscript; pandoc for math, python-docx for layout.
The output content signature is compared against the pre-style conversion.
PDF typesetting is separate and uses the same canonical Markdown through XeLaTeX.
"""
from pathlib import Path
import argparse,subprocess,json,hashlib,re,tempfile,zipfile
from lxml import etree
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
def signature(path):
 with zipfile.ZipFile(path) as z:
  el=etree.fromstring(z.read('word/document.xml'));out=[]
  for node in el.find('w:body',NS):
   if node.tag==qn('w:sectPr'):continue
   text=''.join(node.xpath('.//w:t/text()|.//m:t/text()',namespaces=NS));maths=[]
   for m in node.xpath('.//m:oMath',namespaces=NS):
    maths.append(etree.tostring(m,method='c14n').decode())
   # strip style attributes from equation signature, retain exact math text and operator structure
   out.append({'tag':etree.QName(node).localname,'text':text,'math_texts':[''.join(m.xpath('.//m:t/text()',namespaces=NS)) for m in node.xpath('.//m:oMath',namespaces=NS)],'math_count':len(maths),'tables':len(node.xpath('.//w:tr',namespaces=NS)),'drawings':len(node.xpath('.//wp:docPr',namespaces=NS))})
  return out

def style_named(doc,name,kind=WD_STYLE_TYPE.PARAGRAPH):
 for st in doc.styles:
  if st.name.casefold()==name.casefold():return st
 return doc.styles.add_style(name,kind)

def build(md):
 root=md.parent.parent;quality=root/'verification'/'build';quality.mkdir(parents=True,exist_ok=True);raw=quality/(md.stem+'_prestyle.docx');out=md.with_suffix('.docx')
 src=md.read_text();assert '\u2013' not in src and '\u2014' not in src
 assert all(ord(c)>=32 or c in '\n\r\t' for c in src), 'Control character in source'
 assert r'\vert ' not in src, 'Use renderer-tested literal ket bars; inspect table escaping separately'
 subprocess.run(['pandoc',str(md),'-f','markdown+autolink_bare_uris-implicit_figures','-t','docx','--resource-path',str(md.parent),'-o',str(raw)],check=True)
 doc=Document(raw)
 # Replace automatically growing OMML delimiters with explicit native math runs.
 # Some LibreOffice exports substitute right parentheses for brackets/ket angles.
 # The intended begin/end characters are read from the OOXML, never guessed from extraction.
 delimiter_log=[]
 for dnode in reversed(list(doc._element.iter(qn('m:d')))):
  pr=dnode.find(qn('m:dPr'))
  def char(name,default):
   x=pr.find(qn('m:'+name)) if pr is not None else None
   return x.get(qn('m:val'),default) if x is not None else default
  beg,end,sep=char('begChr','('),char('endChr',')'),char('sepChr','|')
  parent=dnode.getparent();idx=parent.index(dnode);new=[]
  def mr(t):
   rr=OxmlElement('m:r');rp=OxmlElement('m:rPr');st=OxmlElement('m:sty');st.set(qn('m:val'),'p');rp.append(st);rr.append(rp);tt=OxmlElement('m:t');tt.text='∣' if t=='|' else t;rr.append(tt);return rr
  if beg:new.append(mr(beg))
  es=dnode.findall(qn('m:e'))
  for ei,ee in enumerate(es):
   if ei and sep:new.append(mr(sep))
   for child in list(ee):new.append(child)
  if end:new.append(mr(end))
  for j,child in enumerate(new):parent.insert(idx+j,child)
  parent.remove(dnode);delimiter_log.append({'begin':beg,'end':end,'arguments':len(es)})
 # Coalesce plain upright letter runs emitted one letter at a time by pandoc.
 # LibreOffice otherwise treats a roman operator name as separately italic variables.
 operators={'Tr','tr','Pr','min','max','inf','sup','span','Stab','sgn','Var','exp','log','ln','sin','cos','diag','dim','Ad','Re','Im','rank'}
 for par in doc._element.iter():
  children=list(par);i=0
  while i<len(children):
   r=children[i];t=r.find(qn('m:t'));rp=r.find(qn('m:rPr'));st=rp.find(qn('m:sty')) if rp is not None else None
   if r.tag!=qn('m:r') or t is None or not (t.text or '').isalpha() or st is None or st.get(qn('m:val'))!='p' or rp.find(qn('m:scr')) is not None:
    i+=1;continue
   rs=[r];text=t.text;j=i+1
   while j<len(children):
    c=children[j];ct=c.find(qn('m:t'));cp=c.find(qn('m:rPr'));cs=cp.find(qn('m:sty')) if cp is not None else None
    if c.tag!=qn('m:r') or ct is None or not (ct.text or '').isalpha() or cs is None or cs.get(qn('m:val'))!='p' or cp.find(qn('m:scr')) is not None:break
    text+=ct.text;rs.append(c);j+=1
   if text in operators:
    t.text=text
    for c in rs[1:]:par.remove(c)
   i=j
 # U+2223 is the mathematical vertical stroke; the ASCII bar is parsed as logical OR by LO.
 for tt in doc._element.iter(qn('m:t')):
  if tt.text=='|':tt.text='∣'
 operator_runs=0
 for rr in doc._element.iter(qn('m:r')):
  tt=rr.find(qn('m:t'))
  if tt is not None and tt.text in {'Tr','tr','Pr','min','max','inf','sup','span','Stab','sgn','Var','exp','log','ln','sin','cos','diag','dim','Ad','Re','Im','rank'}:
   rp=rr.find(qn('m:rPr'))
   if rp is None:rp=OxmlElement('m:rPr');rr.insert(0,rp)
   if rp.find(qn('m:nor')) is None:
    nr=OxmlElement('m:nor');nr.set(qn('m:val'),'1');rp.append(nr)
   wp=rr.find(qn('w:rPr'))
   if wp is None:wp=OxmlElement('w:rPr');rr.insert(1,wp)
   it=OxmlElement('w:i');it.set(qn('w:val'),'0');wp.append(it);operator_runs+=1
 doc.save(raw)
 sig=signature(raw);doc=Document(raw);sec=doc.sections[0];sec.page_width=Inches(8.2677);sec.page_height=Inches(11.6929);sec.left_margin=sec.right_margin=Inches(.72);sec.top_margin=Inches(.64);sec.bottom_margin=Inches(.63);sec.header_distance=Inches(.23);sec.footer_distance=Inches(.24)
 for st in doc.styles:
  if st.type==WD_STYLE_TYPE.PARAGRAPH:
   st.font.name='Carlito';st.font.size=Pt(10.5);st.paragraph_format.space_after=Pt(5);st.paragraph_format.line_spacing=1.06;st.paragraph_format.widow_control=True
 for name in ['Table','Compact','First Paragraph','CaptionedFigure','Body Text','Block Text','Source Code']:
  style_named(doc,name)
 for name,size in [('Title',23),('Subtitle',14),('Heading 1',15),('Heading 2',12.3),('Heading 3',11)]:
  st=style_named(doc,name);st.font.name='Carlito';st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string('253C50');st.font.bold=name.startswith('Heading');st.paragraph_format.keep_with_next=True;st.paragraph_format.space_before=Pt(11);st.paragraph_format.space_after=Pt(6)
 for name in ['Source Code','Verbatim Char']:
  style_named(doc,name).font.name='DejaVu Sans Mono';style_named(doc,name).font.size=Pt(8.4)
 if doc.paragraphs:doc.paragraphs[0].style=style_named(doc,'Title')
 for p in doc.paragraphs:
  if p.text.startswith('Figure '):p.style=style_named(doc,'Caption');p.paragraph_format.space_after=Pt(9)
  if p.text.startswith('Table '):p.paragraph_format.keep_with_next=True
  if p._p.xpath('.//w:drawing'):p.paragraph_format.keep_with_next=True;p.alignment=WD_ALIGN_PARAGRAPH.CENTER
  if p.style.name.startswith('Heading') and p.text.startswith(('References','Appendix')):p.paragraph_format.keep_with_next=True
 for shape in doc.inline_shapes:
  maxwidth=Inches(6.55)
  if shape.width>maxwidth:ratio=maxwidth/shape.width;shape.width=int(shape.width*ratio);shape.height=int(shape.height*ratio)
 for tab in doc.tables:
  tab.autofit=False;tab.alignment=WD_TABLE_ALIGNMENT.CENTER;n=len(tab.columns);width=6.8277
  weights={2:[.29,.71],3:[.25,.39,.36],4:[.18,.24,.31,.27],5:[.12,.17,.24,.25,.22],6:[.09,.14,.22,.22,.18,.15],7:[.10,.14,.16,.14,.14,.14,.18]}.get(n,[1/n]*n);ws=[width*x for x in weights]
  pr=tab._tbl.tblPr
  for old in list(pr):
   if old.tag in [qn('w:tblBorders'),qn('w:tblCellMar')]:pr.remove(old)
  bo=OxmlElement('w:tblBorders')
  for edge in ['top','left','bottom','right','insideH','insideV']:
   e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'A4AFB8');bo.append(e)
  pr.append(bo);tw=pr.find(qn('w:tblW'));tw.set(qn('w:type'),'dxa');tw.set(qn('w:w'),str(int(width*1440)))
  for col,width1 in zip(tab.columns,ws):col.width=Inches(width1)
  for i,row in enumerate(tab.rows):
   if i==0:row._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
   row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
   for j,cell in enumerate(row.cells):
    cell.width=Inches(ws[j]);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
    for p in cell.paragraphs:
     p.paragraph_format.space_after=Pt(3);p.paragraph_format.line_spacing=1.0
     for run in p.runs:run.font.name='Carlito';run.font.size=Pt(8.7 if n>4 else 9.2);run.bold=True if i==0 else run.bold
    if i==0:
     sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'EAF0F4');cell._tc.get_or_add_tcPr().insert(0,sh)
 header=sec.header.paragraphs[0];header.text=doc.paragraphs[0].text;header.style=style_named(doc,'Caption')
 footer_style=style_named(doc,'Footer');footer_style.font.name='Carlito';footer_style.font.size=Pt(8)
 foot=sec.footer.paragraphs[0];foot.style=footer_style;foot.alignment=WD_ALIGN_PARAGRAPH.RIGHT;foot.add_run('Review edition | ');fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');foot._p.append(fld)
 for run in foot.runs:run.font.size=Pt(8)
 doc.core_properties.title=doc.paragraphs[0].text;doc.core_properties.author='James McGaughran';doc.core_properties.subject='ORSH/AIU v1.8 external review edition; canonical source '+md.name;doc.core_properties.comments='Generated from the supplied canonical Markdown; not an independent prose source.'
 # Unused pandoc numbering can contain prohibited dash glyphs.
 for part in doc.part.package.parts:
  if hasattr(part,'_element'):
   for e in part._element.iter():
    if len(e)==0 and e.text:e.text=e.text.replace('\u2013','-').replace('\u2014',': ')
    for k,v in list(e.attrib.items()):e.set(k,v.replace('\u2013','-').replace('\u2014',': '))
 doc.save(out);actual=signature(out)
 if sig!=actual:raise AssertionError('Styling changed content: '+md.name)
 report={'markdown':str(md.relative_to(root)),'markdown_sha256':hashlib.sha256(md.read_bytes()).hexdigest(),'pipeline':'pandoc canonical Markdown to DOCX; explicit native math delimiters; python-docx styling; independent PDF from canonical Markdown via XeLaTeX','vertical_stroke_glyph':'ASCII bar mapped to U+2223 in native math only; same delimiter meaning','delimiter_normalizations':delimiter_log,'upright_operator_runs':operator_runs,'post_style_content_parity':True,'ordered_blocks':len(sig),'math_objects':sum(x['math_count'] for x in sig),'tables':len(doc.tables),'images':len(doc.inline_shapes),'blocks':sig}
 (quality/(md.stem+'_build.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2));raw.unlink();print(out.name,len(sig),'blocks',report['math_objects'],'math objects',len(doc.tables),'tables')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('markdown',type=Path,nargs='+');a=p.parse_args()
 for md in a.markdown:build(md.resolve())
