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
body { background:#000; color:#fff; padding-bottom:90px; }
.top-flags { display:flex; justify-content:space-between; padding:10px 15px; font-size:32px; }
.logo { text-align:center; font-size:70px; font-weight:900; color:#ffcc00; text-shadow:0 0 20px #ffcc00; line-height:1; }
.stars { text-align:center; color:#ffcc00; font-size:22px; letter-spacing:10px; }
.white-card { background:#fff; color:#000; margin:20px 15px; border-radius:18px; border:2px solid #ffcc00; text-align:center; padding:25px 10px; }
.white-card .crown { font-size:45px; }
.white-card h2 { font-size:30px; margin:10px 0 5px; }
.white-card p { color:#b8962e; font-size:15px; }
.search-area { background:#0a0a0a; border:2px solid #ffcc00; margin:0 15px; border-radius:18px; padding:15px; }
.search-box { background:#000; border:2px solid #ffcc00; border-radius:14px; padding:14px; display:flex; align-items:center; justify-content:center; }
.search-box input { background:transparent; border:none; outline:none; color:#fff; width:100%; font-size:18px; text-align:center; }
.btns { display:flex; gap:8px; overflow-x:auto; padding:15px 0 10px; }
.btns button { white-space:nowrap; background:#000; color:#ffcc00; border:1.5px solid #ffcc00; padding:12px 20px; border-radius:25px; font-size:16px; font-weight:bold; }
.btns button.active { background:#ffcc00; color:#000; }
.big-btn { background:linear-gradient(#ffcc00,#ff9900); text-align:center; padding:16px; border-radius:14px; color:#000; font-weight:bold; font-size:19px; cursor:pointer; }
.cards { display:grid; grid-template-columns:1fr 1fr; gap:12px; padding:15px; }
.card { background:#111; border-radius:16px; overflow:hidden; border:1px solid #333; }
.card img { width:100%; height:180px; object-fit:cover; }
.card p { padding:10px; font-size:14px; text-align:center; }
.card button { width:90%; margin:0 5% 10px; background:#ffcc00; border:none; padding:9px; border-radius:10px; font-weight:bold; }
#player { display:none; position:fixed; bottom:75px; left:10px; right:10px; background:#1a1a1a; border:2px solid #ffcc00; border-radius:15px; padding:10px; z-index:99; text-align:center; }
#player audio { width:100%; }
.bottom { position:fixed; bottom:0; left:0; right:0; background:#000; display:flex; justify-content:space-around; padding:12px 0; border-top:1px solid #333; }
.bottom div { text-align:center; font-size:13px; color:#ffcc00; }
.bottom span { font-size:24px; display:block; }
</style>
</head>
<body>
<div class="top-flags"><span>🇸🇩</span><span>🇸🇩</span></div>
<div class="stars">✦✦✦</div>
<div class="logo">تفلتات</div>
<div class="stars">✦✦✦</div>
<div class="white-card"><div class="crown">👑</div><h2>تامر ود الدروشاب</h2><p>مطور ومصمم المحتوى • الحساب الملكي</p></div>
<div class="search-area">
<div class="search-box"><input id="searchInput" placeholder="🔍 اكتب اسم أي حاجة" onkeyup="searchNow()"></div>
<div class="btns"><button class="active">فيديو ▶️</button><button>اغاني 🎵</button><button>صور 🖼️</button><button>العاب 🎮</button><button>المزيد</button></div>
<div class="big-btn" onclick="searchNow()">🔍 ابحث طوالي - بدون رابط</div>
</div>
<div id="player"><p id="nowPlaying">🎵 بتشغل...</p><audio id="audioPlayer" controls></audio><br><button onclick="closePlayer()" style="background:#ff3333;color:#fff;border:none;padding:5px 15px;border-radius:10px;margin-top:5px;">اقفل</button></div>
<div class="cards" id="list"></div>
<div class="bottom"><div><span>🏠</span>الرئيسية</div><div><span>📚</span>المكتبة</div><div><span>⬇️</span>التحميلات</div><div><span>⚙️</span>الاعدادات</div></div>
<script>
const songs = [
  { name: "أغنية سودانية 1 - تامر", img: "https://picsum.photos/300/200?random=11", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" },
  { name: "أغنية سودانية 2 - الدروشاب", img: "https://picsum.photos/300/200?random=12", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3" },
  { name: "أغنية سودانية 3 - جنقو", img: "https://picsum.photos/300/200?random=13", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3" },
  { name: "أغنية سودانية 4 - تفلتات", img: "https://picsum.photos/300/200?random=14", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3" },
];
function render(list){
  let box = document.getElementById('list'); box.innerHTML = "";
  list.forEach(s => { box.innerHTML += `<div class="card"><img src="${s.img}"><p>${s.name}</p><button onclick="playSong('${s.url}','${s.name}')">▶ تشغيل طوالي</button></div>`; });
}
function playSong(url, name){
  document.getElementById('player').style.display = "block";
  document.getElementById('nowPlaying').innerText = "🎵 شغال هسي: " + name;
  let a = document.getElementById('audioPlayer'); a.src = url; a.play();
}
function closePlayer(){ document.getElementById('player').style.display = "none"; document.getElementById('audioPlayer').pause(); }
function searchNow(){
  let q = document.getElementById('searchInput').value.toLowerCase();
  let f = songs.filter(s => s.name.toLowerCase().includes(q));
  render(f.length ? f : songs);
}
render(songs);
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
