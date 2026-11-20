from flask import Flask, render_template_string
import os
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
.big-btn { background:linear-gradient(#ffcc00,#ff9900); margin:0 15px; text-align:center; padding:16px; border-radius:12px; color:#000; font-weight:bold; font-size:18px; cursor:pointer; }
.cards { display:grid; grid-template-columns:1fr 1fr; gap:12px; padding:15px; }
.card { background:#111; border-radius:16px; overflow:hidden; border:1px solid #333; }
.card img { width:100%; height:190px; object-fit:cover; }
.card p { padding:10px; font-size:14px; text-align:center; }
.card button { width:90%; margin:0 5% 10px; background:#ffcc00; border:none; padding:9px; border-radius:10px; font-weight:bold; }
#player { display:none; position:fixed; bottom:75px; left:10px; right:10px; background:#1a1a1a; border:2px solid #ffcc00; border-radius:15px; padding:10px; z-index:99; text-align:center; }
#player audio { width:100%; }
.bottom { position:fixed; bottom:0; left:0; right:0; background:#000; display:flex; justify-content:space-around; padding:12px 0; border-top:1px solid #333; }
.bottom div { text-align:center; font-size:12px; color:#fff; }
.bottom span { font-size:24px; display:block; }
</style>
</head>
<body>
<div class="top"><span>🇸🇩</span><span>🇸🇩</span></div>
<div class="center"><div class="crown">👑</div><h2>تامر ود الدروشاب</h2><p>مطور ومصمم المحتوى • الحساب الملكي</p></div>
<div class="search-box">🔍 <input id="searchInput" placeholder="اكتب اسم أي حاجة" onkeyup="if(event.key==='Enter')searchNow()"></div>
<div class="btns"><button>العاب</button><button>صور</button><button>صور</button><button>اغاني</button><button>فيديو</button></div>
<div class="big-btn" onclick="searchNow()">🔍 ابحث طوالي - بدون رابط</div>
<div id="status" style="text-align:center;padding:10px;color:#ffcc00;"></div>
<div id="player"><p id="nowPlaying">🎵 بتشغل...</p><audio id="audioPlayer" controls></audio><br><button onclick="closePlayer()" style="background:#ff3333;color:#fff;border:none;padding:5px 15px;border-radius:10px;margin-top:5px;">اقفل</button></div>
<div class="cards" id="list"></div>
<div class="bottom"><div><span>🏠</span>الرئيسية</div><div><span>📚</span>المكتبة</div><div><span>⬇️</span>التحميلات</div><div><span>⚙️</span>الاعدادات</div></div>
<script>
const defaultSongs = [
  { name: "تفلتات - تامر ود الدروشاب", img: "https://picsum.photos/300/300?random=21", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" },
  { name: "تفلتات - الدروشاب", img: "https://picsum.photos/300/300?random=22", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3" },
];
function render(list){
  let box = document.getElementById('list'); box.innerHTML = "";
  list.forEach(s => { box.innerHTML += `<div class="card"><img src="${s.img}"><p>${s.name}</p><button onclick="playSong('${s.url}','${s.name.replace(/'/g,'')}')">▶ تشغيل طوالي</button></div>`; });
}
function playSong(url, name){
  document.getElementById('player').style.display = "block";
  document.getElementById('nowPlaying').innerText = "🎵 شغال هسي: " + name;
  let a = document.getElementById('audioPlayer'); a.src = url; a.play();
}
function closePlayer(){ document.getElementById('player').style.display = "none"; document.getElementById('audioPlayer').pause(); }
async function searchNow(){
  let q = document.getElementById('searchInput').value.trim();
  if(!q){ render(defaultSongs); return; }
  document.getElementById('status').innerText = "🔍 جاري البحث عن: " + q + "...";
  try{
    let res = await fetch(`https://itunes.apple.com/search?term=${encodeURIComponent(q)}&media=music&limit=12&country=SA`);
    let data = await res.json();
    if(data.results && data.results.length){
      let list = data.results.map(r => ({ name: r.trackName + " - " + r.artistName, img: r.artworkUrl100 ? r.artworkUrl100.replace('100x100','300x300') : 'https://picsum.photos/300/300?random=99', url: r.previewUrl }));
      render(list);
      document.getElementById('status').innerText = "✅ لقيت " + list.length + " نتيجة لـ " + q;
    } else { document.getElementById('status').innerText = "❌ ما لقيت نتيجة"; render(defaultSongs); }
  }catch(e){ document.getElementById('status').innerText = "❌ النت ضعيف، حاول تاني"; }
}
render(defaultSongs);
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
  
