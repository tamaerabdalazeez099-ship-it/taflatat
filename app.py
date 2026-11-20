from flask import Flask, request, jsonify, render_template_string
import yt_dlp, os
app = Flask(__name__)
HTML = """<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>تفلتات - حمل من كل التطبيقات</title><style>body{background:#111;color:white;font-family:sans-serif;text-align:center;padding:20px}h1{font-size:42px}input{width:92%;max-width:500px;padding:15px;border-radius:15px;border:none;font-size:16px;text-align:center}button{background:#ff2d55;color:white;border:none;padding:15px 30px;border-radius:15px;font-size:18px;font-weight:bold;margin-top:15px;width:92%;max-width:500px}span{background:#222;padding:10px 15px;border-radius:20px;display:inline-block;margin:5px}a.dl{display:block;background:#00c853;color:white;padding:15px;border-radius:15px;text-decoration:none;font-weight:bold;margin-top:10px}video{width:100%;max-width:500px;border-radius:15px}</style></head><body><h1>تفلتات 🔥</h1><p>حمل من كل التطبيقات بدون علامة مائية</p><div><span>🎵 تيك توك</span><span>📘 فيسبوك</span><span>📸 انستقرام</span><span>▶️ يوتيوب</span><span>🐦 تويتر</span></div><br><input id="url" placeholder="الصق رابط الفيديو هنا..."><br><button onclick="dl()">تحميل الآن ⬇️</button><div id="result"></div><button onclick="shareApp()" style="background:#25D366">شارك تفلتات في الواتساب 📤</button><p style="margin-top:30px">صنع بواسطة تامر ود الدروشاب<br>صنع في السودان 🇸🇩</p><script>async function dl(){let url=document.getElementById('url').value;if(!url) return alert('الصق الرابط اول');document.getElementById('result').innerHTML='جاري التحميل... ⏳';let r=await fetch('/download',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:url})});let d=await r.json();if(d.error) document.getElementById('result').innerHTML='❌ '+d.error;else document.getElementById('result').innerHTML='<video src="'+d.video_url+'" controls></video><a class="dl" href="'+d.video_url+'" download>حفظ الفيديو 📥</a><p>'+d.title+'</p>';}function shareApp(){let t='جرب تفلتات 🔥 حمل من تيك توك وفيسبوك وانستقرام ويوتيوب بدون علامة مائية - '+window.location.href;window.open('https://wa.me/?text='+encodeURIComponent(t));}</script></body></html>"""
@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/download', methods=['POST'])
def download():
 url=request.json.get('url','')
 try:
  ydl_opts={'format':'best','quiet':True,'noplaylist':True}
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
   info=ydl.extract_info(url, download=False)
   return jsonify({"title":info.get('title','تفلتات'),"video_url":info.get('url')})
 except Exception as e: return jsonify({"error":"الرابط ما اتعرف، جرب رابط تاني"})
if __name__=='__main__': app.run(host='0.0.0.0', port=int(os.environ.get('PORT',10000)))
