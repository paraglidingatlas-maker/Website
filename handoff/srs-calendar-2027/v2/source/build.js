// SRS 2027 calendar page builder. Pages are data; add a month by adding an entry to PAGES.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const DIR=__dirname, OUT=__dirname+'/out';
const ROUNDS=[
 {n:1,place:'Lijak',country:'Slovenia',code:'SVN',from:'2027-03-15',to:'2027-03-21',status:'Confirmed'},
 {n:2,place:'St Jean Montclar',country:'France',code:'FRA',from:'2027-06-20',to:'2027-06-27',status:'Provisional'},
 {n:3,place:'Gemona',country:'Italy',code:'ITA',from:'2027-07-17',to:'2027-07-24',status:'Confirmed'},
 {n:4,place:'Krushevo',country:'North Macedonia',code:'MKD',from:'2027-08-22',to:'2027-08-29',status:'Confirmed'},
 {n:5,place:'St André',country:'France',code:'FRA',from:'2027-09-12',to:'2027-09-19',status:'Confirmed'},
];
const PAGES=[
 {file:'01-cover',type:'coverF',img:'t6_138_d.jpg',size:'392mm auto',pos:'65% 80%',cap:'Tapalpa, Mexico · SRS 2026 · Task 6'},
 {file:'02-january',type:'quiet',m:1,img:'t6_66_sd.jpg',size:'297mm auto',pos:'0 -6mm',t:{x:12,y:149,w:150,max:30},c:{x:12,y:24},
  sh:'linear-gradient(90deg,rgba(20,21,25,.72) 0%,rgba(20,21,25,.3) 34%,rgba(20,21,25,0) 52%),linear-gradient(180deg,rgba(20,21,25,.4) 0%,rgba(20,21,25,0) 14%,rgba(20,21,25,0) 62%,rgba(20,21,25,.9) 90%,#141519 100%)',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 6'},
 {file:'03-february',type:'quiet',m:2,img:'t6_100_nat.jpg',size:'297mm auto',pos:'0 0',t:{x:12,y:24,w:118,max:26},c:{x:12,y:104},
  sh:'linear-gradient(90deg,rgba(20,21,25,.93) 0%,rgba(20,21,25,.84) 32%,rgba(20,21,25,0) 58%),linear-gradient(180deg,rgba(20,21,25,.7) 0%,rgba(20,21,25,0) 18%,rgba(20,21,25,0) 70%,rgba(20,21,25,.92) 91%,#141519 100%)',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 6'},
 {file:'04-march',type:'fan',m:3,head:'tr',hw:100,img:'t6_t454_sd.jpg',size:'auto 175mm',pos:'0 0',
  sh:'linear-gradient(270deg,#141519 0,#141519 50mm,rgba(20,21,25,.5) 96mm,rgba(20,21,25,0) 150mm),linear-gradient(180deg,rgba(20,21,25,.3) 0%,rgba(20,21,25,0) 14%,rgba(20,21,25,0) 84%,#141519 100%)',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 4',capL:true},
 {file:'05-april',type:'fan',m:4,head:'tl',hw:88,img:'t6_t494_fx.jpg',size:'262mm auto',pos:'35mm 0',
  sh:'linear-gradient(90deg,#141519 0,#141519 37mm,rgba(20,21,25,.55) 80mm,rgba(20,21,25,0) 150mm),linear-gradient(180deg,rgba(20,21,25,.35) 0%,rgba(20,21,25,0) 16%,rgba(20,21,25,0) 80%,#141519 100%)',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 4'},
 {file:'06-may',type:'fan',m:5,head:'tl',hw:92,img:'t6_t4152_nat.jpg',size:'297mm auto',pos:'0 -18mm',
  sh:'linear-gradient(180deg,rgba(20,21,25,.55) 0%,rgba(20,21,25,0) 30%,rgba(20,21,25,0) 80%,#141519 100%),linear-gradient(90deg,rgba(20,21,25,.55) 0%,rgba(20,21,25,0) 40%)',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 4'},
 {file:'07-june',type:'fan',m:6,img:'t6_t4118_night.jpg',size:'297mm auto',pos:'0 -5mm',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 4'},
 {file:'08-july',type:'fan',m:7,head:'tl',hw:104,img:'t6_t345_sd.jpg',size:'auto 175mm',pos:'43.2mm 0',
  sh:'linear-gradient(90deg,#141519 0,#141519 43mm,rgba(20,21,25,0) 124mm),linear-gradient(180deg,rgba(20,21,25,.3) 0%,rgba(20,21,25,0) 14%,rgba(20,21,25,0) 84%,#141519 100%)',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 3',capV:true},
 {file:'09-august',type:'depthrow',m:8,img:'t6_t357_depth.jpg',cut:'t6_t357_cut.png',size:'297mm auto',pos:'0 0',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 3'},
 {file:'10-september',type:'lightrow',m:9,img:'t6_t376_day.jpg',pos:'50% 8%',cap:'Tapalpa, Mexico',sub:'SRS 2026 · Task 3'},
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
/* light: a gallery print on paper, ink type */
.lt{background:#f6f4f4;color:#141519}
.lt .lab{color:#5c5d63}
.lt .ph{position:absolute;left:12mm;right:12mm;top:12mm;height:126mm;background-size:cover}
.lt .cap{position:absolute;left:17mm;top:127mm;color:#f6f4f4;font:600 2.5mm/1 "DM Sans";letter-spacing:.3em;text-transform:uppercase;text-shadow:0 0 2mm rgba(20,21,25,.5)}
.lt .cr{position:absolute;right:17mm;top:127mm;color:#f6f4f4;font:500 2.5mm/1 "DM Sans";letter-spacing:.3em;text-transform:uppercase;text-shadow:0 0 2mm rgba(20,21,25,.5)}
.lt .hd{position:absolute;left:12mm;top:147mm;display:flex;gap:6mm;align-items:center}
.lt .hd i{width:9mm;height:.5mm;background:#e8112d}
.lt .name{position:absolute;left:11mm;top:153mm;font:800 var(--fs)/1 Poppins;letter-spacing:-.03em;text-transform:uppercase;white-space:nowrap}
.lt .rd{position:absolute;left:12mm;bottom:12mm;display:flex;align-items:baseline;gap:5mm}
.lt .rd .tag{font:800 2.9mm/1 Poppins;letter-spacing:.14em;background:#e8112d;color:#fff;padding:1.7mm 3mm;transform:skewX(-12deg)}
.lt .rd .p{font:700 5.2mm/1 Poppins;text-transform:uppercase}
.lt .rd .t{font:600 3.2mm/1 Poppins;letter-spacing:.14em}
.lt .gr{position:absolute;right:12mm;top:146mm;width:104mm;display:grid;grid-template-columns:repeat(7,1fr);isolation:isolate}
.lt .gr .h{font:600 1.9mm/1 "DM Sans";letter-spacing:.22em;color:#77767c;text-align:center;padding-bottom:2.4mm;border-bottom:.3mm solid #141519;margin-bottom:.8mm}
.lt .gr .c{position:relative;height:var(--rh);display:flex;align-items:center;justify-content:center;font:500 3.9mm/1 Poppins;font-variant-numeric:tabular-nums}
.lt .gr .c.we{color:#9a999e}.lt .gr .c.rc{color:#fff;font-weight:700}
.lt .gr .c.rc::before{content:"";position:absolute;inset:.8mm 0;background:#e8112d;z-index:-1}
.lt .gr .c.rc.f::before{left:1mm;border-radius:1mm 0 0 1mm}.lt .gr .c.rc.l::before{right:1mm;border-radius:0 1mm 1mm 0}
/* ===== designer F: the season line, the round as the headline ===== */
.lb{font:500 2.4mm/1 "DM Sans";letter-spacing:.2em;text-transform:uppercase;color:#b9b8bd;white-space:nowrap}
.tagf{display:inline-block;font:800 3.3mm/1 Poppins;letter-spacing:.14em;background:#e8112d;color:#fff;padding:2mm 3.4mm;transform:skewX(-12deg)}
.pvc{display:inline-block;font:700 2.4mm/1 "DM Sans";letter-spacing:.2em;text-transform:uppercase;color:#fff;padding:1.5mm 2.6mm;box-shadow:0 0 0 .3mm #e8112d inset;background:repeating-linear-gradient(135deg,rgba(232,17,45,.6) 0 .45mm,rgba(20,21,25,.55) .45mm 1.25mm)}
/* the season line: the year at scale, every round at its real dates */
.sln{position:absolute;height:8mm}
.sln .ax{position:absolute;left:0;right:0;top:0;height:.25mm;background:rgba(246,244,244,.32)}
.sln .ax::after{content:"";position:absolute;right:0;top:0;width:.25mm;height:2mm;background:rgba(246,244,244,.32)}
.sln .m{position:absolute;top:0;height:2mm;border-left:.25mm solid rgba(246,244,244,.32)}
.sln .m u{position:absolute;left:1.2mm;top:2.7mm;text-decoration:none;font:500 2.2mm/1 "DM Sans";letter-spacing:.16em;color:#77767c}
.sln .m.on u{color:#f6f4f4;font-weight:700}
.sln .m.on::before{content:"";position:absolute;left:-.25mm;right:0;top:-.3mm;height:.85mm;background:#f6f4f4}
.sln .r{position:absolute;top:-1.1mm;height:2.45mm;background:#e8112d;z-index:1}
.sln .r.pv{background:repeating-linear-gradient(135deg,#e8112d 0 .4mm,#141519 .4mm 1mm);box-shadow:0 0 0 .3mm #e8112d inset}
.sln em{position:absolute;top:2.7mm;font:700 2.2mm/1 Poppins;font-style:normal;letter-spacing:.06em;color:#e8112d}
.sln .w{position:absolute;top:0;width:.2mm;height:1.2mm;background:rgba(246,244,244,.2)}
.sln.big .m{height:3.2mm}.sln.big .m u{top:4.4mm;font-size:2.5mm;color:#b9b8bd}
.sln.big .r{top:-1.7mm;height:3.65mm}
/* cover: the season at a glance */
.cf .ph{position:absolute;inset:0;background-repeat:no-repeat}
.cf .sh{position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,21,25,.82) 0%,rgba(20,21,25,.42) 30%,rgba(20,21,25,0) 52%),linear-gradient(180deg,rgba(20,21,25,.5) 0%,rgba(20,21,25,0) 20%,rgba(20,21,25,0) 55%,rgba(20,21,25,.9) 70%,#141519 85%)}
.cf .top{position:absolute;left:16mm;right:16mm;top:13mm;display:flex;justify-content:space-between}
.cf .ttl{position:absolute;left:15mm;top:27mm}
.cf .ttl .a{font:800 45mm/.84 Poppins;letter-spacing:-.035em}
.cf .ttl .b{font:500 45mm/.84 Poppins;letter-spacing:-.045em;margin-left:-.6mm}
.cf .ttl .c{margin-top:8mm;margin-left:1mm;display:flex;align-items:center;gap:5mm}
.cf .ttl .c i{width:14mm;height:.5mm;background:#e8112d}
.cf .ttl .c span{font:600 4mm/1 Poppins;letter-spacing:.4em;text-transform:uppercase}
.cf .ttl .d{margin:5mm 0 0 20mm}
.cf .fl{position:absolute;left:16mm;bottom:21mm;width:265mm;height:0}
.cf .fl>div{position:absolute;bottom:0;border-left:.25mm solid rgba(246,244,244,.5);padding:0 0 5mm 2.4mm;white-space:nowrap}
.cf .fl>div.hi{padding-bottom:27.5mm}
.cf .fl .n{font:700 2.7mm/1 Poppins;letter-spacing:.12em;color:#e8112d}
.cf .fl .p{font:800 4.7mm/1.04 Poppins;text-transform:uppercase;margin-top:1.7mm;letter-spacing:-.005em}
.cf .fl .t{font:600 3.3mm/1 Poppins;letter-spacing:.08em;margin-top:1.9mm;font-variant-numeric:tabular-nums}
.cf .fl .c{font:400 2.5mm/1 "DM Sans";color:#b9b8bd;margin-top:1.7mm}
.cf .fl .c b{font-weight:600;color:#ff5a6e}
.cf .lg{position:absolute;right:16mm;bottom:26mm;text-align:right}
.cf .lg div{display:flex;justify-content:flex-end;align-items:center;gap:2.4mm;margin-top:2.2mm}
.cf .lg i{display:inline-block;width:6mm;height:2.6mm;background:#e8112d}
.cf .lg i.pv{background:repeating-linear-gradient(135deg,#e8112d 0 .4mm,#141519 .4mm 1mm);box-shadow:0 0 0 .3mm #e8112d inset}
.cf .ftr{position:absolute;left:16mm;right:16mm;bottom:6mm;display:flex;justify-content:space-between}.cf .ftr .lb{font-size:2.2mm;letter-spacing:.14em;text-transform:none;color:#8d8c92}
.cf .sc{position:absolute;left:16mm;bottom:26mm;color:#8d8c92;line-height:1.7;white-space:normal;width:44mm}
/* round poster: the place is the headline, the wing flies in front of it */
.rp .ph,.rp .cut{position:absolute;inset:0;background-repeat:no-repeat}
.rp .cut{filter:drop-shadow(0 2.2mm 2.6mm rgba(0,0,0,.5))}
.rp .sh{position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,21,25,.6) 0%,rgba(20,21,25,0) 46%),linear-gradient(180deg,rgba(20,21,25,.4) 0%,rgba(20,21,25,0) 16%,rgba(20,21,25,0) 80%,rgba(20,21,25,.92) 93%,#141519 100%)}
.rp .big{position:absolute;left:12mm;top:8mm;font:800 var(--fs)/1 Poppins;letter-spacing:-.03em;text-transform:uppercase;white-space:nowrap;margin-left:-.045em}
.rp .top{position:absolute;left:12mm;right:12mm;top:9.5mm;display:flex;justify-content:space-between}
.rp .fx{position:absolute;left:12.6mm;top:98mm;display:flex;align-items:center;gap:5mm}
.rp .fx .co{font:600 3.8mm/1 Poppins;letter-spacing:.2em;text-transform:uppercase}
.rp .dt{position:absolute;left:12mm;top:108.5mm;font:700 12.5mm/1 Poppins;letter-spacing:-.01em;font-variant-numeric:tabular-nums;white-space:nowrap}
.rp .cal{position:absolute;left:12mm;top:128.5mm;width:98mm}
.mh{display:flex;align-items:baseline;gap:3.4mm;padding-bottom:3.2mm;border-bottom:.25mm solid rgba(246,244,244,.3)}
.mh b{font:800 8.6mm/1 Poppins;text-transform:uppercase;letter-spacing:-.01em}
.mh span{font:500 3.2mm/1 Poppins;letter-spacing:.2em;color:#b9b8bd}
.grf{display:grid;grid-template-columns:repeat(7,1fr);isolation:isolate;margin-top:2.6mm}
.grf .h{font:500 2.2mm/1 "DM Sans";letter-spacing:.18em;color:#8d8c92;text-align:center;padding-bottom:1.6mm}
.grf .c{position:relative;height:var(--rh);display:flex;align-items:center;justify-content:center;font:500 4.5mm/1 Poppins;font-variant-numeric:tabular-nums}
.grf .c.we{color:#8d8c92}.grf .c.rc{color:#fff;font-weight:700}
.grf .c.rc::before{content:"";position:absolute;inset:.9mm 0;background:#e8112d;z-index:-1}
.grf .c.rc.f::before{left:.8mm;border-radius:.9mm 0 0 .9mm}.grf .c.rc.l::before{right:.8mm;border-radius:0 .9mm .9mm 0}
.grf.pv .c.rc::before{background:repeating-linear-gradient(135deg,rgba(232,17,45,.5) 0 .35mm,rgba(232,17,45,.1) .35mm 1.25mm);border-top:.3mm solid #e8112d;border-bottom:.3mm solid #e8112d}
.grf.pv .c.rc.f::before{border-left:.3mm solid #e8112d}.grf.pv .c.rc.l::before{border-right:.3mm solid #e8112d}
.rp .cap{position:absolute;right:12mm;top:185mm;text-align:right}
.rp .cap .lb{display:block}.rp .cap .lb+.lb{margin-top:2.2mm;color:#8d8c92}
.rp .sln{left:12mm;top:199.2mm}
/* fan: the month's days in one row, opened out of the season line */
.fs .ph{position:absolute;left:0;right:0;top:0;height:175mm;background-repeat:no-repeat}
.fs .sh{position:absolute;left:0;right:0;top:0;height:175mm;background:linear-gradient(180deg,rgba(20,21,25,.5) 0%,rgba(20,21,25,0) 16%),radial-gradient(120% 90% at 0% 100%,rgba(20,21,25,.78) 0%,rgba(20,21,25,.45) 38%,rgba(20,21,25,0) 62%)}
.fs .top{position:absolute;left:12mm;right:12mm;top:9.5mm;display:flex;justify-content:space-between}
.fs .fx{position:absolute;left:12.6mm;top:117.5mm;display:flex;align-items:center;gap:5mm}
.fs .fx .co{font:600 3.8mm/1 Poppins;letter-spacing:.2em;text-transform:uppercase}
.fs .fx .dt{font:700 6mm/1 Poppins;font-variant-numeric:tabular-nums;white-space:nowrap}
.fs .big{position:absolute;left:12mm;top:127.5mm;font:800 var(--fs)/.9 Poppins;letter-spacing:-.03em;text-transform:uppercase;white-space:nowrap;margin-left:-.045em}
.fs .mn{position:absolute;left:12mm;top:180.4mm}
.fs .mn b{display:block;font:800 var(--fs)/1 Poppins;text-transform:uppercase;letter-spacing:-.015em}
.fs .mn .lb{display:block;margin-top:2.2mm}
.fs .row{position:absolute;left:52mm;right:12mm;top:178.8mm;display:grid;isolation:isolate;border-bottom:.25mm solid rgba(246,244,244,.32)}
.fs .row .h{font:500 2.2mm/1 "DM Sans";letter-spacing:.1em;color:#8d8c92;text-align:center;padding-bottom:1.5mm}
.fs .row .c{position:relative;height:9mm;display:flex;align-items:center;justify-content:center;font:500 4.4mm/1 Poppins;font-variant-numeric:tabular-nums}
.fs .row .mo{box-shadow:-.25mm 0 0 rgba(246,244,244,.32)}
.fs .row .c.we,.fs .row .h.we{color:#8d8c92}.fs .row .h.we{color:#6f6e74}
.fs .row .c.rc{color:#fff;font-weight:700}
.fs .row .c.rc::before{content:"";position:absolute;inset:1.1mm 0;background:#e8112d;z-index:-1}
.fs .row.pv .c.rc::before{background:repeating-linear-gradient(135deg,rgba(232,17,45,.5) 0 .35mm,rgba(232,17,45,.1) .35mm 1.25mm);border-top:.3mm solid #e8112d;border-bottom:.3mm solid #e8112d}
.fs .row.pv .c.rc.f::before{border-left:.3mm solid #e8112d}.fs .row.pv .c.rc.l::before{border-right:.3mm solid #e8112d}
.fs svg{position:absolute;left:0;top:191.75mm;width:297mm;height:7.45mm}
.fs .sln{left:12mm;top:199.2mm}
/* ===== v2: the three designers combined ===== */
.tagn{display:inline-block;font:800 3.3mm/1 Poppins;letter-spacing:.14em;color:#f6f4f4;padding:2mm 3.4mm;transform:skewX(-12deg);box-shadow:0 0 0 .3mm rgba(246,244,244,.75) inset;white-space:nowrap}
.cr2{color:#8d8c92}
.capl{position:absolute;right:12mm;top:160mm;text-align:right}.capl .lb{display:block}.capl .lb+.lb{margin-top:2.2mm;color:#8d8c92}
.capv{position:absolute;right:5.5mm;top:12mm;writing-mode:vertical-rl}
/* quiet month: the month is the headline, the calendar sits in the photo's own dark */
.qm .ph{position:absolute;inset:0;background-repeat:no-repeat}
.qm .sh{position:absolute;inset:0}
.qm .top{position:absolute;left:12mm;right:12mm;top:9.5mm;display:flex;justify-content:space-between}
.qm .ttl{position:absolute;font:800 var(--fs)/1 Poppins;letter-spacing:-.03em;text-transform:uppercase;white-space:nowrap;margin-left:-.045em}
.qm .yr{position:absolute;display:flex;align-items:center;gap:3.5mm}
.qm .yr i{width:9mm;height:.5mm;background:rgba(246,244,244,.55)}
.qm .yr span{font:500 3.2mm/1 Poppins;letter-spacing:.2em;color:#b9b8bd}
.qm .cal{position:absolute;width:98mm}
.qm .cal .grf{margin-top:0}
.qm .nx{margin-top:3.6mm;padding-top:4.6mm;border-top:.25mm solid rgba(246,244,244,.3);display:flex;align-items:center;gap:4mm}
.qm .nx .pl{font:700 4.6mm/1 Poppins;text-transform:uppercase;white-space:nowrap}
.qm .nx .dt{margin-left:auto;font:600 3.3mm/1 Poppins;letter-spacing:.08em;white-space:nowrap}
.qm .cap{position:absolute;right:12mm;top:185mm;text-align:right}
.qm .cap .lb{display:block}.qm .cap .lb+.lb{margin-top:2.2mm;color:#8d8c92}
.qm .sln{left:12mm;top:199.2mm}
/* depth row: the month set into the landscape behind the wing, the round on a plate, the days on one line */
.fs.dr .ph,.fs.dr .cut{position:absolute;left:0;right:0;top:0;height:198mm;background-repeat:no-repeat}
.fs.dr .sh{height:198mm;background:linear-gradient(180deg,rgba(20,21,25,.35) 0%,rgba(20,21,25,0) 18%,rgba(20,21,25,0) 58%,rgba(20,21,25,.8) 74%,#141519 89%)}
.dr .name{position:absolute;left:9mm;right:9mm;top:17mm;font:800 var(--fs)/.8 Poppins;letter-spacing:-.03em;text-transform:uppercase;text-align:center;white-space:nowrap}
.dr .plate{position:absolute;right:12mm;top:145.5mm;border-left:.6mm solid #e8112d;padding:1mm 0 1mm 4.4mm}
.dr .plate .hd{display:flex;gap:4mm;align-items:center}
.dr .plate .n{font:700 2.7mm/1 Poppins;letter-spacing:.14em;color:#e8112d}
.dr .plate .p{font:800 10mm/1 Poppins;text-transform:uppercase;letter-spacing:-.01em;margin-top:2.6mm;white-space:nowrap}
.dr .plate .c{font:400 3.3mm/1 "DM Sans";color:#d5d4d8;margin-top:2.2mm}
.dr .plate .t{font:700 4.2mm/1 Poppins;letter-spacing:.06em;margin-top:2.8mm;white-space:nowrap}
/* light row: a gallery print on paper, ink type */
.fs.lt2{background:#f6f4f4;color:#141519}
.lt2 .lb{color:#5c5d63}
.fs.lt2 .ph{left:12mm;right:12mm;top:12mm;height:119mm;background-size:cover}
.fs.lt2 .sh{display:none}
.lt2 .pc{position:absolute;top:124mm;color:#f6f4f4;font:600 2.4mm/1 "DM Sans";letter-spacing:.2em;text-transform:uppercase;text-shadow:0 0 2mm rgba(20,21,25,.55)}
.lt2 .fx .co,.lt2 .fx .dt{color:#141519}
.fs.lt2 .row{border-bottom-color:rgba(20,21,25,.45)}
.fs.lt2 .row .h{color:#77767c}.fs.lt2 .row .c.we{color:#9a999e}.fs.lt2 .row .h.we{color:#a5a4a9}
.fs.lt2 .row .c.rc{color:#fff}
.fs.lt2 .row .mo{box-shadow:-.25mm 0 0 rgba(20,21,25,.35)}
.lt2 svg{color:#141519}.fs svg{color:#f6f4f4}
.lt2 .sln .ax,.lt2 .sln .ax::after{background:rgba(20,21,25,.4)}
.lt2 .sln .m{border-left-color:rgba(20,21,25,.4)}.lt2 .sln .m u{color:#8d8c92}
.lt2 .sln .m.on u{color:#141519}.lt2 .sln .m.on::before{background:#141519}
.lt2 .sln .r.pv{background:repeating-linear-gradient(135deg,#e8112d 0 .4mm,#f6f4f4 .4mm 1mm)}
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
function light(p){const y=2027,m=p.m,first=new Date(Date.UTC(y,m-1,1)),days=new Date(Date.UTC(y,m,0)).getUTCDate(),off=(first.getUTCDay()+6)%7,rows=Math.ceil((off+days)/7);
 const iso=n=>`${y}-${pad(m)}-${pad(n)}`, rOf=n=>ROUNDS.find(r=>iso(n)>=r.from&&iso(n)<=r.to);
 let cells=['MON','TUE','WED','THU','FRI','SAT','SUN'].map(h=>`<div class="h">${h}</div>`).join('')+'<div></div>'.repeat(off);
 for(let n=1;n<=days;n++){const col=(off+n-1)%7,r=rOf(n);let c='c'+(col>4?' we':'');if(r){c+=' rc';if(iso(n)==r.from||col==0||n==1)c+=' f';if(iso(n)==r.to||col==6||n==days)c+=' l'}cells+=`<div class="${c}">${n}</div>`}
 const mine=ROUNDS.filter(r=>r.from.slice(5,7)==pad(m)||r.to.slice(5,7)==pad(m)), nxt=ROUNDS.find(r=>r.from>iso(days)), r=mine[0]||nxt;
 const L=MN[m-1].length, fs=Math.min(26,150/(L*0.69));
 return `<div class="pg lt"><div class="ph" style="background-image:url(file://${DIR}/${p.img});background-position:${p.pos}"></div>
<div class="cap">${p.cap} · ${p.sub}</div><div class="cr">Photo · Aninder Singh / Paragliding Atlas</div>
<div class="hd"><span class="lab">SRS <span class="red">/</span> 2027</span><i></i><span class="lab">${pad(m)} / 12</span></div>
<div class="name" style="--fs:${fs.toFixed(1)}mm">${MN[m-1]}</div>
${r?`<div class="rd"><span class="tag">${mine[0]?'':'NEXT · '}ROUND ${pad(r.n)}</span><span class="p">${r.place}, ${r.country}</span><span class="t">${span(r)}</span><span class="lab">${r.status}</span></div>`:`<div class="rd"><span class="lab">Season complete</span></div>`}
<div class="gr" style="--rh:${rows>5?7.4:8.8}mm">${cells}</div></div>`}

// ---------- designer F ----------
const DOY=x=>Math.round((d(x)-d('2027-01-01'))/864e5), EMW={};   // EMW: measured width of a word in em (Poppins 800, -.03em)
const fit=(t,mm,max)=>Math.min(max||999,mm/(EMW[t.toUpperCase()]||t.length*.68));
const bgf=(p,f)=>`background-image:url(file://${DIR}/${f});background-size:${p.size};background-position:${p.pos}`;
const rinfo=m=>{const iso=`2027-${pad(m)}-`,mine=ROUNDS.filter(r=>r.from.slice(5,7)==pad(m)||r.to.slice(5,7)==pad(m)),nxt=ROUNDS.find(r=>r.from>iso+'31');return{r:mine[0]||nxt,here:!!mine[0]}};
function sline(W,cur,big){const k=W/365;let h='';
 for(let i=0;i<12;i++){const a=DOY(`2027-${pad(i+1)}-01`),n=new Date(Date.UTC(2027,i+1,0)).getUTCDate();
  h+=`<span class="m${cur==i+1?' on':''}" style="left:${(a*k).toFixed(2)}mm;width:${(n*k).toFixed(2)}mm"><u>${MS[i]}</u></span>`}
 if(big)for(let x=3;x<365;x+=7)h+=`<span class="w" style="left:${(x*k).toFixed(2)}mm"></span>`;      // 4 Jan 2027 is the first Monday
 for(const r of ROUNDS){const a=DOY(r.from),n=DOY(r.to)-a+1;
  h+=`<span class="r${r.status=='Provisional'?' pv':''}" style="left:${(a*k).toFixed(2)}mm;width:${(n*k).toFixed(2)}mm"></span>`+(big?'':`<em style="left:${(a*k).toFixed(2)}mm">R${pad(r.n)}</em>`)}
 return `<div class="sln${big?' big':''}" style="width:${W}mm"><i class="ax"></i>${h}</div>`}
function gridF(m,rh){const y=2027,first=new Date(Date.UTC(y,m-1,1)),days=new Date(Date.UTC(y,m,0)).getUTCDate(),off=(first.getUTCDay()+6)%7,rows=Math.ceil((off+days)/7);
 const iso=n=>`${y}-${pad(m)}-${pad(n)}`, rOf=n=>ROUNDS.find(r=>iso(n)>=r.from&&iso(n)<=r.to);let pv=false;
 let cells=['MON','TUE','WED','THU','FRI','SAT','SUN'].map(h=>`<div class="h">${h}</div>`).join('')+'<div></div>'.repeat(off);
 for(let n=1;n<=days;n++){const col=(off+n-1)%7,r=rOf(n);let c='c'+(col>4?' we':'');if(r){pv=pv||r.status=='Provisional';c+=' rc';if(iso(n)==r.from||col==0||n==1)c+=' f';if(iso(n)==r.to||col==6||n==days)c+=' l'}cells+=`<div class="${c}">${n}</div>`}
 return `<div class="grf${pv?' pv':''}" style="--rh:${rows>5?rh*5/6:rh}mm">${cells}</div>`}
function coverF(p){const W=265,k=W/365;
 const fl=ROUNDS.map((r,i)=>{const nm=r.place.length>12?r.place.replace(/ (?=\S+$)/,'<br>'):r.place;
  return `<div class="${i%2?'hi':''}" style="left:${(DOY(r.from)*k).toFixed(2)}mm"><div class="n">R${pad(r.n)}</div><div class="p">${nm}</div><div class="t">${span(r)}</div><div class="c">${r.country} · ${r.status=='Provisional'?'<b>Provisional</b>':r.status}</div></div>`}).join('');
 return `<div class="pg cf"><div class="ph" style="${bgf(p,p.img)}"></div><div class="sh"></div>
<div class="top"><span class="lb">Sports-Class Racing Series</span></div>
<div class="ttl"><div class="a">SRS</div><div class="b">2027</div><div class="c"><i></i><span>Race Calendar</span></div><div class="d lb">${ROUNDS.length} rounds · ${span({from:ROUNDS[0].from,to:ROUNDS[ROUNDS.length-1].to})}</div><div class="d lb cr2" style="margin-top:9mm">Photographed at ${p.cap}</div><div class="d lb cr2" style="margin-top:2.2mm">${CREDIT}</div></div>
<div class="fl">${fl}</div>
<div class="sc lb">The year at scale<br>One tick, one week</div>
<div class="lg"><div><span class="lb">Confirmed</span><i></i></div><div><span class="lb">Provisional</span><i class="pv"></i></div></div><div class="ftr"><span class="lb">paraglidingatlas.com</span><span class="lb">Dates: sportsracingseries.org/events</span></div>
<div style="position:absolute;left:16mm;top:189mm">${sline(W,0,true)}</div></div>`}
function round(p){const m=p.m,{r,here}=rinfo(m),pv=r.status=='Provisional';
 return `<div class="pg rp"><div class="ph" style="${bgf(p,p.img)}"></div><div class="sh"></div>
<div class="big" style="--fs:${fit(r.place,273,100).toFixed(1)}mm">${r.place}</div><div class="cut" style="${bgf(p,p.cut)}"></div>
<div class="top"><span class="lb">SRS <span class="red">/</span> 2027 &nbsp;·&nbsp; Race Calendar</span><span class="lb">${CREDIT}</span></div>
<div class="fx"><span class="tagf">ROUND ${pad(r.n)}</span><span class="co">${r.country}</span>${pv?'<span class="pvc">Provisional</span>':'<span class="lb">Confirmed</span>'}</div>
<div class="dt">${span(r)}</div>
<div class="cal"><div class="mh"><b>${MN[m-1]}</b><span>2027</span></div>${gridF(m,9.3)}</div>
<div class="cap"><span class="lb">Photographed at ${p.cap} · ${p.sub}</span></div>
${sline(273,m)}</div>`}
const CREDIT='Photo · Aninder Singh / Paragliding Atlas';
function nextLab(r,here){return here?`ROUND ${pad(r.n)}`:(r.n==1?'SEASON OPENS':'NEXT')+` · ROUND ${pad(r.n)}`}
function statusTag(r){return r.status=='Provisional'?'<span class="pvc">Provisional</span>':'<span class="lb">Confirmed</span>'}
// the month's days on one line, opened out of the season line (designer F); a round that crosses a week stays one bar (designer D)
function rowBlock(m,label){const y=2027,days=new Date(Date.UTC(y,m,0)).getUTCDate(),WD=['SUN','MON','TUE','WED','THU','FRI','SAT'],{r,here}=rinfo(m),pv=here&&r.status=='Provisional';
 const iso=n=>`${y}-${pad(m)}-${pad(n)}`, rOf=n=>ROUNDS.find(q=>iso(n)>=q.from&&iso(n)<=q.to);let h='',c='';
 for(let n=1;n<=days;n++){const wd=new Date(Date.UTC(y,m-1,n)).getUTCDay(),we=wd==0||wd==6,q=rOf(n),mo=wd==1&&n>1?' mo':'';
  h+=`<div class="h${we?' we':''}${mo}">${WD[wd]}</div>`;c+=`<div class="c${we?' we':''}${mo}${q?' rc'+(iso(n)==q.from||n==1?' f':'')+(iso(n)==q.to||n==days?' l':''):''}">${n}</div>`}
 const k=273/365,xa=(12+DOY(iso(1))*k).toFixed(2),xb=(12+(DOY(iso(days))+1)*k).toFixed(2);
 return `<div class="mn"><b style="--fs:${Math.min(9.6,36/(label.length*.7)).toFixed(1)}mm">${label}</b><span class="lb">${label==MN[m-1]?'2027':MN[m-1]}</span></div>
<div class="row${pv?' pv':''}" style="grid-template-columns:repeat(${days},1fr)">${h}${c}</div>
<svg viewBox="0 0 297 8" preserveAspectRatio="none"><defs><linearGradient id="fg${m}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".09"/><stop offset="1" stop-color="currentColor" stop-opacity=".02"/></linearGradient></defs>
<polygon points="52,0 285,0 ${xb},8 ${xa},8" fill="url(#fg${m})"/><path d="M52 0L${xa} 8M285 0L${xb} 8" stroke="currentColor" stroke-opacity=".34" stroke-width=".25" fill="none"/></svg>
${sline(273,m)}`}
function headline(m,hw,max2,max1){const {r,here}=rinfo(m);if(!here)return{lines:[MN[m-1]],fs:fit(MN[m-1],hw,max1)};
 const words=r.place.split(' '),cutAt=Math.ceil(words.length/2),lines=r.place.length>10?[words.slice(0,cutAt).join(' '),words.slice(cutAt).join(' ')]:[r.place];
 return{lines,fs:Math.min(...lines.map(t=>fit(t,hw,lines.length>1?max2:max1)))}}
function fxRow(m){const {r,here}=rinfo(m);if(!r)return '<span class="lb">Season complete</span>';
 return here?`<span class="tagf">ROUND ${pad(r.n)}</span><span class="co">${r.country}</span><span class="dt">${span(r)}</span>${statusTag(r)}`
  :`<span class="tagn">${nextLab(r,false)}</span><span class="co">${r.place}, ${r.country}</span><span class="dt">${span(r)}</span>${statusTag(r)}`}
function fan(p){const m=p.m,{r,here}=rinfo(m),tl=p.head=='tl',H=headline(m,p.hw||128,21,34),two=H.lines.length>1;
 const tr=p.head=='tr', fxTop=tl||tr?23:(two?120:126.5), bigTop=tl||tr?32.5:(two?130:136.5), side=tr?'left:auto;right:12mm;':'';
 return `<div class="pg fs"><div class="ph" style="${bgf(p,p.img)}"></div><div class="sh"${p.sh?` style="background:${p.sh}"`:''}></div>
<div class="top"><span class="lb">SRS <span class="red">/</span> 2027 &nbsp;·&nbsp; Race Calendar</span>${p.capV||p.capL?'':`<span class="lb">Photographed at ${p.cap} · ${p.sub} &nbsp;·&nbsp; ${CREDIT}</span>`}</div>${p.capL?`<div class="capl"><span class="lb">Photographed at ${p.cap} · ${p.sub}</span><span class="lb">${CREDIT}</span></div>`:''}${p.capV?`<div class="capv lb">${p.cap} · ${p.sub} &nbsp;·&nbsp; ${CREDIT}</div>`:''}
<div class="fx" style="${side}top:${fxTop}mm">${fxRow(m)}</div>
<div class="big" style="${side}${tr?'text-align:right;':''}--fs:${H.fs.toFixed(1)}mm;top:${bigTop}mm">${H.lines.join('<br>')}</div>
${rowBlock(m,here?MN[m-1]:'2027')}</div>`}
function depthrow(p){const m=p.m,{r,here}=rinfo(m);
 return `<div class="pg fs dr"><div class="ph" style="${bgf(p,p.img)}"></div><div class="sh"></div>
<div class="name" style="--fs:${fit(MN[m-1],279).toFixed(1)}mm">${MN[m-1]}</div><div class="cut" style="${bgf(p,p.cut)}"></div>
<div class="top"><span class="lb">SRS <span class="red">/</span> 2027 &nbsp;·&nbsp; Race Calendar</span><span class="lb">Photographed at ${p.cap} · ${p.sub} &nbsp;·&nbsp; ${CREDIT}</span></div>
${r?`<div class="plate"><div class="hd"><span class="n">${nextLab(r,here)} / ${pad(ROUNDS.length)}</span>${statusTag(r)}</div><div class="p">${r.place}</div><div class="c">${r.country}</div><div class="t">${span(r)}</div></div>`:''}
${rowBlock(m,'2027')}</div>`}
function lightrow(p){const m=p.m,{r,here}=rinfo(m),H=headline(m,150,22,22);
 return `<div class="pg fs lt2"><div class="ph" style="background-image:url(file://${DIR}/${p.img});background-position:${p.pos}"></div>
<div class="pc" style="left:17mm">Photographed at ${p.cap} · ${p.sub}</div><div class="pc" style="right:17mm">${CREDIT}</div>
<div class="fx" style="top:137mm">${fxRow(m)}</div>
<div class="big" style="--fs:${H.fs.toFixed(1)}mm;top:148.5mm">${H.lines.join('<br>')}</div>
${rowBlock(m,here?MN[m-1]:'2027')}</div>`}
function quiet(p){const m=p.m,{r,here}=rinfo(m),fs=fit(MN[m-1],p.t.w,p.t.max);
 return `<div class="pg qm"><div class="ph" style="${bgf(p,p.img)}"></div><div class="sh" style="background:${p.sh}"></div>
<div class="top"><span class="lb">SRS <span class="red">/</span> 2027 &nbsp;·&nbsp; Race Calendar</span><span class="lb">${CREDIT}</span></div>
<div class="ttl" style="left:${p.t.x}mm;top:${p.t.y}mm;--fs:${fs.toFixed(1)}mm">${MN[m-1]}</div>
<div class="yr" style="left:${p.t.x+.6}mm;top:${(p.t.y+fs+3).toFixed(1)}mm"><i></i><span>2027</span></div>
<div class="cal" style="left:${p.c.x}mm;top:${p.c.y}mm">${gridF(m,9.3)}
${r?`<div class="nx"><span class="tagn">${nextLab(r,here)}</span><span class="pl">${r.place}</span><span class="dt">${span(r)}</span></div>`:''}</div>
<div class="cap"><span class="lb">Photographed at ${p.cap} · ${p.sub}</span></div>
${sline(273,m)}</div>`}

(async()=>{const only=process.argv.slice(2);const b=await chromium.launch({args:['--allow-file-access-from-files']});
 const pg=await b.newPage({viewport:{width:1123,height:794},deviceScaleFactor:3});const all=[];
 const words=[...new Set(ROUNDS.flatMap(r=>[r.place,...r.place.split(' '),...r.place.split(' ').map((_,i,a)=>a.slice(0,i+1).join(' ')),...r.place.split(' ').map((_,i,a)=>a.slice(i).join(' '))]).concat(MN).map(x=>x.toUpperCase()))];
 fs.writeFileSync(`${DIR}/measure.html`,`<!doctype html><meta charset="utf-8"><style>${CSS}</style><body><span style="font:800 20px Poppins">ÉA</span>`);await pg.goto('file://'+DIR+'/measure.html');await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(200);
 Object.assign(EMW,await pg.evaluate(ws=>{const o={};for(const w of ws){const e=document.createElement('span');e.style.cssText='font:800 100px Poppins;letter-spacing:-.03em;white-space:nowrap;position:absolute';e.textContent=w;document.body.appendChild(e);o[w]=e.getBoundingClientRect().width/100;e.remove()}return o},words));
 for(const p of PAGES){const body=p.type=='coverF'?coverF(p):p.type=='round'?round(p):p.type=='fan'?fan(p):p.type=='quiet'?quiet(p):p.type=='depthrow'?depthrow(p):p.type=='lightrow'?lightrow(p):p.type=='cover'?cover(p):p.type=='strip'?strip(p):p.type=='tower'?tower(p):p.type=='depth'?depth(p):p.type=='light'?light(p):month(p);all.push(body);if(only.length&&!only.includes(p.file))continue;
  const f=`${DIR}/${p.file}.html`;fs.writeFileSync(f,`<!doctype html><meta charset="utf-8"><style>${CSS}</style>${body}`);
  await pg.goto('file://'+f);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);
  await pg.screenshot({path:`${OUT}/${p.file}.png`,clip:{x:0,y:0,width:1122.5,height:793.7}})}
 const f=`${DIR}/all.html`;fs.writeFileSync(f,`<!doctype html><meta charset="utf-8"><style>${CSS}html,body{height:auto;overflow:visible}.pg{break-after:page}</style>${all.join('')}`);
 await pg.goto('file://'+f);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);
 await pg.pdf({path:`${OUT}/SRS-2027-Calendar-draft.pdf`,width:'297mm',height:'210mm',printBackground:true,preferCSSPageSize:true});
 await b.close()})();
