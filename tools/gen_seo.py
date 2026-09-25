# -*- coding: utf-8 -*-
"""Gera as páginas de SEO do Bodas: 1 por boda (content1-3.py), o hub da tabela, sitemap.xml, robots.txt e README.
Rodar de qualquer lugar: python apps/bodas/tools/gen_seo.py"""
import os, re, json, html, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
BASE = "https://giogas-pm.github.io/bodas/"
HOJE = datetime.date.today().isoformat()

# ---------- tabela (lida do data.js, fonte única) ----------
js = open(os.path.join(ROOT, "data.js"), encoding="utf-8").read()
ROWS = []
for m in re.finditer(r'\[(\d+),"([^"]+)","(\w+)","(#[0-9a-f]{6})","([^"]+)",(null|"[^"]+")\]', js):
    ROWS.append(dict(ano=int(m[1]), nome=m[2], icon=m[3], cor=m[4], sig=m[5], slug=None if m[6] == "null" else m[6].strip('"')))
assert len(ROWS) == 100, len(ROWS)
BY = {r["ano"]: r for r in ROWS}

from content1 import C as C1
from content2 import C as C2
from content3 import C as C3
CONTENT = {**C1, **C2, **C3}
for a, r in BY.items():
    if r["slug"]: assert a in CONTENT, ("sem conteúdo", a)

def anos(n): return "1 ano" if n == 1 else f"{n} anos"
def e(s): return html.escape(s, quote=True)
def link(r, txt=None):
    txt = txt or f"Bodas de {r['nome']}"
    return f'<a href="/bodas/{r["slug"]}/">{txt}</a>' if r["slug"] else txt
def app(slug): return f"/bodas/?src=seo&amp;b={slug}"

