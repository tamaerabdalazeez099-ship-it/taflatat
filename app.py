from flask import Flask, request, jsonify, send_file
import yt_dlp, os, uuid

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
body{background:#000;color:#fff;overflow-x:hidden}
/* --- برا - Splash --- */
#splash{position:fixed;inset:0;z-index:999;background:radial-gradient(circle,#FFD700,#FF8C00,#000);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;animation:fade 3.5s forwards}
#splash h1{font-size:70px;color:#000;text-shadow:0 0 20px #fff;animation:pop 1s}
#splash h2{font-size:32px;color:#000;margin-top:10px}
#splash p{font-size:22px;color:#fff;background:#000;padding:10px 20px;border-radius:30px;margin-top:20px;font-weight:bold}
@keyframes pop{0%{transform:scale(0)}100%{transform:scale(1)}}
@keyframes fade{0%,80%{opacity:1}100%{opacity:0;visibility:hidden}}
/* --- جوا --- */
.top{background:linear-gradient(135deg,#FFD700,#FF6B00,#FFD700);padding:25px 15px 35px;text-align:center;border-radius:0 0 30px 30px;box-shadow:0 10px 30px #FFD70055}
.top .badge{background:#000;color:#FFD700;padding:6px 18px;border-radius:30px;display:inline-block;font-weight:bold}
.top h1{font-size:58px;color:#000;margin:10px 0;text-shadow:2px 2px 0 #fff}
.top .name{font-size:28px;font-weight:900;color:#000;background:#fff;padding:8px 20px;border-radius:15px;display:inline-block;box-shadow:0 5px 15px #0005}
.top p{margin-top:10px;color:#000;font-weight:bold;font-size:18px}
.box{margin:-20px 15px 15px;background:#111;border:2px solid #FFD700;border-radius:25px;padding:20px;box-shadow:0 10px 30px #000}
input{width:100%;padding:16px;border-radius:15px;border:2px solid #FFD700;font-size:17px;text-align:center;outline:none}
.btn{width:100%;padding:16px;border:none;border-radius:15px;font-size:20px;font-weight:900;margin-top:12px;cursor:pointer}
.btn-play{background:linear-gradient(#FFD700,#FF8C00);color:#000}
.btn-dl{background:#fff;color:#000}
.card{background:#1a1a1a;border:1px solid #FFD70088;border-radius:20px;padding:15px;margin:15px;overflow:hidden}
.card img{width:100%;border-radius:15px}
.card h3{margin:12px 0;color:#FFD700}
.footer{background:linear-gradient(#FFD700,#FF8C00);color:#000;text-align:center;padding:25px;margin-top:20px;border-radius:30px 30px 0 0}
.footer b{font-size:26px}
.footer p{margin-top:5px;font-weight:bold}
video{width:100%;border-radius:15px;margin-top:10px}
</style>
</head>
<body>
<!-- برا -->
<div id="splash">
<h1>تفلتات 🔥</h1>
<h2>TAFLTAT</h2>
<p>تامر ود الدروشاب ❤️🇸🇩</p>
<p style="background:transparent;color:#000;font-size:16px;margin-top:10px">فخر السودان - أقوى تطبيق في السودان</p>
</div>

<!-- جوا -->
<div class="top">
<div class="badge">🇸🇩 فخر السودان 🇸🇩</div>
<h1>تفلتات</h1>
<div class="name">تامر ود الدروشاب 👑</div>
<p>الصق أي رابط - شاهد - حمل - استمتع</p>
<p>يوتيوب • تيك توك • فيسبوك • انستقرام • تويتر</p>
</div>

<div class="box">
<input id="url" placeholder="🔍 الصق الرابط هنا... يوتيوب، تيك توك، فيس...">
<button class="btn btn-play" onclick="play()">▶️ شغل الرابط</button>
<button class="btn btn-dl" onclick="dl()">⬇️ تنزيل الفيديو</button>
<div id="result"></div>
</div>

<div class="card">
<img src="https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=800">
<h3>🔥 حفلة تفلتات - أقوى حفلة</h3>
<button class="btn btn-play" onclick="document.getElementById('url').value='https://www.youtube.com/watch?v=dQw4w9WgXcQ';play()">شاهد الآن</button>
</div>

<div class="card">
<img src="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800">
<h3>🎵 أغاني سودانية - تفلتات</h3>
<button class="btn btn-play" onclick="document.getElementById('url').value='https://www.youtube.com/watch?v=dQw4w9WgXcQ';play()">شاهد الآن</button>
</div>

<div class="footer">
<b>تفلتات - تامر ود الدروشاب 👑</b>
<p>صنع بحب في السودان 🇸🇩 | © 2026</p>
<p>أي رابط يشتغل هنا - جرب بنفسك!</p>
</div>

<script>
async function play(){
let u=document.getElementById('url').value;
if(!u) return alert('الصق رابط أول!');
document
