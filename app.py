from flask import Flask, render_template_string, jsonify, request
import os, requests
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
body { background:#0a0a0a; color:#fff; }
.phone { max-width:520px; margin:0 auto; background:#111; min-height:100vh; padding:12px; padding-bottom:80px; }
.top-banner { text-align:center; padding:20px 10px 12px; border-bottom:2px solid #ffcc00; }
.top-banner h1 { font-size:58px; color:#e8b800; line-height:1; }
.top-banner h2 { font-size:34px; color:#e8b800; }
.top-banner p { font-size:14px; margin-top:6px; }
.search-box { background:#d9d9d9; margin:15px 0 10px; border-radius:10px; padding:13px; display:flex; gap:8px; }
.search-box input { background:transparent; border:none; outline:none; width:100%; font-size:15px; text-align:center; color:#000; font-weight:bold; }
.btns { display:flex; gap:7px; overflow-x:auto; padding:5px 0 8px; }
.btns button { white-space:nowrap; background:#111; color:#ffcc00; border:1.5px solid #ffcc00; padding:10px 14px; border-radius:10px; font-weight:bold; cursor:pointer; }
.btns button.active { background:#ffcc00; color:#000; }
.sources { display:flex; gap:7px; overflow-x:auto; padding:0 0 10px; }
.sources button { white-space:nowrap; background:#222; color:#fff; border:1px solid #555; padding:8px 14px; border-radius:20px; font-size:13px; cursor:pointer; }
.sources button.active { background:#fff; color:#000; }
.big-btn { background:linear-gradient(#ffcc00,#ff9900); text-align:center; padding:15px; border-radius:10px; color:#000; font-weight:900; font-size:17px; cursor:pointer; }
.cards { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:12px; }
.card { background:#1a1a1a; border-radius:12px; overflow:hidden; border:1px solid #333; }
.thumb { position:relative; }
.thumb img { width:100%; height:140px; object-fit:cover; display:block; }
.play { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:48px; height:48px; background:rgba(0,0,0,0.7); border:2px solid #ffcc00; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px; }
.src-badge { position:absolute; top:6px; left:6px; background:#ffcc00; color:#000; font-size:11px; font-weight:bold; padding:3px 7px; border-radius:6px; }
.duration { position:absolute; bottom:6px; right:6px; background:#000; color:#fff; font-size:11px; padding:3px 7px; border-radius:6px; }
.card p { padding:8px 6px 2px; font-size:13px; text-align:center; min-height:38px; }
.download { background:#00a651; text-align:center; padding:10px; font-weight:bold; margin:6px; border-radius:8px; cursor:pointer; }
#player { display:none; background:#000; border:2px solid #ffcc00; border-radius:12px; padding:10px; margin:10px 0; text-align:center; }
.footer { text-align:center; padding:20px 10px; color:#ffcc00; }
.bottom-nav { position:fixed; bottom:0; left:0; right:0; background:#000; display:flex; justify-content:space-around; padding:12px 0; border-top:1px solid #333; max-width:520px; margin:0 auto; }
.bottom-nav div { text-align:center; font-size:12px; }
.bottom-nav span { font-size:22px; display:block; }
</style>
</head>
<body>
<div class="phone">
<div class="top-banner"><h1>تفلتات</h1><h2>TAFLTAT</h2><p>فيديوهات سودانية • كوميديا • موسيقى • كرة قدم</p></div>
<div class="search-box">🔍 <input id="searchInput" placeholder="اكتب أي حاجة - من أي حتة" onkeyup="if(event.key==='Enter')searchNow()"></div>
<div class="btns"><button onclick="setType('all',this)" class="active">الكل</button><button onclick="setType('كوميديا',this)">😂 كوميديا</button><button onclick="setType('موسيقى',this)">🎵 موسيقى</button><button onclick="setType('كرة قدم',this)">⚽ كرة قدم</button><button onclick="setType('اغاني',this)">🎤 اغاني</button></div>
<div class="sources"><button onclick="setSource('all',this)" class="active">🌍 الدنيا كلها</button><button onclick="setSource('youtube',this)">▶️ يوتيوب</button><button onclick="setSource('tiktok',this)">🎵 تيك توك</button><button onclick="setSource('facebook',this)">📘 فيسبوك</button><button onclick="setSource('twitter',this)">🐦 تويتر</button></div>
<div class="big-btn" onclick="searchNow()">🔍 ابحث طوالي - من أي حتة</div>
<div id="status" style="text-align:center;padding:8px;color:#ffcc00;font-weight:bold;"></div>
<div id="player"><p id="nowPlaying"></p><div id="videoBox"></div><br><button onclick="closePlayer()" style="background:#ff3333;color:#fff;border:none;padding:7px 20px;border-radius:10px;">اقفل ✖️</button></div>
<div class="cards" id="list"></div>
<div class="footer"><p>https://taflatat.onrender.com</p><p style="margin-top:10px;">👑 تامر ود الدروشاب • شاهد، حمّل، وشارك</p></div>
</div>
<div class="bottom-nav"><div><span>🏠</span>الرئيسية</div><div><span>📚</span>المكتبة</div><div><span>⬇️</span>التحميلات</div><div><span>⚙️</span>الاعدادات</div></div>
<script>
let currentType='all', currentSource='all';
function setType(t,el){ currentType=t; document.querySelectorAll('.btns button').forEach(b=>b.classList.remove('active')); el.classList.add('active'); searchNow(); }
function setSource(s,el){ currentSource=s; document.querySelectorAll('.sources button').forEach(b=>b.classList.remove('active')); el.classList.add('active'); searchNow(); }
function render(list){
  let box=document.getElementById('list'); box.innerHTML="";
  if(!list.length){ box.innerHTML="<p style='grid-column:1/3;text-align:center;'>❌ ما لقيت حاجة، جرب كلمة تانية</p>"; return; }
  list.forEach(s=>{ box.innerHTML+=`<div class="card"><div class="thumb" onclick="playSong('${s.id}','${s.name.replace(/'/g,'')}','${s.src}','${s.link||''}')"><img src="${s.img}"><div class="play">▶</div><div class="src-badge">${s.src}</div><div class="duration">${s.dur||''}</div></div><p>${s.name}</p><div class="download" onclick="playSong('${s.id}','${s.name.replace(/'/g,'')}','${s.src}','${s.link||''}')">⬇️ تحميل / مشاهدة</div></div>`; });
}
function playSong(id,name,src,link){
  document.getElementById('player').style.display="block";
  document.getElementById('nowPlaying').innerText="🎵 شغال هسي من "+src+" : "+name;
  if(src==='يوتيوب'){ document.getElementById('videoBox').innerHTML=`<iframe width="100%" height="240" src="https://www.youtube.com/embed/${id}?autoplay=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>`; }
  else if(src==='تيك توك'){ document.getElementById('videoBox').innerHTML=`<video width="100%" height="300" controls autoplay src="${link}"><source src="${link}"></video><br><a href="https://www.tiktok.com/@/video/${id}" target="_blank" style="color:#ffcc00;">افتح في تيك توك ↗️</a>`; }
  else { document.getElementById('videoBox').innerHTML=`<a href="${link}" target="_blank" style="color:#ffcc00;font-size:18px;font-weight:bold;">افتح في ${src} طوالي ↗️<br><br>${name}</a>`; }
  window.scrollTo({top:0, behavior:'smooth'});
}
function closePlayer(){ document.getElementById('player').style.display="none"; document.getElementById('videoBox').innerHTML=""; }
async function searchNow(){
  let q=document.getElementById('searchInput').value.trim();
  let query=q|| (currentType==='all'?'فيديوهات سودانية':currentType+' سوداني');
  if(q && currentType!=='all') query=q+" "+currentType;
  document.getElementById('status').innerText="🔍 جاري البحث من الدنيا كلها عن: "+query+"...";
  try{
    let res=await fetch(`/api/search?q=${encodeURIComponent(query)}&source=${currentSource}`);
    let data=await res.json(); render(data);
    document.getElementById('status').innerText="✅ لقيت "+data.length+" نتيجة من كل الحتات لـ "+query;
  }catch(e){ document.getElementById('status').innerText="❌ النت ضعيف، حاول تاني"; }
}
searchNow();
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

def search_youtube(q):
    out=[]
    for base in ["https://inv.nadeko.net/api/v1/search", "https://invidious.0011.lt/api/v1/search", "https://vid.puffyan.us/api/v1/search"]:
        try:
            r=requests.get(base, params={"q":q,"type":"video"}, timeout=8)
            if r.status_code==200:
                for e in r.json()[:8]:
                    vid=e.get('videoId','')
                    if not vid: continue
                    length=e.get('lengthSeconds',0)
                    out.append({'id':vid,'name':e.get('title',''),'img':f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",'dur':f"{int(length//60)}:{int(length%60):02d}",'src':'يوتيوب','link':f"https://youtube.com/watch?v={vid}"})
                if out: break
        except: continue
    return out

def search_tiktok(q):
    out=[]
    try:
        r=requests.get("https://www.tikwm.com/api/feed/search", params={"keywords":q,"count":8}, timeout=8)
        data=r.json().get('data',{}).get('videos',[])
        for v in data:
            out.append({'id':str(v.get('video_id','')),'name':v.get('title') or v.get('desc','فيديو تيك توك'),'img':v.get('cover',''),'dur':'تيك توك','src':'تيك توك','link':v.get('play','')})
    except: pass
    return out

@app.route('/api/search')
def search():
    q=request.args.get('q','')
    source=request.args.get('source','all')
    results=[]
    if source in ('all','youtube'):
        results += search_youtube(q)
    if source in ('all','tiktok'):
        results += search_tiktok(q)
    if source in ('all','facebook'):
        results.append({'id':'fb-'+q,'name':f"فيديوهات {q} في فيسبوك - دوس وشوف كل النتائج",'img':f"https://picsum.photos/400/300?random=11",'dur':'فيسبوك','src':'فيسبوك','link':f"https://www.facebook.com/search/videos/?q={q}"})
        results.append({'id':'fb2-'+q,'name':f"كوميديا {q} في فيسبوك",'img':f"https://picsum.photos/400/300?random=12",'dur':'فيسبوك','src':'فيسبوك','link':f"https://www.facebook.com/search/videos/?q={q}"})
    if source in ('all','twitter'):
        results.append({'id':'tw-'+q,'name':f"فيديوهات {q} في تويتر / X",'img':f"https://picsum.photos/400/300?random=13",'dur':'تويتر','src':'تويتر','link':f"https://x.com/search?q={q}&f=video"})
        results.append({'id':'tw2-'+q,'name':f"ترند {q} في تويتر",'img':f"https://picsum.photos/400/300?random=14",'dur':'تويتر','src':'تويتر','link':f"https://x.com/search?q={q}"})
    return jsonify(results)

if __name__=='__main__':
    port=int(os.environ.get('PORT',10000))
    app.run(host='0.0.0.0',port=port)
  
