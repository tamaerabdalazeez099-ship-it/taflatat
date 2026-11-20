from flask import Flask, request, jsonify, send_file
import yt_dlp, os, uuid

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تفلتات - TAFLTAT</title>
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#FFD700">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial;background:#000;color:#fff}
/* الخلفية برا - Splash */
#splash{position:fixed;inset:0;background:#000 url('https://images.unsplash.com/photo-1509099863732-ef4bff19e808') center/cover no-repeat;display:flex;flex-direction:column;justify-content:center;align-items:center;z-index:9999;text-align:center}
#splash:before{content:'';position:absolute;inset:0;background:rgba(0,0,0,0.75)}
#splash *{position:relative;z-index:1}
#splash h1{color:#FFD700;font-size:75px;margin:0}
#splash h2{color:#fff;letter-spacing:8px;margin:5px}
#splash p{color:#FFD700;font-size:18px}
.loader{width:80%;height:14px;background:#333;border-radius:20px;overflow:hidden;margin-top:20px}
.loader div{width:60%;height:100%;background:gold}
/* الخلفية جوة */
#app{display:none;min-height:100vh;background:linear-gradient(180deg,#000 0%,#1a1a1a 50%,#000 100%);padding-bottom:30px}
.top{background:linear-gradient(135deg,#007A3D,#FFD700,#D21034);padding:20px;text-align:center}
.top h1{font-size:42px;margin:0;color:#FFD700;text-shadow:2px 2px #000}
.top p{margin:5px;color:#fff;font-weight:bold}
.badge{background:#FFD700;color:#000;padding:5px 15px;border-radius:20px;display:inline-block;font-weight:bold}
.box{margin:-10px 15px 15px;background:#1a1a1a;border:2px solid #FFD700;border-radius:20px;padding:15px}
input{width:100%;padding:16px;border-radius:14px;border:2px solid #FFD700;font-size:18px;text-align:center}
.btn{width:100%;padding:16px;border:none;border-radius:14px;font-size:20px;font-weight:bold;margin-top:10px}
.btn-gold{background:#FFD700;color:#000}
.btn-white{background:#fff;color:#000}
.card{background:#222;border:1px solid #FFD700;border-radius:16px;padding:12px;margin:15px}
.card img{width:100%;border-radius:12px}
.card b{display:block;padding:8px;font-size:14px}
#msg{text-align:center;color:#FFD700;margin:10px}
</style>
</head>
<body>

<!-- 1. الخلفية برا -->
<div id="splash">
  <h1>تفلتات</h1>
  <h2>TAFLTAT</h2>
  <p>تامر ود الدروشاب - صنع في السودان 🇸🇩</p>
  <div class="loader"><div></div></div>
  <p style="color:#fff">Loading... 60%</p>
</div>

<!-- 2. الخلفية جوة -->
<div id="app">
  <div class="top">
    <div class="badge">🇸🇩 فخر السودان 🇸🇩</div>
    <h1>تفلتات</h1>
    <p>الصق أي رابط - شاهد - حمل</p>
  </div>

  <div class="box">
    <input id="q" placeholder="🔍 الصق الرابط هنا... يوتيوب، تيك توك، فيس، انستا">
    <button class="btn btn-gold" onclick="getVideo()">▶️ شغل الرابط</button>
    <button class="btn btn-white" onclick="downloadVideo()">⬇️ تنزيل الفيديو</button>
    <div id="msg"></div>
  </div>

  <div class="card">
    <img src="https://images.unsplash.com/photo-1509099863732-ef4bff19e808">
    <b>🔥 حكاية من السودان - رحلة في نهر النيل</b>
    <button class="btn btn-gold" onclick="document.getElementById('q').value='https://www.youtube.com/watch?v=dQw4w9WgXcQ';getVideo()">شاهد الآن</button>
  </div>

  <div class="card">
    <img src="https://images.unsplash.com/photo-1516450360452-9312f5e86fc7">
    <b>🎵 تراث وناس - أغاني سودانية</b>
    <button class="btn btn-gold">شاهد الآن</button>
  </div>
</div>

<script>
setTimeout(()=>{document.getElementById('splash').style.display='none';document.getElementById('app').style.display='block'},3000);
async function getVideo(){
  let url=document.getElementById('q').value;
  if(!url){alert('الصق رابط أول!');return;}
  document.getElementById('msg').innerText='⏳ جاري جلب الفيديو...';
  let r=await fetch('/info?url='+encodeURIComponent(url));
  let d=await r.json();
  if(d.error){document.getElementById('msg').innerText='❌ '+d.error;return;}
  document.getElementById('msg').innerHTML='<div class="card"><img src="'+(d.thumb||'')+'"><b>'+d.title+'</b><video controls style="width:100%" src="'+d.video_url+'"></video><br><a href="/download?url='+encodeURIComponent(url)+'" style="color:gold;font-size:18px">⬇️ تنزيل بجودة عالية</a></div>';
}
function downloadVideo(){
  let url=document.getElementById('q').value;
  if(!url){alert('الصق رابط أول!');return;}
  window.location='/download?url='+encodeURIComponent(url);
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "تفلتات TAFLTAT",
        "short_name": "تفلتات",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#000000",
        "theme_color": "#FFD700",
        "icons": [{"src": "https://cdn-icons-png.flaticon.com/512/2983/2983815.png","sizes": "512x512","type": "image/png"}]
    })

@app.route('/info')
def info():
    url = request.args.get('url','')
    try:
        with yt_dlp.YoutubeDL({'quiet':True,'skip_download':True}) as ydl:
            data = ydl.extract_info(url, download=False)
            return jsonify({"title": data.get('title','تفلتات'), "thumb": data.get('thumbnail',''), "video_url": data.get('url','')})
    except Exception as e:
        return jsonify({"error": "ما قدرنا نجيب الفيديو، جرب رابط تاني"})

@app.route('/download')
def download():
    url = request.args.get('url','')
    try:
        fname = f"/tmp/{uuid.uuid4()}.mp4"
        with yt_dlp.YoutubeDL({'outtmpl': fname, 'format': 'best[ext=mp4]/best'}) as ydl:
            ydl.download([url])
        return send_file(fname, as_attachment=True, download_name="tafltat.mp4")
    except Exception as e:
        return f"خطأ في التنزيل: {e}", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
