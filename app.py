from flask import Flask, request, send_file, render_template_string
import yt_dlp, os, re

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>تفلتات 🔥</title><style>
body{background:#111;color:#fff;font-family:sans-serif;text-align:center;padding:20px}
input{width:90%;padding:15px;border-radius:30px;border:none;text-align:center;font-size:16px;direction:ltr}
button{width:90%;padding:15px;border:none;border-radius:30px;font-size:18px;font-weight:bold;margin-top:10px;cursor:pointer}
.btn{background:#ff2d55;color:#fff}
.share{background:#25D366;color:#fff;display:block;width:90%;margin:15px auto;padding:15px;border-radius:30px;text-decoration:none;font-weight:bold}
.pill{display:inline-block;background:#222;padding:10px 15px;border-radius:20px;margin:5px}
</style></head><body>
<h1>🔥 تفلتات</h1><p>حمل من كل التطبيقات بدون علامة مائية</p>
<div><span class="pill">🎵 تيك توك</span><span class="pill">📘 فيسبوك</span><span class="pill">📸 انستقرام</span><span class="pill">▶️ يوتيوب</span><span class="pill">🐦 تويتر</span></div>
<form method="POST" action="/download"><input name="url" placeholder="الصق الرابط هنا..." required><br><button class="btn">⬇️ تحميل الآن</button></form>
{% if msg %}<p>{{msg}}</p>{% endif %}
<a class="share" href="https://wa.me/?text=جرب تطبيق تفلتات 🔥 حمل من تيك توك ويوتيوب بدون علامة مائية: https://taflatat.onrender.com">📤 شارك تفلتات في الواتساب</a>
<p>صنع بواسطة تامر ود الدروشاب<br>🇸🇩 صنع في السودان</p>
</body></html>
"""

def clean_url(u):
    u = u.strip()
    # امسح اي مسافات او / في البداية والنهاية
    u = u.strip().strip('/').strip()
    # لو ناقص h في البداية
    if u.startswith('ttps://'): u = 'h' + u
    if u.startswith('ttp://'): u = 'h' + u
    if u.startswith('www.'): u = 'https://' + u
    if not u.startswith('http'):
        u = 'https://' + u
    # صلح غلطة youtube.comwatch
    u = u.replace('youtube.comwatch', 'youtube.com/watch')
    u = u.replace('youtube.com/watch?', 'youtube.com/watch?v=').replace('watch?v=v=', 'watch?v=')
    # صلح tiktok المختصر
    u = u.replace('vt.tiktok.com/', 'vt.tiktok.com/')
    return u

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/download', methods=['POST'])
def download():
    url = clean_url(request.form.get('url',''))
    if 'tiktok.com' not in url and 'youtube.com' not in url and 'youtu.be' not in url and 'facebook.com' not in url and 'fb.watch' not in url and 'instagram.com' not in url and 'twitter.com' not in url and 'x.com' not in url:
        return render_template_string(HTML, msg='❌ الرابط ما اتعرف، جرب رابط تاني')
    try:
        ydl_opts = {'format':'best','outtmpl':'video.%(ext)s','quiet':True,'noplaylist':True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            fname = ydl.prepare_filename(info)
        return send_file(fname, as_attachment=True)
    except Exception as e:
        return render_template_string(HTML, msg='❌ حصل خطأ، جرب رابط تاني - يمكن الفيديو خاص')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
