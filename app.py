from flask import Flask, request, send_file, render_template_string
import yt_dlp, os, re, requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>تفلتات 🔥</title><style>
body{background:#111;color:#fff;font-family:sans-serif;text-align:center;padding:15px}
input{width:92%;padding:15px;border-radius:30px;border:none;text-align:center;font-size:16px;direction:ltr}
button{width:92%;padding:15px;border:none;border-radius:30px;font-size:18px;font-weight:bold;margin-top:10px;cursor:pointer}
.btn{background:#ff2d55;color:#fff}
.dl{background:#25D366;color:#fff;display:block;width:92%;margin:15px auto;padding:16px;border-radius:30px;text-decoration:none;font-weight:bold;font-size:18px}
.card{background:#1e1e1e;border-radius:20px;padding:15px;margin:15px auto;max-width:420px}
.card img{width:100%;border-radius:15px}
.pill{display:inline-block;background:#222;padding:8px 13px;border-radius:20px;margin:4px}
.share{background:#222;color:#fff;display:block;width:92%;margin:10px auto;padding:12px;border-radius:30px;text-decoration:none}
</style></head><body>
<h1>🔥 تفلتات</h1><p>حمل من كل التطبيقات بدون علامة مائية</p>
<div><span class="pill">🎵 تيك توك</span><span class="pill">📘 فيسبوك</span><span class="pill">📸 انستقرام</span><span class="pill">▶️ يوتيوب</span></div>
<form method="POST" action="/"><input name="url" value="{{url or ''}}" placeholder="الصق الرابط هنا..." required><br><button class="btn">🔍 جيب الفيديو</button></form>
{% if msg %}<p>{{msg}}</p>{% endif %}
{% if video %}
<div class="card"><img src="{{video.thumb}}"><h3>{{video.title}}</h3><p>👤 {{video.author}}</p>
<a class="dl" href="{{video.dl_url}}">⬇️ تحميل الآن 🔥</a>
<a class="dl" style="background:#ff2d55" href="/download?url={{url}}">⬇️ تحميل بديل</a></div>
{% endif %}
<a class="share" href="https://wa.me/?text=جرب تطبيق تفلتات 🔥 https://taflatat.onrender.com">📤 شارك تفلتات في الواتساب</a>
<p>صنع بواسطة تامر ود الدروشاب<br>🇸🇩 صنع في السودان</p>
</body></html>
"""

def clean_url(u):
    u = u.strip()
    if u.startswith('ttps://'): u = 'h' + u
    if u.startswith('www.'): u = 'https://' + u
    if not u.startswith('http'): u = 'https://' + u
    u = re.sub(r'(tiktok\.com)([A-Za-z0-9])', r'\1/\2', u)
    return u

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        url = clean_url(request.form.get('url',''))
        # 1 - تيك توك بطريقة جديدة سريعة
        if 'tiktok.com' in url:
            try:
                r = requests.get(f"https://www.tikwm.com/api/?url={url}", timeout=20).json()
                d = r.get('data', {})
                if d and d.get('play'):
                    video = {'title': d.get('title','فيديو تيك توك'), 'thumb': d.get('cover',''), 'author': d.get('author',{}).get('nickname',''), 'dl_url': d.get('play')}
                    return render_template_string(HTML, video=video, url=url)
            except Exception as e:
                print("TIKWM ERROR", e)
        # 2 - باقي التطبيقات
        try:
            with yt_dlp.YoutubeDL({'quiet':True,'noplaylist':True,'skip_download':True}) as ydl:
                info = ydl.extract_info(url, download=False)
            video = {'title': info.get('title','فيديو'), 'thumb': info.get('thumbnail',''), 'author': info.get('uploader',''), 'dl_url': f"/download?url={url}"}
            return render_template_string(HTML, video=video, url=url)
        except Exception as e:
            print("ERROR:", e)
            return render_template_string(HTML, msg='❌ جرب تاني بعد 10 ثواني، السيرفر كان نايم وصحى هسي', url=url)
    return render_template_string(HTML)

@app.route('/download')
def download():
    url = clean_url(request.args.get('url',''))
    try:
        with yt_dlp.YoutubeDL({'quiet':True,'noplaylist':True,'format':'best','outtmpl':'video.%(ext)s'}) as ydl:
            info = ydl.extract_info(url, download=True)
            fname = ydl.prepare_filename(info)
        return send_file(fname, as_attachment=True)
    except:
        return "جرب زر التحميل الأول"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
