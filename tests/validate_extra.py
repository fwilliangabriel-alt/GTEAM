import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
root=Path(__file__).resolve().parents[1];out={}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':960},reduced_motion='reduce')
 page.add_init_script('''window.metrics={cls:0,lcp:0};new PerformanceObserver(l=>{for(let e of l.getEntries())if(!e.hadRecentInput)metrics.cls+=e.value}).observe({type:'layout-shift',buffered:true});new PerformanceObserver(l=>{for(let e of l.getEntries())metrics.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});''')
 page.goto(os.environ.get('GTEAM_BASE_URL','http://127.0.0.1:8000/'),wait_until='networkidle');page.wait_for_timeout(500);out['lab_metrics']=page.evaluate('metrics')
 page.get_by_role('button',name='Em movimento',exact=True).click();out['videos']=[]
 for v in page.locator('video').all():
  v.scroll_into_view_if_needed();page.wait_for_timeout(200);v.evaluate('(v)=>v.play()');page.wait_for_function('(n)=>document.querySelectorAll("video")[n].currentTime>0',arg=len(out['videos']))
  v.evaluate('(v)=>v.pause()');out['videos'].append({'src':v.locator('source').get_attribute('src'),'played':True,'paused':v.evaluate('(v)=>v.paused'),'duration':v.evaluate('(v)=>v.duration')})
 # Verify all anchors and the selected service table match the user-approved guide.
 out['broken_local_anchors']=page.evaluate('''()=>[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash)''');assert not out['broken_local_anchors']
 out['has_prices']=page.evaluate('document.body.innerText.includes("R$")');assert not out['has_prices']
 assert page.locator('#panel-anual').inner_text().find('6 avaliações')>=0
 assert 'Sem suporte' in page.locator('.plan').nth(2).inner_text()
 # Mouse control and real horizontal gesture result, using touch emulation.
 ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);touch=ctx.new_page();touch.goto(os.environ.get('GTEAM_BASE_URL','http://127.0.0.1:8000/'),wait_until='networkidle');touch.get_by_role('button',name='O time',exact=True).click();track=touch.locator('.gallery-track');track.scroll_into_view_if_needed();touch.wait_for_timeout(300)
 box=track.bounding_box();cdp=ctx.new_cdp_session(touch);x=box['x']+box['width']*.9;y=min(700,max(180,box['y']+120));before=track.evaluate('(t)=>t.scrollLeft')
 cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
 for n in range(1,13):
  cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-n*20,'y':y}]});touch.wait_for_timeout(15)
 cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});touch.wait_for_timeout(600);after=track.evaluate('(t)=>t.scrollLeft');assert after>before,(before,after)
 out['touch_swipe']={'before':before,'after':after};ctx.close();b.close()
(root/'docs/extra-validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
