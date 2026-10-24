"""Build the standalone review copy; production index.html keeps separate cached assets."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import base64,mimetypes
root=Path(__file__).resolve().parents[1]
cache={}
def embed(path):
 if not path.startswith('assets/'): return path
 if path not in cache:
  file=(root/path).resolve();assert file.is_relative_to(root/'assets')
  mime=mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
  cache[path]=f'data:{mime};base64,'+base64.b64encode(file.read_bytes()).decode('ascii')
 return cache[path]
class Portable(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.parts=[];self.skip_script=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='link' and a.get('rel')=='stylesheet':
   self.parts.append('<style>'+ (root/a['href']).read_text()+'</style>');return
  if tag=='script' and a.get('src')=='app.js':
   self.parts.append('<script>'+ (root/'app.js').read_text()+'</script>');self.skip_script=True;return
  if tag=='source' and a.get('srcset'):return # The original image is embedded, so no external responsive variants.
  if tag=='img':
   a.pop('srcset',None);a.pop('sizes',None)
  for key in ['src','poster']:
   if key in a:a[key]=embed(a[key])
  if tag=='a' and a.get('href','').startswith('assets/'):a['href']=embed(a['href'])
  if tag=='meta' and a.get('property')=='og:image':a['content']=embed(a.get('content',''))
  attr=''.join(' '+k+(f'="{escape(v,quote=True)}"' if v is not None else '') for k,v in a.items())
  self.parts.append('<'+tag+attr+'>')
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
 def handle_endtag(self,tag):
  if tag=='script' and self.skip_script:self.skip_script=False;return
  self.parts.append('</'+tag+'>')
 def handle_data(self,data):self.parts.append(data)
 def handle_entityref(self,name):self.parts.append('&'+name+';')
 def handle_charref(self,name):self.parts.append('&#'+name+';')
 def handle_decl(self,decl):self.parts.append('<!'+decl+'>')
 def handle_comment(self,data):self.parts.append('<!--'+data+'-->')
parser=Portable()
# Inline script executes at the end, after the document exists, instead of defer in the head.
source=(root/'index.html').read_text()
source=source.replace('<script defer="" src="app.js"></script>','').replace('<script src="app.js" defer></script>','')
source=source.replace('</body>','<script src="app.js"></script></body>')
parser.feed(source)
out=root/'ABRIR-NO-CELULAR.html';out.write_text(''.join(parser.parts))
print(f'{out.name}: {out.stat().st_size:,} bytes; {len(cache)} embedded assets')
