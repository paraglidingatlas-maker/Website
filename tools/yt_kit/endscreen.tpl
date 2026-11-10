<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@500;600&display=block" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
html,body{width:3840px;height:2160px;overflow:hidden;background:#000}
.c{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center}
.logo{position:relative;width:1440px;height:300px}
.logo img{position:absolute;inset:0;width:100%;height:100%}
.glow{position:absolute;left:50%;top:40%;width:1800px;height:600px;transform:translate(-50%,-50%);background:radial-gradient(closest-side,rgba(255,117,23,.10),rgba(255,117,23,0));}
.t{margin-top:90px;font:500 50px/1 "Barlow",sans-serif;letter-spacing:.42em;text-transform:uppercase;color:rgba(246,244,244,.78);white-space:nowrap;padding-left:.42em}
.line{width:0;height:2px;margin-top:70px;background:linear-gradient(90deg,rgba(255,117,23,0),rgba(255,117,23,.8),rgba(255,117,23,0))}
</style></head><body>
<div class="glow"></div>
<div class="c">
  <div class="logo"><img class="arc" src="arc.png"><img class="let" src="letters.png"></div>
  <div class="line"></div>
  <div class="t">A Paragliding Atlas Production</div>
</div>
<script>
function A(sel,kf,o){document.querySelectorAll(sel).forEach(function(e){var x=Object.assign({fill:'both',easing:'linear'},o);kf=kf.map(function(k){return Object.assign({easing:o.ke||'cubic-bezier(.2,.8,.2,1)'},k)});delete x.ke;e.animate(kf,x).pause()})}
function render(t){document.getAnimations().forEach(function(a){a.currentTime=t})}
A('.glow',[{opacity:0},{opacity:1}],{duration:2200,delay:300,ke:'linear'});
A('.arc',[{clipPath:'inset(0 100% 0 0)',filter:'blur(6px)'},{clipPath:'inset(0 0% 0 0)',filter:'blur(0)'}],{duration:1300,delay:300,ke:'cubic-bezier(.65,0,.25,1)'});
A('.let',[{opacity:0,transform:'translateY(40px)',filter:'blur(10px)'},{opacity:1,transform:'none',filter:'blur(0)'}],{duration:1100,delay:1000});
A('.line',[{width:'0px',opacity:0},{width:'900px',opacity:1}],{duration:1100,delay:1700,ke:'cubic-bezier(.65,0,.25,1)'});
A('.t',[{opacity:0,letterSpacing:'.7em'},{opacity:1,letterSpacing:'.42em'}],{duration:1400,delay:1900});
</script></body></html>
