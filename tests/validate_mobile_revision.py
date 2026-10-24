import os,json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
url=os.environ.get('GTEAM_BASE_URL','http://127.0.0.1:8000/')
results={}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in [320,375,390,430]:
  page=b.new_page(viewport={'width':width,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce');page.goto(url,wait_until='networkidle')
  data=page.evaluate('''()=>{const image=document.querySelector('.hero-visual picture'),r=image.getBoundingClientRect();return {width:r.width,height:r.height,top:r.top,corners:getComputedStyle(image).borderRadius,portraitFilter:getComputedStyle(document.querySelector('.about-image img')).filter,source:document.querySelector('.hero-visual img').currentSrc,planDirection:getComputedStyle(document.querySelector('.plans-list')).flexDirection,overflow:document.documentElement.scrollWidth>innerWidth,contactVisible:document.querySelector('.hero-actions .button').getBoundingClientRect().bottom<innerHeight}}''')
  assert abs(data['width']-data['height'])<1 and data['corners']=='0px'
  assert data['portraitFilter']=='none' and 'media-10' in data['source']
  assert data['top']<200 and data['planDirection']=='column' and not data['overflow']
  page.screenshot(path=str(root/'docs'/f'mobile-opening-{width}.png'))
  if width==390:
   page.screenshot(path=str(root/'docs/mobile-revision-hero.png'))
   page.locator('.site-header').evaluate('(header)=>header.style.visibility="hidden"')
   page.locator('.plan.featured').screenshot(path=str(root/'docs/mobile-revision-premium-full.png'))
   page.locator('.plan').nth(1).screenshot(path=str(root/'docs/mobile-revision-basic.png'))
   page.locator('.plan').nth(2).screenshot(path=str(root/'docs/mobile-revision-ready.png'))
   page.locator('.about-image img').scroll_into_view_if_needed();page.locator('.about-image img').evaluate('(img)=>img.decode()')
   page.locator('.about-image').screenshot(path=str(root/'docs/mobile-revision-founder.png'))
  results[str(width)]=data;page.close()
 # Network simulation uses the actual mobile viewport.
 ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);page=ctx.new_page();cdp=ctx.new_cdp_session(page);cdp.send('Network.enable');cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':200000,'uploadThroughput':100000});page.goto(url,wait_until='load');page.wait_for_timeout(500)
 results['mobile_slow_network']=page.evaluate('''()=>({htmlBytes:performance.getEntriesByType('navigation')[0].decodedBodySize,loadMs:performance.getEntriesByType('navigation')[0].loadEventEnd,videoRequests:performance.getEntriesByType('resource').filter(r=>r.name.endsWith('.mp4')).length,h1Visible:document.querySelector('h1').getBoundingClientRect().bottom<innerHeight})''')
 assert results['mobile_slow_network']['videoRequests']==0 and results['mobile_slow_network']['h1Visible']
 ctx.close();b.close()
(root/'docs/mobile-revision.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
