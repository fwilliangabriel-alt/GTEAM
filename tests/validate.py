import os
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time
root=Path(__file__).resolve().parents[1];out=root/'docs';results={};base=os.environ.get('GTEAM_BASE_URL','http://127.0.0.1:8000/')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 errors=[];failures=[]
 for w in [320,375,390,430,768,1024,1440,1920]:
  page=b.new_page(viewport={'width':w,'height':960},device_scale_factor=1,is_mobile=w<500,has_touch=w<500)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:failures.append({'url':r.url,'status':r.status}) if r.status>=400 else None)
  page.goto(base,wait_until='networkidle')
  for section in page.locator('main>section').all():section.scroll_into_view_if_needed();page.wait_for_timeout(80)
  page.evaluate('window.scrollTo(0,0)');page.wait_for_timeout(100)
  layout=page.evaluate('''() => ({overflow:document.documentElement.scrollWidth>innerWidth,mainWidth:document.querySelector('main').clientWidth,brokenImages:[...document.images].filter(i=>i.getAttribute('src')&&i.complete&&!i.naturalWidth).length,headingOverflow:[...document.querySelectorAll('h1,h2,h3')].some(el=>el.scrollWidth>el.clientWidth+2)})''')
  assert not layout['overflow'],(w,layout)
  assert not layout['headingOverflow'],(w,layout)
  assert not layout['brokenImages'],(w,layout)
  if w in [320,390,768,1440,1920]:
   page.screenshot(path=str(out/f'after-{w}.png'),full_page=True)
  results[str(w)]=layout
  if w==390:
   page.get_by_role('button',name='Antes e depois',exact=True).click();assert page.locator('.media-card:visible').count()==14
   page.get_by_role('button',name='O time',exact=True).click();assert page.locator('.media-card:visible').count()==21
   page.get_by_role('button',name='Em movimento',exact=True).click();assert page.locator('.media-card:visible').count()==9
   video=page.locator('video').first;video.scroll_into_view_if_needed();video.evaluate('(v)=>v.play()');page.wait_for_function('document.querySelector("video").currentTime>0');video.evaluate('(v)=>v.pause()')
   results['video']={'played':True,'paused':video.evaluate('(v)=>v.paused'),'readyState':video.evaluate('(v)=>v.readyState')}
   page.get_by_role('button',name='Antes e depois',exact=True).click();page.locator('.media-card:visible .enlarge').first.click();assert page.locator('.lightbox').is_visible();page.keyboard.press('Escape');assert not page.locator('.lightbox').is_visible()
   page.locator('label[for=cycle-bimestral]').click();assert page.locator('#panel-bimestral').is_visible();assert not page.locator('#panel-anual').is_visible()
   page.locator('#cycle-bimestral').focus();page.keyboard.press('ArrowRight');assert page.locator('#panel-quadrimestral').is_visible()
   page.locator('#duration-1').select_option(index=1);assert 'Semestral' in page.locator('#duration-1').input_value()
   summary=page.locator('summary').first;summary.click();assert page.locator('details').first.get_attribute('open') is not None;summary.focus();page.keyboard.press('Enter');assert page.locator('details').first.get_attribute('open') is None
   page.get_by_role('button',name='Privacidade',exact=True).click();assert page.locator('.privacy-dialog').is_visible();page.keyboard.press('Escape')
   page.get_by_role('button',name='O time',exact=True).click();track=page.locator('.gallery-track');track.focus();page.keyboard.press('ArrowRight');page.wait_for_timeout(450);assert track.evaluate('(t)=>t.scrollLeft')>0
   # Swipe via Chromium touch protocol, in addition to keyboard and mouse controls.
   box=track.bounding_box();cdp=page.context.new_cdp_session(page)
   x=box['x']+box['width']*.8;y=max(180,box['y']+120)
   cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
   for n in range(1,9):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-n*20,'y':y}]})
   cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   results['interactions']='filters, image dialog/Escape, cycles/mouse/keyboard, native select, FAQ/mouse/keyboard, privacy, gallery keyboard and touch gesture dispatched'
  page.close()
 # No-JS and reduced motion.
 for mode in ['no_js','reduced_motion']:
  context=b.new_context(java_script_enabled=mode!='no_js',reduced_motion='reduce' if mode=='reduced_motion' else 'no-preference',viewport={'width':390,'height':844})
  page=context.new_page();page.goto(base,wait_until='networkidle')
  page.locator('label[for=cycle-semestral]').click();assert page.locator('#panel-semestral').is_visible()
  page.locator('summary').first.click();assert page.locator('details').first.get_attribute('open') is not None
  assert page.locator('.hero h1').is_visible()
  if mode=='no_js':assert page.locator('.enlarge').first.get_attribute('href').startswith('assets/')
  else:
   page.get_by_role('button',name='Em movimento',exact=True).click();page.locator('video').first.scroll_into_view_if_needed();page.wait_for_timeout(500);assert page.locator('video').first.evaluate('(v)=>v.paused')
  results[mode]='passed';context.close()
 # Simulate a slow connection, without loading all gallery media.
 context=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);page=context.new_page();cdp=context.new_cdp_session(page);cdp.send('Network.enable');cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':200000,'uploadThroughput':100000})
 page.goto(base,wait_until='load');page.wait_for_timeout(1000)
 results['slow_network']=page.evaluate('''()=>({htmlBytes:performance.getEntriesByType('navigation')[0].decodedBodySize,loadMs:performance.getEntriesByType('navigation')[0].loadEventEnd,videoRequests:performance.getEntriesByType('resource').filter(r=>r.name.endsWith('.mp4')).length,transferBytes:performance.getEntriesByType('resource').reduce((n,r)=>n+r.transferSize,0),h1Visible:document.querySelector('h1').getBoundingClientRect().top<innerHeight})''')
 assert results['slow_network']['videoRequests']==0
 context.close();results['js_errors']=errors;results['http_failures']=failures
 assert not errors,errors;assert not failures,failures
 b.close()
(out/'validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False,indent=2))
