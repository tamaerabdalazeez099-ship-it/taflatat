from flask import Flask, request, render_template_string
import yt_dlp, os, requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تفلتات | نزل من أي مكان</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
body{background:#0a0f0a;color:white;min-height:100vh}
.top{height:6px;background:linear-gradient(90deg,#007A3A 33%,white 33%,white 66%,#D21034 66%)}
.header{text-align:center;padding:28px 18px 10px}
.logo{font-size:52px;font-weight:900;color:#FFD700}
.sub{color:#FFD700;font-weight:700;margin-top:6px}
.made{margin:14px auto 0;background:rgba(255,215,0,.12);border:1px solid #FFD700;border-radius:50px;padding:8px 16px;display:inline-block;font-size:14px}
.card{max-width:480px;margin:22px auto;background:#151a15;border:1px solid #2a332a;border-radius:28px;padding:22px;margin-left:16px;margin-right:16px}
@media(min-width:520px){.card{margin-left:auto;margin-right:auto}}
input{width:100%;padding:16px;border-radius:16px;border:2px solid #333;background:#0f130f;color:white;font-size:16px;margin:10px 0;outline:none;text-align:left;direction:ltr}
input:focus{border-color:#FFD700}
.btn{width:100%;padding:17px;border:none;border-radius:16px;background:linear-gradient(135deg,#007A3A,#00b050);color:white;font-size:19px;font-weight:900;cursor:pointer}
.btn2{width:100%;padding:17px;border:none;border-radius:16px;background:linear-gradient(135deg,#FFD700,#FF8c00);color:black;font-size:19px;font-weight:900;cursor:pointer;margin-top:12px;display:block;text-align:center;text-decoration:none}
.platforms{display:flex;gap:8px;justify-content:center;margin:16px 10px;flex-wrap:wrap}
.p{background:#1a211a;border:1px solid #FFD700;padding:9px 13px;border-radius:50px;font-size:13px}
video{width:100%;border-radius:18px;margin-top:14px;background:black}
.error{background:#3a1010;color:#ffb3b3;padding:12px;border-radius:12px;margin-top:12px;text-align:center}
.success{background:#0f3a1a;color:#aaffc4;padding:12px;border-radius:12px;margin-top:12px;text-align:center}
.footer{text-align:center;padding:20px;color:#888;font-size:13px;line-height:1.8}
.footer b{color:#FFD700}
</style>
</head>
<body>
<div class="top"></div>
<div class="header">
<div style="font-size:42px">🇸🇩</div>
<div class="logo">تفلتات</div>
<div class="sub">نزل من أي مكان - بدون علامة مائية</div>
<div class="made">صُنع بفخر في السودان 🇸🇩 بواسطة <b>تامر ود الدروشاب</b></div>
</div>
<div class="platforms">
<div class="p">🎵 تيك توك</div>
<div class="p">📘 فيسبوك</div>
<div class="p">📸 انستغرام</div>
<div class="p">▶️ يوتيوب</div>
<div class="p">𝕏 تويتر</div>
</div>
<div class="card">
<form method="POST">
<label>الصق رابط الفيديو من أي تطبيق هنا 👇</label>
<input name="url" placeholder="الصق الرابط هنا..." value="{{url or ''}}" required>
<button class="btn">جيب الفيديو 🔥</button>
</form>
{% if error %}<div class="error">{{error}}</div>{% endif %}
{% if video %}
<div class="success">تم ✅ الفيديو جاهز!</div>
<video controls playsinline src="{{video}}"></video>
<a class="btn2" href="{{video}}" download>⬇️ تحميل الفيديو الآن</a>
{% endif %}
</div>
<div class="footer"><b>تفلتات - TAFLATAT</b><br>صُنع بحب في الدروشاب - الخرطوم - السودان 🇸🇩<br>تامر ود الدروشاب © 2026</div>
</body>
</html>
"""

def get_video(url):
    # خيارات قوية لكل التطبيقات - خاصة يوتيوب
    opts = {
        "format": "best[ext=mp4][height<=720]/best[height<=720]/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        },
        "extractor_args": {"youtube": {"player_client": ["android", "ios", "web"]}},
        "socket_timeout": 30,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # لو فيديو مباشر
        if info.get("url"):
            return info.get("url")
        # لو فيه فورمات كتيرة
        for f in info.get("formats", []) or []:
            if f.get("url") and f.get("vcodec") != "none":
                return f["url"]
        return None

@app.route("/", methods=["GET","POST"])
def index():
    video=None; error=None; url=""
    if request.method=="POST":
        url=request.form.get("url","").strip()
        if not url:
            error="الصق الرابط أولاً"
        else:
            try:
                # تابع الروابط المختصرة
                try:
                    r=requests.get(url, timeout=10, allow_redirects=True, headers={"User-Agent":"Mozilla/5.0"})
                    url_final=r.url
                except:
                    url_final=url
                video=get_video(url_final)
                if not video:
                    error="ما قدرنا نجيب الفيديو ده. جرب رابط تيك توك أو فيسبوك - يوتيوب مرات بيحظر السيرفر"
            except Exception as e:
                print("ERROR:", e)
                if "youtube" in url.lower() or "youtu.be" in url.lower():
                    error="يوتيوب حظر السيرفر هسي. جرب رابط تيك توك أو فيسبوك، ديل شغالين 100% ✅"
                else:
                    error="حصلت مشكلة، جرب رابط تاني - يمكن الفيديو خاص"
    return render_template_string(HTML, video=video, error=error, url=url)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))dashboard.render.com
    
