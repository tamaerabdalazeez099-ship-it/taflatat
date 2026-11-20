from flask import Flask, request, jsonify, send_file
import yt_dlp, uuid
app = Flask(__name__)
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>تفلتات | تامر ود الدروشاب</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#000;color:#fff}
#splash{position:fixed;inset:0;z-index:999;background:radial-gradient(circle,#FFD700,#FF8C00,#000);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;animation:fade 3.5s forwards}
#splash h1{font-size:75px;color:#000;text-shadow:0 0 20px #fff}
#splash p{font-size:23px;color:#fff;background:#000;padding:12px 22px;border-radius:30px;margin-top:15px;font-weight:bold}
@keyframes fade{0%,80%{opacity:1}100%{opacity:0;visibility:hidden}}
.top{background:linear-gradient(135deg,#FFD700,#FF6B00,#FFD700);padding:25px 15px 35px;text-align:center;border-radius:0 0 30px 30px}
.top h1{font-size:60px;color:#000}
.top .name{font-size:29px;font-weight:900;color:#000;background:#fff;padding:9px 22px;border-radius:15px;display:inline-block;margin-top:8px;box-shadow:0 5px 15px #0005}
.top p{margin-top:10px;color:#000;font-weight:bold}
.box{margin:-20px 15px 15px;background:#111;border:2px solid #FFD700;border-radius:25px;padding:20px}
input{width:100%;padding:16px;border-radius:15px;border:2px solid #FFD700;font-size:17px;text-align:center;outline:none;margin-top:10px}
.btn{width:100%;padding:15px;border:none;border-radius:15px;font-size:19px;font-weight:900;margin-top:12px;cursor:pointer}
.btn-play{background:linear-gradient(#FFD700,#FF8C00);color:#000}
.btn-dl{background:#fff;color:#000}
.btn-search{background:#FFD700;color:#000}
.cats{display:flex;gap:8px;overflow-x:auto;padding:10px 0}
.cats button{white-space:nowrap;padding:12px 18px;border-radius:30px;border:2px solid #FFD700;background:#000;color:#FFD700;font-weight:bold;cursor:pointer;font-size:16px}
.cats button.active{background:#FFD700;color:#000}
.card{background:#1a1a1a;border:1px solid #FFD70088;border-radius:20px;padding:15px;margin:15px;cursor:pointer}
.card img{width:100%;border-radius:15px}
.card h3{margin:10px 0;color:#FFD700;font-size:16px}
.card p{color:#aaa;font-size:14px}
.card .actions{display:flex;gap:8px;margin-top:10px}
.card .actions button{flex:1;padding:10px;border-radius:12px;border:none;font-weight:bold;cursor:pointer}
.footer{background:linear-gradient(#FFD700,#FF8C00);color:#000;text-align:center;padding:25px;margin-top:20px;border-radius:30px 30px 0 0}
.footer b{font-size:27px}
video{width:100%;border-radius:15px;margin-top:10px}
.tabs{display:flex;gap:10px}
.tabs button{flex:1;padding:12px;border-radius:12px;border:2px solid #FFD700;background:#000;color:#FFD700;font-weight:bold;cursor:pointer}
.tabs button.active{background:#FFD700;color:#000}
.section-title{color:#FFD700;margin:15px 15px 0;font-size:22px}
</style>
</head>
<body>
<div id="splash">
<h1>تفلتات 🔥</h1>
<h2 style="color:#000">TAFLTAT</h2>
<p>تامر ود الدروشاب ❤️🇸🇩</p>
<p style="background:transparent;color:#000;font-size:16px">فخر السودان - أقوى تطبيق في السودان</p>
</div>

<div class="top">
<div style="background:#000;color:#FFD700;padding:6px 18px;border-radius:30px;display:inline-block;font-weight:bold">🇸🇩 فخر السودان 🇸🇩</div>
<h1>تفلتات</h1>
<div class="name">تامر ود الدروشاب 👑</div>
<p>اكتب اسم الفيديو أو الصق الرابط - شاهد طوالي</p>
</div>

<div class="box">
<div class="tabs">
<button id="tab-search" class="active" onclick="showTab('search')">🔍 بحث بالاسم</button>
<button id="tab-link" onclick="showTab('link')">🔗 بالرابط</button>
</div>
<div id="tab1">
<input id="searchText" placeholder="🔍 اكتب اسم الفيديو... مثلا: حفلة تفلتات">
<button class="btn btn-search" onclick="searchVideo()">🔍 ابحث وشاهد طوالي</button>
</div>
<div id="tab2" style="display:none">
<input id="url" placeholder="🔗 الصق الرابط هنا...">
<button class="btn btn-play" onclick="playLink()">▶️ شغل الرابط</button>
<button class="btn btn-dl" onclick="dl()">⬇️ تنزيل الفيديو</button>
</div>
<div id="player"></div>
<div id="result"></div>
</div>

<h2 class="section-title">🔥 اختار قسمك المفضل:</h2>
<div class="cats">
<button onclick="quick('اغاني سودانية جديدة')">🎵 أغاني سودانية</button>
<button onclick="quick('حفلات سودانية')">🎤 حفلات</button>
<button onclick="quick('كورة سودانية')">⚽ كورة</button>
<button onclick="quick('مضحك سوداني')">😂 مضحك</button>
<button onclick="quick('ترند السودان اليوم')">🔥 ترند اليوم</button>
<button onclick="quick('طبخ سوداني')">🍲 طبخ</button>
<button onclick="showFav()">❤️ المفضلة</button>
</div>

<div id="homeList"></div>

<div class="footer">
<b>تفلتات - تامر ود الدروشاب 👑</b>
<p>صنع بحب في السودان 🇸🇩 | © 2026</p>
<p>شارك التطبيق مع أصحابك ❤️</p>
<button onclick="shareApp()" style="background:#000;color:#FFD700;padding:12px 25px;border:none;border-radius:30px;font-weight:bold;margin-top:10px;font-size:17px;cursor:pointer">📤 شارك التطبيق</button>
</div>

<script>
let favs = JSON.parse(localStorage.getItem('fav')||'[]');
function showTab(t){
 document.getElementById('tab1').style.display = t=='search'?'block':'none';
 document.getElementById('tab2').style.display = t=='link'?'block':'none';
 document.getElementById('tab-search').className = t=='search'?'active':'';
 document.getElementById('tab-link').className = t=='link'?'active':'';
}
function quick(q){
 document.getElementById('searchText').value=q;
 showTab('search');
 searchVideo();
 window.scrollTo({top:200,behavior:'smooth'});
}
async function searchVideo(){
 let q=document.getElementById('searchText').value;
 if(!q) return alert('اكتب اسم الفيديو أول!');
 document.getElementById('result').innerHTML='<p style="text-align:center;padding:20px">⏳ جاري البحث... ثواني يا ملك 👑</p>';
 let r=await fetch('/api/search?q='+encodeURIComponent(q));
 let d=await r.json();
 if(!d.results || d.results.length==0) return document.getElementById('result').innerHTML='<p>❌ ما لقيت، جرب اسم تاني</p>';
 let html='<h3 style="color:#FFD700;margin:15px 0">🔥 النتائج - دوس على أي فيديو:</h3>';
 d.results.forEach(v=>{
  html+=`<div class="card"><div onclick="playId('${v.id}')"><img src="${v.thumb}"><h3>${v.title}</h3><p>${v.uploader} • ${v.duration}</p></div><div class="actions"><button style="background:#FFD700" onclick="playId('${v.id}')">▶️ شاهد</button><button style="background:#fff" onclick="addFav('${v.id}','${v.title.replace(/'/g,'')}','${v.thumb}')">❤️ مفضلة</button><button style="background:#25D366;color:#fff" onclick="shareVideo('${v.id}','${v.title.replace(/'/g,'')}')">📤 مشاركة</button></div></div>`;
 });
 document.getElementById('result').innerHTML=html;
}
async function playId(id){
 document.getElementById('player').innerHTML='<p style="text-align:center;padding:20px">⏳ جاري التشغيل...</p>';
 window.scrollTo({top:0,behavior:'smooth'});
 let r=await fetch('/api/info?url=https://www.youtube.com/watch?v='+id);
 let d=await r.json();
 document.getElementById('player').innerHTML=`<h3 style="color:#FFD700;margin:15px 0">${d.title}</h3><video controls autoplay src="${d.video_url}"></video><button class="btn btn-dl" onclick="window.open('/api/download?url=https://www.youtube.com/watch?v=${id}')">⬇️ تنزيل الفيديو دا</button><button class="btn btn-play" onclick="shareVideo('${id}','${d.title.replace(/'/g,'')}')">📤 شارك الفيديو دا مع أصحابك</button>`;
}
async function playLink(){
 let u=document.getElementById('url').value;
 if(!u) return alert('الصق رابط أول!');
 document.getElementById('player').innerHTML='<p style="text-align:center">⏳ جاري التشغيل...</p>';
 let r=await fetch('/api/info?url='+encodeURIComponent(u));
 let d=await r.json();
 if(d.error) return document.getElementById('player').innerHTML='<p>❌ الرابط ما اشتغل</p>';
 document.getElementById('player').innerHTML=`<h3 style="color:#FFD700">${d.title}</h3><video controls autoplay src="${d.video_url}"></video>`;
}
function dl(){
 let u=document.getElementById('url').value;
 if(!u) return alert('الصق رابط أول!');
 window.open('/api/download?url='+encodeURIComponent(u));
}
function addFav(id,title,thumb){
 if(favs.find(f=>f.id==id)) return alert('موجود في المفضلة أصلا ❤️');
 favs.push({id,title,thumb});
 localStorage.setItem('fav',JSON.stringify(favs));
 alert('تمت الإضافة للمفضلة ❤️');
}
function showFav(){
 if(favs.length==0) return alert('المفضلة فاضية، دوس ❤️ على أي فيديو');
 let html='<h3 style="color:#FFD700;margin:15px">❤️ فيديوهاتك المفضلة:</h3>';
 favs.forEach(v=>{
  html+=`<div class="card" onclick="playId('${v.id}')"><img src="${v.thumb}"><h3>${v.title}</h3></div>`;
 });
 document.getElementById('result').innerHTML=html;
 window.scrollTo({top:200,behavior:'smooth'});
}
function shareVideo(id,title){
 let text=`شوف الفيديو دا في تطبيق تفلتات - تامر ود الدروشاب 🔥\\n${title}\\nhttps://taflatat.onrender.com`;
 if(navigator.share) navigator.share({text});
 else {navigator.clipboard.writeText(text); alert('تم نسخ رابط المشاركة! الصقو لأصحابك 📤');}
}
function shareApp(){
 let text='يا فردة! 🔥🇸🇩 تطبيق تفلتات - تامر ود الدروشاب - أي فيديو تكتب اسمو يظهر ليك طوالي! جربو هسي 👇 https://taflatat.onrender.com';
 if(navigator.share) navigator.share({text});
 else {navigator.clipboard.writeText(text); alert('تم نسخ رسالة المشاركة!');}
}
document.getElementById('searchText').addEventListener('keypress',e=>{if(e.key=='Enter') searchVideo();});
// أول ما يفتح يجيب ترند
quick('ترند السودان اليوم');
</script>
</body>
</html>
"""
@app.route('/')
def home(): return HTML
@app.route('/api/search')
def search():
    q=request.args.get('q','')
    try:
        with yt_dlp.YoutubeDL({'quiet':True,'noplaylist':True,'extract_flat':True}) as y:
            d=y.extract_info(f"ytsearch10:{q}", download=False)
            res=[]
            for e in d.get('entries',[])[:10]:
                res.append({'id':e.get('id'),'title':e.get('title'),'thumb':e.get('thumbnails',[{}])[-1].get('url','') if e.get('thumbnails') else '','uploader':e.get('uploader') or e.get('channel') or 'تفلتات','duration':e.get('duration_string') or ''})
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
            return jsonify({'title':d.get('title','فيديو تفلتات'),'thumb':d.get('thumbnail',''),'uploader':d.get('uploader','تفلتات'),'video_url':fmt})
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
