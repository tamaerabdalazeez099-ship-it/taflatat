from flask import Flask, request, jsonify, send_file, Response
import yt_dlp, uuid, json
app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>تفلتات - تامر ود الدروشاب</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#050505;color:#fff}
.top{display:flex;justify-content:space-between;padding:12px 15px}
.top img{width:55px;border-radius:5px}
.hero{text-align:center;padding:5px 15px 15px}
.hero h1{font-size:80px;color:#FFD700;text-shadow:0 0 20px #FFD700,0 0 40px #FF8C00;line-height:1}
.hero .stars{color:#FFD700;font-size:18px}
.king{margin:18px 14px;background:#fff;border:2px solid #FFD700;border-radius:15px;padding:20px;text-align:center;box-shadow:0 0 20px #FFD70055}
.king .crown{font-size:38px}
.king b{font-size:30px;color:#000;display:block}
.king span{color:#8B6508;font-size:15px}
.search{margin:0 14px;background:#111;border:2px solid #FFD700;border-radius:18px;padding:16px}
.search input{width:100%;padding:16px;border-radius:14px;border:2px solid #FFD700;background:#000;color:#fff;font-size:18px;text-align:center;outline:none}
.btn{width:100%;padding:15px;border:none;border-radius:14px;font-size:18px;font-weight:900;margin-top:10px;cursor:pointer}
.btn-gold{background:linear-gradient(#FFD700,#FF8C00);color:#000}
.types{display:flex;gap:7px;overflow-x:auto;padding:12px 0}
.types button{white-space:nowrap;padding:11px 14px;border-radius:30px;border:1px solid #FFD700;background:#000;color:#FFD700;font-weight:900;cursor:pointer}
.types button.active{background:#FFD700;color:#000}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:14px}
.card{background:#111;border:1px solid #FFD70088;border-radius:16px;overflow:hidden}
.card img{width:100%;height:130px;object-fit:cover}
.card .t{padding:10px}
.card .t h3{color:#fff;font-size:14px;line-height:1.4;min-height:40px}
.card .t p{color:#aaa;font-size:12px;margin-top:4px}
.card .btns{display:flex;gap:6px;padding:0 10px 10px}
.card .btns button{flex:1;padding:10px;border-radius:10px;border:none;font-weight:900;cursor:pointer;font-size:14px}
.bottom{position:sticky;bottom:0;background:#000;border-top:1px solid #FFD700;display:flex;justify-content:space-around;padding:12px 0}
.bottom div{text-align:center;color:#FFD700;font-size:13px}
.bottom div span{font-size:24px;display:block}
.footer{text-align:center;padding:15px;color:#FFD700;font-size:13px}
video,audio{width:100%;border-radius:12px;margin-top:10px}
</style>
</head>
<body>
<div class="top"><img src="https://flagcdn.com/w80/sd.png"><img src="https://flagcdn.com/w80/sd.png"></div>
<div class="hero"><div class="stars">✦ ✦ ✦</div><h1>تفلتات</h1><div style="color:#FFD700">✦ ✦ ✦</div></div>
<div class="king"><div class="crown">👑</div><b>تامر ود الدروشاب</b><span>مطور ومصمم المحتوى • الحساب الملكي</span></div>
<div class="search">
<input id="searchText" placeholder="🔍 اكتب اسم أي حاجة">
<div class="types" id="types">
<button data-type="video" class="active" onclick="setType('video')">▶️ فيديو</button>
<button data-type="song" onclick="setType('song')">🎵 اغاني</button>
<button data-type="image" onclick="setType('image')">🖼️ صور</button>
<button data-type="game" onclick="setType('game')">🎮 العاب</button>
<button data-type="movie" onclick="setType('movie')">🎬 افلام</button>
<button data-type="quran" onclick="setType('quran')">🌙 قرآن</button>
</div>
<button class="btn btn-gold" onclick="searchAll()">🔍 ابحث طوالي - بدون رابط</button>
<div id="player"></div>
<div id="result"></div>
</div>
<div id="home" class="grid"></div>
<div class="footer">💎 صنع بفخر • نهر النيل • الخرطوم • تامر ود الدروشاب 💎</div>
<div class="bottom"><div><span>🏠</span>الرئيسية</div><div><span>📚</span>المكتبة</div><div><span>⬇️</span>التحميلات</div><div><span>⚙️</span>الاعدادات</div></div>
<script>
var curType='video';
function setType(t){curType=t;document.querySelectorAll('#types button').forEach(function(b){b.classList.remove('active')});document.querySelector('[data-type="'+t+'"]').classList.add('active');}
function quickType(t,q){setType(t);document.getElementById('searchText').value=q;searchAll();}
async function searchAll(){
  var q=document.getElementById('searchText').value;
  if(!q){alert('اكتب الاسم اول يا ملك');return;}
  document.getElementById('result').innerHTML='<p style="text-align:center;padding:20px">⏳ بنجيب ليك '+q+'...</p>';
  if(curType=='image'){
    var html='<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px">';
    for(var i=0;i<6;i++){var url='https://picsum.photos/seed/'+encodeURIComponent(q)+i+'/600/400';html+='<div onclick="window.open(\\''+url+'\\')"><img src="'+url+'" style="width:100%;height:130px;object-fit:cover;border-radius:12px;border:1px solid #FFD700"><p style="text-align:center;color:#FFD700">⬇️ تنزيل</p></div>';}
    html+='</div>';document.getElementById('result').innerHTML=html;return;
  }
  var query=q;
  if(curType=='song') query=q+' اغنية';
  if(curType=='game') query=q+' gameplay';
  if(curType=='movie') query=q+' فيلم كامل';
  if(curType=='quran') query='قرآن '+q;
  var r=await fetch('/api/search?q='+encodeURIComponent(query));
  var d=await r.json();
  var html='<h3 style="color:#FFD700;padding:10px">🔥 النتائج:</h3><div class="grid">';
  d.results.forEach(function(v){
    html+='<div class="card"><img src="'+v.thumb+'"><div class="t"><h3>'+v.title+'</h3><p>'+v.uploader+'</p></div><div class="btns"><button style="background:#FFD700" onclick="playId(\\''+v.id+'\\')">⬇️ تنزيل</button><button style="background:#000;color:#FFD700;border:1px solid #FFD700" onclick="playId(\\''+v.id+'\\')">▶️ شاهد</button></div></div>';
  });
  html+='</div>';document.getElementById('result').innerHTML=html;
}
async function playId(id){
  document.getElementById('player').innerHTML='<p style="text-align:center">⏳ جاري التشغيل...</p>';
  var r=await fetch('/api/info?url=https://www.youtube.com/watch?v='+id);
  var d=await r.json();
  if(curType=='song'){document.getElementById('player').innerHTML='<h3 style="color:#FFD700;padding:10px">'+d.title+'</h3><audio controls autoplay src="'+d.video_url+'"></audio>';}
  else{document.getElementById('player').innerHTML='<h3 style="color:#FFD700;padding:10px">'+d.title+'</h3><video controls autoplay src="'+d.video_url+'"></video><button class="btn btn-gold" onclick="window.open(\\'/api/download?url=https://www.youtube.com/watch?v='+id+'\\')">⬇️ تنزيل</button>';}
  window.scrollTo({top:200,behavior:'smooth'});
}
document.getElementById('searchText').addEventListener('keypress',function(e){if(e.key=='Enter') searchAll();});
// محتوى جاهز زي الصورة
document.getElementById('home').innerHTML = `
<div class="card"><img src="https://images.unsplash.com/photo-1547234935-80c7145ec969?w=600"><div class="t"><h3>ليالي النيل - جولة ليلية 04:12</h3></div><div class="btns"><button style="background:#FFD700" onclick="quickType('video','ليالي النيل')">⬇️ تنزيل</button><button style="background:#000;color:#FFD700;border:1px solid #FFD700" onclick="quickType('video','ليالي النيل')">▶️ شاهد</button></div></div>
<div class="card"><img src="https://images.unsplash.com/photo-1512632578888-169bbbc64f33?w=600"><div class="t"><h3>أناشيد وطنية - سوداني 03:37</h3></div><div class="btns"><button style="background:#FFD700" onclick="quickType('video','اناشيد سودانية')">⬇️ تنزيل</button><button style="background:#000;color:#FFD700;border:1px solid #FFD700" onclick="quickType('video','اناشيد سودانية')">▶️ شاهد</button></div></div>
<div class="card"><img src="https://images.unsplash.com/photo-1585036156171-384164a8c675?w=600"><div class="t"><h3>تلاوة قرآن - سورة الملك 06:25</h3></div><div class="btns"><button style="background:#FFD700" onclick="quickType('quran','سورة الملك')">⬇️ تنزيل</button><button style="background:#000;color:#FFD700;border:1px solid #FFD700" onclick="quickType('quran','سورة الملك')">▶️ شاهد</button></div></div>
<div class="card"><img src="https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=600"><div class="t"><h3>كوميديا سودانية - مقطع مضحك 02:19</h3></div><div class="btns"><button style="background:#FFD700" onclick="quickType('video','كوميديا سودانية')">⬇️ تنزيل</button><button style="background:#000;color:#FFD700;border:1px solid #FFD700" onclick="quickType('video','كوميديا سودانية')">▶️ شاهد</button></div></div>
`;
</script>
</body>
</html>
"""
MANIFEST = {"name":"تفلتات","short_name":"تفلتات","start_url":"/","display":"standalone","background_color":"#000000","theme_color":"#FFD700","icons":[{"src":"https://via.placeholder.com/192x192/FFD700/000000?text=T","sizes":"192x192","type":"image/png"}]}
@app.route("/")
def home(): return PAGE
@app.route("/manifest.json")
def manifest(): return Response(json.dumps(MANIFEST), mimetype="application/json")
@app.route("/api/search")
def search():
    q=request.args.get("q","")
    try:
        with yt_dlp.YoutubeDL({"quiet":True,"noplaylist":True,"extract_flat":True}) as y:
            d=y.extract_info(f"ytsearch12:{q}", download=False)
            res=[]
            for e in d.get("entries",[])[:12]:
                th=e.get("thumbnails") or []
                thumb=th[-1].get("url","") if th else ""
                res.append({"id":e.get("id"),"title":e.get("title"),"thumb":thumb,"uploader":e.get("uploader") or "تفلتات"})
            return jsonify({"results":res})
    except Exception as e: return jsonify({"error":str(e)}),400
@app.route("/api/info")
def info():
    url=request.args.get("url","")
    try:
        with yt_dlp.YoutubeDL({"quiet":True,"noplaylist":True}) as y:
            d=y.extract_info(url, download=False)
            fmt=d.get("url")
            if not fmt and d.get("formats"): fmt=d["formats"][-1]["url"]
            return jsonify({"title":d.get("title","فيديو"),"video_url":fmt})
    except Exception as e: return jsonify({"error":str(e)}),400
@app.route("/api/download")
def download():
    url=request.args.get("url","")
    fid=str(uuid.uuid4())[:8]
    path=f"/tmp/{fid}.mp4"
    try:
        with yt_dlp.YoutubeDL({"outtmpl":path,"format":"best[ext=mp4]/best","quiet":True}) as y: y.download([url])
        return send_file(path, as_attachment=True, download_name=f"tafltat-{fid}.mp4")
    except Exception as e: return f"خطأ: {e}",400
if __name__=="__main__": app.run(host="0.0.0.0", port=10000)
  
