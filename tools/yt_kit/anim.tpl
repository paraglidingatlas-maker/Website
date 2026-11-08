<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;1,800;1,900&family=Barlow:wght@600;700&display=block" rel="stylesheet">
<style>
:root{--g:#006847;--r:#ce1126;--o:#ff7517}
*{box-sizing:border-box;margin:0}
html,body{width:3840px;height:2160px;overflow:hidden;background:transparent}
body.bg{background:#0a2a1e}
.slash{position:absolute;top:-200px;bottom:-200px;width:100px;transform:skewX(-18deg)}
.s1{left:2050px;background:var(--g)}.s2{left:2180px;background:#fff}.s3{left:2310px;background:var(--r)}
.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,34,24,.82) 0%,rgba(8,34,24,.6) 30%,rgba(8,34,24,.15) 50%,rgba(8,34,24,0) 60%)}
.kick{position:absolute;left:150px;top:640px;color:#fff;font:800 italic 120px "Barlow Condensed";letter-spacing:.14em;text-transform:uppercase}
.kick b{color:var(--o)}
.big{position:absolute;left:110px;top:760px;color:#fff;font:900 italic 760px/.86 "Barlow Condensed";letter-spacing:-.02em;text-transform:uppercase;white-space:nowrap}
.big span{color:var(--o)}
.strip{position:absolute;left:150px;top:1480px;display:flex;font:800 104px "Barlow Condensed";text-transform:uppercase}
.strip div{padding:18px 48px;background:#fff;color:#111}.strip div+div{background:var(--o)}
.lock{position:absolute;right:110px;top:90px;display:flex;align-items:center;gap:66px}
.lock .l-srs{width:450px}.lock i{display:block;width:8px;height:250px;background:rgba(255,255,255,.7)}
.lock .l-adv{display:flex;flex-direction:column;align-items:center;gap:18px;color:#fff;font:700 66px/1.05 "Barlow";letter-spacing:.32em;text-transform:uppercase;text-align:center}
.lock .l-adv img{width:250px}
.atlas{position:absolute;left:50%;bottom:-20px;width:1500px;margin-left:-750px}
/* end card */
.e-h{position:absolute;left:150px;top:300px;color:#fff;font:900 italic 300px/.9 "Barlow Condensed";text-transform:uppercase}
.e-h span{color:var(--o)}
.e-sub{position:absolute;left:156px;top:600px;color:rgba(255,255,255,.9);font:700 84px "Barlow";letter-spacing:.12em;text-transform:uppercase}
.e-url{position:absolute;left:156px;top:740px;color:#fff;font:700 70px "Barlow";letter-spacing:.04em}
.e-url b{color:var(--o)}
.slot{position:absolute;border:6px dashed rgba(255,255,255,.35);color:rgba(255,255,255,.45);font:700 54px "Barlow";display:grid;place-items:center;text-align:center}
</style></head><body class="BODYCLASS">BODY
<script>
// every move is a Web Animation; render() sets them all to one time
window.T=0;
function A(sel,kf,opt){document.querySelectorAll(sel).forEach(function(e,i){var o=Object.assign({fill:'both'},opt);o.easing='linear';kf=kf.map(function(k){return Object.assign({easing:opt.ke||'cubic-bezier(.2,.8,.2,1)'},k)});o.delay=(opt.delay||0)+(opt.stagger||0)*i;e.animate(kf,o).pause()})}
function render(t){document.getAnimations().forEach(function(a){a.currentTime=t})}
SCRIPT
</script></body></html>