CSS = """
:root{--pri:#8c3b4a;--pri2:#6e2a38;--gold:#b8964a;--ink:#2d2620;--bg:#fbf7ef;--muted:#7a6c60;--line:#ebe1d2;--ok:#2f6b4f}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:Nunito,system-ui,sans-serif;background:var(--bg);color:var(--ink);line-height:1.68;font-size:17px}
a{color:var(--pri)}
header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;padding:14px 16px;max-width:1100px;margin:0 auto}
.logo{font:600 24px 'Cormorant Garamond',serif;color:var(--pri);text-decoration:none}
.hl{font-size:13px;font-weight:700;color:var(--ok);text-decoration:none}
.wrap{max-width:780px;margin:0 auto;padding:0 16px}
.crumbs{font-size:13px;color:var(--muted)}.crumbs a{color:var(--muted)}
h1{font:600 clamp(32px,7vw,48px)/1.08 'Cormorant Garamond',serif;margin:10px 0 12px}
h1 em{color:var(--pri)}
h2{font:600 clamp(26px,5vw,32px)/1.15 'Cormorant Garamond',serif;margin:38px 0 8px}
h3{font-size:17px;margin:0}
.ans{background:#fff;border:2px solid var(--gold);border-radius:16px;padding:14px 18px;margin:14px 0}
.ans b{color:var(--pri2)}
.ans small{display:block;color:var(--muted);margin-top:4px;font-size:14.5px}
.toc{background:#fff;border:1px solid var(--line);border-radius:16px;padding:12px 18px;margin:18px 0;font-size:15.5px}
.toc b{display:block}.toc ol{margin:4px 0 0;padding-left:20px}
.fig{background:#ede3d3;border-radius:18px;padding:14px;margin:18px 0 6px;overflow:hidden}
.fig .fit{transform-origin:top left;width:794px}
.figc{font-size:14px;color:var(--muted);text-align:center;margin:6px 0 0}
.btn{display:inline-block;border:0;border-radius:14px;padding:14px 20px;font:800 16px Nunito,sans-serif;cursor:pointer;text-decoration:none;text-align:center;line-height:1.25}
.btn-pri{background:linear-gradient(180deg,#a04657,var(--pri2));color:#fff;box-shadow:0 8px 18px rgba(140,59,74,.25)}
.cta{background:#fff;border:2px solid var(--gold);border-radius:18px;padding:18px;margin:24px 0;text-align:center}
.cta .ct{font:600 25px/1.2 'Cormorant Garamond',serif;margin:0 0 6px}
.cta p{margin:0 0 12px}.cta .btn{width:100%;max-width:440px}
.price{font-size:13px;color:var(--muted);margin:10px 0 0!important}
ul.gifts{list-style:none;padding:0;margin:0;display:grid;gap:8px}
ul.gifts li{background:#fff;border:1px solid var(--line);border-radius:14px;padding:11px 15px}
ul.tips{padding-left:20px}ul.tips li{margin:6px 0}
.frase{background:#fff;border:1px solid #e6d6b3;border-radius:14px;margin:10px 0;padding:12px 16px}
.frase .fh{display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:13.5px;color:var(--muted);font-weight:700}
.frase p{margin:6px 0 0;font:italic 500 20px/1.45 'Cormorant Garamond',serif;color:var(--ink)}
.copy{flex:none;border:1px solid #dccfbd;background:#fff;border-radius:999px;padding:6px 12px;font:700 13px Nunito,sans-serif;cursor:pointer;color:var(--ok)}
.copy.ok{background:var(--ok);color:#fff;border-color:var(--ok)}
.faq{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 16px;margin:10px 0}
.nav2{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:30px 0 0}
.nav2 a,.nav2 span{display:block;background:#fff;border:1px solid var(--line);border-radius:12px;padding:11px 14px;text-decoration:none;font-weight:700;font-size:15px}
.nav2 small{display:block;color:var(--muted);font-weight:400}
.nav2 .nx{text-align:right}
table.tb{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;font-size:15px}
.tb th,.tb td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.tb th{background:#f3eadb;font-size:13px;text-transform:uppercase;letter-spacing:1px}
.tb td:first-child{white-space:nowrap;font-weight:800}
.tb td:nth-child(2){white-space:nowrap}
.tb .s{color:var(--muted);font-size:14px}
@media(max-width:560px){.tb .s{display:none}}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.chips a{border:1px solid var(--line);background:#fff;border-radius:999px;padding:5px 11px;font-size:14px;text-decoration:none}
footer{text-align:center;color:var(--muted);font-size:13px;padding:30px 16px 40px}
footer nav{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 12px;margin-bottom:10px}
footer nav a{color:var(--muted)}
.toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:#2d2620;color:#fff;padding:10px 16px;border-radius:12px;font-size:14px;opacity:0;transition:.25s;pointer-events:none;z-index:9}
.toast.show{opacity:1}
"""

