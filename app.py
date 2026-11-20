from flask import Flask, render_template_string, jsonify, request, redirect
import os
app = Flask(__name__)
HERO_URL = "https://raw.githubusercontent.com/tamaerabdalazeez099-ship-it/taflatat/main/Messenger_creation_1050237001420020.jpeg"
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>👑 تفلتات TAFLTAT 👑</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family: Tahoma, sans-serif; }
body { background:#000; color:#fff; }
@keyframes shine { 0%{background-position:-200% center} 100%{background-position:200% center} }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
@keyframes glow { 0%,100%{box-shadow:0 0 15px #FFD700} 50%{box-shadow:0 0 35px #FFD700,0 0 60px #FFAA00} }
@keyframes pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.08)} }
.phone { max-width:520px; margin:0 auto; background:radial-gradient(circle at top, #2a1f00 0%, #0a0a0a 45%, #000 100%); min-height:100vh; padding:12px; padding-bottom:95px; border-left:3px solid #FFD700; border-right:3px solid #FFD700; }
.vip-bar { background:linear-gradient(90deg,#FFD700,#FFF3A0,#FFAA00,#FFD700); background-size:200% auto; animation:shine 3s linear infinite; color:#000; text-align:center; padding:9px; border-radius:20px; font-weight:900; font-size:13px; }
.top-title { text-align:center; padding:14px 5px 2px; }
.top-title .crown { font-size:48px; animation:float 2s ease-in-out infinite; display:block; filter:drop-shadow(0 0 15px #FFD700); }
.top-title h1 { font-size:48px; background:linear-gradient(90deg,#FFD700,#FFF8A0,#FFAA00,#FFD700); background-size:200% auto; -webkit-background-clip:text; -webkit-text-fill-color:transparent; animation:shine 3s linear infinite; }
.top-title p { color:#FFD700; font-size:12px; margin-top:4px; letter-spacing:3px; }
.gold-line { height:3px; background:linear-gradient(90deg, transparent, #FFD700, #FFF3A0, #FFD700, transparent); margin:12px 0; border-radius:10px; }
.hero-wrap { position:relative; padding:4px; background:linear-gradient(45deg,#FFD700,#FFF3A0,#FFAA00,#FFD700); border-radius:22px; animation:glow 3s ease-in-out infinite; }
.hero { border-radius:18px; overflow:hidden; position:relative; }
.hero img { width:100%; display:block; }
.hero-badge { position:absolute; bottom:12px; left:50%; transform:translateX(-50%); background:linear-gradient(90deg,#000,#1a1400,#000); border:2px solid #FFD700; color:#FFD700; padding:8px 18px; border-radius:25px; font-weight:900; font-size:13px; white-space:nowrap; box-shadow:0 0 20px #FFD700; }
.sudan-flag { display:flex; height:16px; border-radius:10px; overflow:hidden; margin:12px 0 4px; border:2px solid #FFD700; box-shadow:0 0 10px rgba(255,215,0,0.5); }
.sudan-flag div { flex:1; } .c1{background:#D21034} .c2{background:#fff} .c3{background:#000} .c4{background:#007A3D}
.king-card { background:linear-gradient(135deg, rgba(255,215,0,0.18), rgba(0,0,0,0.9)); border:2px solid #FFD700; border-radius:20px; padding:14px; margin:10px 0 14px; text-align:center; box-shadow:0 0 25px rgba(255,215,0,0.35); }
.king-card h3 { color:#FFD700; font-size:18px; text-shadow:0 0 10px #FFD700; }
.king-card p { font-size:13px; color:#fff; margin-top:7px; line-height:1.8; }
.search-box { background:linear-gradient(180deg,#fff,#FFF8D0); margin:12px 0 6px; border-radius:20px; padding:16px; display:flex; gap:8px; align-items:center; border:3px solid #FFD700; box-shadow:0 0 20px rgba(255,215,0,0.5); }
.search-box input { background:transparent; border:none; outline:none; width:100%; font-size:17px; text-align:center; color:#000; font-weight:bold; }
.hint { text-align:center; color:#FFD700; font-size:13px; padding-bottom:8px; font-weight:bold; }
.section-title { color:#FFD700; font-weight:900; font-size:17px; padding:12px 4px 8px; text-shadow:0 0 8px #FFD700; display:flex; justify-content:space-between; align-items:center; }
.section-title span { background:#FFD700; color:#000; font-size:11px; padding:4px 10px; border-radius:15px; }
.trend-grid { display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:12px; margin-bottom:10px; }
.trend-app { text-align:center; cursor:pointer; position:relative; }
.trend-app .icon { width:64px; height:64px; margin:0 auto; border-radius:18px; display:flex; align-items:center; justify-content:center; font-size:30px; box-shadow:0 6px 15px rgba(0,0,0,0.6), inset 0 2px 0 rgba(255,255,255,0.4); border:2px solid rgba(255,255,255,0.3); }
.trend-app b { font-size:11px; color:#fff; display:block; margin-top:6px; line-height:1.2; }
.trend-app small { font-size:9px; color:#FFD700; }
.trend-badge { position:absolute; top:-5px; right:8px; background:#D21034; color:#fff; font-size:8px; padding:2px 6px; border-radius:10px; font-weight:900; animation:pulse 1.5s infinite; z-index:2; }
.trend-app.active .icon { outline:3px solid #FFD700; box-shadow:0 0 18px #FFD700; transform:scale(1.08); }
.trend-app.active b { color:#FFD700; }
.g1{background:linear-gradient(135deg,#25D366,#128C7E)} .g2{background:linear-gradient(135deg,#1877F2,#0A4AA0)} .g3{background:linear-gradient(135deg,#000,#333)} .g4{background:linear-gradient(135deg,#E1306C,#F77737)} .g5{background:linear-gradient(135deg,#FF0000,#AA0000)} .g6{background:linear-gradient(135deg,#0088cc,#00A8E8)} .g7{background:linear-gradient(135deg,#FFFC00,#FFAA00)} .g8{background:linear-gradient(135deg,#FFD700,#FFAA00)}
.c1{background:linear-gradient(135deg,#FF6B6B,#D21034)} .c2{background:linear-gradient(135deg,#FFD93D,#FFAA00)} .c3{background:linear-gradient(135deg,#6BCB77,#007A3D)} .c4{background:linear-gradient(135deg,#4D96FF,#6C63FF)} .c5{background:linear-gradient(135deg,#9B5DE5,#F15BB5)} .c6{background:linear-gradient(135deg,#00F5D4,#00BBF9)} .c7{background:linear-gradient(135deg,#FF8C42,#FF3D68)} .c8{background:linear-gradient(135deg,#00C9A7,#0088cc)}
.cards { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:5px; }
.card { background:linear-gradient(180deg,#222,#0a0a0a); border-radius:18px; overflow:hidden; border:2px solid #FFD700; box-shadow:0 6px 18px rgba(0,0,0,0.7); }
.thumb { position:relative; }
.thumb img { width:100%; height:160px; object-fit:cover; display:block; }
.play { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:58px; height:58px; background:linear-gradient(180deg,#FFD700,#FFAA00); border:3px solid #fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px; box-shadow:0 0 20px #FFD700; color:#000; }
.card p { padding:9px 6px 2px; font-size:13px; text-align:center; min-height:40px; }
.watch { background:linear-gradient(90deg,#FFD700,#FFAA00); color:#000; text-align:center; padding:12px; font-weight:900; margin:6px; border-radius:12px; cursor:pointer; }
#player { display:none; background:#000; border:3px solid #FFD700; border-radius:20px; padding:12px; margin:10px 0; text-align:center; position:sticky; top:10px; z-index:99; box-shadow:0 0 25px #FFD700; }
#downloadBtn { display:none; background:linear-gradient(90deg,#007A3D,#00AA55); color:#fff; padding:15px; border-radius:14px; font-weight:900; font-size:16px; margin-top:10px; cursor:pointer; border:2px solid #FFD700; }
#watchMsg { color:#FFD700; font-size:13px; margin-top:8px; }
.footer { text-align:center; padding:22px 10px; background:linear-gradient(180deg,#1a1400,#000); border:2px solid #FFD700; border-radius:20px; margin-top:15px; }
.footer h3 { color:#FFD700; font-size:19px; }
.footer p { color:#fff; margin-top:6px; font-size:13px; }
.bottom-nav { position:fixed; bottom:0; left:0; right:0; background:linear-gradient(180deg,#111,#000); display:flex; justify-content:space-around; padding:12px 0; border-top:3px solid #FFD700; max-width:520px; margin:0 auto; }
.bottom-nav div { text-align:center; font-size:12px; color:#FFD700; }
.bottom-nav span { font-size:24px; display:block; }
</style>
</head>
<body>
<div class="phone">
<div class="vip-bar">🔥 TRENDING NOW • تطبيقات ترند • فخامة ملوك 👑</div>
<div class="top-title"><span class="crown">👑</span><h1>تفلتات</h1><p>TAFLTAT • TREND APPS</p></div>
<div class="gold-line"></div>
<div class="hero-wrap"><div class="hero"><img src="__HERO__"><div class="hero-badge">👑 تامر ود الدروشاب 👑</div></div></div>
<div class="sudan-flag"><div class="c1"></div><div class="c2"></div><div class="c3"></div><div class="c4"></div></div>
<div class="king-card"><h3>🇸🇩 من السودان، للسودان، للعالم كلو 🇸🇩</h3><p>ما دام في القلب إخوان .. ما بنخاف من الأيام<br>من الدروشاب بدينا .. وبالحب حنوصل لي قدام<br>💎 فخامة .. هيبة .. ذهب .. ملوك 💎</p></div>
<div class="search-box">💎 <input id="searchInput" placeholder="اكتب أي حاجة هنا... ح تظهر طوالي" autocomplete="off"> 🔍</div>
<div class="hint">✍️ اكتب بس... أو دوس على أي تطبيق تحت 👇</div>
<div class="section-title">📱 تطبيقات التواصل - ترند <span>🔥 HOT</span></div>
<div class="trend-grid">
<div class="trend-app" onclick="pickApp('واتساب',this)"><span class="trend-badge">TREND</span><div class="icon g1">💚</div><b>واتساب</b><small>WhatsApp</small></div>
<div class="trend-app" onclick="pickApp('فيسبوك',this)"><span class="trend-badge">TREND</span><div class="icon g2">💙</div><b>فيسبوك</b><small>Facebook</small></div>
<div class="trend-app" onclick="pickApp('تيك توك',this)"><span class="trend-badge">🔥 HOT</span><div class="icon g3">🎶</div><b>تيك توك</b><small>TikTok</small></div>
<div class="trend-app" onclick="pickApp('انستقرام',this)"><div class="icon g4">📸</div><b>انستقرام</b><small>Instagram</small></div>
<div class="trend-app" onclick="pickApp('يوتيوب',this)"><div class="icon g5">▶️</div><b>يوتيوب</b><small>YouTube</small></div>
<div class="trend-app" onclick="pickApp('تليجرام',this)"><div class="icon g6">✈️</div><b>تليجرام</b><small>Telegram</small></div>
<div class="trend-app" onclick="pickApp('سناب شات',this)"><div class="icon g7">👻</div><b>سناب شات</b><small>Snapchat</small></div>
<div class="trend-app active" onclick="pickApp('all',this)"><div class="icon g8">🌍</div><b>الكل</b><small>All Apps</small></div>
</div>
<div class="section-title">🎬 تطبيقات الفيديو - ترند <span>⭐ TOP</span></div>
<div class="trend-grid">
<div class="trend-app" onclick="setType('كوميديا',this)"><span class="trend-badge">😂</span><div class="icon c1">😂</div><b>كوميديا</b><small>Comedy</small></div>
<div class="trend-app" onclick="setType('موسيقى',this)"><div class="icon c2">🎵</div><b>موسيقى</b><small>Music</small></div>
<div class="trend-app" onclick="setType('اغاني',this)"><span class="trend-badge">TREND</span><div class="icon c3">🎤</div><b>اغاني</b><small>Songs</small></div>
<div class="trend-app" onclick="setType('كرة قدم',this)"><span class="trend-badge">⚽</span><div class="icon c4">⚽</div><b>كرة قدم</b><small>Football</small></div>
<div class="trend-app" onclick="setType('افلام',this)"><div class="icon c5">🎬</div><b>أفلام</b><small>Movies</small></div>
<div class="trend-app" onclick="setType('مسلسلات',this)"><div class="icon c6">📺</div><b>مسلسلات</b><small>Series</small></div>
<div class="trend-app" onclick="setType('قرآن',this)"><div class="icon c7">📖</div><b>قرآن</b><small>Quran</small></div>
<div class="trend-app" onclick="setType('اخبار',this)"><div class="icon c8">📰</div><b>أخبار</b><small>News</small></div>
<div class="trend-app" onclick="setType('العاب',this)"><span class="trend-badge">🎮</span><div class="icon c1">🎮</div><b>ألعاب</b><small>Games</small></div>
<div class="trend-app" onclick="setType('طبخ',this)"><div class="icon c2">🍲</div><b>طبخ</b><small>Cooking</small></div>
<div class="trend-app" onclick="setType('رياضة',this)"><div class="icon c3">💪</div><b>رياضة</b><small>Sport</small></div>
<div class="trend-app" onclick="setType('تعليم',this)"><div class="icon c4">📚</div><b>تعليم</b><small>Learn</small></div>
<div class="trend-app" onclick="setType('تكنولوجيا',this)"><div class="icon c5">💻</div><b>تكنولوجيا</b><small>Tech</small></div>
<div class="trend-app" onclick="setType('تطبيقات',this)"><span class="trend-badge">📱</span><div class="icon c6">📱</div><b>تطبيقات</b><small>Apps</small></div>
<div class="trend-app" onclick="setType('all',this)"><div class="icon c7">🌍</div><b>الكل</b><small>All</small></div>
<div class="trend-app" onclick="setType('اغاني سودانية',this)"><span class="trend-badge">🇸🇩</span><div class="icon c8">🇸🇩</div><b>سوداني</b><small>Sudan</small></div>
</div>
<div id="status" style="text-align:center;padding:6px;color:#FFD700;font-weight:bold;"></div>
<div id="player"><p id="nowPlaying"></p><div id="videoBox"></div><p id="watchMsg">👀 شوف الفيديو أول... زر التحميل ح يظهر بعد 5 ثواني</p><div id="downloadBtn" onclick="downloadNow()">⬇️ حمل الفيديو دا هسي</div><br><button onclick="closePlayer()" style="background:#D21034;color:#fff;border:none;padding:7px 20px;border-radius:10px;margin-top:8px;">اقفل ✖️</button></div>
<div class="cards" id="list"></div>
<div class="footer"><h3>👑 🇸🇩 تفلتات - TAFLTAT 🇸🇩 👑</h3><p>https://taflatat.onrender.com</p><p>👑 تامر ود الدروشاب • الملك • مع تحياتي للجميع ❤️</p><p style="color:#FFD700;">🇸🇩 الخرطوم • أم درمان • بحري • مدني • بورتسودان 🇸🇩</p></div>
</div>
<div class="bottom-nav"><div><span>🏠</span>الرئيسية</div><div><span>🔥</span>ترند</div><div><span>⬇️</span>التحميلات</div><div><span>👑</span>VIP</div></div>
<script>
let currentType='all', timer=null, lastQ='', currentId='', currentApp='all';
function pickApp(t,el){ currentApp=t; document.querySelectorAll('.trend-grid .trend-app').forEach(b=>b.classList.remove('active')); el.classList.add('active'); doSearch(document.getElementById('searchInput').value || t); }
function setType(t,el){ currentType=t; document.querySelectorAll('.trend-grid .trend-app').forEach(b=>b.classList.remove('active')); if(el) el.classList.add('active'); doSearch(document.getElementById('searchInput').value); }
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
  let q=(raw||'').trim();
  if(q.length<2){
    if(currentApp!=='all') q=currentApp;
    else if(currentType!=='all') q=currentType;
    else { render([]); document.getElementById('status').innerText="دوس على أي تطبيق فوق 👆"; return; }
  }
  let query=q; if(currentType!=='all' && !query.includes(currentType)) query=q+" "+currentType+" سوداني";
  if(currentApp!=='all' && !query.includes(currentApp)) query=query+" "+currentApp;
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
""".replace("__HERO__", HERO_URL)
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
  
