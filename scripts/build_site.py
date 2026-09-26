"""Build browser views from the unchanged canonical Markdown using Pandoc."""
from pathlib import Path
import json, shutil, subprocess, hashlib, html
from lxml import html as lh
import markdown

R=Path(__file__).resolve().parents[1]; O=R/'_site'
BASE='https://mathgov.github.io/ORSH-AIU/'
RELEASE='https://github.com/MathGov/ORSH-AIU/releases/tag/v1.8-open.1'
ASSET='https://github.com/MathGov/ORSH-AIU/releases/download/v1.8-open.1/'
papers=json.loads((R/'papers.json').read_text(encoding='utf-8'))
O.mkdir(exist_ok=True)
shutil.copytree(R/'publication',O/'publication',dirs_exist_ok=True)
shutil.copytree(R/'site',O,dirs_exist_ok=True)
shutil.copytree(R/'node_modules/katex/dist',O/'vendor/katex',dirs_exist_ok=True)
shutil.copyfile(R/'node_modules/katex/LICENSE',O/'vendor/katex/LICENSE.txt')
for f in ['LICENSE','NOTICE.md','CITATION.cff','citations.bib']:
 shutil.copyfile(R/f,O/f)
shutil.copytree(R/'LICENSES',O/'LICENSES',dirs_exist_ok=True)
shutil.copytree(R/'provenance',O/'provenance',dirs_exist_ok=True)

def page(title,body,path,desc,math=False):
 prefix='/ORSH-AIU/' if path=='404.html' else ('../' if '/' in path else './')
 extra=f'<link rel="stylesheet" href="{prefix}vendor/katex/katex.min.css"><script defer src="{prefix}vendor/katex/katex.min.js"></script><script defer src="{prefix}vendor/katex/contrib/auto-render.min.js"></script><script defer src="{prefix}math.js"></script>' if math else ''
 out=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | ORSH / AIU Research</title><meta name="description" content="{html.escape(desc,quote=True)}">