SCRIPT = """<script>
(function(){
  var t=document.getElementById('toast');
  function toast(m){t.textContent=m;t.classList.add('show');clearTimeout(toast._t);toast._t=setTimeout(function(){t.classList.remove('show')},2800)}
  function fb(s){var a=document.createElement('textarea');a.value=s;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(_){}document.body.removeChild(a)}
  document.addEventListener('click',function(ev){var b=ev.target.closest&&ev.target.closest('.copy');if(!b)return;var s=b.closest('.frase').querySelector('p').innerText.trim();
    var ok=function(){b.classList.add('ok');b.textContent='Copiado ✓';toast('Frase copiada! É só colar no WhatsApp ou no cartão.');setTimeout(function(){b.classList.remove('ok');b.textContent='Copiar'},2200)};
    if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(s).then(ok,function(){fb(s);ok()})}else{fb(s);ok()}});
  var f=document.getElementById('qfig');
  if(f&&window.BD){var o=JSON.parse(f.getAttribute('data-q'));var box=f.querySelector('.fit');box.innerHTML=BD.quadroHTML(o);
    var fit=function(){var s=Math.min(1,(f.clientWidth-28)/794);box.style.transform='scale('+s+')';f.style.height=(1123*s+28)+'px'};fit();window.addEventListener('resize',fit);document.fonts&&document.fonts.ready.then(fit)}
})();
</script>"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Great+Vibes&family=Jost:wght@200;300;400;500&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">'

def footer_nav():
    items = ['<a href="/bodas/">Calculadora de bodas</a>', '<a href="/bodas/tabela-de-bodas-de-casamento/">Tabela de bodas</a>']
    items += [f'<a href="/bodas/{r["slug"]}/">Bodas de {r["nome"]}</a>' for r in ROWS if r["slug"]]
    return "".join(items)

def shell(url, title, desc, crumbs_html, body, ld, extra_head="", scripts=""):
    assert len(title) <= 60, (url, len(title), title)
    assert len(desc) <= 158, (url, len(desc), desc)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title, quote=False)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="pt_BR">
<meta property="og:image" content="{BASE}og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E💍%3C/text%3E%3C/svg%3E">
{FONTS}
{extra_head}<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header><a class="logo" href="/bodas/">💍 Bodas</a><a class="hl" href="/bodas/">Calculadora de bodas →</a></header>
<main class="wrap">
<nav class="crumbs" aria-label="Você está em">{crumbs_html}</nav>
{body}
</main>
<footer><nav aria-label="Bodas de casamento">{footer_nav()}</nav>Bodas · feito com carinho no Brasil</footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
{scripts}{SCRIPT}
</body>
</html>
"""

ESTILOS = ["classico", "floral", "noite", "minimal"]
def estilo_para(a):
    if a in (50, 25, 45, 60, 65, 70, 75, 16): return "noite"
    if a in (4, 17, 35, 6, 30): return "floral"
    if a in (11, 10, 13, 55): return "minimal"
    return "classico"

