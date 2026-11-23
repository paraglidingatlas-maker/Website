// SRS 2027 calendar page builder. Pages are data; add a month by adding an entry to PAGES.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const DIR=__dirname, OUT='/home/user/srs-calendar-2027';
const ROUNDS=[
 {n:1,place:'Lijak',country:'Slovenia',code:'SVN',from:'2027-03-15',to:'2027-03-21',status:'Confirmed'},
 {n:2,place:'St Jean Montclar',country:'France',code:'FRA',from:'2027-06-20',to:'2027-06-27',status:'Provisional'},
 {n:3,place:'Gemona',country:'Italy',code:'ITA',from:'2027-07-17',to:'2027-07-24',status:'Confirmed'},
 {n:4,place:'Krushevo',country:'North Macedonia',code:'MKD',from:'2027-08-22',to:'2027-08-29',status:'Confirmed'},
 {n:5,place:'St André',country:'France',code:'FRA',from:'2027-09-12',to:'2027-09-19',status:'Confirmed'},
];
const PAGES=[
 {file:'01-cover',type:'cover',img:'t6_138_fx.jpg',pos:'70% 50%',cap:'Tapalpa, Mexico · SRS 2026 · Task 6'},
 {file:'02-january',type:'month',m:1,img:'t6_66_fx.jpg',pos:'66% 50%',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 6'},
 {file:'03-february',type:'month',m:2,img:'t6_100_fx.jpg',pos:'90% 50%',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 6'},
 {file:'04-march',type:'month',m:3,img:'t6_t454_fx.jpg',pos:'12% 50%',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 4'},
 {file:'05-april',type:'month',m:4,img:'t6_t494_fx.jpg',pos:'50% 0%',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 4'},
 {file:'06-may',type:'strip',m:5,img:'t6_t4152_nat.jpg',pos:'40% 72%',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 4'},
 {file:'07-june',type:'tower',m:6,img:'t6_t4118_dusk.jpg',pos:'100% 50%',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 4'},
 {file:'08-july',type:'month',cls:'sl',m:7,img:'t6_t345_fx.jpg',pos:'46% 50%',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 3'},
 {file:'09-august',type:'depth',m:8,img:'t6_t357_depth.jpg',cut:'t6_t357_cut.png',pos:'30% 50%',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 3'},
];
const MN=['January','February','March','April','May','June','July','August','September','October','November','December'];
const MS=MN.map(x=>x.slice(0,3).toUpperCase());
const d=s=>new Date(s+'T00:00:00Z'), pad=n=>String(n).padStart(2,'0');
const span=r=>{const a=d(r.from),b=d(r.to);return a.getUTCMonth()==b.getUTCMonth()?`${a.getUTCDate()}–${b.getUTCDate()} ${MS[b.getUTCMonth()]}`:`${a.getUTCDate()} ${MS[a.getUTCMonth()]} – ${b.getUTCDate()} ${MS[b.getUTCMonth()]}`};
const FONTS=[['Poppins','poppins',[400,500,600,700,800]],['DM Sans','dm-sans',[400,500,600]]].map(([fam,f,ws])=>ws.map(w=>['latin','latin-ext'].map(s=>
`@font-face{font-family:"${fam}";font-weight:${w};src:url(file://${DIR}/fonts/${f}-${s}-${w}-normal.woff2) format("woff2");unicode-range:${s=='latin'?'U+0000-00FF,U+2000-206F,U+2212':'U+0100-02AF,U+1E00-1EFF'}}`).join('')).join('')).join('');
const CSS=`${FONTS}
@page{size:297mm 210mm;margin:0}*{margin:0;padding:0;box-sizing:border-box}
html,body{width:297mm;height:210mm;background:#141519;color:#f6f4f4;font-family:"DM Sans",sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact;overflow:hidden}
.pg{position:relative;width:297mm;height:210mm;overflow:hidden}
.lab{font:500 2.5mm/1 "DM Sans";letter-spacing:.34em;text-transform:uppercase;color:#b9b8bd}
.red{color:#e8112d}
/* cover */
.cv .ph{position:absolute;inset:0;background-size:cover}
.cv .sh{position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,21,25,.9) 0%,rgba(20,21,25,.55) 34%,rgba(20,21,25,0) 62%),linear-gradient(180deg,rgba(20,21,25,.45) 0%,rgba(20,21,25,0) 22%,rgba(20,21,25,0) 63%,rgba(20,21,25,.9) 77%,#141519 96%)}
.cv .top{position:absolute;left:16mm;right:16mm;top:14mm;display:flex;justify-content:space-between}
.cv .ttl{position:absolute;left:15mm;top:34mm}
.cv .ttl .a{font:800 46mm/.86 Poppins;letter-spacing:-.03em}
.cv .ttl .b{font:800 46mm/.86 Poppins;letter-spacing:-.03em;color:transparent;-webkit-text-stroke:.35mm rgba(246,244,244,.85)}
.cv .ttl .c{margin-top:8mm;margin-left:1mm;display:flex;align-items:center;gap:5mm}
.cv .ttl .c i{width:14mm;height:.5mm;background:#e8112d}
.cv .ttl .c span{font:600 4.2mm/1 Poppins;letter-spacing:.42em;text-transform:uppercase}
.cv .rd{position:absolute;left:16mm;right:16mm;bottom:12mm;display:grid;grid-template-columns:1fr 1.32fr 1fr 1fr 1fr;border-top:.25mm solid rgba(246,244,244,.28)}
.cv .rd>div{padding:4.2mm 3mm 0 0}
.cv .rd>div+div{padding-left:5mm;border-left:.25mm solid rgba(246,244,244,.16)}
.cv .rd .r{font:600 2.5mm/1 "DM Sans";letter-spacing:.3em;color:#e8112d}
.cv .rd .p{font:700 5mm/1.05 Poppins;text-transform:uppercase;margin-top:2.6mm;letter-spacing:-.005em;white-space:nowrap}
.cv .rd .c{font:400 2.9mm/1 "DM Sans";color:#b9b8bd;margin-top:1.8mm}
.cv .rd .t{font:600 3.3mm/1 Poppins;letter-spacing:.14em;margin-top:3.4mm}
.cv .rd .s{font:500 2mm/1 "DM Sans";letter-spacing:.28em;text-transform:uppercase;color:#8d8c92;margin-top:2mm}
/* month */
.mo .ph{position:absolute;left:0;top:0;bottom:0;width:190mm;background-size:cover}
.mo .phs{position:absolute;left:0;top:0;bottom:0;width:190mm;background:linear-gradient(180deg,rgba(20,21,25,.35) 0%,rgba(20,21,25,0) 18%,rgba(20,21,25,0) 68%,rgba(20,21,25,.8) 100%),linear-gradient(270deg,rgba(20,21,25,.55) 0%,rgba(20,21,25,0) 14%)}
.mo .cap{position:absolute;left:12mm;bottom:11mm}
.mo .cap b{display:block;font:700 5mm/1 Poppins;text-transform:uppercase;letter-spacing:.02em;margin-bottom:2.4mm}
.mo .cr{position:absolute;left:12mm;top:12mm}
.mo .pn{position:absolute;right:0;top:0;bottom:0;width:107mm;background:#141519;padding:12mm 12mm 11mm}
.mo .hd{display:flex;justify-content:space-between}
.mo .num{position:absolute;right:9mm;top:17mm;font:800 62mm/1 Poppins;letter-spacing:-.04em;color:transparent;-webkit-text-stroke:.3mm rgba(246,244,244,.2)}
.mo .name{position:absolute;left:12mm;top:62mm;font:800 15.5mm/1 Poppins;letter-spacing:-.02em;text-transform:uppercase}
.mo .yr{position:absolute;left:12.6mm;top:80.5mm;display:flex;align-items:center;gap:3.5mm}
.mo .yr i{width:9mm;height:.5mm;background:#e8112d}
.mo .gr{position:absolute;left:12mm;right:12mm;top:94mm;display:grid;grid-template-columns:repeat(7,1fr)}
.mo .gr .h{font:500 2.1mm/1 "DM Sans";letter-spacing:.24em;color:#8d8c92;text-align:center;padding-bottom:3.4mm;border-bottom:.25mm solid #2b2c33;margin-bottom:1.6mm}
.mo .gr .c{position:relative;height:var(--rh);display:flex;align-items:center;justify-content:center;font:500 4.3mm/1 Poppins;font-variant-numeric:tabular-nums}
.mo .gr .c.we{color:#8d8c92}
.mo .gr .c.rc{color:#fff;font-weight:700}
.mo .gr .c.rc::before{content:"";position:absolute;inset:1.3mm 0;background:#e8112d;z-index:-1}
.mo .gr .c.rc.f::before{left:1.2mm;border-radius:1mm 0 0 1mm}.mo .gr .c.rc.l::before{right:1.2mm;border-radius:0 1mm 1mm 0}
.mo .gr{isolation:isolate}
.mo .ft{position:absolute;left:12mm;right:12mm;bottom:11mm;border-top:.25mm solid #2b2c33;padding-top:5mm;display:flex;justify-content:space-between;align-items:flex-end}
.mo .ft .p{font:700 5.6mm/1 Poppins;text-transform:uppercase;margin-top:3mm}
.mo .ft .c{font:400 2.9mm/1 "DM Sans";color:#b9b8bd;margin-top:1.8mm}
.mo .ft .t{font:600 3.4mm/1 Poppins;letter-spacing:.14em;text-align:right}
.mo .ft .s{font:500 2mm/1 "DM Sans";letter-spacing:.28em;text-transform:uppercase;color:#8d8c92;margin-top:2mm;text-align:right}
/* strip: full-width photo, one-line month */
.st .ph{position:absolute;left:0;right:0;top:0;height:166mm;background-size:cover}
.st .phs{position:absolute;left:0;right:0;top:0;height:166mm;background:linear-gradient(180deg,rgba(20,21,25,.5) 0%,rgba(20,21,25,0) 30%,rgba(20,21,25,0) 78%,#141519 100%),linear-gradient(90deg,rgba(20,21,25,.5) 0%,rgba(20,21,25,0) 40%)}
.st .top{position:absolute;left:12mm;right:12mm;top:12mm;display:flex;justify-content:space-between}
.st .num{position:absolute;left:10mm;top:20mm;font:800 54mm/1 Poppins;letter-spacing:-.04em;color:transparent;-webkit-text-stroke:.3mm rgba(246,244,244,.38)}
.st .name{position:absolute;left:12mm;top:57mm;font:800 22mm/1 Poppins;letter-spacing:-.02em;text-transform:uppercase}
.st .yr{position:absolute;left:12.6mm;top:83mm;display:flex;align-items:center;gap:3.5mm}
.st .yr i{width:9mm;height:.5mm;background:#e8112d}
.st .cap{position:absolute;right:12mm;top:146mm;text-align:right}
.st .cap b{display:block;font:700 4.4mm/1 Poppins;text-transform:uppercase;letter-spacing:.02em;margin-bottom:2.2mm}
.st .row{position:absolute;left:12mm;right:12mm;top:170mm;display:grid;isolation:isolate}
.st .row .h{font:500 1.9mm/1 "DM Sans";letter-spacing:.14em;color:#8d8c92;text-align:center;padding-bottom:2.4mm}
.st .row .c{position:relative;height:9mm;display:flex;align-items:center;justify-content:center;font:500 4mm/1 Poppins;font-variant-numeric:tabular-nums;border-top:.25mm solid #2b2c33}
.st .row .c.we,.st .row .h.we{color:#77767c}.st .row .c.we{color:#8d8c92}
.st .row .c.rc{color:#fff;font-weight:700;border-top-color:#e8112d}
.st .row .c.rc::before{content:"";position:absolute;inset:.9mm 0;background:#e8112d;z-index:-1}
.st .ft{position:absolute;left:12mm;right:12mm;bottom:10mm;display:flex;justify-content:space-between;align-items:baseline}
.st .ft .p{font:700 4.4mm/1 Poppins;text-transform:uppercase;margin:0 4mm}
.st .ft .t{font:600 3.2mm/1 Poppins;letter-spacing:.14em}
.st .ft .r{display:flex;align-items:baseline}
/* tower: full-bleed photo, the month as a timing tower */
.tw .ph{position:absolute;inset:0;background-size:cover}
.tw .phs{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,21,25,.72) 0%,rgba(20,21,25,0) 26%,rgba(20,21,25,0) 60%,rgba(20,21,25,.82) 100%)}
.tw .twr{position:absolute;left:0;top:0;bottom:0;width:50mm;background:rgba(20,21,25,.9);padding:12mm 8mm 0 12mm;border-right:.25mm solid rgba(246,244,244,.14)}
.tw .twr .hd{display:flex;justify-content:space-between;margin-bottom:6mm;white-space:nowrap}.tw .twr .hd .lab{letter-spacing:.2em;font-size:2.3mm}
.tw .twr .r{position:relative;display:grid;grid-template-columns:8.5mm 10mm 1fr;align-items:center;height:var(--rh);border-top:.2mm solid rgba(246,244,244,.09);isolation:isolate}
.tw .twr .r b{font:600 3.1mm/1 Poppins;font-variant-numeric:tabular-nums}
.tw .twr .r i{font:500 1.9mm/1 "DM Sans";font-style:normal;letter-spacing:.2em;color:#8d8c92}
.tw .twr .r u{font:700 2mm/1 "DM Sans";text-decoration:none;letter-spacing:.2em;text-align:right;padding-right:1.6mm}
.tw .twr .r.we b{color:#8d8c92}
.tw .twr .r.rc{border-top-color:transparent}.tw .twr .r.rc b,.tw .twr .r.rc i{color:#fff}
.tw .twr .r.rc::before{content:"";position:absolute;left:-12mm;right:-8mm;top:.25mm;bottom:.25mm;background:#e8112d;z-index:-1}
.tw .rb{position:absolute;left:138mm;top:12mm}
.tw .rb .tag{display:inline-block;font:800 3.4mm/1 Poppins;letter-spacing:.14em;background:#e8112d;padding:2mm 3.4mm;transform:skewX(-12deg)}
.tw .rb .p{white-space:nowrap;font:800 9mm/1 Poppins;text-transform:uppercase;letter-spacing:-.015em;margin-top:4mm}
.tw .rb .c{font:600 3.6mm/1 Poppins;letter-spacing:.16em;text-transform:uppercase;margin-top:3mm}
.tw .rb .s{margin-top:2.6mm}
.tw .num{position:absolute;left:58mm;bottom:38mm;font:800 54mm/1 Poppins;letter-spacing:-.04em;color:transparent;-webkit-text-stroke:.3mm rgba(246,244,244,.4)}
.tw .name{position:absolute;left:60mm;bottom:19mm;font:800 30mm/1 Poppins;letter-spacing:-.025em;text-transform:uppercase}
.tw .yr{position:absolute;left:60.6mm;bottom:12mm;display:flex;align-items:center;gap:3.5mm}
.tw .yr i{width:9mm;height:.5mm;background:#e8112d}
.tw .cap{position:absolute;right:12mm;bottom:12mm;text-align:right}
.tw .cap b{display:block;font:700 4.4mm/1 Poppins;text-transform:uppercase;letter-spacing:.02em;margin-bottom:2.2mm}
.tw .cap .lab+.lab{display:block;margin-top:2.4mm;color:#8d8c92}
/* slant: the month on the left, the photo cut on a racing angle */
.mo.sl .pn{left:0;right:auto}
.mo.sl .ph,.mo.sl .phs{left:104mm;width:193mm;clip-path:polygon(0 0,100% 0,100% 100%,15mm 100%)}
.mo.sl .phs{background:linear-gradient(180deg,rgba(20,21,25,.4) 0%,rgba(20,21,25,0) 18%,rgba(20,21,25,0) 68%,rgba(20,21,25,.8) 100%)}
.mo.sl::after{content:"";position:absolute;left:102.6mm;top:0;bottom:0;width:16.4mm;background:#e8112d;clip-path:polygon(0 0,.8mm 0,15.8mm 100%,15mm 100%)}
.mo.sl .cap{left:auto;right:12mm;text-align:right}.mo.sl .cr{left:auto;right:6mm;top:12mm;writing-mode:vertical-rl}
/* depth: the month's name set into the landscape, behind the wing */
.dp .ph,.dp .cut{position:absolute;inset:0;background-size:cover}
.dp .phs{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,21,25,.35) 0%,rgba(20,21,25,0) 20%,rgba(20,21,25,0) 62%,rgba(20,21,25,.78) 100%)}
.dp .name{position:absolute;left:9mm;right:9mm;top:17mm;font:800 var(--fs)/.8 Poppins;letter-spacing:-.03em;text-transform:uppercase;text-align:center;white-space:nowrap;color:#f6f4f4}
.dp .top{position:absolute;left:12mm;right:12mm;top:10mm;display:flex;justify-content:space-between}
.dp .cap{position:absolute;left:12mm;bottom:12mm}
.dp .cap b{display:block;font:700 5mm/1 Poppins;text-transform:uppercase;letter-spacing:.02em;margin-bottom:2.4mm}
.dp .cap .lab+.lab{display:block;margin-top:2.4mm;color:#b9b8bd}
.dp .card{position:absolute;right:12mm;bottom:12mm;width:98mm;background:rgba(20,21,25,.84);border:.25mm solid rgba(246,244,244,.14);padding:7mm 7mm 6mm}
.dp .card .hd{display:flex;justify-content:space-between;margin-bottom:5mm}
.dp .card .gr{display:grid;grid-template-columns:repeat(7,1fr);isolation:isolate}
.dp .card .gr .h{font:500 1.9mm/1 "DM Sans";letter-spacing:.22em;color:#8d8c92;text-align:center;padding-bottom:2.6mm;border-bottom:.25mm solid #2b2c33;margin-bottom:1mm}
.dp .card .gr .c{position:relative;height:var(--rh);display:flex;align-items:center;justify-content:center;font:500 3.7mm/1 Poppins;font-variant-numeric:tabular-nums}
.dp .card .gr .c.we{color:#8d8c92}.dp .card .gr .c.rc{color:#fff;font-weight:700}
.dp .card .gr .c.rc::before{content:"";position:absolute;inset:1mm 0;background:#e8112d;z-index:-1}
.dp .card .gr .c.rc.f::before{left:1mm;border-radius:1mm 0 0 1mm}.dp .card .gr .c.rc.l::before{right:1mm;border-radius:0 1mm 1mm 0}
.dp .card .ft{margin-top:4mm;border-top:.25mm solid #2b2c33;padding-top:4.4mm;display:flex;justify-content:space-between;align-items:flex-end}
.dp .card .ft .p{font:700 5mm/1 Poppins;text-transform:uppercase;margin-top:2.6mm}
.dp .card .ft .c{font:400 2.7mm/1 "DM Sans";color:#b9b8bd;margin-top:1.6mm}
.dp .card .ft .t{font:600 3.1mm/1 Poppins;letter-spacing:.14em;text-align:right}
.dp .card .ft .s{font:500 1.9mm/1 "DM Sans";letter-spacing:.28em;text-transform:uppercase;color:#8d8c92;margin-top:1.8mm;text-align:right}
`;
function cover(p){return `<div class="pg cv"><div class="ph" style="background-image:url(file://${DIR}/${p.img});background-position:${p.pos}"></div><div class="sh"></div>
<div class="top"><span class="lab">Sports-Class Racing Series</span><span class="lab">${p.cap}</span></div>
<div class="ttl"><div class="a">SRS</div><div class="b">2027</div><div class="c"><i></i><span>Race Calendar</span></div></div>
<div class="rd">${ROUNDS.map(r=>`<div><div class="r">ROUND ${pad(r.n)}</div><div class="p">${r.place}</div><div class="c">${r.country}</div><div class="t">${span(r)}</div><div class="s">${r.status}</div></div>`).join('')}</div></div>`}
function month(p){const y=2027,m=p.m,first=new Date(Date.UTC(y,m-1,1)),days=new Date(Date.UTC(y,m,0)).getUTCDate(),off=(first.getUTCDay()+6)%7,rows=Math.ceil((off+days)/7);
 const iso=n=>`${y}-${pad(m)}-${pad(n)}`, rOf=n=>ROUNDS.find(r=>iso(n)>=r.from&&iso(n)<=r.to);
 let cells=['MON','TUE','WED','THU','FRI','SAT','SUN'].map(h=>`<div class="h">${h}</div>`).join('')+'<div></div>'.repeat(off);
 for(let n=1;n<=days;n++){const col=(off+n-1)%7,r=rOf(n);let c='c'+(col>4?' we':'');if(r){c+=' rc';if(iso(n)==r.from||col==0||n==1)c+=' f';if(iso(n)==r.to||col==6||n==days)c+=' l'}cells+=`<div class="${c}">${n}</div>`}
 const mine=ROUNDS.filter(r=>r.from.slice(5,7)==pad(m)||r.to.slice(5,7)==pad(m)), nxt=ROUNDS.find(r=>r.from>iso(days));
 const r=mine[0]||nxt, lab=mine[0]?`Round ${pad(r.n)} · This month`:(r?(r.n==1?'Season opens':'Next round')+` · Round ${pad(r.n)}`:'Season complete');
 const ft=r?`<div><div class="lab red">${lab}</div><div class="p"${r.place.length>10?' style="font-size:4.5mm"':''}>${r.place}</div><div class="c">${r.country}</div></div><div><div class="t">${span(r)}</div><div class="s">${r.status}</div></div>`:`<div><div class="lab">${lab}</div></div>`;
 return `<div class="pg mo ${p.cls||''}"><div class="ph" style="background-image:url(file://${DIR}/${p.img});background-position:${p.pos}"></div><div class="phs"></div>
<div class="cr lab">Photo · Aninder Singh / Paragliding Atlas</div><div class="cap"><b>${p.cap}</b><span class="lab">${p.sub}</span></div>
<div class="pn"><div class="hd"><span class="lab">SRS <span class="red">/</span> 2027</span><span class="lab">${pad(m)} / 12</span></div>
<div class="num">${pad(m)}</div><div class="name">${MN[m-1]}</div><div class="yr"><i></i><span class="lab">2027</span></div>
<div class="gr" style="--rh:${rows>5?10.6:12.4}mm">${cells}</div><div class="ft">${ft}</div></div></div>`}
function strip(p){const y=2027,m=p.m,days=new Date(Date.UTC(y,m,0)).getUTCDate(),WD=['S','M','T','W','T','F','S'];
 const iso=n=>`${y}-${pad(m)}-${pad(n)}`, rOf=n=>ROUNDS.find(r=>iso(n)>=r.from&&iso(n)<=r.to);let h='',c='';
 for(let n=1;n<=days;n++){const wd=new Date(Date.UTC(y,m-1,n)).getUTCDay(),we=wd==0||wd==6;h+=`<div class="h${we?' we':''}">${WD[wd]}</div>`;c+=`<div class="c${we?' we':''}${rOf(n)?' rc':''}">${n}</div>`}
 const mine=ROUNDS.filter(r=>r.from.slice(5,7)==pad(m)||r.to.slice(5,7)==pad(m)), nxt=ROUNDS.find(r=>r.from>iso(days));
 const r=mine[0]||nxt, lab=mine[0]?`Round ${pad(r.n)} · This month`:(r?(r.n==1?'Season opens':'Next round')+` · Round ${pad(r.n)}`:'Season complete');
 return `<div class="pg st"><div class="ph" style="background-image:url(file://${DIR}/${p.img});background-position:${p.pos}"></div><div class="phs"></div>
<div class="top"><span class="lab">SRS <span class="red">/</span> 2027</span><span class="lab">Photo · Aninder Singh / Paragliding Atlas</span></div>
<div class="num">${pad(m)}</div><div class="name">${MN[m-1]}</div><div class="yr"><i></i><span class="lab">2027</span></div>
<div class="cap"><b>${p.cap}</b><span class="lab">${p.sub}</span></div>
<div class="row" style="grid-template-columns:repeat(${days},1fr)">${h}${c}</div>
<div class="ft"><span class="lab">${pad(m)} / 12</span>${r?`<span class="r"><span class="lab red">${lab}</span><span class="p">${r.place}, ${r.country}</span><span class="t">${span(r)}</span></span>`:`<span class="lab">${lab}</span>`}</div></div>`}
function tower(p){const y=2027,m=p.m,days=new Date(Date.UTC(y,m,0)).getUTCDate(),WD=['SUN','MON','TUE','WED','THU','FRI','SAT'];
 const iso=n=>`${y}-${pad(m)}-${pad(n)}`, rOf=n=>ROUNDS.find(r=>iso(n)>=r.from&&iso(n)<=r.to);let rows='';
 for(let n=1;n<=days;n++){const wd=new Date(Date.UTC(y,m-1,n)).getUTCDay(),r=rOf(n);rows+=`<div class="r${wd==0||wd==6?' we':''}${r?' rc':''}"><b>${pad(n)}</b><i>${WD[wd]}</i><u>${r?(iso(n)==r.from?'R'+pad(r.n):iso(n)==r.to?'END':''):''}</u></div>`}
 const mine=ROUNDS.filter(r=>r.from.slice(5,7)==pad(m)||r.to.slice(5,7)==pad(m)), nxt=ROUNDS.find(r=>r.from>iso(days)), r=mine[0]||nxt;
 const rb=r?`<div class="rb"><span class="tag">${mine[0]?'':'NEXT · '}ROUND ${pad(r.n)}</span><div class="p">${r.place}</div><div class="c">${r.country} · ${span(r)}</div><div class="s lab">${r.status}</div></div>`:'';
 return `<div class="pg tw"><div class="ph" style="background-image:url(file://${DIR}/${p.img});background-position:${p.pos}"></div><div class="phs"></div>
<div class="twr" style="--rh:${((210-12-8.5-10)/days).toFixed(3)}mm"><div class="hd"><span class="lab">SRS <span class="red">/</span> 2027</span><span class="lab">${pad(m)}/12</span></div>${rows}</div>
${rb}<div class="num">${pad(m)}</div><div class="name">${MN[m-1]}</div><div class="yr"><i></i><span class="lab">2027</span></div>
<div class="cap"><b>${p.cap}</b><span class="lab">${p.sub}</span><span class="lab">Photo · Aninder Singh / Paragliding Atlas</span></div></div>`}
function depth(p){const y=2027,m=p.m,first=new Date(Date.UTC(y,m-1,1)),days=new Date(Date.UTC(y,m,0)).getUTCDate(),off=(first.getUTCDay()+6)%7,rows=Math.ceil((off+days)/7);
 const iso=n=>`${y}-${pad(m)}-${pad(n)}`, rOf=n=>ROUNDS.find(r=>iso(n)>=r.from&&iso(n)<=r.to);
 let cells=['MON','TUE','WED','THU','FRI','SAT','SUN'].map(h=>`<div class="h">${h}</div>`).join('')+'<div></div>'.repeat(off);
 for(let n=1;n<=days;n++){const col=(off+n-1)%7,r=rOf(n);let c='c'+(col>4?' we':'');if(r){c+=' rc';if(iso(n)==r.from||col==0||n==1)c+=' f';if(iso(n)==r.to||col==6||n==days)c+=' l'}cells+=`<div class="${c}">${n}</div>`}
 const mine=ROUNDS.filter(r=>r.from.slice(5,7)==pad(m)||r.to.slice(5,7)==pad(m)), nxt=ROUNDS.find(r=>r.from>iso(days)), r=mine[0]||nxt;
 const lab=mine[0]?`Round ${pad(r.n)} · This month`:(r?`Next round · Round ${pad(r.n)}`:'Season complete');
 const bgs=f=>`background-image:url(file://${DIR}/${f});background-position:${p.pos}`;
 return `<div class="pg dp"><div class="ph" style="${bgs(p.img)}"></div><div class="phs"></div>
<div class="name" style="--fs:${(1180/MN[m-1].length/ (MN[m-1].length>6?0.74:0.72)/4.2).toFixed(1)}mm">${MN[m-1]}</div><div class="cut" style="${bgs(p.cut)}"></div>
<div class="top"><span class="lab">SRS <span class="red">/</span> 2027</span><span class="lab">${pad(m)} / 12</span></div>
<div class="cap"><b>${p.cap}</b><span class="lab">${p.sub}</span><span class="lab">Photo · Aninder Singh / Paragliding Atlas</span></div>
<div class="card"><div class="hd"><span class="lab">${MN[m-1]} 2027</span><span class="lab red">${r&&mine[0]?'Race month':''}</span></div><div class="gr" style="--rh:${rows>5?8.4:9.6}mm">${cells}</div>
${r?`<div class="ft"><div><div class="lab red">${lab}</div><div class="p">${r.place}</div><div class="c">${r.country}</div></div><div><div class="t">${span(r)}</div><div class="s">${r.status}</div></div></div>`:''}</div></div>`}
(async()=>{const only=process.argv.slice(2);const b=await chromium.launch({args:['--allow-file-access-from-files']});
 const pg=await b.newPage({viewport:{width:1123,height:794},deviceScaleFactor:3});const all=[];
 for(const p of PAGES){const body=p.type=='cover'?cover(p):p.type=='strip'?strip(p):p.type=='tower'?tower(p):p.type=='depth'?depth(p):month(p);all.push(body);if(only.length&&!only.includes(p.file))continue;
  const f=`${DIR}/${p.file}.html`;fs.writeFileSync(f,`<!doctype html><meta charset="utf-8"><style>${CSS}</style>${body}`);
  await pg.goto('file://'+f);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);
  await pg.screenshot({path:`${OUT}/${p.file}.png`,clip:{x:0,y:0,width:1122.5,height:793.7}})}
 const f=`${DIR}/all.html`;fs.writeFileSync(f,`<!doctype html><meta charset="utf-8"><style>${CSS}html,body{height:auto;overflow:visible}.pg{break-after:page}</style>${all.join('')}`);
 await pg.goto('file://'+f);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);
 await pg.pdf({path:`${OUT}/SRS-2027-Calendar-draft.pdf`,width:'297mm',height:'210mm',printBackground:true,preferCSSPageSize:true});
 await b.close()})();
