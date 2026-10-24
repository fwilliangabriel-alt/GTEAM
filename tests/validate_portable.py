from pathlib import Path
import json,shutil
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
isolated=Path('/tmp/gteam-single-file');isolated.mkdir(exist_ok=True)
shutil.copy2(root/'ABRIR-NO-CELULAR.html',isolated/'index.html');url='http://127.0.0.1:8003/index.html'
out={}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for js in [True,False]:
  ctx=b.new_context(offline=False,java_script_enabled=js,viewport={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce')
  page=ctx.new_page();page.route('**/*',lambda route: route.continue_() if route.request.url==url else route.abort());errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url[:80]));page.goto(url,wait_until='load');ctx.set_offline(True)
  hero=page.locator('.hero-visual img');hero.evaluate('(i)=>i.decode()') if js else None
  state=page.evaluate('''()=>({heroLoaded:document.querySelector('.hero-visual img').naturalWidth>0,photoSquare:(()=>{const r=document.querySelector('.hero-visual picture').getBoundingClientRect();return Math.abs(r.width-r.height)<1})(),cssApplied:getComputedStyle(document.querySelector('.site-header')).position==='sticky',overflow:document.documentElement.scrollWidth>innerWidth,externalReferences:[...document.querySelectorAll('img[src],source[src],link[rel=stylesheet],script[src]')].filter(e=>(e.src||e.href||'').startsWith('file:')).length})''')
  assert state['heroLoaded'] and state['photoSquare'] and state['cssApplied'] and not state['overflow'] and not state['externalReferences'],state
  page.screenshot(path=str(root/'docs'/('portable-mobile-js.png' if js else 'portable-mobile-no-js.png')))
  page.locator('label[for=cycle-bimestral]').click();assert page.locator('#panel-bimestral').is_visible()
  page.locator('summary').first.click();assert page.locator('details').first.get_attribute('open') is not None
  if js:
   page.get_by_role('button',name='Antes e depois',exact=True).click();assert page.locator('.media-card:visible').count()==14
   page.locator('.enlarge:visible').first.click();assert page.locator('.lightbox').is_visible();page.keyboard.press('Escape')
   page.get_by_role('button',name='Em movimento',exact=True).click();v=page.locator('video').first;v.scroll_into_view_if_needed();page.wait_for_timeout(200);v.evaluate('(v)=>v.play()');page.wait_for_function('document.querySelector("video").currentTime>0');v.evaluate('(v)=>v.pause()');state['videoPlayedOffline']=True
  assert not errors,errors
  state['jsErrors']=errors;state['networkRequests']=requests;out['with_js' if js else 'without_js']=state;ctx.close()
 b.close()
(root/'docs/portable-validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