def boda_page(r):
    a, c = r["ano"], CONTENT[r["ano"]]
    url = BASE + r["slug"] + "/"
    prev, nxt = BY.get(a - 1), BY.get(a + 1)
    title = f"Bodas de {r['nome']} ({anos(a)}): significado e presentes"
    if len(title) > 60: title = f"Bodas de {r['nome']} ({anos(a)}): significado"
    desc = f"{anos(a).capitalize()} de casados são Bodas de {r['nome']}. Significado, ideias de presente, frases prontas pra copiar e como comemorar."
    if len(desc) > 158: desc = f"{anos(a).capitalize()} de casados = Bodas de {r['nome']}. Significado, presentes, frases prontas e como comemorar."
    nome = r["nome"]
    body = f'<h1>Bodas de <em>{nome}</em>: {anos(a)} de casados</h1>\n'
    ans = f'<b>{anos(a).capitalize()} de casados = Bodas de {nome}.</b>'
    viz = []
    if prev: viz.append(f'antes: {anos(prev["ano"])}, {link(prev, prev["nome"])}')
    if nxt: viz.append(f'depois: {anos(nxt["ano"])}, {link(nxt, nxt["nome"])}')
    body += f'<div class="ans">{ans} {e(r["sig"])}<small>{" · ".join(viz).capitalize()} · <a href="/bodas/">descubra as suas na calculadora</a></small></div>\n'
    body += f'<p>{c["intro"]}</p>\n'
    q = dict(n1="Helena", n2="Roberto", y=2026 - a, m=5, d=16, ano=a, estilo=estilo_para(a), frase="", foto="", unlocked=False)
    body += f'<div class="fig" id="qfig" data-q="{e(json.dumps(q))}"><div class="fit"></div></div><p class="figc">Exemplo do Quadro das Bodas de {nome} (estilo {["Clássico","Floral","Noite de gala","Moderno"][ESTILOS.index(q["estilo"])]}). Troque pelos nomes e pela data do casal.</p>\n'
    body += f'''<aside class="cta"><p class="ct">Quadro das Bodas de {nome} com os nomes do casal</p><p>Digite os nomes e a data: o quadro sai com o símbolo da boda, os {anos(a)} e os dias juntos, pronto pra imprimir em A4 ou A3.</p><a class="btn btn-pri" href="{app(r["slug"])}" data-cta="top">Criar o quadro das Bodas de {nome}</a><p class="price">Prévia grátis na tela · R$24,90 pra liberar o PDF sem marca · cartão ou boleto</p></aside>\n'''
    body += f'''<div class="toc"><b>Nesta página</b><ol><li><a href="#significado">Significado das Bodas de {nome}</a></li><li><a href="#origem">De onde vem a tradição</a></li><li><a href="#presentes">Ideias de presente</a></li><li><a href="#frases">Frases e mensagens prontas</a></li><li><a href="#comemorar">Como comemorar</a></li><li><a href="#faq">Perguntas frequentes</a></li></ol></div>\n'''
    body += f'<h2 id="significado">Significado das Bodas de {nome}</h2>\n' + "".join(f"<p>{p}</p>\n" for p in c["sig"])
    body += f'<h2 id="origem">De onde vem a tradição</h2>\n<p>{c["origem"]}</p>\n'
    body += f'<h2 id="presentes">Ideias de presente para Bodas de {nome}</h2>\n<ul class="gifts">' + "".join(
        f'<li><b>{t}</b> — {d}{" <a href=\"" + app(r["slug"]) + "\">Criar o quadro</a>" if t.startswith("Quadro") else ""}</li>' for t, d in c["presentes"]) + "</ul>\n"
    body += f'<h2 id="frases">Frases e mensagens para Bodas de {nome}</h2>\n<p>Copie, troque o que quiser e mande no WhatsApp, no cartão ou use no quadro (tem um campo pra frase).</p>\n'
    body += "".join(f'<div class="frase"><div class="fh"><span>{p}</span><button class="copy" type="button">Copiar</button></div><p>{t}</p></div>\n' for p, t in c["frases"])
    body += f'<h2 id="comemorar">Como comemorar as Bodas de {nome}</h2>\n<ul class="tips">' + "".join(f"<li>{x}</li>" for x in c["comemorar"]) + "</ul>\n"
    body += f'''<aside class="cta"><p class="ct">Esqueceu o presente? Dá tempo.</p><p>O Quadro das Bodas de {nome} fica pronto em 1 minuto: você imprime hoje em casa ou numa gráfica rápida.</p><a class="btn btn-pri" href="{app(r["slug"])}" data-cta="end">Fazer o quadro agora</a><p class="price">Veja a prévia antes de pagar · 4 estilos · A4 e A3</p></aside>\n'''
    seg = [BY[k] for k in range(a + 1, min(101, a + 4))]
    faq = list(c["faq"]) + [(f"Quais são as próximas bodas depois das Bodas de {nome}?",
        "Depois vêm " + ", ".join(f"{anos(s['ano'])}: Bodas de {s['nome']}" for s in seg) + "." if seg else "É a última da lista tradicional.")]
    body += '<h2 id="faq">Perguntas frequentes</h2>\n' + "".join(f'<div class="faq"><h3>{html.escape(qq)}</h3><p style="margin:6px 0 0">{html.escape(aa)}</p></div>\n' for qq, aa in faq)
    pl = f'<a href="/bodas/{prev["slug"]}/"><small>← {anos(prev["ano"])}</small>Bodas de {prev["nome"]}</a>' if prev and prev["slug"] else (f'<span><small>← {anos(prev["ano"])}</small>Bodas de {prev["nome"]}</span>' if prev else "<span></span>")
    nl = f'<a class="nx" href="/bodas/{nxt["slug"]}/"><small>{anos(nxt["ano"])} →</small>Bodas de {nxt["nome"]}</a>' if nxt and nxt["slug"] else (f'<span class="nx"><small>{anos(nxt["ano"])} →</small>Bodas de {nxt["nome"]}</span>' if nxt else "<span></span>")
    body += f'<div class="nav2">{pl}{nl}</div>\n<p style="margin-top:14px">Veja todas na <a href="/bodas/tabela-de-bodas-de-casamento/#ano-{a}">tabela de bodas de casamento</a> ou descubra as suas na <a href="/bodas/">calculadora de bodas</a>.</p>\n'
    crumbs = f'<a href="/bodas/">Bodas</a> › <a href="/bodas/tabela-de-bodas-de-casamento/">Tabela de bodas</a> › Bodas de {nome}'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Bodas", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Tabela de bodas de casamento", "item": BASE + "tabela-de-bodas-de-casamento/"},
            {"@type": "ListItem", "position": 3, "name": f"Bodas de {nome}", "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": qq, "acceptedAnswer": {"@type": "Answer", "text": aa}} for qq, aa in faq]}]}
    head = '<link rel="stylesheet" href="/bodas/quadro.css">\n'
    scripts = '<script src="/bodas/data.js"></script><script src="/bodas/quadro.js"></script>\n'
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    return url, shell(url, title, desc, crumbs, body, ld, head, scripts), words

