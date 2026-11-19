from flask import Flask, request, render_template_string, redirect
import yt_dlp
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>تافلاتات - تحميل فيديو تيك توك</title>
<style>body{font-family:sans-serif;text-align:center;padding:20px;background:#f8f8f8}input{width:90%;padding:15px;border-radius:10px;border:1px solid #ccc}button{padding:15px 30px;background:#000;color:#fff;border:none;border-radius:10px;margin-top:10px;font-size:18px}.box{background:#fff;padding:20px;border-radius:15px;max-width:500px;margin:auto}</style>
</head>
<body><div class="box"><h1>تافلاتات 🔥</h1><p>الصق رابط فيديو تيك توك</p>
<form method="POST"><input name="url" placeholder="الصق الرابط هنا..." required><br><button>تحميل الفيديو</button></form>
{% if video %}<hr><video src="{{video}}" controls style="width:100%"></video><br><br><a href="{{video}}" download><button>حفظ الفيديو</button></a>{% endif %}
{% if error %}<p style="color:red">{{error}}</p>{% endif %}
</div></body></html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    video = None
    error = None
    if request.method == "POST":
        url = request.form.get("url","").strip()
        try:
            ydl_opts = {"format":"mp4","quiet":True,"no_warnings":True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video = info.get("url")
        except Exception as e:
            error = "الرابط ما اشتغل، جرب رابط تاني"
    return render_template_string(HTML, video=video, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