<link rel="canonical" href="{BASE}{path}"><meta property="og:title" content="{html.escape(title,quote=True)}"><meta property="og:description" content="{html.escape(desc,quote=True)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}social-card.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{prefix}icon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}site.css">{extra}
<script defer src="{prefix}site.js"></script></head><body><a class="skip" href="#main">Skip to content</a>
<header class="mast"><a class="brand" href="{prefix}index.html"><span class="mark" aria-hidden="true">⊙</span> ORSH / AIU <small>RESEARCH</small></a><nav aria-label="Main navigation"><a href="{prefix}index.html#papers">Papers</a><a href="{prefix}downloads.html">Downloads</a><a href="{prefix}reproduce.html">Reproduce</a><a href="{prefix}search.html">Search</a></nav></header>
<main id="main">{body}</main><footer><p>James McGaughran · MathGov / RippleLogic Research Program</p><p><a href="{prefix}license.html">CC BY 4.0 research · Apache 2.0 code</a> · <a href="{prefix}cite.html">Cite</a> · <a href="https://github.com/MathGov/ORSH-AIU">GitHub</a> · <a href="{prefix}evidence.html">Evidence & limits</a></p><p class="fine">Finalized collection v1.8 · Open-publication edition 1 · 27 September 2026</p></footer></body></html>'''
 target=O/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(out,encoding='utf-8')

cards=''
for i,d in enumerate(papers):
 cards+=f'''<article class="card"><p class="eyebrow">{i+1:02} / {d['kind']}</p><h3><a href="read/{d['slug']}.html">{d['title']}</a></h3><p>{d['description']}</p><p class="cardfoot">Version {d['version']} <a href="publication/{d['path']}.pdf">PDF ↗</a></p></article>'''
page('Frame-Aligned Records and Absolute Infinite Union',f'''
<section class="hero"><div><p class="eyebrow">AN OPEN RESEARCH COLLECTION</p><h1>What makes a<br>record meaningful?</h1><p class="lede">Frame-Aligned Records<br><span class="muted">& Absolute Infinite Union</span></p><p class="intro">Quantum records, locality, and philosophical foundations—presented as distinct arguments, with their sources, calculations and limits open to examination.</p><div class="actions"><a class="button" href="#papers">Read the papers</a><a class="button secondary" href="downloads.html">Download collection</a></div><p><a href="reproduce.html">Reproduce the results</a> <span aria-hidden="true"> / </span> <a href="cite.html">Cite the work</a></p></div><div class="orb" aria-hidden="true"><span class="orbit one"></span><span class="orbit two"></span><span class="orbit three"></span><span class="core"></span><span class="orbitlabel">STRUCTURE · ACCESS · RECORDS</span></div></section>
<div class="edition"><span>5 current works</span><span>PDF · DOCX · Markdown</span><span>Data + code included</span><span>Open-publication v1.8 / 1</span></div>
<section id="papers"><div class="sectionhead"><p class="eyebrow">START READING</p><h2>One collection.<br>Two kinds of inquiry.</h2><p>Begin with the scientific manuscript, then its supporting material. Read AIU as a separate philosophical argument.</p></div><div class="cards">{cards}</div></section>
<section class="split"><div><p class="eyebrow">READ THE EVIDENCE CAREFULLY</p><h2>Different questions.<br>Different contrasts.</h2></div><div><p>The original six-qubit pilot reports a negative readability-change mean. Later factorial comparisons report positive Hamiltonian-orientation contrasts at fixed injection. Their signs answer different questions.</p><p>The work does not establish a spacetime metric or a consciousness result. Reproducing the calculations does not validate the philosophical thesis.</p><a href="evidence.html">Read the evidence and limitations →</a></div></section>
<section class="split"><div><p class="eyebrow">BUILT FOR EXAMINATION</p><h2>Read. Reproduce.<br>Question. Reuse.</h2></div><div><p>Canonical Markdown, editable documents, figures and retained numerical data accompany the papers. The supplied archive remains unchanged; this open-publication edition adds readers, citations, licensing and verification.</p><p>ORSH is the historical programme label, Open Relational Substrate Hypothesis. AIU stands for Absolute Infinite Union. This is a specialist-review release; journal acceptance and external replication are not claimed.</p><a href="https://github.com/MathGov/ORSH-AIU/issues">Report a correction or reproduction result →</a></div></section>
<section class="related"><p class="eyebrow">IN THE MATHGOV RESEARCH FAMILY</p><a href="https://mathgov.github.io/ripple-logic/">RippleLogic ↗</a><a href="https://github.com/MathGov/AIAP">AIAP ↗</a><a href="https://github.com/MathGov/Auditable-Flourishing">Auditable Flourishing ↗</a></section>
''','index.html','Open research by James McGaughran: five works on quantum records, locality and Absolute Infinite Union, with PDFs, source, data and code.')

index=[];build=[]
for d in papers:
 source=R/'publication'/(d['path']+'.md')
 fragment=subprocess.check_output(['pandoc',str(source),'-f','markdown+autolink_bare_uris-implicit_figures','-t','html5','--mathjax','--wrap=none'],text=True,encoding='utf-8')
 tree=lh.fragment_fromstring(fragment,create_parent='article');tree.set('class','paper');tree.set('aria-label',d['title'])
 toc=[]
 for el in tree.xpath('.//h1 | .//h2'):
  if el.get('id'):toc.append(f'<li><a href="#{el.get("id")}">{html.escape(el.text_content())}</a></li>')
 for el in tree.xpath('.//*[@src]'):
  src=el.get('src')
  if src.startswith('../figures/'):el.set('src','../publication/figures/'+src.split('/')[-1])
 for el in tree.xpath('.//img'):
  el.set('loading','lazy')
 for table in tree.xpath('.//table'):
  wrap=lh.Element('div',{'class':'table-scroll','tabindex':'0','role':'region','aria-label':'Scrollable research table'});table.addprevious(wrap);wrap.append(table)
 for n,el in enumerate(tree.xpath('.//p | .//h1 | .//h2 | .//h3 | .//li')):
  if not el.get('id'):el.set('id',f'passage-{n+1}')
  text=' '.join(el.text_content().split())
  if len(text)>25:index.append({'title':d['title'],'slug':d['slug'],'url':'read/'+d['slug']+'.html#'+el.get('id'),'text':text})
 links=' · '.join(f'<a href="../publication/{d["path"]}.{ext}">{label}</a>' for ext,label in [('pdf','Download PDF'),('docx','Editable DOCX'),('md','Canonical Markdown')])
 body=f'<div class="readerhead"><p class="eyebrow">{d["kind"]} · Version {d["version"]}</p><p>{links}</p><p class="fine">Unchanged finalized source, 26 September 2026. Browser layout is derived. <a href="../license.html">Open license and provenance</a>.</p></div><div class="reading"><aside><details class="contents" open><summary>On this page</summary><nav aria-label="Paper contents"><ol>{"".join(toc)}</ol></nav></details></aside>{lh.tostring(tree,encoding="unicode")}</div>'
 page(d['title'],body,'read/'+d['slug']+'.html',d['description'],math=True)
 build.append({'path':d['path']+'.md','sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'reader':'read/'+d['slug']+'.html','math_elements':len(tree.cssselect('.math')) if False else len(tree.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," math ")]'))})

guide_map={'REPRODUCING.md':'reproduce.html','CITATION.md':'cite.html','EVIDENCE.md':'evidence.html','NOTICE.md':'license.html'}
for filename,url in guide_map.items():
 text=(R/filename).read_text(encoding='utf-8')
 frag=markdown.markdown(text,extensions=['tables','fenced_code','toc'])
 tree=lh.fragment_fromstring(frag,create_parent='div')
 for a in tree.xpath('.//a[@href]'):
  href=a.get('href')
  if href in guide_map:a.set('href',guide_map[href])
 if filename=='NOTICE.md':tree.append(lh.fragment_fromstring('<p>Full license texts: <a href="LICENSES/CC-BY-4.0.txt">CC BY 4.0</a> · <a href="LICENSES/Apache-2.0.txt">Apache 2.0</a>. <a href="provenance/source-inventory.json">Source inventory and hashes</a>.</p>'))
 if filename=='REPRODUCING.md':tree.append(lh.fragment_fromstring('<p><a href="https://github.com/MathGov/ORSH-AIU/actions">View automated verification runs</a> · <a href="provenance/publication-checks.json">Open-publication check receipt</a></p>'))
 page(text.splitlines()[0].lstrip('# '),'<article class="guide">'+lh.tostring(tree,encoding='unicode')+'</article>',url,'Guidance for the ORSH / AIU open research collection.')

rows=''.join(f'<tr><th scope="row">{d["title"]}<small>v{d["version"]}</small></th>'+''.join(f'<td><a href="publication/{d["path"]}.{ext}">{ext.upper()}</a></td>' for ext in ['pdf','docx','md'])+'</tr>' for d in papers)
assets=[('ORSH_AIU_v1_8_Open_Publication_1.zip','Open-publication bundle','Start here: current research, maintained guides, licensing and website source.'),('ORSH_AIU_v1_8_Finalized_Complete.zip','Original complete archive','Unchanged source package, including historical bundles and review records (72.8 MB).'),('Reproduction_v1_8.zip','Reproduction bundle','Research source, numerical code/data, provenance and environment instructions.'),('ORSH_AIU_v1_8_Collected_Reading_Copy.pdf','Collected reading PDF','All five works in the supplied reading copy.'),('SHA256SUMS.txt','Download checksums','Verify every named release asset against its SHA-256 digest.')]
assethtml=''.join(f'<li><a href="{ASSET}{name}">{title}</a><p>{desc}</p></li>' for name,title,desc in assets)
page('Downloads',f'<article class="guide"><p class="eyebrow">FIXED EDITION · v1.8-open.1</p><h1>Keep a copy.<br>Work from the source.</h1><p>Five current works, in three formats. PDF is for reading and printing; DOCX is editable; Markdown is canonical. Individual document bytes are unchanged.</p><div class="table-scroll" tabindex="0" role="region" aria-label="Document downloads"><table><thead><tr><th scope="col">Work</th><th scope="col">PDF</th><th scope="col">Word</th><th scope="col">Source</th></tr></thead><tbody>{rows}</tbody></table></div><h2>Complete bundles</h2><ul class="bundles">{assethtml}</ul><p><a href="{RELEASE}">Release notes and all assets →</a></p><p>The original archive records a prior pending-license state. The <a href="license.html">new public grant</a> applies to author-owned material; retain it alongside downloaded documents.</p></article>','downloads.html','Download the five papers, the complete archive, open-publication bundle and reproducible code and data.')
options=''.join(f'<option value="{d["slug"]}">{d["title"]}</option>' for d in papers)
page('Search the collection',f'<article class="guide"><p class="eyebrow">FULL-TEXT SEARCH · FIVE CURRENT WORKS</p><h1>Find a passage.</h1><p>Search words across the canonical texts. All entered words must occur in a passage. Search stays in your browser; equations are indexed as source notation.</p><form id="search-form"><label for="query">Words or phrase</label><input id="query" name="q" type="search" placeholder="e.g. conditional typicality" required><label for="scope">Work</label><select id="scope"><option value="">All five works</option>{options}</select><button type="submit">Search</button></form><p id="status" role="status">Ready to search.</p><div id="results"></div><button id="more" hidden>Show more results</button><noscript>Search requires JavaScript. Download the Markdown or PDF and use your document viewer’s search.</noscript></article><script defer src="search.js"></script>','search.html','Search passages across all five ORSH / AIU works and jump to their exact location.')
(O/'search-index.json').write_text(json.dumps(index,ensure_ascii=False),encoding='utf-8')
(O/'build-manifest.json').write_text(json.dumps({'pandoc':subprocess.check_output(['pandoc','--version'],text=True).splitlines()[0],'sources':build},indent=2),encoding='utf-8')
urls=['index.html','downloads.html','reproduce.html','cite.html','evidence.html','license.html','search.html']+['read/'+d['slug']+'.html' for d in papers]
(O/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+x+'</loc></url>' for x in urls)+'</urlset>',encoding='utf-8')
(O/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n',encoding='utf-8')
(O/'.nojekyll').write_text('',encoding='utf-8')
page('Page not found','<article class="guide"><h1>Page not found</h1><p><a href="/ORSH-AIU/">Return to the collection</a> or <a href="/ORSH-AIU/search.html">search the papers</a>.</p></article>','404.html','Return to the ORSH / AIU research collection.')
print(f'Built {len(papers)} readers, {len(index)} indexed passages and {len(urls)} sitemap pages.')
