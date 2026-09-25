# -*- coding: utf-8 -*-
"""Gera og.png (1200x630) e 3 pins (1000x1500) fotografando o quadro real (quadro.js) com Chrome headless.
Rodar: python apps/bodas/tools/mockups.py  (NÃO publica nada; os pins ficam prontos em apps/bodas/pins/)"""
import os, subprocess, json
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
U = lambda p: "file:///" + os.path.join(ROOT, p).replace("\\", "/")
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Great+Vibes&family=Jost:wght@200;300;400;500&family=Nunito:wght@600;800;900&display=swap" rel="stylesheet">'
BASE = """body{margin:0;overflow:hidden;font-family:Nunito,sans-serif}
.bg{position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#fdf8f1,#efe3d0 75%)}
.hl{position:absolute;color:#2d2620;font:600 60px/1.05 'Cormorant Garamond',serif}
.hl em{font-family:'Great Vibes',cursive;font-style:normal;font-weight:400;color:#8c3b4a}
.sub{position:absolute;color:#5a4c40;font:700 26px/1.35 Nunito,sans-serif}
.pill{position:absolute;background:#8c3b4a;color:#fff;font:900 30px Nunito,sans-serif;border-radius:999px;padding:14px 30px;white-space:nowrap}
.shot{position:absolute;transform-origin:top left}
.shot .qd{box-shadow:0 30px 60px rgba(60,40,20,.28)}"""

def page(w, h, body, quadros):
    js = "".join(f"document.getElementById('q{i}').innerHTML=BD.quadroHTML({json.dumps(q)});" for i, q in enumerate(quadros))
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<link rel="stylesheet" href="{U("quadro.css")}"><style>{BASE}</style></head>'
            f'<body style="width:{w}px;height:{h}px;position:relative">{body}<script src="{U("data.js")}"></script><script src="{U("quadro.js")}"></script><script>{js}</script></body></html>')

def shot(out, w, h, body, quadros):
    src = os.path.join(HERE, "_mk.html"); open(src, "w", encoding="utf-8").write(page(w, h, body, quadros))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files", f"--window-size={w},{h}",
                    "--virtual-time-budget=7000", f"--screenshot={out}", "file:///" + src.replace("\\", "/")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(src); print("ok", out)

def q(slot, x, y, s, rot=0): return f'<div class="shot" id="q{slot}" style="left:{x}px;top:{y}px;transform:rotate({rot}deg) scale({s})"></div>'
Q = lambda n1, n2, y, ano, est: dict(n1=n1, n2=n2, y=y, m=5, d=16, ano=ano, estilo=est, frase="", foto="", unlocked=True)

shot(os.path.join(ROOT, "og.png"), 1200, 630,
     '<div class="bg"></div><div class="hl" style="left:60px;top:70px;width:560px">Que <em>bodas</em><br>vocês fazem?</div>'
     '<div class="sub" style="left:62px;top:300px;width:520px">Calculadora grátis com significado e contagem de dias. E o quadro de bodas pra imprimir em 1 minuto.</div>'
     '<div class="pill" style="left:60px;top:480px">Descubra as suas ✨</div>' + q(0, 880, 70, .42, 5) + q(1, 640, 40, .48, -4),
     [Q("Terezinha", "Antônio", 1976, 50, "noite"), Q("Helena", "Roberto", 2006, 20, "classico")])

os.makedirs(os.path.join(ROOT, "pins"), exist_ok=True)
PINS = [
    ("pin-bodas-de-ouro", "Presente de<br><em>Bodas de Ouro</em>", "quadro com os nomes dos seus pais · imprima hoje", Q("Terezinha", "Antônio", 1976, 50, "noite")),
    ("pin-bodas-de-prata", "Quadro de<br><em>Bodas de Prata</em>", "25 anos, a data e os 9.131 dias juntos", Q("Cláudia", "Marcelo", 2001, 25, "classico")),
    ("pin-que-bodas", "Que <em>bodas</em><br>vocês fazem?", "papel, porcelana, pérola… descubra grátis e veja o significado", Q("Helena", "Roberto", 2006, 20, "floral")),
]
for name, t1, t2, qq in PINS:
    shot(os.path.join(ROOT, "pins", name + ".png"), 1000, 1500,
         f'<div class="bg"></div><div class="hl" style="left:50px;top:60px;width:900px;text-align:center;font-size:84px">{t1}</div>'
         f'<div class="sub" style="left:90px;top:290px;width:820px;text-align:center;font-size:32px">{t2}</div>'
         + q(0, 170, 390, .835, -2) + '<div class="pill" style="left:50%;transform:translateX(-50%);bottom:50px;font-size:34px">giogas-pm.github.io/bodas</div>', [qq])
