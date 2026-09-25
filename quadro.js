/* Bodas — motor compartilhado: cálculo de datas, ícones e render do quadro (app, páginas de SEO e mockups). */
(function (W) {
  var MESES = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'];
  var DIAS = ['domingo','segunda-feira','terça-feira','quarta-feira','quinta-feira','sexta-feira','sábado'];
  function B(ano) { var r = W.BODAS[ano - 1]; return r ? { ano: r[0], nome: r[1], icon: r[2], cor: r[3], sig: r[4], slug: r[5] } : null; }
  function porSlug(s) { for (var i = 0; i < W.BODAS.length; i++) if (W.BODAS[i][5] === s) return B(i + 1); return null; }
  function valida(y, m, d) { if (!(y > 1900 && y < 2200 && m >= 1 && m <= 12 && d >= 1 && d <= 31)) return false; var t = new Date(y, m - 1, d); return t.getFullYear() === y && t.getMonth() === m - 1 && t.getDate() === d; }
  /* aniversário num ano: 29/02 vira 28/02 nos anos não bissextos */
  function aniv(y, m, d, ano) { var dt = new Date(ano, m - 1, d); if (dt.getMonth() !== m - 1) dt = new Date(ano, m, 0); return dt; }
  function dias(a, b) { return Math.round((Date.UTC(b.getFullYear(), b.getMonth(), b.getDate()) - Date.UTC(a.getFullYear(), a.getMonth(), a.getDate())) / 864e5); }
  function hoje0(t) { t = t || new Date(); return new Date(t.getFullYear(), t.getMonth(), t.getDate()); }
  function fmtData(dt) { return dt.getDate() + ' de ' + MESES[dt.getMonth()] + ' de ' + dt.getFullYear(); }
  function fmtCurta(dt) { return ('0' + dt.getDate()).slice(-2) + '/' + ('0' + (dt.getMonth() + 1)).slice(-2) + '/' + dt.getFullYear(); }
  function num(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
  function calc(y, m, d, agora) {
    if (!valida(y, m, d)) return { ok: false };
    var t = hoje0(agora), wed = new Date(y, m - 1, d), r = { ok: true, wed: wed, hoje: t };
    if (wed > t) { r.futuro = true; r.faltamCasar = dias(t, wed); r.anos = 0; r.juntos = 0; }
    else {
      var a = t.getFullYear() - y; if (t < aniv(y, m, d, t.getFullYear())) a--;
      r.anos = a; r.juntos = dias(wed, t);
      r.ehHoje = a >= 1 && dias(aniv(y, m, d, t.getFullYear()), t) === 0;
      r.meses = (t.getFullYear() - y) * 12 + (t.getMonth() - (m - 1)) - (t.getDate() < d ? 1 : 0);
    }
    var pa = r.anos + 1; r.prox = pa <= 100 ? { boda: B(pa), data: aniv(y, m, d, y + pa) } : null;
    if (r.prox) r.prox.faltam = dias(t, r.prox.data);
    r.atual = r.anos >= 1 && r.anos <= 100 ? { boda: B(r.anos), data: aniv(y, m, d, y + r.anos) } : null;
    r.marcos = [];
    [25, 50, 60, 75].forEach(function (k) { if (k > r.anos + 1) { var dt = aniv(y, m, d, y + k); r.marcos.push({ boda: B(k), data: dt, faltam: dias(t, dt) }); } });
    r.seguintes = [];
    for (var k = pa + 1; k <= Math.min(100, pa + 3); k++) r.seguintes.push({ boda: B(k), data: aniv(y, m, d, y + k) });
    return r;
  }
  /* boda "sugerida" pro quadro: a de hoje, senão a próxima */
  function bodaSugerida(r) { if (!r || !r.ok) return 1; if (r.ehHoje) return r.anos; return Math.min(100, Math.max(1, r.anos + 1)); }

  /* ---------- ícones (traço fino, cor da boda) ---------- */
  function svg(inner, c, sw) { return '<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" fill="' + c + '" fill-opacity=".13" stroke="' + c + '" stroke-width="' + (sw || 2.4) + '" stroke-linecap="round" stroke-linejoin="round">' + inner + '</svg>'; }
  var HEART = function (x, y, s) { return '<path transform="translate(' + x + ' ' + y + ') scale(' + s + ')" d="M0 12C-9 5-14 0-14-6a7 7 0 0 1 14-3a7 7 0 0 1 14 3C14 0 9 5 0 12z"/>'; };
  var ICONS = {
    papel: function (c) { return svg('<path d="M32 16h42l18 18v72H32z"/><path d="M74 16v18h18" fill="none"/><path d="M44 44h26M44 54h36" fill="none" stroke-opacity=".6"/>' + HEART(62, 76, 1.1), c); },
    tecido: function (c) { return svg('<rect x="34" y="18" width="52" height="10" rx="4"/><rect x="34" y="92" width="52" height="10" rx="4"/><rect x="41" y="28" width="38" height="64" fill-opacity=".22"/><path d="M41 38l38 8M41 50l38 8M41 62l38 8M41 74l38 8" fill="none" stroke-opacity=".7"/><path d="M79 86c14 2 22 8 18 16s-20 4-30 10" fill="none"/>', c); },
    couro: function (c) { return svg('<path d="M60 102C28 80 14 64 14 44a22 22 0 0 1 46-10a22 22 0 0 1 46 10c0 20-14 36-46 58z"/><path d="M60 92C34 74 23 61 23 45a14 14 0 0 1 28-6l9 9l9-9a14 14 0 0 1 28 6c0 16-11 29-37 47z" fill="none" stroke-dasharray="4 5" stroke-width="1.8"/>', c); },
    flor: function (c) { var p = ''; for (var i = 0; i < 6; i++) p += '<ellipse cx="60" cy="30" rx="11" ry="19" transform="rotate(' + (i * 60) + ' 60 50)"/>'; return svg(p + '<circle cx="60" cy="50" r="9" fill-opacity=".5"/><path d="M60 70v42" fill="none"/><path d="M60 96c-14-2-20-10-22-18 10 0 20 6 22 18zM60 90c12-2 18-9 20-16-9 0-18 5-20 16z"/>', c); },
    rosa: function (c) { return svg('<path d="M60 22c18 0 30 12 30 27 0 17-13 29-30 29S30 66 30 49c0-15 12-27 30-27z"/><path d="M60 36c9 0 15 6 15 13s-6 13-15 13-14-5-14-12c0-6 5-10 11-10 5 0 8 3 8 7" fill="none"/><path d="M60 78v36" fill="none"/><path d="M60 100c-14-1-22-9-24-18 11 0 21 6 24 18zM60 92c11-3 17-11 18-19-9 1-17 7-18 19z"/>', c); },
    arvore: function (c) { return svg('<path d="M54 112V78h12v34" fill-opacity=".3"/><circle cx="60" cy="44" r="26"/><circle cx="38" cy="60" r="18"/><circle cx="82" cy="60" r="18"/><path d="M60 78l-12-12M60 72l14-14" fill="none"/><path d="M36 112h48" fill="none"/>', c); },
    folha: function (c) { var p = '<path d="M60 112C58 80 62 44 72 12" fill="none"/>'; var L = [[64, 90, -50], [60, 76, 40], [66, 60, -45], [62, 46, 42], [70, 32, -40], [67, 20, 40]]; L.forEach(function (l) { p += '<ellipse cx="' + (l[0] + (l[2] < 0 ? -12 : 12)) + '" cy="' + l[1] + '" rx="13" ry="6" transform="rotate(' + l[2] + ' ' + l[0] + ' ' + l[1] + ')"/>'; }); return svg(p, c); },
    doce: function (c) { var cube = function (x, y) { return '<path d="M' + x + ' ' + (y + 10) + 'l20-10 20 10v24l-20 10-20-10z"/><path d="M' + x + ' ' + (y + 10) + 'l20 10 20-10M' + (x + 20) + ' ' + (y + 20) + 'v24" fill="none"/>'; }; return svg(cube(20, 58) + cube(60, 58) + cube(40, 26), c); },
    vaso: function (c) { return svg('<path d="M46 16h28M50 16c0 10-4 14-4 18 0 6 8 8 8 12-14 6-22 18-22 32 0 18 12 30 28 30s28-12 28-30c0-14-8-26-22-32 0-4 8-6 8-12 0-4-4-8-4-18"/><path d="M36 74c16 6 32 6 48 0" fill="none"/>', c); },
    metal: function (c) { return svg('<circle cx="46" cy="66" r="26" fill-opacity=".05"/><circle cx="46" cy="66" r="20" fill="none" stroke-opacity=".5"/><circle cx="74" cy="56" r="26" fill-opacity=".05"/><circle cx="74" cy="56" r="20" fill="none" stroke-opacity=".5"/><path d="M74 24l6-8 6 8-6 6z" fill-opacity=".4"/>', c); },
    gema: function (c) { return svg('<path d="M26 46l16-22h36l16 22-34 52z" fill-opacity=".2"/><path d="M26 46h68M42 24l8 22 10-22 10 22 8-22M50 46l10 52 10-52" fill="none"/>', c); },
    perola: function (c) { var p = ''; for (var i = 0; i < 9; i++) { var a = Math.PI * (0.12 + i * 0.095), x = 60 - 44 * Math.cos(a), y = 34 + 40 * Math.sin(a); p += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="' + (i === 4 ? 12 : 7) + '"/>'; } return svg(p + '<circle cx="56" cy="70" r="3" fill-opacity=".5" stroke="none"/>', c); },
    xicara: function (c) { return svg('<path d="M28 52h56v12c0 16-12 28-28 28S28 80 28 64z"/><path d="M84 58h6a10 10 0 0 1 0 20h-9" fill="none"/><ellipse cx="56" cy="98" rx="38" ry="7"/><path d="M46 40c-4-6 4-10 0-18M60 40c-4-6 4-10 0-18M74 40c-4-6 4-10 0-18" fill="none" stroke-opacity=".6"/><path d="M40 66c4 6 10 9 16 9" fill="none" stroke-opacity=".6"/>', c); },
    coral: function (c) { return svg('<path d="M60 112V70M60 70L44 50M44 50V30M44 50L30 40M60 70l18-22M78 48V26M78 48l14-8M60 86L40 76M40 76L28 80M60 86l20-8M80 78l12 4" fill="none" stroke-width="5" stroke-opacity=".8"/><path d="M36 112h48" fill="none"/>', c); },
    taca: function (c) { var g = function (x, r) { return '<g transform="rotate(' + r + ' ' + x + ' 60)"><path d="M' + (x - 14) + ' 22h28c0 22-4 36-14 38-10-2-14-16-14-38z"/><path d="M' + x + ' 60v30M' + (x - 11) + ' 92h22" fill="none"/><path d="M' + (x - 12) + ' 36h24" fill="none" stroke-opacity=".5"/></g>'; }; return svg(g(44, -12) + g(76, 12) + '<path d="M58 12l2-6M52 14l-4-4M66 14l4-4" fill="none"/>', c); },
    fruta: function (c) { return svg('<circle cx="42" cy="84" r="18"/><circle cx="80" cy="80" r="18"/><path d="M42 66c4-22 14-40 30-50M80 62c-2-18-4-30-8-46" fill="none"/><path d="M72 16c10-4 22 0 26 8-10 4-20 2-26-8z"/>', c); },
    neve: function (c) { var p = ''; for (var i = 0; i < 6; i++) p += '<g transform="rotate(' + (i * 60) + ' 60 60)"><path d="M60 60V14M60 28l-9-9M60 28l9-9M60 42l-8-7M60 42l8-7" fill="none"/></g>'; return svg(p + '<circle cx="60" cy="60" r="6"/>', c); }
  };
  function icon(nome, c) { return (ICONS[nome] || ICONS.couro)(c); }

  /* ---------- quadro ---------- */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]; }); }
  var ESTILOS = { classico: 'Clássico', minimal: 'Moderno', floral: 'Floral', noite: 'Noite de gala' };
  function wreath(c) { var s = ''; for (var i = 0; i < 28; i++) { var a = i / 28 * Math.PI * 2, x = 150 + 132 * Math.cos(a), y = 150 + 132 * Math.sin(a), deg = a * 180 / Math.PI + 90 + (i % 2 ? 28 : -28); s += '<ellipse cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" rx="7" ry="17" transform="rotate(' + deg.toFixed(0) + ' ' + x.toFixed(1) + ' ' + y.toFixed(1) + ')" fill="' + (i % 3 ? '#7f9a6e' : c) + '" fill-opacity="' + (i % 3 ? '.55' : '.7') + '"/>'; } for (var j = 0; j < 7; j++) { var b = j / 7 * Math.PI * 2 + .2, bx = 150 + 136 * Math.cos(b), by = 150 + 136 * Math.sin(b); s += '<circle cx="' + bx.toFixed(1) + '" cy="' + by.toFixed(1) + '" r="10" fill="' + c + '" fill-opacity=".85"/><circle cx="' + bx.toFixed(1) + '" cy="' + by.toFixed(1) + '" r="4" fill="#fff" fill-opacity=".8"/>'; } return '<svg class="qd-wreath" viewBox="0 0 300 300">' + s + '</svg>'; }
  function sprig(c) { return '<svg viewBox="0 0 160 160"><path d="M8 152C40 110 80 70 150 10" fill="none" stroke="#7f9a6e" stroke-width="2.5"/>' + [[40, 118, 30], [62, 96, -20], [84, 74, 35], [104, 54, -25], [124, 34, 30]].map(function (l) { return '<ellipse cx="' + l[0] + '" cy="' + l[1] + '" rx="16" ry="7" transform="rotate(' + l[2] + ' ' + l[0] + ' ' + l[1] + ')" fill="#7f9a6e" fill-opacity=".5"/>'; }).join('') + '<circle cx="150" cy="12" r="9" fill="' + c + '" fill-opacity=".8"/><circle cx="30" cy="140" r="7" fill="' + c + '" fill-opacity=".7"/></svg>'; }
  var ORN = '<svg viewBox="0 0 240 20" class="qd-orn"><path d="M0 10h96M144 10h96" stroke="currentColor" stroke-width="1"/><path d="M104 10l8-6 8 6-8 6zM120 10l8-6 8 6-8 6z" fill="currentColor"/></svg>';
  /* o = {n1, n2, y, m, d, ano, estilo, frase, foto, unlocked} */
  function quadroHTML(o) {
    var b = B(o.ano) || B(1), est = ESTILOS[o.estilo] ? o.estilo : 'classico';
    var dtB = aniv(o.y, o.m, o.d, o.y + b.ano), wed = new Date(o.y, o.m - 1, o.d), dj = dias(wed, dtB);
    var ic = est === 'noite' ? '#d9b86c' : b.cor;
    var nomeLen = b.nome.length, fsNome = nomeLen > 13 ? 76 : nomeLen > 9 ? 96 : 118;
    var n1 = esc(o.n1 || 'Helena'), n2 = esc(o.n2 || 'Roberto');
    var casalLen = (o.n1 || 'Helena').length + (o.n2 || 'Roberto').length + 3;
    var fsCasal = Math.max(34, Math.min(76, Math.floor(610 / (casalLen * 0.43))));
    var fsMin = Math.max(16, Math.min(34, Math.floor((610 - casalLen * 6) / (casalLen * 0.74))));
    fsNome = Math.min(fsNome, Math.floor(600 / (nomeLen * 0.42)));
    var media = o.foto ? '<div class="qd-foto" style="background-image:url(' + o.foto + ')"></div><div class="qd-badge">' + icon(b.icon, ic) + '</div>' : '<div class="qd-icon">' + icon(b.icon, ic) + '</div>';
    var frase = String(o.frase || '').trim();
    var stats = '<div class="qd-stats"><div><b>' + b.ano + '</b>' + (b.ano === 1 ? 'ano' : 'anos') + '</div><div><b>' + num(b.ano * 12) + '</b>meses</div><div><b>' + num(dj) + '</b>dias</div><div><b>' + num(dj * 24) + '</b>horas</div></div>';
    var h = '<div class="qd s-' + est + (o.unlocked ? ' unlocked' : '') + '" style="--ac:' + b.cor + '">';
    h += '<div class="qd-frame"></div>';
    if (est === 'floral') h += '<div class="qd-sprig tl">' + sprig(b.cor) + '</div><div class="qd-sprig br">' + sprig(b.cor) + '</div>';
    if (est === 'noite') h += '<div class="qd-deco tl"></div><div class="qd-deco tr"></div><div class="qd-deco bl"></div><div class="qd-deco br"></div>';
    h += '<div class="qd-in">';
    if (est === 'minimal') {
      h += '<div class="qd-top">Bodas de</div><div class="qd-nome" style="font-size:' + Math.round(fsNome * .82) + 'px">' + esc(b.nome) + '</div>';
      h += '<div class="qd-big">' + b.ano + '<small>' + (b.ano === 1 ? 'ano' : 'anos') + '</small></div>';
      h += '<div class="qd-media">' + media + '</div>';
      h += '<div class="qd-casal" style="font-size:' + fsMin + 'px;letter-spacing:' + (fsMin < 26 ? 4 : 6) + 'px">' + n1 + ' <span>&amp;</span> ' + n2 + '</div>';
    } else {
      h += '<div class="qd-top">Bodas de</div><div class="qd-nome" style="font-size:' + fsNome + 'px">' + esc(b.nome) + '</div>' + ORN;
      h += '<div class="qd-media">' + (est === 'floral' ? wreath(b.cor) : '') + media + '</div>';
      h += '<div class="qd-anos"><b>' + b.ano + '</b> ' + (b.ano === 1 ? 'ano' : 'anos') + ' de casados</div>';
      h += '<div class="qd-casal" style="font-size:' + fsCasal + 'px">' + n1 + ' <span>&amp;</span> ' + n2 + '</div>';
    }
    h += '<div class="qd-datas">' + fmtData(wed) + ' <i>—</i> ' + fmtData(dtB) + '</div>' + stats;
    h += frase ? '<div class="qd-frase">“' + esc(frase) + '”</div>' : '<div class="qd-sig">' + esc(b.sig) + '</div>';
    h += '</div><div class="wm"></div></div>';
    return h;
  }
  W.BD = { B: B, porSlug: porSlug, calc: calc, valida: valida, aniv: aniv, dias: dias, fmtData: fmtData, fmtCurta: fmtCurta, num: num, icon: icon, quadroHTML: quadroHTML, ESTILOS: ESTILOS, MESES: MESES, DIAS: DIAS, bodaSugerida: bodaSugerida, esc: esc };
})(window);
