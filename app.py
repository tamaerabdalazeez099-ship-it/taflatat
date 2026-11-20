<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تفلتات - تامر ود الدروشاب</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
body { background:#0a0a0a; color:#fff; padding-bottom:90px; }
.top { text-align:center; padding:20px 10px 10px; }
.flags { display:flex; justify-content:space-between; padding:0 15px; font-size:24px; }
.crown { font-size:50px; }
h1 { font-size:26px; margin:5px 0; }
.sub { color:#d4af37; font-size:13px; margin-bottom:15px; }
.search-box { background:#222; margin:10px 15px; border-radius:12px; display:flex; align-items:center; padding:12px; }
.search-box input { background:transparent; border:none; outline:none; color:#fff; width:100%; font-size:16px; text-align:center; }
.btns { display:flex; gap:8px; justify-content:center; padding:10px; flex-wrap:wrap; }
.btns button { background:#ffcc00; border:none; padding:10px 18px; border-radius:20px; font-weight:bold; font-size:15px; cursor:pointer; }
.btns button.active { background:#fff; }
.big-btn { background:linear-gradient(#ffcc00,#ff9900); margin:5px 15px; text-align:center; padding:14px; border-radius:12px; color:#000; font-weight:bold; font-size:17px; cursor:pointer; }
.cards { display:grid; grid-template-columns:1fr 1fr; gap:10px; padding:15px; }
.card { background:#1a1a1a; border-radius:15px; overflow:hidden; border:1px solid #333; }
.card img { width:100%; height:160px; object-fit:cover; }
.card p { padding:8px; font-size:14px; text-align:center; }
.card button { width:90%; margin:0 5% 10px; background:#ffcc00; border:none; padding:8px; border-radius:10px; font-weight:bold; cursor:pointer; }
#player { display:none; position:fixed; bottom:70px; left:10px; right:10px; background:#1a1a1a; border:2px solid #ffcc00; border-radius:15px; padding:10px; z-index:99; text-align:center; }
#player audio { width:100%; }
.bottom { position:fixed; bottom:0; left:0; right:0; background:#111; display:flex; justify-content:space-around; padding:12px 0; border-top:1px solid #333; }
.bottom div { text-align:center; font-size:12px; cursor:pointer; }
.bottom span { font-size:22px; display:block; }
</style>
</head>
<body>

<div class="flags"><span>🇸🇩</span><span>🇸🇩</span></div>
<div class="top">
<div class="crown">👑</div>
<h1>تامر ود الدروشاب</h1>
<div class="sub">مطور ومصمم المحتوى • الحساب الملكي</div>
</div>

<div class="search-box">
<span>🔍</span>
<input id="searchInput" placeholder="اكتب اسم أي حاجة" onkeyup="searchNow()">
</div>

<div class="btns">
<button onclick="show('games')">العاب</button>
<button onclick="show('pics')">صور</button>
<button onclick="show('songs')" class="active">اغاني</button>
<button onclick="show('videos')">فيديو</button>
</div>

<div class="big-btn" onclick="searchNow()">🔍 ابحث طوالي - بدون رابط</div>

<div id="player">
<p id="nowPlaying">🎵 بتشغل...</p>
<audio id="audioPlayer" controls></audio>
<button onclick="closePlayer()" style="background:#ff3333;color:#fff;border:none;padding:5px 15px;border-radius:10px;margin-top:5px;">اقفل</button>
</div>

<div class="cards" id="list"></div>

<div class="bottom">
<div><span>🏠</span>الرئيسية</div>
<div><span>📚</span>المكتبة</div>
<div><span>⬇️</span>التحميلات</div>
<div><span>⚙️</span>الاعدادات</div>
</div>

<script>
// هنا الأغاني - تدوس تشتغل طوالي، ما بتنزل
const songs = [
  { name: "أغنية سودانية 1 - تامر", img: "https://via.placeholder.com/300x200?text=تفلتات", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" },
  { name: "أغنية سودانية 2 - الدروشاب", img: "https://via.placeholder.com/300x200?text=تفلتات", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3" },
  { name: "أغنية سودانية 3 - جنقو", img: "https://via.placeholder.com/300x200?text=تفلتات", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3" },
  { name: "أغنية سودانية 4 - تفلتات", img: "https://via.placeholder.com/300x200?text=تفلتات", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3" },
];

function render(list){
  let box = document.getElementById('list');
  box.innerHTML = "";
  list.forEach(s => {
    box.innerHTML += `
    <div class="card">
      <img src="${s.img}">
      <p>${s.name}</p>
      <button onclick="playSong('${s.url}','${s.name}')">▶ تشغيل طوالي</button>
    </div>`;
  });
}
function playSong(url, name){
  let p = document.getElementById('player');
  let a = document.getElementById('audioPlayer');
  document.getElementById('nowPlaying').innerText = "🎵 شغال هسي: " + name;
  p.style.display = "block";
  a.src = url;
  a.play();
}
function closePlayer(){
  document.getElementById('player').style.display = "none";
  document.getElementById('audioPlayer').pause();
}
function searchNow(){
  let q = document.getElementById('searchInput').value.toLowerCase();
  let f = songs.filter(s => s.name.toLowerCase().includes(q));
  render(f.length ? f : songs);
}
function show(type){
  if(type=='songs') render(songs);
  else alert("القسم دا جاي قريب إن شاء الله ❤️");
}
render(songs);
</script>
</body>
</html>
