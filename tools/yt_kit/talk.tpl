<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;1,800;1,900&family=Barlow:wght@500;600;700&display=block" rel="stylesheet">
<style>
/* SRS Tapalpa Talks overlays, 3840x2160 transparent; the Tapalpa film look (Barlow, tricolour, one orange), calmer */
:root{--g:#006847;--r:#ce1126;--o:#ff7517;--ink:#0b0d10}
*{box-sizing:border-box;margin:0}
html,body{width:3840px;height:2160px;overflow:hidden;background:transparent;-webkit-font-smoothing:antialiased}
body.bg{background:radial-gradient(120% 90% at 20% 30%,#1a1d22 0%,#0b0d10 60%)}
body.flat{background:#0b0d10}
.tri{display:flex;gap:8px}.tri i{display:block;width:14px}
.tri i:nth-child(1){background:var(--g)}.tri i:nth-child(2){background:#fff}.tri i:nth-child(3){background:var(--r)}
.sh{text-shadow:0 6px 30px rgba(0,0,0,.55)}
/* opener */
.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,10,12,.86) 0%,rgba(8,10,12,.62) 32%,rgba(8,10,12,.12) 55%,rgba(8,10,12,0) 66%)}
.o-tri{position:absolute;left:180px;top:690px;height:780px;transform:skewX(-14deg)}
.o-kick{position:absolute;left:330px;top:700px;color:#fff;font:700 104px "Barlow Condensed";letter-spacing:.2em;text-transform:uppercase}
.o-kick b{color:var(--o);font-weight:700}
.o-name{position:absolute;left:316px;top:830px;color:#fff;font:900 italic 380px/.88 "Barlow Condensed";text-transform:uppercase;letter-spacing:-.005em}
.o-name span{display:block}
.o-line{position:absolute;left:330px;top:1540px;width:900px;height:8px;background:var(--o);transform-origin:left}
.lock{position:absolute;right:120px;top:100px;display:flex;align-items:center;gap:60px}
.lock .l-srs{width:400px}.lock i{display:block;width:6px;height:220px;background:rgba(255,255,255,.7)}
.lock .l-adv{display:flex;flex-direction:column;align-items:center;gap:16px;color:#fff;font:700 58px/1.05 "Barlow";letter-spacing:.32em;text-transform:uppercase;text-align:center}
.lock .l-adv img{width:220px}
.o-atlas{position:absolute;left:330px;bottom:150px;width:620px}
/* name plate */
.plate{position:absolute;left:220px;bottom:290px;display:flex;align-items:stretch;filter:drop-shadow(0 18px 40px rgba(0,0,0,.45))}
.plate .tri{margin-right:20px;transform:skewX(-14deg)}
.p-col{display:flex;flex-direction:column;align-items:flex-start}
.p-tag{margin-bottom:16px;padding-left:6px;color:#fff;font:700 54px/1 "Barlow Condensed";letter-spacing:.22em;text-transform:uppercase}
.p-tag b{color:var(--o)}
.p-name{background:#fff;color:#111;font:900 italic 150px/1 "Barlow Condensed";text-transform:uppercase;padding:14px 60px 10px 46px;white-space:nowrap}
.p-bar{height:12px;width:100%;background:var(--o)}
/* career line */
.band{position:absolute;left:0;right:0;bottom:0;height:900px;background:linear-gradient(0deg,rgba(8,10,12,.82) 0%,rgba(8,10,12,.55) 55%,rgba(8,10,12,0) 100%)}
.cl-kick{position:absolute;left:300px;top:1400px;color:#fff;font:700 58px "Barlow Condensed";letter-spacing:.24em;text-transform:uppercase}
.cl-kick b{color:var(--o)}
.cl-base{position:absolute;left:300px;top:1700px;width:3240px;height:4px;background:rgba(255,255,255,.22)}
.cl-fill{position:absolute;left:300px;top:1699px;width:3240px;height:6px;background:var(--o);transform-origin:left}
.cl-it{position:absolute;top:1550px;width:540px;margin-left:-270px;text-align:center;color:#fff}
.cl-it .y{font:800 italic 120px/1 "Barlow Condensed";color:#fff;margin-bottom:46px}
.cl-it i{position:absolute;left:50%;top:136px;width:34px;height:34px;margin-left:-17px;border-radius:50%;background:var(--o);box-shadow:0 0 0 10px rgba(255,117,23,.25)}
.cl-it .t{margin-top:40px;font:600 50px/1.2 "Barlow";letter-spacing:.02em}
.cl-it.last .y{color:var(--o)}
/* brand chips */
.ch-wrap{position:absolute;left:220px;bottom:250px;display:flex;flex-direction:column;align-items:flex-start;gap:26px;filter:drop-shadow(0 14px 34px rgba(0,0,0,.5))}
.ch-kick{color:#fff;font:700 54px "Barlow Condensed";letter-spacing:.24em;text-transform:uppercase}
.ch-kick b{color:var(--o)}
.chips{display:flex;gap:22px}
.chip{display:flex;align-items:stretch;font:800 italic 92px/1 "Barlow Condensed";text-transform:uppercase}
.chip b{background:#fff;color:#111;padding:20px 36px 16px}
.chip span{background:rgba(11,13,16,.92);color:#fff;padding:20px 34px 16px;font:700 64px/1.45 "Barlow";font-style:normal;text-transform:none;letter-spacing:.02em}
.chip.now b{background:var(--o)}
/* chapter card */
.cc{position:absolute;left:200px;top:180px;display:flex;align-items:stretch;filter:drop-shadow(0 14px 34px rgba(0,0,0,.5))}
.cc .tri{margin-right:18px;transform:skewX(-14deg)}
.cc-col{display:flex;flex-direction:column;align-items:flex-start}
.cc-k{background:var(--o);color:#111;font:800 52px/1 "Barlow Condensed";letter-spacing:.2em;text-transform:uppercase;padding:16px 30px 12px}
.cc-t{background:rgba(11,13,16,.9);color:#fff;font:800 italic 108px/1.04 "Barlow Condensed";text-transform:uppercase;padding:20px 40px 18px;max-width:2600px}
/* patreon */
.pt{position:absolute;left:220px;bottom:290px;display:flex;flex-direction:column;align-items:flex-start;filter:drop-shadow(0 18px 40px rgba(0,0,0,.45))}
.pt-q{background:rgba(11,13,16,.92);color:#fff;font:600 66px/1 "Barlow";padding:26px 40px 22px;letter-spacing:.02em}
.pt-a{display:flex;align-items:center;gap:30px;background:var(--o);color:#111;font:900 italic 128px/1 "Barlow Condensed";text-transform:uppercase;padding:18px 48px 12px 40px}
.pt-a svg{width:96px;height:96px;flex:none}
.pt-s{margin-top:16px;color:#fff;font:600 48px "Barlow";letter-spacing:.06em;padding-left:6px}
/* like and subscribe */
.ls{position:absolute;right:220px;bottom:280px;display:flex;align-items:center;gap:30px;filter:drop-shadow(0 18px 40px rgba(0,0,0,.5))}
.ls-who{position:absolute;right:0;bottom:200px;display:flex;align-items:center;gap:26px;color:#fff;font:700 54px "Barlow Condensed";letter-spacing:.2em;text-transform:uppercase;white-space:nowrap}
.ls-who img{width:330px}
.btn{position:relative;display:flex;align-items:center;gap:26px;height:170px;padding:0 56px;border-radius:85px;font:700 72px/1 "Barlow";letter-spacing:.01em;white-space:nowrap}
.like{background:rgba(255,255,255,.96);color:#111}
.like svg{width:84px;height:84px}
.like .on{position:absolute;inset:0;border-radius:85px;background:var(--o);display:flex;align-items:center;gap:26px;padding:0 56px;color:#111}
.sub{background:var(--o);color:#111;min-width:640px;justify-content:center}
.sub .done{position:absolute;inset:0;border-radius:85px;background:#2a2d33;color:#fff;display:flex;align-items:center;justify-content:center}
.bell{width:170px;height:170px;border-radius:50%;background:rgba(255,255,255,.96);display:grid;place-items:center}
.bell svg{width:92px;height:92px;transform-origin:50% 12%}
.cur{position:absolute;width:110px;height:130px;left:0;top:0}
/* end card */
.e-tri{position:absolute;left:200px;top:420px;height:620px;transform:skewX(-14deg)}
.e-k{position:absolute;left:340px;top:420px;color:#fff;font:700 76px "Barlow Condensed";letter-spacing:.22em;text-transform:uppercase}
.e-k b{color:var(--o)}
.e-h{position:absolute;left:326px;top:520px;color:#fff;font:900 italic 300px/.9 "Barlow Condensed";text-transform:uppercase}
.e-h span{color:var(--o)}
.e-url{position:absolute;left:340px;top:1180px;color:#fff;font:600 70px "Barlow";letter-spacing:.02em}
.e-url b{color:var(--o);font-weight:700}
.e-pt{position:absolute;left:340px;top:1300px;color:rgba(255,255,255,.75);font:500 58px "Barlow"}
.e-next{position:absolute;left:2140px;top:330px;color:rgba(255,255,255,.7);font:700 58px "Barlow Condensed";letter-spacing:.24em;text-transform:uppercase}
.e-next b{color:var(--o)}
.e-atlas{position:absolute;left:340px;bottom:170px;width:760px}
.e-lock{position:absolute;right:160px;bottom:150px;display:flex;align-items:center;gap:50px}
.e-lock .l-srs{width:300px}.e-lock i{display:block;width:5px;height:170px;background:rgba(255,255,255,.6)}
.e-lock .l-adv{display:flex;flex-direction:column;align-items:center;gap:12px;color:#fff;font:700 44px/1.05 "Barlow";letter-spacing:.32em;text-transform:uppercase;text-align:center}
.e-lock .l-adv img{width:170px}
</style></head><body class="BODYCLASS">BODY
<script>
// every move is a Web Animation; render(t) sets them all to one time (exact frames at any fps)
function A(sel,kf,opt){document.querySelectorAll(sel).forEach(function(e,i){var o=Object.assign({fill:'both'},opt);o.easing='linear';var k2=kf.map(function(k){return Object.assign({easing:opt.ke||'cubic-bezier(.2,.8,.2,1)'},k)});o.delay=(opt.delay||0)+(opt.stagger||0)*i;delete o.ke;delete o.stagger;e.animate(k2,o).pause()})}
function render(t){document.getAnimations().forEach(function(a){a.currentTime=t})}
SCRIPT
</script></body></html>
