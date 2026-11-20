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
.search-box { background:#fff; margin:15px 0 10px; border-radius:12px; padding:14px; display:flex; gap:8px; align-items:center; border:2px solid #ffcc00; }
.search-box input { background:transparent; border:none; outline:none; width:100%; font-size:17px; text-align:center; color:#000; font-weight:bold; }
.hint { text-align:center; color:#ffcc00; font-size:13px; padding-bottom:8px; }
.btns { display:flex; gap:7px; overflow-x:auto; padding:5px 0 10px; }
.btns button { white-space:nowrap; background:#111; color:#ffcc00; border:1.5px solid #ffcc00; padding:10px 14px; border-radius:10px; font-weight:bold; cursor:pointer; }
.btns button.active { background:#ffcc00; color:#000; }
.cards { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:5px; }
.card { background:#1a1a1a; border-radius:12px; overflow:hidden; border:1px solid #333; }
.thumb { position:relative; }
.thumb img { width:100%; height:150px; object-fit:cover; display:block; }
.play { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:50px; height:50px; background:rgba(0,0,0,0.75); border:2px solid #ffcc00; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px; }
.src { position:absolute; top:6px; left:6px; background:#ffcc00; color:#000; font-size:11px; font-weight:bold; padding:3px 8px; border-radius:6px; }
.card p { padding:8px 6px 2px; font-size:13px; text-align:center; min-height:38px; }
.download { background:#00a651; text-align:center; padding:10px; font-weight:bold; margin:6px; border-radius:8px; cursor:pointer; }
#player { display:none; background:#000; border:2px solid #ffcc00; border-radius:12px; padding:10px; margin:10px 0; text-align:center; position:sticky; top:10px; z-index:99; }
.footer { text-align:center; padding:20px 10px; color:#ffcc00; }
.bottom-nav { position:fixed; bottom:0; left:0; right:0; background:#000; display:flex; justify-content:space-around; padding:12px 0; border-top:1px solid #333; max-width:520px; margin:0 auto; }
.bottom-nav div { text-align:center; font-size:12px; }
.bottom-nav span { font-size:22px; display:block; }
</style>
</head>
<body>
<div class="phone">
<div class="top-banner"><h1>تفلتات</h1><h2>TAFLTAT</h2><p>فيديوهات سودانية • كوميديا • موسيقى • كرة قدم</p></div>
<div class="search-box">🔍 <input id="searchInput" placeholder="اكتب أي حاجة هنا... ح تظهر طوالي جوة" autocomplete="off"></div>
<div class="hint">✍️ اكتب بس... ما تدوس أي زر، النتيجة بتجيك طوالي جوة التطبيق</div>
<div class="btns"><button onclick="setType('all',this)" class="active">🌍 الكل</button><button onclick="setType('كوميديا',this)">😂 كوميديا</button><button onclick="setType('موسيقى',this)">🎵 موسيقى</button><button onclick="setType('كرة قدم',this)">⚽ كرة قدم</button><button onclick="setType('اغاني',this)">🎤 اغاني</button></div>
<div id="status" style="text-align:center;padding:6px;color:#ffcc00;font-weight:bold;"></div>
<div id="player"><p id="nowPlaying"></p><div id="videoBox"></div><br><button onclick="closePlayer()" style="background:#ff3333;color:#fff;border:none;padding:7px 20px;border-radius:10px;">اقفل ✖️</button></div>
<div class="cards" id="list"></div>
<div class="footer"><p>https://taflatat.onrender.com</p><p style="margin-top:10px;">👑 تامر ود الدروشاب • شاهد، حمّل، وشارك</p></div>
</div>
<div class="bottom-nav"><div><span>🏠</span>الرئيسية</div><div><span>📚</span>المكتبة</div><div><span>⬇️</span>التحميلات</div><div><span>⚙️</span>الاعدادات</div></div>
<script>
let currentType='all', timer=null, lastQ='';
function setType(t,el){ currentType=t; document.querySelectorAll('.btns button').forEach(b=>b.classList.remove('active')); el.classList.add('active'); doSearch(document.getElementById('searchInput').value); }
function render(list){
  let box=document.getElementById('list'); box.innerHTML="";
  if(!list.length){ box.innerHTML="<p style='grid-column:1/3;text-align:center;padding:20px;'>🔍 اكتب أي حاجة فوق...<br>أي أغنية، أي فيديو، أي كوميديا</p>"; return; }
  list.forEach(s=>{ box.innerHTML+=`<div class="card"><div class="thumb" onclick="playSong('${s.id}','${s.name.replace(/'/g,'')}','${s.src}','${s.link||''}')"><img src="${s.img}"><div class="play">▶</div><div class="src">${s.src}</div></div><p>${s.name}</p><div class="download" onclick="playSong('${s.id}','${s.name.replace(/'/g,'')}','${s.src}','${s.link||''}')">▶ تشغيل طوالي جوة</div></div>`; });
}
function playSong(id,name,src,link){
  document.getElementById('player').style.display="block";
  document.getElementById('nowPlaying').innerText="🎵 شغال هسي جوة التطبيق: "+name;
  if(src==='يوتيوب'){ document.getElementById('videoBox').innerHTML=`<iframe width="100%" height="250" src="https://www.youtube.com/embed/${id}?autoplay=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>`; }
  else { document.getElementById('videoBox').innerHTML=`<video width="100%" height="320" controls autoplay playsinline src="${link}"></video>`; }
  window.scrollTo({top:0, behavior:'smooth'});
}
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
    document.getElementById('status').innerText="✅ لقيت "+data.length+" نتيجة جوة التطبيق لـ "+q;
  }catch(e){ document.getElementById('status').innerText="❌ النت ضعيف، حاول تاني"; }
}
document.getElementById('searchInput').addEventListener('input', function(){
  clearTimeout(timer);
  let val=this.value;
  timer=setTimeout(()=>doSearch(val), 600);
});
doSearch('فيديوهات سودانية كوميديا');
</script>
</body>
</html>
"""

def search_youtube(q):
    out=[]
    for base in ["https://inv.nadeko.net/api/v1/search", "https://invidious.0011.lt/api/v1/search", "https://vid.puffyan.us/api/v1/search"]:
        try:
            r=requests.get(base, params={"q":q,"type":"video"}, timeout=8)
            if r.status_code==200:
                for e in r.json()[:10]:
                    vid=e.get('videoId','')
                    if not vid: continue
                    out.append({'id':vid,'name':e.get('title',''),'img':f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",'src':'يوتيوب','link':f"https://youtube.com/watch?v={vid}"})
                if out: break
        except: continue
    return out

def search_tiktok(q):
    out=[]
    try:
        r=requests.get("https://www.tikwm.com/api/feed/search", params={"keywords":q,"count":8}, timeout=8)
        for v in r.json().get('data',{}).get('videos',[]):
            out.append({'id':str(v.get('video_id','')),'name':v.get('title') or v.get('desc','فيديو تيك توك'),'img':v.get('cover',''),'src':'تيك توك','link':v.get('play','')})
    except: pass
    return out

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/search')
def search():
    q=request.args.get('q','')
    res = search_youtube(q) + search_tiktok(q)
    return jsonify(res)

if __name__=='__main__':
    port=int(os.environ.get('PORT',10000))
    app.run(host='0.0.0.0',port=port)
  
