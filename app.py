from flask import Flask, request, jsonify, send_file, Response
import yt_dlp, uuid, json
app = Flask(__name__)
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#000">
<link rel="manifest" href="/manifest.json">
<title>تفلتات | الملك تامر ود الدروشاب</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#000;color:#fff;min-height:100vh}
body:before{content:"";position:fixed;inset:0;z-index:-1;background:linear-gradient(180deg,#000,#1a1400,#000)}
#splash{position:fixed;inset:0;z-index:9999;background:radial-gradient(circle,#FFD700,#B8860B,#000);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;animation:splashOut 4s forwards}
#splash h1{font-size:90px;color:#000;text-shadow:0 0 20px #fff}
#splash .name{background:#000;color:#FFD700;padding:14px 30px;border-radius:50px;font-size:24px;font-weight:900;margin-top:10px;border:3px solid #FFD700}
@keyframes splashOut{0%,82%{opacity:1}100%{opacity:0;visibility:hidden}}
/* الهيدر الملكي */
.hero{padding:28px 15px 35px;text-align:center;background:linear-gradient(180deg,#000,#1a1400);border:3px solid #FFD700;border-radius:0 0 35px 35px;position:relative}
.hero:before{content:"💎 👑 💎";position:absolute;top:8px;left:0;right:0;font-size:18px;opacity:0.8}
.hero .flags{font-size:28px;margin-bottom:5px}
.hero h1{font-size:78px;color:#FFD700;line-height:0.9;text-shadow:0 0 25px #FFD700,0 0 50px #FF8C00;letter-spacing:2px}
.hero .en{color:#FFD700;letter-spacing:10px;font-size:18px;margin-top:5px}
/* صندوق الملك - زي الصورة */
.king-box{margin:18px auto 0;max-width:460px;background:linear-gradient(135deg,#fff,#FFEFD5,#fff);border:4px solid #FFD700;border-radius:22px;padding:20px;box-shadow:0 0 30px #FFD700,0 0 60px #FFD70055;position:relative}
.king-box:before{content:"💎";position:absolute;top:5px;left:8px;font-size:22px}
.king-box:after{content:"💎";position:absolute;top:5px;right:8px;font-size:22px}
.king-box .crown{font-size:48px}
.king-box b{font-size:32px;color:#000;display:block;margin-top:5px}
.king-box span{color:#8B6508;font-size:15px;font-weight:bold}
.king-box .line{color:#FFD700;margin-top:8px;font-size:18px}
/* بحث دهبي */
.search-box{margin:16px 14px;background:#111;border:3px solid #FFD700;border-radius:20px;padding:16px;box-shadow:0 0 20px #FFD70044}
.search-box h3{color:#FFD700;text-align:center}
input{width:100%;padding:16px;border-radius:14px;border:2px solid #FFD700;font-size:17px;text-align:center;margin-top:12px;background:#000;color:#fff;outline:none}
.btn{width:100%;padding:15px;border:none;border-radius:14px;font-size:18px;font-weight:900;margin-top:10px;cursor:pointer}
.btn-gold{background:linear-gradient(135deg,#FFD700,#FF8C00);color:#000;box-shadow:0 8px 20px #FFD70055}
.btn-white{background:#fff;color:#000}
.tabs{display:flex;gap:8px;margin-top:12px}
.tabs button{flex:1;padding:12px;border-radius:12px;border:2px solid #FFD700;background:#000;color:#FFD700;font-weight:bold;cursor:pointer}
.tabs button.active{background:#FFD700;color:#000}
/* خلفيات */
.bg-picker{background:#111;border:2px solid #FFD700;border-radius:20px;margin:0 14px;padding:14px;text-align:center}
.bg-picker b{color:#FFD700}
.bg-btns{display:flex;gap:8px;justify-content:center;margin-top:10px;flex-wrap:wrap}
.bg-btns button{padding:11px 14px;border-radius:14px;border:2px solid #fff;font-weight:900;cursor:pointer;color:#fff}
/* أقسام */
.all-title{color:#FFD700;margin:18px 15px 0;font-size:22px;text-align:center;text-shadow:0 0 15px #FFD700}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:14px}
.grid button{padding:18px 10px;border-radius:20px;border:2px solid #FFD700;background:linear-gradient(180deg,#1a1a1a,#000);color:#fff;font-weight:900;cursor:pointer;font-size:16px;box-shadow:0 5px 15px #000}
.grid button span{display:block;font-size:30px}
.grid button:hover{background:#FFD700;color:#000}
.cats{display:flex;gap:8px;overflow-x:auto;padding:0 14px 12px}
.cats button{white-space:nowrap;padding:12px 18px;border-radius:30px;border:2px solid #FFD700;background:#FFD700;color:#000;font-weight:900;cursor:pointer;box-shadow:0 0 15px #FFD70066}
.card{background:#1a1a1a;border:2px solid #FFD70088;border-radius:20px;padding:14px;margin:14px;cursor:pointer;box-shadow:0 10px 25px #000}
.card img{width:100%;border-radius:15px;border:1px solid #FFD700}
.card h3{color:#FFD700;margin:10px 0}
.card .actions{display:flex;gap:8px;margin-top:10px}
.card .actions button{flex:1;padding:11px;border-radius:12px;border:none;font-weight:900;cursor:pointer}
.footer{background:linear-gradient(180deg,#FFD700,#FF8C00);color:#000;text-align:center;padding:30px 15px;border-radius:35px 35px 0 0;border-top:4px solid #fff}
.footer b{font-size:29px}
video{width:100%;border-radius:15px;margin-top:10px}
</style>
</head>
<body>
<div id="splash">
<div style="font-size:55px">🇸🇩</div>
<div style="font-size:75px">👑</div>
<h1>تفلتات</h1>
<div class="name">تامر ود الدروشاب ❤️</div>
<p style="color:#fff;margin-top:12px;font-weight:bold">💎 النسخة الملكية 💎</p>
</div>

<div class="hero">
<div class="flags">🇸🇩 🇸🇩</div>
<h1>تفلتات</h1>
<div class="en">— TAFLTAT —</div>
<div class="king-box">
<div class="crown">👑</div>
<b>تامر ود الدروشاب</b>
<span>مالك التطبيق • مؤسس تفلتات</span>
<div class="line">✦ ✦ ✦</div>
</div>
<div style="margin-top:14px">
<button class="btn" style="background:#25D366;color:#fff" onclick="manualInstall()">📲 نزل التطبيق الملكي في تلفونك</button>
</div>
<div style="color:#FFD700;margin-top:10px;font-weight:bold">💎 صنع بفخر • نهر النيل • الخرطوم 💎</div>
</div>

<div class="bg-picker">
<b>🎨 اختار خلفية الملك على كيفك:</b>
<div class="bg-btns">
<button style="background:#000" onclick="setBG('black')">⬛ أسود ملكي</button>
<button style="background:#FFD700;color:#000" onclick="setBG('gold')">🟨 دهبي ملكي</button>
<button style="background:#007A3A" onclick="setBG('green')">🟩 أخضر السودان</button>
<button style="background:linear-gradient(135deg,#00f,#f0f)" onclick="setBG('neon')">🌈 ملون</button>
<button style="background:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400') center/cover" onclick="setBG('sea')">🌊 بحر</button>
</div>
</div>

<div class="search-box">
<h3>🔍 ابحث عن أي حاجة في الدنيا 👑</h3>
<div class="tabs">
<button id="tab-search" class="active" onclick="showTab('search')">🔍 بحث بالاسم</button>
<button id="tab-link" onclick="showTab('link')">🔗 بالرابط</button>
</div>
<div id="tab1">
<input id="searchText" placeholder="🔍 اكتب اسم الفيديو، أغنية، مباراة...">
<button class="btn btn-gold" onclick="searchVideo()">🔍 ابحث وشاهد طوالي</button>
</div>
<div id="tab2" style="display:none">
<input id="url" placeholder="🔗 الصق الرابط هنا">
<button class="btn btn-gold" onclick="playLink()">▶️ شغل الرابط</button>
<button class="btn btn-white" onclick="dl()">⬇️ تنزيل</button>
</div>
<div id="player"></div>
<div id="result"></div>
</div>

<h2 class="all-title">👑 اختار جوك يا ملك 👑</h2>
<div class="cats">
<button onclick="quick('اغاني سودانية')">🎵 الأغاني السودانية</button>
<button onclick="quick('كورة سودانية')">⚽ كرة القدم</button>
<button onclick="quick('مضحك سوداني')">😂 كوميديا</button>
</div>
<div class="grid">
<button onclick="quick('اغاني سودانية جديدة')"><span>🎵</span>أغاني سودانية</button>
<button onclick="quick('قرآن كريم')"><span>🕌</span>قرآن كريم</button>
<button onclick="quick('كورة سودانية الهلال المريخ')"><span>⚽</span>كورة سودانية</button>
<button onclick="quick('أخبار السودان اليوم')"><span>📰</span>أخبار السودان</button>
<button onclick="quick('مضحك سوداني')"><span>😂</span>ضحك سوداني</button>
<button onclick="quick('افلام سودانية')"><span>🎬</span>أفلام</button>
<button onclick="quick('طبخ سوداني')"><span>🍲</span>أكل سوداني</button>
<button onclick="showFav()"><span>❤️</span>المفضلة</button>
</div>

<div class="footer">
<b>تفلتات - تامر ود الدروشاب 👑</b>
<p style="font-weight:bold;margin-top:8px">💎 النسخة الملكية - فخر السودان 💎</p>
<p>الدروشاب • أم درمان • الخرطوم 🇸🇩</p>
<div style="background:#000;color:#FFD700;padding:12px;border-radius:20px;display:inline-block;margin-top:12px;font-weight:900">❤️ من السودان .. للسودان .. بالسودان ❤️</div>
</div>

<script>
let deferredPrompt=null;
window.addEventListener('beforeinstallprompt',(e)=>{e.preventDefault();deferredPrompt=e;});
function manualInstall(){if(deferredPrompt){deferredPrompt.prompt();}else{alert('دوس النقط الثلاثة ⋮ فوق، بعدين (إضافة إلى الشاشة الرئيسية)');}}
function setBG(type){
  if(type=='black') document.body.style.background='#000';
  if(type=='gold') document.body.style.background='linear-gradient(180deg,#FFD700,#000)';
  if(type=='green') document.body.style.background='linear-gradient(180deg,#007A3A,#000)';
  if(type=='neon') document.body.style.background='linear-gradient(135deg,#00f,#f0f,#ff0)';
  if(type=='sea') document.body.style.background="url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800') center/cover";
  alert('تم تغيير الخلفية يا ملك 👑✅');
}
let favs = JSON.parse(localStorage.getItem('fav')||'[]');
function showTab(t){document.getElementById('tab1').style.display=t=='search'?'block':'none';document.getElementById('tab2').style.display=t=='link'?'block':'none';document.getElementById('tab-search').className=t=='search'?'active':'';document.getElementById('tab-link').className=t=='link'?'active':'';}
function quick(q){document.getElementById('searchText').value=q;showTab('search');searchVideo();window.scrollTo({top:350,behavior:'smooth'});}
async function searchVideo(){let q=document.getElementById('searchText').value;if(!q) return alert('اكتب أي حاجة أول يا ملك!');document.getElementById('result').innerHTML='<p style="text-align:center;padding:20px">⏳ بنجيب ليك أحلى حاجة يا ملك 👑...</p>';let r=await fetch('/api/search?q='+encodeURIComponent(q));let d=await r.json();let html='<h3 style="color:#FFD700;margin:15px 0">🔥 النتائج:</h3>';d.results.forEach(v=>{html+=`<div class="card"><div onclick="playId('${v.id}')"><img src="${v.thumb}"><h3>${v.title}</h3><p>${v.uploader}</p></div><div class="actions"><button style="background:#FFD700" onclick="playId('${v.id}')">▶️ شاهد</button><button style="background:#fff" onclick="addFav('${v.id}','${v.title.replace(/'/g,'')}','${v.thumb}')">❤️ مفضلة</button></div></div>`;});document.getElementById('result').innerHTML=html;}
async function playId(id){document.getElementById('player').innerHTML='<p style="text-align:center">⏳ جاري التشغيل...</p>';window.scrollTo({top:0,behavior:'smooth'});let r=await fetch('/api/info?url=https://www.youtube.com/watch?v='+id);let d=await r.json();document.getElementById('player').innerHTML=`<h3 style="color:#FFD700">${d.title}</h3><video controls autoplay src="${d.video_url}"></video><button class="btn btn-white" onclick="window.open('/api/download?url=https://www.youtube.com/watch?v=${id}')">⬇️ تنزيل</button>`;}
async function playLink(){let u=document.getElementById('url').value;if(!u) return alert('الصق رابط أول!');let r=await fetch('/api/info?url='+encodeURIComponent(u));let d=await r.json();document.getElementById('player').innerHTML=`<h3>${d.title}</h3><video controls autoplay src="${d.video_url}"></video>`;}
function dl(){let u=document.getElementById('url').value;if(!u) return alert('الصق رابط أول!');window.open('/api/download?url='+encodeURIComponent(u));}
function addFav(id,title,thumb){if(favs.find(f=>f.id==id)) return alert('موجود ❤️');favs.push({id,title,thumb});localStorage.setItem('fav',JSON.stringify(favs));alert('تمت الإضافة ❤️');}
function showFav(){if(favs.length==0) return alert('المفضلة فاضية');let html='<h3 style="color:#FFD700;margin:15px">❤️ المفضلة:</h3>';favs.forEach(v=>{html+=`<div class="card" onclick="playId('${v.id}')"><img src="${v.thumb}"><h3>${v.title}</h3></div>`;});document.getElementById('result').innerHTML=html;}
document.getElementById('searchText').addEventListener('keypress',e=>{if(e.key=='Enter') searchVideo();});
quick('ترند السودان اليوم');
</script>
</body>
</html>
"""
MANIFEST = {"name":"تفلتات - تامر ود الدروشاب","short_name":"تفلتات","start_url":"/","display":"standalone","background_color":"#000000","theme_color":"#FFD700","icons":[{"src":"https://via.placeholder.com/192x192/FFD700/000000?text=T","sizes":"192x192","type":"image/png"},{"src":"https://via.placeholder.com/512x512/FFD700/000000?text=T","sizes":"512x512","type":"image/png"}]}
@app.route('/')
def home(): return HTML
@app.route('/manifest.json')
def manifest(): return Response(json.dumps(MANIFEST), mimetype='application/json')
@app.route('/api/search')
def search():
    q=request.args.get('q','')
    try:
        with yt_dlp.YoutubeDL({'quiet':True,'noplaylist':True,'extract_flat':True}) as y:
            d=y.extract_info(f"ytsearch10:{q}", download=False)
            res=[]
            for e in d.get('entries',[])[:10]:
                res.append({'id':e.get('id'),'title':e.get('title'),'thumb':e.get('thumbnails',[{}])[-1].get('url','') if e.get('thumbnails') else '','uploader':e.get('uploader') or 'تفلتات'})
            return jsonify({'results':res})
    except Exception as e: return jsonify({'error':str(e)}),400
@app.route('/api/info')
def info():
    url=request.args.get('url','')
    try:
        with yt_dlp.YoutubeDL({'quiet':True,'noplaylist':True}) as y:
            d=y.extract_info(url, download=False)
            fmt=d.get('url')
            if not fmt and d.get('formats'): fmt=d['formats'][-1]['url']
            return jsonify({'title':d.get('title','فيديو'),'video_url':fmt})
    except Exception as e: return jsonify({'error':str(e)}),400
@app.route('/api/download')
def download():
    url=request.args.get('url','')
    fid=str(uuid.uuid4())[:8]
    path=f"/tmp/{fid}.mp4"
    try:
        with yt_dlp.YoutubeDL({'outtmpl':path,'format':'best[ext=mp4]/best','quiet':True}) as y: y.download([url])
        return send_file(path, as_attachment=True, download_name=f"tafltat-{fid}.mp4")
    except Exception as e: return f"خطأ: {e}",400
if __name__=='__main__': app.run(host='0.0.0.0', port=10000)
