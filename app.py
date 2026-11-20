from flask import Flask, request, render_template_string, redirect
import yt_dlp, os, requests, re

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تفلتات | أول تطبيق سوداني لتنزيل الفيديوهات</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
body{background:#0a0f0a;color:white;min-height:100vh}
.top{height:6px;background:linear-gradient(90deg,#007A3A 33%,white 33%,white 66%,#D21034 66%)}
.header{text-align:center;padding:28px 18px 10px}
.flag{font-size:42px}
.logo{font-size:52px;font-weight:900;background:linear-gradient(180deg,#FFD700,#B8860B);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.2}
.sub{color:#FFD700;font-weight:700;margin-top:6px;font-size:17px}
.made{margin:14px auto 0;background:rgba(255,215,0,.12);border:1px solid #FFD700;border-radius:50px;padding:8px 16px;display:inline-block;font-size:14px}
.made b{color:#FFD700}
.card{max-width:480px;margin:22px auto;background:#151a15;border:1px solid #2a332a;border-radius:28px;padding:22px;margin-left:16px;margin-right:16px}
@media(min-width:520px){.card{margin-left:auto;margin-right:auto}}
label{color:#ccc;font-size:14px}
input{width:100%;padding:16px;border-radius:16px;border:2px solid #333;background:#0f130f;color:white;font-size:16px;margin:10px 0;outline:none;text-align:left;direction:ltr}
input:focus{border-color:#FFD700}
.btn{width:100%;padding:17px;border:none;border-radius:16px;background:linear-gradient(135deg,#007A3A,#00b050);color:white;font-size:19px;font-weight:900;cursor:pointer}
.btn2{width:100%;padding:17px;border:none;border-radius:16px;background:linear-gradient(135deg,#FFD700,#FF8c00);color:black;font-size:19px;font-weight:900;cursor:pointer;margin-top:12px;display:block;text-align:center;text-decoration:none}
.features{display:flex;gap:10px;justify-content:center;margin:18px 10px;flex-wrap:wrap}
.f{background:#1a211a;border:1px solid #2a332a;padding:10px 14px;border-radius:50px;font-size:13px}
video{width:100%;border-radius:18px;margin-top:14px;background:black}
.error{background:#3a1010;color:#ffb3b3;padding:12px;border-radius:12px;margin-top:12px;text-align:center}
.footer{text-align:center;padding:20px;color:#888;font-size:13px;line-height:1.8}
.footer b{color:#FFD700}
</style>
</head>
<body>
<div class="top"></div>
<div class="header">
<div class="flag">🇸🇩</div>
<div class="logo">تفلتات</div>
<div class="sub">أول تطبيق سوداني لتنزيل الفيديوهات بدون علامة مائية</div>
<div class="made">صُنع بفخر في السودان 🇸🇩 بواسطة <b>تامر ود الدروشاب</b></div>
</div>

<div class="card">
<form method="POST">
<label>الصق رابط الفيديو من تيك توك هنا 👇</label>
<input name="url" placeholder="https://vt.tiktok.com/..." value="{{url or ''}}" required>
<button class="btn">جيب الفيديو 🔥</button>
</form>
{% if error %}<div class="error">{{error}}</div>{% endif %}
{% if video %}
<video controls playsinline src="{{video}}"></video>
<a class="btn2" href="{{video}}" download>⬇️ تحميل الفيديو الآن</a>
<p style="text-align:center;color:#aaa;font-size:13px;margin-top:10px">اضغط مطولاً على الفيديو واختر حفظ - أو اضغط تحميل</p>
{% endif %}
</div>

<div class="features">
<div class="f">✅ بدون علامة مائية</div>
<div class="f">⚡ سريع جداً</div>
<div class="f">🇸🇩 سوداني 100%</div>
<div class="f">🆓 مجاني للأبد</div>
</div>

<div class="footer">
<b>تفلتات - TAFLATAT</b><br>
صُنع بحب في الدروشاب - الخرطوم - السودان 🇸🇩<br>
تامر ود الدروشاب © 2026
</div>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    video=None; error=None; url=""
    if request.method=="POST":
        url=request.form.get("url","").strip()
        if not url:
            error="الصق الرابط أولاً"
        else:
            try:
                headers={"User-Agent":"Mozilla/5.0"}
                r=requests.get(url, headers=headers, timeout=15, allow_redirects=True)
                final=r.url
                if "tiktok.com" not in final:
                    error="الرابط ده ما تيك توك، جرب رابط تاني"
                else:
                    ydl_opts={"format":"mp4","quiet":True,"no_warnings":True}
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info=ydl.extract_info(final, download=False)
                        video=info.get("url")
                        if not video:
                            for f in info.get("formats",[]):
                                if f.get("url"):
                                    video=f["url"]; break
                    if not video:
                        error="ما قدرنا نجيب الفيديو، جرب رابط تاني"
            except Exception as e:
                error="حصلت مشكلة، جرب تاني - يمكن الفيديو خاص"
    return render_template_string(HTML, video=video, error=error, url=url)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
