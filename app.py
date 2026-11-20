from flask import Flask, request, jsonify, send_file, render_template_string
import yt_dlp
import os
import uuid

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>تفلتات - TAFLETAT</title>
<style>
body{background:#0f0f0f;color:white;font-family:sans-serif;text-align:center;padding:20px}
h1{color:#FFD700;font-size:40px;margin:5px} p{color:#aaa}
input{width:90%;max-width:500px;padding:15px;border-radius:15px;border:2px solid #FFD700;background:#222;color:white;font-size:16px;text-align:left;direction:ltr}
button{background:#FFD700;color:black;border:none;padding:15px 30px;border-radius:15px;font-weight:bold;font-size:18px;margin-top:15px;cursor:pointer;width:90%;max-width:500px}
.card{background:#1e1e1e;padding:15px;border-radius:15px;margin:15px auto;max-width:500px}
img{width:100%;border-radius:10px}
a{display:block;background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;margin-top:10px;font-weight:bold}
#msg{color:#ff5555;margin-top:10px}
</style></head>
<body>
<h1>تفلتات 🔥</h1>
<p>تامر ود الدروشاب - حمل من أي رابط زي سناب تيوب</p>
<input id="url" placeholder="الصق أي رابط هنا - تيك توك / يوتيوب / فيس / انستا / تويتر ...">
<br><button onclick="get()">جيب الفيديو 🔥</button>
<div id="msg"></div>
<div id="res"></div>
<script>
async function get(){
 let u=document.getElementById('url').value.trim();
 if(!u){document.getElementById('msg').innerText='الصق رابط أول يا تامر!';return}
 document.getElementById('msg').innerText='جاري جلب الفيديو... اصبر شوية ⏳';
 let r=await fetch('/download',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:u})});
 let d=await r.json();
 if(d.error){document.getElementById('msg').innerText='❌ '+d.error;return}
 document.getElementById('msg').innerText='✅ تم! دوس تحميل';
 document.getElementById('res').innerHTML=`<div class="card"><img src="${d.thumbnail}"><h3>${d.title}</h3><p>${d.uploader} - ${d.platform}</p><a href="/file/${d.file_id}">⬇️ تحميل الفيديو</a></div>`;
}
</script></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url','').strip()
    if not url:
        return jsonify({'error':'ما في رابط! الصق رابط'}), 400
    # لو الرابط ناقص، كملو
    if 'youtube.com/watch' in url and 'v=' not in url:
        return jsonify({'error':'الرابط دا ناقص، انسخو كامل من زر مشاركة'}), 400
    
    file_id = str(uuid.uuid4())[:8]
    out = f"/tmp/{file_id}.mp4"
    opts = {
        'outtmpl': out,
        'format': 'mp4/best[height<=720]/best',
        'quiet': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
        'extractor_args': {'youtube': {'player_client': ['android','web']}},
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                return jsonify({'error':'ما لقينا الفيديو، جرب رابط تاني'}), 400
            return jsonify({
                'title': info.get('title','فيديو')[:80],
                'uploader': info.get('uploader',''),
                'thumbnail': info.get('thumbnail',''),
                'platform': info.get('extractor',''),
                'file_id': file_id
            })
    except Exception as e:
        err = str(e)
        if 'Private' in err or 'private' in err:
            msg = 'الفيديو دا خاص، صاحب الفيديو قافلو، جرب فيديو عام'
        elif 'Login' in err or 'Sign in' in err:
            msg = 'الفيديو دا محتاج تسجيل دخول، جرب فيديو عام تاني'
        elif 'not available' in err:
            msg = 'الفيديو دا محذوف أو ما متوفر في بلدك'
        else:
            msg = 'الرابط دا ما اشتغل، جرب رابط تيك توك أو فيديو عام تاني'
        return jsonify({'error': msg}), 400

@app.route('/file/<file_id>')
def get_file(file_id):
    path = f"/tmp/{file_id}.mp4"
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name='taflatat.mp4')
    return 'الملف انتهى، حملو تاني', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
