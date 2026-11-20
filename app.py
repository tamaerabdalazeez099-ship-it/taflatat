from flask import Flask, render_template_string, jsonify, request, redirect
import os
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تفلتات TAFLTAT</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family: Tahoma; }
body { background:#000; color:#fff; }
.phone { max-width:520px; margin:0 auto; background:#111; min-height:100vh; padding:12px; padding-bottom:90px; }

/* ===== الصورة الفوق - صورة السودان الشديدة ===== */
.hero {
  height: 250px;
  border-radius: 18px;
  overflow: hidden;
  position: relative;
  border: 3px solid #FFD700;
  background-image: url('https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1000&q=80');
  background-size: cover;
  background-position: center;
  margin-bottom: 5px;
}
.hero::after {
  content:''; position:absolute; inset:0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.15), rgba(0,0,0,0.75));
}
.hero-top-img {
  position:absolute; top:0; left:0; right:0; height:110px;
  background-image: url('https://images.unsplash.com/photo-1547235001-d703406d3f17?w=1000&q=80');
  background-size: cover; background-position: center;
  border-bottom: 3px solid #FFD700;
  z-index:1;
}
.hero-content { position:relative; z-index:2; text-align:center; padding-top:125px; }
.hero-content h1 { font-size:62px; color:#FFD700; line-height:1; text-shadow: 3px 3px 0 #D21034, 0 0 25px #FFD700; }
.hero-content h2 { font-size:36px; color:#fff; letter-spacing:3px; text-shadow:2px 2px 0 #000; }
.hero-content .flag { font-size:20px; margin-top:4px; }
.hero-content p { font-size:13px; margin-top:5px; color:#FFE680; font-weight:bold; text-shadow:1px 1px 0 #000; }

.sudan-bar { display:flex; height:8px; border-radius:10px; overflow:hidden; margin:12px 0; border:1px solid #FFD700; }
.sudan-bar div { flex:1; } .c1{background:#D21034} .c2{background:#fff} .c3{background:#000} .c4{background:#007A3D}
.search-box { background:#fff; margin:12px 0 8px; border-radius:14px; padding:14px; display:flex; gap:8px; align-items:center; border:3px solid #FFD700; }
.search-box input { background:transparent; border:none; outline:none; width:100%; font-size:17px; text-align:center; color:#000; font-weight:bold; }
.hint { text-align:center; color:#FFD700; font-size:13px; padding-bottom:8px; font-weight:bold; }
.btns { display:flex; gap:7px; overflow-x:auto; padding:5px 0 10px; }
.btns button { white-space:nowrap; background:#111; color:#FFD700; border:2px solid #FFD700; padding:11px 15px; border-radius:12px; font-weight:bold; cursor:pointer; }
.btns button.active { background:#FFD700; color:#000; }
.cards { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:5px; }
.card { background:#1a1a1a; border-radius:14px; overflow:hidden; border:2px solid #FFD700; }
.thumb { position:relative; }
.thumb img { width:100%; height:155px; object-fit:cover; display:block; }
.play { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:52px; height:52px; background:rgba(210,16,52,0.9); border:3px solid #FFD700; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px; }
.card p { padding:9px 6px 2px; font-size:13px; text-align:center; min-height:40px; }
.watch { background:linear-gradient(#FFD700,#FFAA00); color:#000; text-align:center; padding:11px; font-weight:900; margin:6px; border-radius:10px; cursor:pointer; }
#player { display:none; background:#000; border:3px solid #FFD700; border-radius:16px; padding:12px; margin:10px 0; text-align:center; position:sticky; top:10px; z-index:99; }
#downloadBtn { display:none; background:#007A3D; color:#fff; padding:14px; border-radius:10px; font-weight:900; font-size:16px; margin-top:10px; cursor:pointer; border:2px solid #FFD700; }
#watchMsg { color:#FFD700; font-size:13px; margin-top:8px; }
.footer { text-align:center; padding:22px 10px; background:linear-gradient(#007A3D,#000); border:2px solid #FFD700; border-radius:14px; margin-top:15px; }
.footer h3 { color:#FFD700; font-size:18px; }
.footer p { color:#fff; margin-top:6px; }
.bottom-nav { position:fixed; bottom:0; left:0; right:0; background:#000; display:flex; justify-content:space-around; padding:12px 0; border-top:3px solid #FFD700; max-width:520px; margin:0 auto; }
.bottom-nav div { text-align:center; font-size:12px; color:#FFD700; }
.bottom-nav span { font-size:24px; display:block; }
</style>
</head>
<body>
<div class="phone">

<!-- ===== هنا الصورة الفوق - ما مسحنا أي حاجة ===== -->
<div class="hero">
  <div class="hero-top-img"></div>
  <div class="hero-content">
    <h1>تفلتات</h1>
    <h2>TAFLTAT</h2>
    <div class="flag">🇸🇩 🇸🇩 🇸🇩</div>
    <p>فيديوهات سودانية • كوميديا • موسيقى • كرة قدم</p>
  </div>
</div>

<div class="sudan-bar"><div class="c1"></div><div class="c2"></div><div class="c3"></div><div class="c4"></div></div>
<div class="search-box">🔍 <input id="searchInput" placeholder="اكتب أي حاجة هنا... ح تظهر طوالي جوة" autocomplete="off"></div>
<div class="hint">✍️ اكتب بس... شوف أول، بعدين حمل</div>
<div class="btns"><button onclick="setType('all',this)" class="active">🌍 الكل</button><button onclick="setType('كوميديا',this)">😂 كوميديا</button><button onclick="setType('موسيقى',this)">🎵 موسيقى</button><button onclick="setType('كرة قدم',this)">⚽ كرة قدم</button><button onclick="setType('اغاني',this)">🎤 اغاني</button></div>
<div id="status" style="text-align:center;padding:6px;color:#FFD700;font-weight:bold;"></div>
<div id="player"><p id="nowPlaying"></p><div id="videoBox"></div><p id="watchMsg">👀 شوف الفيديو أول... زر التحميل ح يظهر بعد 5 ثواني</p><div id="downloadBtn" onclick="downloadNow()">⬇️ حمل الفيديو دا هسي</div><br><button onclick="closePlayer()" style="background:#D21034;color:#fff;border:none;padding:7px 20px;border-radius:10px;margin-top:8px;">اقفل ✖️</button></div>
<div class="cards" id="list"></div>
<div class="footer"><h3>🇸🇩 تفلتات - TAFLTAT 🇸🇩</h3><p>https://taflatat.onrender.com</p><p>👑 تامر ود الدروشاب • من السودان، للسودان، للعالم كلو</p><p style="color:#FFD700;">الخرطوم • أم درمان • بحري • مدني • بورتسودان</p></div>
</div>
<div class="bottom-nav"><div><span>🏠</span>الرئيسية</div><div><span>📚</span>المكتبة</div><div><span>⬇️</span>التحميلات</div><div><span>⚙️</span>الاعدادات</div></div>
<script>
let currentType='all', timer=null, lastQ='', currentId='';
function setType(t,el){ currentType=t; document.querySelectorAll('.btns button').forEach(b=>b.classList.remove('active')); el.classList.add('active'); doSearch(document.getElementById('searchInput').value); }
function render(list){
  let box=document.getElementById('list'); box.innerHTML="";
  if(!list.length){ box.innerHTML="<p style='grid-column:1/3;text-align:center;padding:20px;'>❌ ما لقيت حاجة، جرب كلمة تانية</p>"; return; }
  list.forEach(s=>{ box.innerHTML+=`<div class="card"><div class="thumb" onclick="playSong('${s.id}','${s.name.replace(/'/g,'')}')"><img src="${s.img}"><div class="play">▶</div></div><p>${s.name}</p><div class="watch" onclick="playSong('${s.id}','${s.name.replace(/'/g,'')}')">▶ شاهد أول</div></div>`; });
}
function playSong(id,name){
  currentId=id;
  document.getElementById('player').style.display="block";
  document.getElementById('nowPlaying').innerText="🎵 شغال هسي جوة التطبيق: "+name;
  document.getElementById('videoBox').innerHTML=`<iframe width="100%" height="250" src="https://www.youtube.com/embed/${id}?autoplay=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
  document.getElementById('downloadBtn').style.display="none";
  document.getElementById('watchMsg').innerText="👀 شوف الفيديو أول... زر التحميل ح يظهر بعد 5 ثواني";
  setTimeout(()=>{ document.getElementById('downloadBtn').style.display="block"; document.getElementById('watchMsg').innerText="✅ خلاص شفتو؟ هسي ممكن تحملو 👇"; }, 5000);
  window.scrollTo({top:0, behavior:'smooth'});
}
function downloadNow(){ window.open(`/api/download?id=${currentId}`, '_blank'); }
function closePlayer(){ document.getElementById('player').style.display="none"; document.getElementById('videoBox').innerHTML=""; }
async function doSearch(raw){
  let q=raw.trim();
  if(q.length<2){ render([]); document.getElementById('status').innerText="اكتب أي حاجة فوق 👆"; return; }
  if(q===lastQ) return; lastQ=q;
  let query=q; if(currentType!=='all') query=q+" "+currentType+" سوداني";
  document.getElementById('status').innerText="🔍 جاري البحث جوة التطبيق عن: "+q+"...";
  try{
    let res=await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    let data=await res.json(); render(data);
    document.getElementById('status').innerText="✅ لقيت "+data.length+" فيديو حقيقي لـ "+q;
  }catch(e){ document.getElementById('status').innerText="❌ النت ضعيف، حاول تاني"; }
}
document.getElementById('searchInput').addEventListener('input', function(){ clearTimeout(timer); let v=this.value; timer=setTimeout(()=>doSearch(v), 700); });
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/search')
def search():
    q = request.args.get('q','')
    try:
        from yt_dlp import YoutubeDL
        ydl_opts = {'quiet': True, 'no_warnings': True, 'skip_download': True, 'extract_flat': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch15:{q}", download=False)
            out=[]
            for e in info.get('entries', []):
                if not e: continue
                vid=e.get('id','')
                if not vid: continue
                title=e.get('title','')
                thumb=e.get('thumbnails', [{}])[-1].get('url','') if e.get('thumbnails') else f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
                if not thumb: thumb=f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
                out.append({'id':vid,'name':title,'img':thumb})
            return jsonify(out)
    except Exception as e:
        print(e)
        return jsonify([])

@app.route('/api/download')
def download():
    vid = request.args.get('id','')
    try:
        from yt_dlp import YoutubeDL
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(f"https://youtube.com/watch?v={vid}", download=False)
            url = info.get('url') or info.get('formats', [{}])[-1].get('url','')
            return redirect(url)
    except:
        return redirect(f"https://youtube.com/watch?v={vid}")

if __name__=='__main__':
    port=int(os.environ.get('PORT',10000))
    app.run(host='0.0.0.0',port=port)
