from flask import Flask, render_template_string, jsonify, request
import os, requests
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تفلتات - تامر ود الدروشاب</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family: Tahoma; }
body { background:#000; color:#fff; padding-bottom:90px; border:2px solid #ffcc00; min-height:100vh; }
.top { display:flex; justify-content:space-between; padding:12px 15px; font-size:28px; }
.center { text-align:center; }
.crown { font-size:48px; }
.center h2 { font-size:28px; margin:5px 0; }
.center p { color:#ccc; font-size:14px; }
.search-box { background:#e8e8e8; margin:18px 15px 10px; border-radius:12px; padding:14px; display:flex; align-items:center; justify-content:center; gap:8px; }
.search-box input { background:transparent; border:none; outline:none; width:100%; font-size:17px; text-align:center; color:#000; font-weight:bold; }
.btns { display:flex; gap:8px; overflow-x:auto; padding:10px 15px; }
.btns button { white-space:nowrap; background:#ffcc00; color:#000; border:none; padding:11px 22px; border-radius:20px; font-size:16px; font-weight:bold; }
.btns button.active { background:#fff; }
.big-btn { background:linear-gradient(#ffcc00,#ff9900); margin:0 15px; text-align:center; padding:16px; border-radius:12px; color:#000; font-weight:bold; font-size:18px; cursor:pointer; }
.cards { display:grid; grid-template-columns:1fr 1fr; gap:12px; padding:15px; }
.card { background:#111; border-radius:16px; overflow:hidden; border:1px solid #333; }
.card img { width:100%; height:170px; object-fit:cover; }
.card p { padding:10px; font-size:13px; text-align:center; min-height:50px; }
.card button { width:90%; margin:0 5% 10px; background:#ffcc00; border:none; padding:9px; border-radius:10px; font-weight:bold; }
#player { display:none; position:fixed; bottom:75px; left:10px; right:10px; background:#1a1a1a; border:2px solid #ffcc00; border-radius:15px; padding:10px; z-index:99; text-align:center; }
.bottom { position:fixed; bottom:0; left:0; right:0; background:#000; display:flex; justify-content:space-around; padding:12px 0; border-top:1px solid #333; }
.bottom div { text-align:center; font-size:12px; color:#fff; }
.bottom span { font-size:24px; display:block; }
</style>
</head>
<body>
<div class="top"><span>🇸🇩</span><span>🇸🇩</span></div>
<div class="center"><div class="crown">👑</div><h2>تامر ود الدروشاب</h2><p>مطور ومصمم المحتوى • الحساب الملكي</p></div>
<div class="search-box">🔍 <input id="searchInput" placeholder="اكتب اسم أي حاجة - اغنية، فيديو" onkeyup="if(event.key==='Enter')searchNow()"></div>
<div class="btns"><button onclick="setType('all',this)" class="active">الكل</button><button onclick="setType('song',this)">اغاني 🎵</button><button onclick="setType('video',this)">فيديو ▶️</button><button onclick="setType('photo',this)">صور 🖼️</button><button onclick="setType('game',this)">العاب 🎮</button></div>
<div class="big-btn" onclick="searchNow()">🔍 ابحث طوالي - بدون رابط</div>
<div id="status" style="text-align:center;padding:12px;color:#ffcc00;font-weight:bold;"></div>
<div id="player"><p id="nowPlaying"></p><div id="videoBox"></div><br><button onclick="closePlayer()" style="background:#ff3333;color:#fff;border:none;padding:7px 20px;border-radius:10px;">اقفل ✖️</button></div>
<div class="cards" id="list"></div>
<div class="bottom"><div><span>🏠</span>الرئيسية</div><div><span>📚</span>المكتبة</div><div><span>⬇️</span>التحميلات</div><div><span>⚙️</span>الاعدادات</div></div>
<script>
let currentType='all';
function setType(t,el){ currentType=t; document.querySelectorAll('.btns button').forEach(b=>b.classList.remove('active')); el.classList.add('active'); searchNow(); }
function render(list){
  let box=document.getElementById('list'); box.innerHTML="";
  if(!list.length){ box.innerHTML="<p style='grid-column:1/3;text-align:center;'>❌ ما لقيت حاجة، جرب كلمة تانية</p>"; return; }
  list.forEach(s=>{ box.innerHTML+=`<div class="card"><img src="${s.img}"><p>${s.name}</p><button onclick="playSong('${s.id}','${s.name.replace(/'/g,'')}')">▶ تشغيل طوالي</button></div>`; });
}
function playSong(id,name){
  document.getElementById('player').style.display="block";
  document.getElementById('nowPlaying').innerText="🎵 شغال هسي: "+name;
  document.getElementById('videoBox').innerHTML=`<iframe width="100%" height="220" src="https://www.youtube.com/embed/${id}?autoplay=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
}
function closePlayer(){ document.getElementById('player').style.display="none"; document.getElementById('videoBox').innerHTML=""; }
async function searchNow(){
  let q=document.getElementById('searchInput').value.trim();
  if(!q){ document.getElementById('status').innerText="اكتب اسم أي حاجة فوق 👆"; return; }
  let query=q; if(currentType==='song') query=q+" اغنية سودانية"; if(currentType==='video') query=q+" فيديو";
  document.getElementById('status').innerText="🔍 جاري البحث في يوتيوب عن: "+q+"... استنى 5 ثواني";
  try{
    let res=await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    let data=await res.json(); render(data);
    document.getElementById('status').innerText="✅ لقيت "+data.length+" نتيجة لـ "+q;
  }catch(e){ document.getElementById('status').innerText="❌ النت ضعيف، حاول تاني"; }
}
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
    # جرب 3 سيرفرات يوتيوب، لو واحد وقف التاني يشتغل
    instances = ["https://inv.nadeko.net/api/v1/search", "https://invidious.0011.lt/api/v1/search", "https://vid.puffyan.us/api/v1/search"]
    for base in instances:
        try:
            r = requests.get(base, params={"q": q, "type": "video"}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                out = []
                for e in data[:12]:
                    vid = e.get('videoId','')
                    if not vid: continue
                    out.append({'id': vid, 'name': e.get('title',''), 'img': f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"})
                if out:
                    return jsonify(out)
        except:
            continue
    return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
