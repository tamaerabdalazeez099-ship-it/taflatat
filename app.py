from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import uuid

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تفلتات - تحميل تيك توك بدون علامة مائية</title>
<style>
body{font-family:Arial;background:#111;color:white;text-align:center;padding:20px;margin:0}
h1{font-size:32px;margin:10px}
h1 span{color:#25F4EE}
.box{background:#1e1e1e;padding:20px;border-radius:20px;max-width:500px;margin:auto}
input{width:90%;padding:15px;border-radius:12px;border:none;font-size:16px;margin:10px 0}
button{background:#FE2C55;color:white;border:none;padding:15px 30px;border-radius:12px;font-size:18px;font-weight:bold;width:95%}
.footer{margin-top:20px;color:#aaa;font-size:14px;line-height:1.8}
.share{padding:20px;text-align:center;background:#1e1e1e;border-radius:15px;margin-top:15px;max-width:500px;margin-left:auto;margin-right:auto}
</style>
</head>
<body>
<h1>تفلتات <span>🔥</span></h1>
<p>نزل اي فيديو من تيك توك بدون علامة مائية - مجاناً</p>
<div class="box">
<form method="POST" action="/download">
<input type="text" name="url" placeholder="الصق رابط التيك توك هنا..." required>
<br><button type="submit">⬇️ تحميل الآن</button>
</form>
</div>
<div class="share">
<h3>🔥 عجبك تطبيق تفلتات؟</h3>
<p style="color:#aaa;">ثبتو عندك وارسلو لأصحابك</p>
<a href="https://wa.me/?text=نزل تطبيق تفلتات 🔥 صنع في السودان 🇸🇩 نزل اي فيديو من تيك توك بدون علامة مائية مجان: https://taflatat.onrender.com" target="_blank" style="display:block;background:#25D366;color:white;padding:14px;border-radius:12px;font-size:18px;font-weight:bold;text-decoration:none;margin-bottom:10px;">📤 شارك في الواتساب</a>
<a href="https://www.facebook.com/sharer/sharer.php?u=https://taflatat.onrender.com" target="_blank" style="display:block;background:#1877F2;color:white;padding:14px;border-radius:12px;font-size:18px;font-weight:bold;text-decoration:none;">📘 شارك في الفيسبوك</a>
</div>
<div class="footer">صنع بواسطة <b style="color:white;">تامر ود الدروشاب</b><br>صنع في السودان 🇸🇩 | الدروشاب - أم درمان<br>تفلتات © 2026</div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "الصق الرابط اولاً"
    filename = f"{uuid.uuid4()}.mp4"
    ydl_opts = {'format': 'mp4', 'outtmpl': filename, 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(filename, as_attachment=True, download_name="taflatat.mp4")
    except Exception as e:
        return f"حصل خطأ، جرب رابط تاني: {e}"
    finally:
        if os.path.exists(filename):
            try: os.remove(filename)
            except: pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
