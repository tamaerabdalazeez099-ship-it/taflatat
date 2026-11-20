from flask import Flask, request, send_file, render_template_string
import yt_dlp, os, re, requests
app = Flask(__name__)
HTML = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>تفلتات</title><style>body{background:#111;color:#fff;font-family:sans-serif;text-align:center;padding:15px}input{width:92%;padding:15px;border-radius:30px;border:none;text-align:center;font-size:16px}button{width:92%;padding:15px;border:none;border-radius:30px;font-size:18px;font-weight:bold;margin-top:10px}.btn{background:#ff2d55;color:#fff}.dl{background:#25D366;color:#fff;display:block;width:92%;margin:15px auto;padding:16px;border-radius:30px;text-decoration:none;font-weight:bold}.card{background:#1e1e1e;border-radius:20px;padding:15px;margin:15px auto;max-width:420px}.card img{width:100%;border-radius:15px}</style></head><body><h1>تفلتات</h1><form method="POST" action="/"><input name="url" value="{{url or ''}}" placeholder="الصق الرابط هنا..." required><br><button class="btn">جيب الفيديو</button></form>{% if msg %}<p>{{msg}}</p>{% endif %}{% if video %}<div class="card"><img src="{{video.thumb}}"><h3>{{video.title}}</h3><p>{{video.author}}</p><a class="dl" href="{{video.dl_url}}">تحميل الان</a><a class="dl" style="background:#ff2d55" href="/download?url={{url}}">تحميل بديل</a></div>{% endif %}</body></html>"""
def clean_url(u):
    u=u.strip()
    if u.startswith('ttps://'): u='h'+u
    if not u.startswith('http'): u='https://'+u
    return u
@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        url=clean_url(request.form.get('url',''))
        if 'tiktok.com' in url:
            try:
                r=requests.get("https://www.tikwm.com/api/?url="+url, timeout=20).json()
                d=r.get('data',{})
                if d and d.get('play'):
                    video={'title':d.get('title','فيديو'),'thumb':d.get('cover',''),'author':d.get('author',{}).get('nickname',''),'dl_url':d.get('play')}
                    return render_template_string(HTML, video=video, url=url)
            except Exception as e:
                print(e)
        try:
            with yt_dlp.YoutubeDL({'quiet':True,'noplaylist':True,'skip_download':True}) as ydl:
                info=ydl.extract_info(url, download=False)
            video={'title':info.get('title','فيديو'),'thumb':info.get('thumbnail',''),'author':info.get('uploader',''),'dl_url':"/download?url="+url}
            return render_template_string(HTML, video=video, url=url)
        except Exception as e:
            return render_template_string(HTML, msg='جرب تاني بعد 10 ثواني', url=url)
    return render_template_string(HTML)
@app.route('/download')
def download():
    url=clean_url(request.args.get('url',''))
    try:
        with yt_dlp.YoutubeDL({'quiet':True,'noplaylist':True,'format':'best','outtmpl':'video.%(ext)s'}) as ydl:
            info=ydl.extract_info(url, download=True)
            fname=ydl.prepare_filename(info)
        return send_file(fname, as_attachment=True)
    except:
        return "جرب زر التحميل الاول"
if __name__=='__main__':
    app.run(host='0.0.0.0', port=10000)