def hub():
    url = BASE + "tabela-de-bodas-de-casamento/"
    title = "Tabela de bodas de casamento: 1 a 100 anos (lista completa)"
    desc = "Lista completa das bodas de casamento, do 1º ao 100º ano, com o significado de cada uma. Veja quantos anos são as bodas de prata, ouro, pérola e mais."
    rows = "".join(f'<tr id="ano-{r["ano"]}"><td>{anos(r["ano"])}</td><td>{link(r)}</td><td class="s">{e(r["sig"])}</td></tr>' for r in ROWS)
    faq = [("Quais são as bodas de casamento mais importantes?", "As mais comemoradas são as de Papel (1 ano), Madeira (5), Estanho (10), Cristal (15), Porcelana (20), Prata (25), Pérola (30), Esmeralda (40), Ouro (50) e Diamante (60)."),
           ("Por que existem listas de bodas diferentes?", "A tradição foi montada aos poucos, em países diferentes, e algumas bodas têm mais de um nome (por exemplo, 4 anos: flores e frutas ou cera; 40 anos: esmeralda ou rubi). Esta tabela segue a lista mais usada no Brasil."),
           ("Quem casou em 29 de fevereiro comemora as bodas quando?", "Nos anos que não são bissextos, o costume é comemorar no dia 28 de fevereiro."),
           ("Bodas de namoro contam?", "A tradição das bodas conta os anos de casamento. Existem listas de \"bodas de namoro\" mensais, mas elas variam muito e não têm um padrão.")]
    marcos = [1, 5, 10, 15, 20, 25, 30, 40, 50, 60]
    body = '<h1>Tabela de <em>bodas de casamento</em>: do 1º ao 100º ano</h1>\n'
    body += '<div class="ans"><b>Resumo:</b> 1 ano = Papel · 5 = Madeira · 10 = Estanho · 15 = Cristal · 20 = Porcelana · 25 = Prata · 30 = Pérola · 40 = Esmeralda · 50 = Ouro · 60 = Diamante.<small>Não sabe quantos anos faz? <a href="/bodas/">Use a calculadora de bodas</a>: ela conta os dias e mostra as próximas.</small></div>\n'
    body += '<p>Cada aniversário de casamento tem um nome, e cada nome tem um porquê. A lógica é quase sempre a mesma: os primeiros anos recebem materiais frágeis e simples (papel, algodão, couro), porque a relação ainda está começando. Com o tempo, os materiais ficam mais resistentes e mais raros — primeiro madeira e metais comuns, depois pedras preciosas e metais nobres. É uma forma bonita de dizer que o casamento fica mais forte e mais valioso a cada ano.</p>\n'
    body += '<p>A lista abaixo é a mais usada no Brasil. Algumas bodas têm nomes alternativos em outras listas; quando isso acontece, explicamos na página de cada uma.</p>\n'
    body += '<div class="chips">' + "".join(f'<a href="#ano-{a}">{a}</a>' for a in [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 90, 100]) + '</div>\n'
    body += f'<table class="tb"><thead><tr><th>Anos</th><th>Bodas de</th><th class="s">Significado</th></tr></thead><tbody>{rows}</tbody></table>\n'
    body += f'''<aside class="cta"><p class="ct">Vai presentear alguém nas bodas?</p><p>Crie um Quadro de Bodas com os nomes, a data, o símbolo da boda e os dias juntos. Pronto pra imprimir em 1 minuto.</p><a class="btn btn-pri" href="/bodas/?src=seo&amp;b=tabela#quadro">Criar o quadro de bodas</a><p class="price">Prévia grátis · R$24,90 pra liberar o PDF · A4 e A3</p></aside>\n'''
    body += '<h2>As bodas mais comemoradas</h2>\n<ul class="tips">' + "".join(f'<li><b>{anos(a)}: {link(BY[a])}</b> — {e(BY[a]["sig"])}</li>' for a in marcos) + '</ul>\n'
    body += '<h2>De onde vem a tradição das bodas</h2>\n<p>A palavra \"bodas\" vem do latim <i>vota</i>, os votos feitos no casamento. O costume de festejar aniversários de casamento com nomes especiais nasceu na Europa medieval: na região da Alemanha, o marido presenteava a esposa com uma coroa de prata aos 25 anos de casados e com uma coroa de ouro aos 50. Com o tempo, outros anos ganharam nomes, e no século 20 as listas completas, com um material pra cada ano, se espalharam pelos Estados Unidos, por Portugal e pelo Brasil.</p>\n<p>Por isso há pequenas diferenças entre países: nos Estados Unidos, por exemplo, os 40 anos são de rubi, enquanto no Brasil são de esmeralda (e o rubi fica pros 45). Nenhuma lista está \"errada\" — o que importa é o significado que o casal dá à data.</p>\n'
    body += '<h2>Como descobrir quais bodas vocês fazem</h2>\n<p>Conte os anos completos desde a data do casamento. Quem casou em 10 de março de 2001 completa 25 anos, as Bodas de Prata, em 10 de março de 2026; um dia antes, ainda está nos 24 anos (Bodas de Opala). Se preferir não fazer conta, a <a href="/bodas/">calculadora de bodas</a> mostra o resultado na hora, com os dias juntos e a data das próximas bodas.</p>\n'
    body += '<h2>Perguntas frequentes</h2>\n' + "".join(f'<div class="faq"><h3>{html.escape(q)}</h3><p style="margin:6px 0 0">{html.escape(a)}</p></div>\n' for q, a in faq)
    crumbs = '<a href="/bodas/">Bodas</a> › Tabela de bodas de casamento'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Bodas", "item": BASE}, {"@type": "ListItem", "position": 2, "name": "Tabela de bodas de casamento", "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    return url, shell(url, title, desc, crumbs, body, ld)

def write(slug, content):
    d = os.path.join(ROOT, slug); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(content)

urls = [BASE]
u, h = hub(); write("tabela-de-bodas-de-casamento", h); urls.append(u)
for r in ROWS:
    if r["slug"]:
        u, h, w = boda_page(r); write(r["slug"], h); urls.append(u); print(r["slug"], "palavras:", w)
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{x}</loc><lastmod>{HOJE}</lastmod></url>\n" for x in urls) + "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(sm)
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(f"User-agent: *\nAllow: /\nDisallow: /tools/\nSitemap: {BASE}sitemap.xml\n")
readme = "# Bodas — calculadora de bodas + Quadro de Bodas para imprimir\n\n- [Calculadora de bodas](https://giogas-pm.github.io/bodas/)\n- [Tabela de bodas de casamento](https://giogas-pm.github.io/bodas/tabela-de-bodas-de-casamento/)\n" + "".join(f"- [Bodas de {r['nome']} ({anos(r['ano'])})]({BASE}{r['slug']}/)\n" for r in ROWS if r["slug"])
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n").write(readme)
print("urls no sitemap:", len(urls))
