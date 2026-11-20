from flask import Flask, request, jsonify, send_file, render_template_string
import yt_dlp, os, uuid
app = Flask(__name__)
HTML = """
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>تفلتات - فخر السودان</title>
<style>*{box-sizing:border-box}body{margin:0;background:#080808;color:white;font-family:sans-serif}
.top{background:linear-gradient(135deg,#007A3D,#000,#D21034);padding:25px 15px 35px;text-align:center;border-radius:0 0 30px 30px}
.top h1{font-size:48px;margin:0;color:#FFD700}.top p{color:#FFD700;font-weight:bold}
.badge{background:#FFD700;color:black;padding:5px 15px;border-radius:20px;font-size:13px;font-weight:bold}
.box{margin:-10px 15px 15px;background:#1a1a1a;padding:15px;border-radius:20px;border:1px solid #333}
input{width:100%;padding:16px;border-radius:14px;border:2px solid #FFD700;background:#111;color:white;font-size:16px}
.btn{width:100%;padding:16px;border:none;border-radius:14px;font-weight:bold;font-size:18px;margin-top:10px;cursor:pointer}
.btn-gold{background:#FFD700;color:black}.btn-green{background:#007A3D;color:white}
.tabs{display:flex;gap:8px;overflow:auto;padding:10px 15px}.tab{background:#222;padding:10px 16px;border-radius:20px;white-space:nowrap;cursor:pointer}
.tab.active{background:#FFD700;color:black;font-weight:bold}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:0 15px 30px}
.card{background:#1c1c1c;border-radius:16px;overflow:hidden}.card img{width:100%;height:110px;object-fit:cover}
.card b{display:block;padding:8px;font-size:13px}.card button{width:calc(100% - 16px);margin:0 8px 8px;background:#FFD700;border:none;padding:9px;border-radius:10px;font-weight:bold}
#msg{text-align:center;color:#FFD700;margin:10px}.footer{text-align:center;color:#888;padding:20px;font-size:13px}
</style></head><body>
<div class="top"><div class="badge">🇸🇩 صنع في السودان - الدروشاب 🇸🇩</div><h1>🔥 تفلتات</h1><p>تامر ود الدروشاب | TAFLTAT</p><p style="color:white">شاهد .. حمل .. استمتع!</p></div>
<div class="box"><input id="q" placeholder="🔍 اكتب اسم الفيديو هنا ..."><button class="btn btn-gold" onclick="search()">🔍 ابحث وشاهد طوالي</button><input id="url" style="margin-top:12px" placeholder="أو الصق أي رابط هنا"><button class="btn btn-green" onclick="byLink()">⬇️ حمل من الرابط زي سناب تيوب</button><div id="msg"></div></div>
<div class="tabs"><div class="tab active" onclick="quick(this,'ترند السودان')">🔥 ترند السودان</div><div class="tab" onclick="quick(this,'اغاني سودانية جديدة')">🎵 اغاني سودانية</div><div class="tab" onclick="quick(this,'ضحك سوداني')">😂 ضحك سوداني</div><div class="tab" onclick="quick(this,'كورة سودانية')">⚽ كورة</div></div>
<div id="res" class="grid"></div><div class="footer">تفلتات - فخر شباب السودان 🇸🇩<br>صممه تامر ود الدروشاب</div>
<script>
async function search(){let q=document.getElementById('q').value.trim();if(!q)return alert('اكتب اسم الفيديو أول!');document.getElementById('msg').innerText='جاري البحث... 🔍';let r=await fetch('/search?q='+encodeURIComponent(q));let d=await r.json();show(d);}
async function quick(el,q){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));el.classList.add('active');document.getElementById('q').value=q;search();}
async function byLink(){let u=document.getElementById('url').value.trim();if(!u)return alert('الصق رابط أول!');document.getElementById('msg').innerText='جاري جلب الفيديو... ⏳';let r=await fetch('/download',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:u})});let d=await r.json();if(d.error){document.getElementById('msg').innerText=d.error;return}document.getElementById('msg').innerText='✅ تم!';document.getElementById('res').innerHTML=`<div class="card" style="grid-column:span 2"><img src="${d.thumbnail}"><b>${d.title}</b><button onclick="window.open('/file/${d.file_id}')">⬇️ تحميل الفيديو</button></div>`;}
function show(list){document.getElementById('msg').innerText='';if(!list.length){document.getElementById('msg').innerText='ما لقينا شي، جرب اسم تاني';return}document.getElementById('res').innerHTML=list.map(v=>`<div class="card"><img src="${v.thumbnail}" onclick="window.open('${v.url}','_blank')"><b>${v.title}</b><button onclick="dl('${v.url}')">⬇️ تحميل</button></div>`).join('');}
async function dl(u){document.getElementById('msg').innerText='جاري التحميل... ⏳';let r=await fetch('/download',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:u})});let d=await r.json();if(d.error){document.getElementById('msg').innerText=d.error;return}window.location.href='/file/'+d.file_id;}
search();
</script></body></html>
"""
@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/search')
def search():
    q=request.args.get('q','')
    opts={'quiet':True,'noplaylist':True,'extract_flat':True,'skip_download':True,'nocheckcertificate':True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info=ydl.extract_info(f"ytsearch10:{q}", download=False)
            out=[]
            for e in (info.get('entries') or [])[:10]:
                out.append({'title':e.get('title','')[:60],'thumbnail':f"https://i.ytimg.com/vi/{e.get('id')}/hqdefault.jpg",'url':f"https://www.youtube.com/watch?v={e.get('id')}"})
            return jsonify(out)
    except: return jsonify([])
@app.route('/download', methods=['POST'])
def download():
    url=request.json.get('url','').strip()
    fid=str(uuid.uuid4())[:8]; out=f"/tmp/{fid}.mp4"
    # 3 محاولات عشان ما يفشل
    for fmt in ['mp4/best[height<=720]/best','best[height<=720]/best','best']:
        opts={'outtmpl':out,'format':fmt,'quiet':True,'noplaylist':True,'nocheckcertificate':True,'user_agent':'Mozilla/5.0 (Linux; Android 10)','merge_output_format':'mp4'}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info=ydl.extract_info(url, download=True)
                return jsonify({'title':info.get('title','')[:80],'thumbnail':info.get('thumbnail',''),'file_id':fid})
        except: continue
    return jsonify({'error':'الفيديو دا خاص أو محذوف، جرب فيديو عام تاني'}),400
@app.route('/file/<fid>')
def get_file(fid):
    p=f"/tmp/{fid}.mp4"
    return send_file(p, as_attachment=True, download_name='taflatat.mp4') if os.path.exists(p) else ('انتهى',404)
if __name__=='__main__': app.run(host='0.0.0.0', port=10000)
