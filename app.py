from flask import Flask, request, render_template_string
import yt_dlp
import os
app = Flask(__name__)
HTML = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>تفلتات - تحميل فيديو تيك توك</title>
<style>
body{font-family:sans-serif;background:#0f0f0f;color:#fff;text-align:center;padding:20px}
h1{color:#25F4EE}
.box{background:#1e1e1e;padding:20px;border-radius:15px;max-width:500px;margin:auto}
input{width:90%;padding:12px;border-radius:10px;border:none;margin:10px 0;font-size:16px}
button{background:#FE2C55;color:#fff;border:none;padding:12px 25px;border-radius:10px;font-size:17px;cursor:pointer;width:95%}
video{width:100%;border-radius:12px;margin-top:15px}
a.dl{display:block;background:#25F4EE;color:#000;padding:12px;border-radius:10px;margin-top:12px;text-decoration:none;font-weight:bold}
.err{color:#ff5b5b;margin-top:10px}
</style>
</head>
<body>
<div class="box">
<h1>🎬 تفلتات</h1>
<p>الصق رابط فيديو تيك توك وحملو بدون علامة مائية</p>
<form method="POST">
<input name="url" placeholder="الصق رابط التيك توك هنا..." required>
<button type="submit">تحميل الفيديو ⬇️</button>
</form>
{% if error %}<div class="err">{{ error }}</div>{% endif %}
{% if video %}
<video controls src="{{ video }}"></video>
<a class="dl" href="{{ video }}" target="_blank">📥 تحميل الفيديو الآن</a>
{% endif %}
</div>
</body>
</html>
"""
@app.route("/", methods=["GET", "POST"])
def index():
    video = None
    error = None
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if not url:
            error = "الصق الرابط اول"
        else:
            try:
                ydl_opts = {'quiet': True,'no_warnings': True,'format': 'best','noplaylist': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video = info.get("url")
                    if not video:
                        formats = info.get("formats", [])
                        if formats:
                            video = formats[-1].get("url")
                    if not video:
                        error = "ما قدرت اجيب الفيديو، جرب رابط تاني"
            except Exception as e:
                error = "الرابط غلط او الفيديو خاص، جرب رابط تاني"
    return render_template_string(HTML, video=video, error=error)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)