from flask import Flask, request, jsonify, send_file, Response
import yt_dlp, uuid, json, urllib.request, urllib.parse
app = Flask(__name__)
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#000">
<link rel="manifest" href="/manifest.json">
<title>تفلتات | اكتب الاسم بس - تامر ود الدروشاب</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#000;color:#fff;min-height:100vh}
body:before{content:"";position:fixed;inset:0;z-index:-1;background:linear-gradient(180deg,#000,#1a1400,#000)}
#splash{position:fixed;inset:0;z-index:9999;background:radial-gradient(circle,#FFD700,#B8860B,#000);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;animation:splashOut 3.5s forwards}
#splash h1{font-size:90px;color:#000}
#splash .name{background:#000;color:#FFD700;padding:14px 30px;border-radius:50px;font-size:24px;font-weight:900;margin-top:10px;border:3px solid #FFD700}
@keyframes splashOut{0%,82%{opacity:1}100%{opacity:0;visibility:hidden}}
.hero{padding:28px 15px 30px;text-align:center;background:linear-gradient(180deg,#000,#1a1400);border:3px solid #FFD700;border-radius:0 0 35px 35px}
.hero h1{font-size:78px;color:#FFD700;text-shadow:0 0 25px #FFD700}
.hero .en{color:#FFD700;letter-spacing:10px}
.king-box{margin:18px auto 0;max-width:460px;background:linear-gradient(135deg,#fff,#FFEFD5,#fff);border:4px solid #FFD700;border-radius:22px;padding:20px;box-shadow:0 0 30px #FFD700}
.king-box b{font-size:32px;color:#000;display:block}
.king-box span{color:#8B6508;font-weight:bold}
/* البحث بالاسم بس */
.search-big{margin:15px;background:#111;border:3px solid #FFD700;border-radius:25px;padding:20px;box-shadow:0 0 25px #FFD70044;text-align:center}
.search-big h2{color:#FFD700;font-size:24px}
.search-big p{color:#aaa;font-size:14px;margin-top:6px}
.search-big input{width:100%;padding:18px;border-radius:16px;border:3px solid #FFD700;font-size:19px;text-align:center;margin-top:14px;background:#000;color:#fff;outline:none}
.search-big input::placeholder{color:#888}
/* أنواع البحث - فيديو أغاني صور ألعاب أفلام */
.types{display:flex;gap:8px;overflow-x:auto;padding:12px 0;justify-content:flex-start}
.types button{white-space:nowrap;padding:13px 18px;border-radius:30px;border:2px solid #FFD700;background:#000;color:#FFD700;font-weight:900;cursor:pointer;font-size:16px}
.types button.active{background:#FFD700;color:#000;box-shadow:0 0 15px #FFD700}
.btn{width:100%;padding:16px;border:none;border-radius:15px;font-size:19px;font-weight:900;margin-top:10px;cursor:pointer}
.btn-gold{background:linear-gradient(#FFD700,#FF8C00);color:#000}
.btn-green{background:#25D366;color:#fff}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:14px}
.grid button{padding:18px 10px;border-radius:20px;border:2px solid #FFD700;background:#111;color:#fff;font-weight:900;cursor:pointer;font-size:16px}
.grid button span{display:block;font-size:30px}
.card{background:#1a1a1a;border:2px solid #FFD70088;border-radius:20px;padding:14px;margin:14px;cursor:pointer}
.card img{width:100%;border-radius:15px;border:1px solid #FFD700;aspect-ratio:16/9;object-fit:cover}
.card h3{color:#FFD700;margin:10px 0;font-size:16px}
.card p{color:#aaa;font-size:13px}
.card .actions{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.card .actions button{flex:1;padding:12px;border-radius:12px;border:none;font-weight:900;cursor:pointer;font-size:15px;min-width:100px}
.footer{background:linear-gradient(#FFD700,#FF8C00);color:#000;text-align:center;padding:28px 15px;border-radius:35px 35px 0 0}
.footer b{font-size:28px}
video,audio{width:100%;border-radius:15px;margin-top:10px}
.img-grid{display:grid;grid-template-columns:1
