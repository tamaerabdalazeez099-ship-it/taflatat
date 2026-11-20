

from flask import Flask, request
import yt_dlp
import os
app = Flask(__name__)
HTML = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>تفلتات - حمل من أي موقع</title>
<style>
body{font-family:sans-serif;background:#0f0f0f;color:#fff;text-align:center;padding:0;margin:0}
.top-ad{background:#222;padding:12px;font-size:13px;color:#aaa}
h1{color:#25F4EE;font-size:38px;margin:10px 0 0}
h1 span{color:#FE2C55}
.box{background:#1e1e1e;padding:20px;border-radius:16px;max-width:520px;margin:15px auto}
input{width:92%;padding:15px;border-radius:10px;border:none;font-size:16px;text-align:center}
button{background:#FE2C55;color:#fff;border:none;padding:15px 25px;border-radius:10px;font-size:18px;margin-top:12px;width:96%;font-weight:bold}
select{width:96%;padding:12px;border-radius:10px;margin-top:10px;font-size:16px;text-align:center}
video{width:100%;border-radius:12px;margin-top:15px}
a.dl{display:block;background:#25F4EE;color:#000;padding:15px;border-radius:10px;margin-top:12px;text-decoration:none;font-weight:bold}
.sites{font-size:13px;color:#aaa}
.footer{padding:20px;color:#888;font-size:14px}
.footer b{color:#fff}
</style></head>
<body>
<div class="top-ad">مساحة إعلانية - تفلتات</div>
<div class="box">
<h1>تفلتات <span>🔥</span></h1>
<p style="color:#25F4EE;font-weight:bold">حمل من أي موقع - بدون علامة مائية</p>
<p class="sites">تيك توك - يوتيوب - انستقرام - فيسبوك - تويتر - كواي - سناب</p>
<form method="POST" action="/get">
<input name="url" placeholder="الصق أي رابط هنا..." required>
<select name="type"><option value="video">تحميل فيديو</option><option value="audio">تحميل صوت MP3</option></select>
<br><button type="submit">جلب الفيديو</button>
</form>
{content}
</div>
<div class="footer">تفلتات 2026<br><b>صنع بواسطة تامر ود الدروشاب</b><br>الدروشاب - أم درمان - السودان</div>
</body></html>
"""
@app.route("/", methods=["GET"])
def home():
    return HTML.format(content="")
@app.route("/get", methods=["POST"])
def get_video():
    url = request.form.get("url", "").strip()
    typ = request.form.get("type", "video")
    fmt = 'bestaudio/best' if typ == 'audio' else 'best'
    try:
        with yt_dlp.YoutubeDL({'quiet':True,'format':fmt,'noplaylist':True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title','فيديو')
            thumb = info.get('thumbnail','')
            site = info.get('extractor_key','')
            if typ == 'audio':
                content = f"<p>{title}</p><audio controls style='width:100%' src='{video_url}'></audio><a class='dl' href='{video_url}' download>تحميل الصوت MP3</a>"
            else:
                content = f"<p>{title}</p><p>من : {site}</p><video controls poster='{thumb}' src='{video_url}'></video><a class='dl' href='{video_url}' download>تحميل الفيديو</a>"
            return HTML.format(content=content)
    except Exception as e:
        return HTML.format(content="<p>ما قدرنا نجيب الرابط دا، حاول تاني</p>")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
