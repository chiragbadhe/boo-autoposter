import sys, subprocess, os, json
from playwright.sync_api import sync_playwright
DUR=json.load(open('timeline.json'))['DUR']
mode=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+os.path.abspath('reel.html')); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
    if mode=='test':
        for t in sys.argv[2:]:
            pg.evaluate(f'render({t})'); pg.screenshot(path=f'test_{t}.jpg',type='jpeg',quality=80)
    else:
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','tmp_video.mp4'],stdin=subprocess.PIPE)
        for i in range(int(DUR*30)):
            pg.evaluate(f'render({i/30})'); ff.stdin.write(pg.screenshot(type='jpeg',quality=90))
        ff.stdin.close(); sys.exit(ff.wait())
    b.close()
