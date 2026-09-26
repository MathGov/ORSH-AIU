from pathlib import Path
import hashlib,json
from urllib.parse import urlsplit,unquote
from lxml import html
R=Path(__file__).resolve().parents[1];O=R/'_site'
trees={p:html.parse(str(p)) for p in O.rglob('*.html') if 'publication' not in p.relative_to(O).parts}
links=0
for path,tree in trees.items():
 ids=tree.xpath('//@id');assert len(ids)==len(set(ids)),f'Duplicate IDs: {path}'
 assert tree.xpath('//html[@lang="en"]') and tree.xpath('//title') and tree.xpath('//main'),path
 for el in tree.xpath('//*[@href or @src]'):
  value=el.get('href') or el.get('src');u=urlsplit(value)
  if u.scheme or u.netloc:continue
  if u.path.startswith('/ORSH-AIU/'):target=O/u.path.removeprefix('/ORSH-AIU/')
  else:target=(path.parent/unquote(u.path)).resolve() if u.path else path
  if target.is_dir():target=target/'index.html'
  assert target.is_file(),f'Missing {value} in {path}'
  if u.fragment and target.suffix=='.html':
   t=trees.get(target) or html.parse(str(target));assert unquote(u.fragment) in t.xpath('//@id'),f'Missing anchor {value} in {path}'
  links+=1
for d in json.loads((R/'papers.json').read_text(encoding='utf-8')):
 for ext in ['md','pdf','docx']:
  a=R/'publication'/(d['path']+'.'+ext);b=O/'publication'/(d['path']+'.'+ext)
  assert hashlib.sha256(a.read_bytes()).digest()==hashlib.sha256(b.read_bytes()).digest()
 reader=html.parse(str(O/'read'/(d['slug']+'.html')))
 assert reader.xpath('//article[contains(@class,"paper")]')
index=json.loads((O/'search-index.json').read_text(encoding='utf-8'))
assert len({x['slug'] for x in index})==5
for x in index:
 u=urlsplit(x['url']);t=trees.get(O/u.path) or html.parse(str(O/u.path));assert u.fragment in t.xpath('//@id')
print(json.dumps({'html_pages':len(trees),'local_links_checked':links,'download_byte_identity':15,'search_passages':len(index)},indent=2))
