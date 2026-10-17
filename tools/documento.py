"""
Documento metodológico dinámico: una fuente de datos (documento.yaml) → Markdown, HTML, Word, PDF y Quarto.

La plantilla (plantillas/documento-metodologico/documento.md.j2) se llena con los datos del modelo, evalúa los
umbrales con las mismas reglas que tools/verificar.py, arma la matriz de cumplimiento desde evidencias.yaml y marca
como «Completar» —con el requisito que lo exige— cada sección sin datos.

Uso:
    python tools/documento.py nuevo  RUTA_REPO_MODELO            # crea docs/documento.yaml desde la plantilla
    python tools/documento.py render DATOS.yaml [--formatos md,html,docx,pdf,qmd] [--salida DIR]
    python tools/documento.py estilos                              # regenera la plantilla de estilos de Word

Requisitos: pyyaml y jinja2; para Word y HTML, pandoc (paquete pypandoc_binary); para PDF, typst (paquete typst).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, Undefined

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
import esfuerzo  # noqa: E402
import verificar  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PLANT = ROOT / "plantillas" / "documento-metodologico"
ESTILOS = PLANT / "estilos"
CUSTODIO = build.CUSTODIO
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV"}
MODELOS = {"lineal": "Lineal", "ml": "Machine learning", "arbol": "Árbol", "acp": "ACP"}
SEAL, INK, MUTED, RULE = "7A2632", "1B2A2F", "5E6B70", "D5DBD8"


# ----------------------------------------------------------------- utilidades
class Vacio(Undefined):
    """Campos ausentes se comportan como vacíos (y encadenables), para que la plantilla muestre «Completar»."""
    def __getattr__(self, name):
        return Vacio()

    def __getitem__(self, key):
        return Vacio()

    def __str__(self):
        return ""

    def __bool__(self):
        return False

    def __iter__(self):
        return iter(())


def pandoc_bin() -> str | None:
    try:
        import pypandoc
        return pypandoc.get_pandoc_path()
    except Exception:  # noqa: BLE001
        return shutil.which("pandoc")


def num(x):
    return "—" if x in (None, "") else f"{x:,.0f}".replace(",", " ")


def dec(x, n=2):
    return "—" if x in (None, "") else f"{x:.{n}f}"


def pct(x, signo=False):
    if x in (None, ""):
        return "—"
    s = f"{x * 100:+.1f} %" if signo else f"{x * 100:.1f} %"
    return s.replace("-", "−")


def completar(texto, ref):
    return f"> **Completar.** {texto} *(Requisito {ref}.)*"


# ----------------------------------------------------------------- cálculos dinámicos
def evaluar_umbrales(d, umbrales_cat):
    tema = {u["id"]: u for u in umbrales_cat}
    out, fallas = [], []
    vals = dict(d.get("umbrales") or {})
    v = (d.get("datos") or {}).get("ventana") or {}
    if v.get("meses_train_test") is not None and "U-01" not in vals:
        vals["U-01"] = f"{v.get('meses_train_test')} + {v.get('meses_oot')}"
    for uid in sorted(vals, key=lambda x: int(x.split("-")[1])):
        val = vals[uid]
        u = tema.get(uid)
        if not u:
            out.append({"id": uid, "tema": "No existe en el estándar", "valor": val, "regla": "—", "resultado": "Revisar"})
            continue
        if uid == "U-01" and v:
            ok = (v.get("meses_train_test") or 0) >= 12 and v.get("meses_oot") == 1
            regla = "≥ 12 meses entrenamiento/prueba; OOT = último mes con desempeño (1 mes)"
        elif uid in verificar.REGLAS and isinstance(val, (int, float)):
            regla, f = verificar.REGLAS[uid]
            ok = f(val)
        else:
            out.append({"id": uid, "tema": u["tema"], "valor": val, "regla": "Revisión manual", "resultado": "Revisar"})
            continue
        exc = any(e.get("umbral") == uid for e in (d.get("excepciones") or []))
        res = "Cumple" if ok else ("Excepción aprobada" if exc else "No cumple")
        if not ok and not exc:
            fallas.append(uid)
        out.append({"id": uid, "tema": u["tema"], "valor": val, "regla": regla, "resultado": res})
    for u in out:
        for k in ("tema", "regla", "valor"):
            u[k] = str(u[k]).replace("|", r"\|")
    return out, fallas


def matriz_cumplimiento(d, base: Path):
    reqs, _ = verificar.cargar_catalogo()
    ev, man = {}, {}
    ruta = d.get("evidencias")
    if ruta:
        p = (base / ruta).resolve()
        if p.exists():
            man = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            ev = {e["requisito"]: e.get("estado", "pendiente") for e in man.get("evidencias", []) if "requisito" in e}
    # El documento manda; lo que falte se toma del manifiesto de evidencias.
    m = {**(man.get("modelo") or {}), **{k: v for k, v in (d.get("modelo") or {}).items() if v}}
    supuesto = not m.get("tier")
    cfg = verificar.cfg_de({"estandar": m.get("estandar") or "Desarrollo", "tier": m.get("tier") or 2,
                            "tipo_modelo": m.get("tipo_modelo"), "enfoque": m.get("enfoque")})
    aplic = [r for r in reqs if esfuerzo.aplica(r, cfg)]
    fases = {}
    for r in aplic:
        f = fases.setdefault(r["fase"], {"fase": r["fase"], "nombre": r["fase_nombre"], "total": 0,
                                          "cumplido": 0, "excepcion": 0, "no_aplica": 0, "pendiente": 0})
        f["total"] += 1
        f[ev.get(r["id"], "pendiente") if ev.get(r["id"], "pendiente") in f else "pendiente"] += 1
    tot = {k: sum(f[k] for f in fases.values()) for k in ("total", "cumplido", "excepcion", "no_aplica", "pendiente")}
    desc = (f"Requisitos aplicables a un modelo {m.get('estandar') or 'Desarrollo'} Tier {ROMAN.get(cfg['tier'], cfg['tier'])}"
            + (f", {MODELOS.get(cfg['model'], cfg['model'])}, enfoque {'ágil' if cfg['enf'] == 'agil' else 'completo'}" if cfg["std"] in ("Desarrollo", "Implementación") else "")
            + (f". Estado tomado de `{ruta}`." if ev else ". Sin manifiesto de evidencias: todos figuran como pendientes "
               "(ver `tools/verificar.py --init`)."))
    if supuesto:
        desc = "**Tier no definido: se asume Tier II hasta completarlo.** " + desc
    return {"fases": list(fases.values()), "descripcion": desc, **tot}


def grafico_gini(d, destino: Path):
    meses = (d.get("desempeno") or {}).get("mensual") or []
    muestras = {x["muestra"].lower(): x for x in (d.get("desempeno") or {}).get("muestras") or []}
    if len(meses) < 2:
        return None
    train = next((x["gini"] for k, x in muestras.items() if k.startswith("entren")), None)
    W, H, L, R, T, B = 640, 300, 56, 20, 28, 46
    ys = [x["gini"] for x in meses] + ([train, train - 10] if train else [])
    lo, hi = min(ys) - 2, max(ys) + 2
    sx = lambda i: L + i * (W - L - R) / (len(meses) - 1)
    sy = lambda v: T + (hi - v) * (H - T - B) / (hi - lo)
    pts = " ".join(f"{sx(i):.1f},{sy(x['gini']):.1f}" for i, x in enumerate(meses))
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, Calibri, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    paso = 2 if hi - lo <= 16 else 5
    v = int(lo) + 1
    while v < hi:
        if v % paso == 0:
            s += [f'<line x1="{L}" x2="{W - R}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="#{RULE}" stroke-width="0.8"/>',
                  f'<text x="{L - 8}" y="{sy(v) + 4:.1f}" font-size="11" fill="#{MUTED}" text-anchor="end">{v}</text>']
        v += 1
    if train:
        s += [f'<rect x="{L}" y="{sy(train):.1f}" width="{W - L - R}" height="{sy(train - 10) - sy(train):.1f}" fill="#{SEAL}" fill-opacity="0.06"/>',
              f'<line x1="{L}" x2="{W - R}" y1="{sy(train):.1f}" y2="{sy(train):.1f}" stroke="#{INK}" stroke-dasharray="5 4" stroke-width="1.2"/>',
              f'<text x="{W - R}" y="{sy(train) - 6:.1f}" font-size="11" fill="#{INK}" text-anchor="end">Entrenamiento {train:.1f}</text>',
              f'<text x="{W - R}" y="{sy(train - 10) - 6:.1f}" font-size="11" fill="#{SEAL}" text-anchor="end">Límite U-11 (−10 pts)</text>']
    s.append(f'<polyline points="{pts}" fill="none" stroke="#{SEAL}" stroke-width="2.4"/>')
    for i, x in enumerate(meses):
        s += [f'<circle cx="{sx(i):.1f}" cy="{sy(x["gini"]):.1f}" r="3.6" fill="#{SEAL}"/>',
              f'<text x="{sx(i):.1f}" y="{H - B + 18}" font-size="11" fill="#{MUTED}" text-anchor="middle">{x["mes"]}</text>']
    s += [f'<text x="{L}" y="16" font-size="12" font-weight="600" fill="#{INK}">Gini por mes: construcción y mes OOT</text>', "</svg>"]
    destino.write_text("\n".join(s), encoding="utf-8")
    return destino.name


def lecturas_citadas(md: str):
    lit = build.load_yaml(build.CAT / "literatura.yaml")["obras"]
    ids = set(re.findall(r"\b(?:DES|CAL|IMP|SEG|GOB|PAR|PRC)-[A-Z]\d{1,2}-\d{2}(?:\.\d{2}){0,2}|\bU-\d{2}\b", md))
    sel = [o for o in lit if any(a in ids or any(i.startswith(a + ".") or i.startswith(a + "-") for i in ids) for a in o["aplica"])]
    canon = [o for o in sel if o["nivel"] in ("Canon", "Regulación")]
    return (canon or sel)[:14]


# ----------------------------------------------------------------- render
def renderizar_md(datos: Path, carpeta: Path) -> tuple[str, dict]:
    d = yaml.safe_load(datos.read_text(encoding="utf-8")) or {}
    for k in ("documento", "modelo", "datos", "segmentacion", "variables", "metodologia", "desempeno",
              "interpretabilidad", "gestion", "seguimiento", "gobierno"):
        d.setdefault(k, {})
        if d[k] is None:
            d[k] = {}
    d["documento"]["fecha"] = d["documento"].get("fecha") or dt.date.today().isoformat()
    umbrales_cat = build.load_yaml(build.CAT / "umbrales.yaml")["umbrales"]
    eval_u, fallas = evaluar_umbrales(d, umbrales_cat)
    muestras = {x["muestra"].lower(): x for x in d["desempeno"].get("muestras") or []}
    g_tr = next((x["gini"] for k, x in muestras.items() if k.startswith("entren")), None)
    g_oot = next((x["gini"] for k, x in muestras.items() if k.startswith("oot")), None)
    ctx = {
        "d": d, "version_estandar": build.load_yaml(build.CAT / "umbrales.yaml") and _version(),
        "eval_umbrales": eval_u, "umbrales_falla": fallas,
        "matriz": matriz_cumplimiento(d, datos.parent),
        "graficos": {"gini": grafico_gini(d, carpeta / "grafico-gini.svg")},
        "gini_dif": abs(g_tr - g_oot) if g_tr is not None and g_oot is not None else None, "gini_oot": g_oot,
        "iv_alertas": [v["nombre"] for v in d["variables"].get("finales") or [] if (v.get("iv") or 0) > 0.5],
        "roman": lambda t: ROMAN.get(int(t), t) if t else "—", "modelo_lbl": lambda m: MODELOS.get(m, m),
        "enfoque_lbl": lambda e: {"agil": "ágil", "completo": "completo", "tradicional": "completo"}.get(e, e),
        "num": num, "dec": dec, "pct": pct, "completar": completar, "lecturas": [],
    }
    env = Environment(loader=FileSystemLoader(str(PLANT)), undefined=Vacio, trim_blocks=True, lstrip_blocks=True,
                      keep_trailing_newline=True)
    tpl = env.get_template("documento.md.j2")
    md = tpl.render(**ctx)
    ctx["lecturas"] = lecturas_citadas(md)
    md = tpl.render(**ctx)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md, ctx


def _version():
    m = re.search(r'"version": "([^"]+)"', (ROOT / "tools" / "build.py").read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def exportar(datos: Path, formatos: list[str], salida: Path):
    salida.mkdir(parents=True, exist_ok=True)
    base = datos.stem.replace("documento", "").strip("-_") or "modelo"
    md, ctx = renderizar_md(datos, salida)
    d = ctx["d"]
    nombre = f"{d['modelo'].get('codigo') or 'MODELO'}_documento-metodologico_v{d['documento'].get('version') or '0.1'}"
    hechos = []
    p_md = salida / f"{nombre}.md"
    p_md.write_text(md, encoding="utf-8")
    hechos.append(p_md)
    if "qmd" in formatos:
        qmd = md.replace("toc: true", "toc: true\nformat:\n  html: {embed-resources: true, css: documento.css}\n"
                         "  docx: {reference-doc: referencia.docx}\n  typst: {papersize: a4}", 1)
        (salida / f"{nombre}.qmd").write_text(qmd, encoding="utf-8")
        for f in ("documento.css", "referencia.docx"):
            if (ESTILOS / f).exists():
                shutil.copy(ESTILOS / f, salida / f)
        hechos.append(salida / f"{nombre}.qmd")
    pd = pandoc_bin()
    need = [f for f in formatos if f in ("html", "docx", "pdf")]
    if need and not pd:
        print("Pandoc no está disponible: instala `pip install pypandoc_binary` para Word, HTML y PDF.")
        return hechos
    comunes = [pd, str(p_md), "--from", "markdown+pipe_tables+yaml_metadata_block+implicit_figures+link_attributes",
               "--resource-path", str(salida)]
    if "html" in formatos:
        out = salida / f"{nombre}.html"
        pie = salida / "_pie.html"
        pie.write_text(f'<footer class="pie">{CUSTODIO} · Estándares de Modelos en Banca v{ctx["version_estandar"]}</footer>', encoding="utf-8")
        subprocess.run(comunes + ["--standalone", "--embed-resources", "--mathml", "--css", str(ESTILOS / "documento.css"),
                                  "--include-after-body", str(pie), "-o", str(out)], check=True)
        pie.unlink()
        hechos.append(out)
    if "docx" in formatos:
        ref = ESTILOS / "referencia.docx"
        if not ref.exists():
            crear_referencia_docx()
        out = salida / f"{nombre}.docx"
        md_docx = p_md
        svg = salida / "grafico-gini.svg"
        if svg.exists():
            png = svg_a_png(svg)
            if png:
                md_docx = salida / "_docx.md"
                md_docx.write_text(md.replace(svg.name, png.name), encoding="utf-8")
        cmd = [pd, str(md_docx)] + comunes[2:] + ["--reference-doc", str(ref), "-o", str(out)]
        subprocess.run(cmd, check=True)
        if md_docx != p_md:
            md_docx.unlink()
        hechos.append(out)
    if "pdf" in formatos:
        try:
            import typst
        except ImportError:
            print("Typst no está disponible: instala `pip install typst` para PDF.")
            return hechos
        env = Environment(loader=FileSystemLoader(str(ESTILOS)))
        m = d["modelo"]
        typ_tpl = salida / "_plantilla.typ"
        typ_tpl.write_text(env.get_template("plantilla.typ.j2").render(
            custodio=CUSTODIO, codigo=(m.get("codigo") or ""), titulo_corto="Documento metodológico",
            version=(d["documento"].get("version") or ""), estado=(d["documento"].get("estado") or ""),
            fecha=(d["documento"].get("fecha") or ""), clasificacion=d["documento"].get("clasificacion") or "Uso interno",
            tier=ROMAN.get(int(m["tier"]), m["tier"]) if m.get("tier") else "—", tipo_modelo=MODELOS.get(m.get("tipo_modelo"), "—"),
            tipo_documento=d["documento"].get("tipo") or "Documento metodológico del modelo"), encoding="utf-8")
        typ = salida / "_documento.typ"
        subprocess.run(comunes + ["--to", "typst", "--standalone", "-M", "toc=false", "-V", f"template={typ_tpl.name}", "-o", str(typ)], check=True)
        out = salida / f"{nombre}.pdf"
        typst.compile(str(typ), output=str(out), root=str(salida))
        typ.unlink()
        typ_tpl.unlink()
        hechos.append(out)
    return hechos


def svg_a_png(svg: Path):
    """Word no siempre muestra SVG y Pandoc necesita rsvg-convert para convertirlo: se usa Typst."""
    try:
        import typst
    except ImportError:
        return None
    tmp = svg.with_name("_png.typ")
    tmp.write_text("#set page(width: auto, height: auto, margin: 0pt)\n"
                   f'#image("{svg.name}", width: 16cm)\n', encoding="utf-8")
    png = svg.with_suffix(".png")
    typst.compile(str(tmp), output=str(png), format="png", ppi=200, root=str(svg.parent))
    tmp.unlink()
    return png


# ----------------------------------------------------------------- estilos de Word
def crear_referencia_docx():
    """Parte de la plantilla de referencia de Pandoc y aplica tipografía, colores, tablas, encabezado y pie."""
    pd = pandoc_bin()
    ESTILOS.mkdir(parents=True, exist_ok=True)
    base = ESTILOS / "_base.docx"
    with open(base, "wb") as f:
        subprocess.run([pd, "--print-default-data-file", "reference.docx"], stdout=f, check=True)
    zin = zipfile.ZipFile(base)
    files = {n: zin.read(n) for n in zin.namelist()}
    zin.close()
    st = files["word/styles.xml"].decode("utf-8")

    def estilo(sid, rpr, ppr=None):
        nonlocal st
        m = re.search(rf'<w:style [^>]*w:styleId="{sid}"[^>]*>.*?</w:style>', st, re.S)
        if not m:
            return
        blk = m.group(0)
        nb = re.sub(r"<w:rPr>.*?</w:rPr>", "", blk, flags=re.S)
        if ppr is not None:
            nb = re.sub(r"<w:pPr>.*?</w:pPr>", "", nb, flags=re.S)
            nb = nb.replace("</w:style>", f"<w:pPr>{ppr}</w:pPr></w:style>")
        nb = nb.replace("</w:style>", f"<w:rPr>{rpr}</w:rPr></w:style>")
        st = st.replace(blk, nb)

    serif = '<w:rFonts w:ascii="Georgia" w:hAnsi="Georgia" w:eastAsia="Georgia" w:cs="Georgia"/>'
    st = re.sub(r"<w:rPrDefault>.*?</w:rPrDefault>",
                '<w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>'
                f'<w:color w:val="{INK}"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="es-PE"/></w:rPr></w:rPrDefault>', st, flags=re.S)
    estilo("Title", f'{serif}<w:b/><w:color w:val="{INK}"/><w:sz w:val="48"/><w:szCs w:val="48"/>')
    estilo("Subtitle", f'<w:color w:val="{MUTED}"/><w:sz w:val="28"/><w:szCs w:val="28"/>')
    estilo("Heading1", f'{serif}<w:b/><w:color w:val="{SEAL}"/><w:sz w:val="30"/><w:szCs w:val="30"/>',
           f'<w:keepNext/><w:keepLines/><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="2" w:color="{RULE}"/></w:pBdr>'
           '<w:spacing w:before="360" w:after="140"/><w:outlineLvl w:val="0"/>')
    estilo("Heading2", f'{serif}<w:b/><w:color w:val="{INK}"/><w:sz w:val="24"/><w:szCs w:val="24"/>',
           '<w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="100"/><w:outlineLvl w:val="1"/>')
    estilo("Heading3", f'<w:b/><w:color w:val="{MUTED}"/><w:sz w:val="21"/><w:szCs w:val="21"/>')
    estilo("BlockText", f'<w:i/><w:color w:val="{INK}"/>',
           f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="{SEAL}"/></w:pBdr><w:shd w:val="clear" w:color="auto" w:fill="F1F4F2"/>'
           '<w:spacing w:before="120" w:after="120"/><w:ind w:left="240" w:right="240"/>')
    estilo("Hyperlink", f'<w:color w:val="{SEAL}"/><w:u w:val="single"/>')
    b = f'w:val="single" w:sz="4" w:space="0" w:color="{RULE}"'
    st = re.sub(r'(<w:style [^>]*w:styleId="Table"[^>]*>.*?)<w:tblPr>.*?</w:tblPr>',
                lambda m: m.group(1) + f'<w:tblPr><w:tblBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="{INK}"/>'
                f'<w:bottom {b}/><w:insideH {b}/></w:tblBorders><w:tblCellMar><w:top w:w="50" w:type="dxa"/>'
                '<w:left w:w="90" w:type="dxa"/><w:bottom w:w="50" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tblCellMar></w:tblPr>',
                st, count=1, flags=re.S)
    files["word/styles.xml"] = st.encode("utf-8")

    NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
    XH = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    r = lambda t, c=MUTED, bold=False: (f'<w:r><w:rPr>{"<w:b/>" if bold else ""}<w:color w:val="{c}"/><w:sz w:val="15"/></w:rPr>'
                                        f'<w:t xml:space="preserve">{xml_escape(t)}</w:t></w:r>')
    fld = lambda code: (f'<w:fldSimple w:instr=" {code} "><w:r><w:rPr><w:color w:val="{MUTED}"/><w:sz w:val="15"/></w:rPr>'
                        '<w:t>1</w:t></w:r></w:fldSimple>')
    files["word/header1.xml"] = (XH + f'<w:hdr {NS}><w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="{SEAL}"/>'
                                 '</w:pBdr><w:tabs><w:tab w:val="right" w:pos="9638"/></w:tabs></w:pPr>'
                                 + r("ESTÁNDARES DE MODELOS EN BANCA", SEAL, True) + '<w:r><w:tab/></w:r>'
                                 + f'<w:fldSimple w:instr=" TITLE "><w:r><w:rPr><w:color w:val="{MUTED}"/><w:sz w:val="15"/></w:rPr><w:t>Documento metodológico</w:t></w:r></w:fldSimple>'
                                 + "</w:p></w:hdr>").encode("utf-8")
    files["word/footer1.xml"] = (XH + f'<w:ftr {NS}><w:p><w:pPr><w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="{RULE}"/>'
                                 '</w:pBdr><w:tabs><w:tab w:val="right" w:pos="9638"/></w:tabs></w:pPr>'
                                 + r(CUSTODIO, INK, True) + r("  ·  Uso interno") + '<w:r><w:tab/></w:r>'
                                 + r("Página ") + fld("PAGE") + r(" de ") + fld("NUMPAGES") + "</w:p></w:ftr>").encode("utf-8")
    rels = files["word/_rels/document.xml.rels"].decode("utf-8")
    if "header1.xml" not in rels:
        rels = rels.replace("</Relationships>",
                            '<Relationship Id="rIdHdr1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>'
                            '<Relationship Id="rIdFtr1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>')
    files["word/_rels/document.xml.rels"] = rels.encode("utf-8")
    ct = files["[Content_Types].xml"].decode("utf-8")
    if "header1.xml" not in ct:
        ct = ct.replace("</Types>",
                        '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
                        '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>')
    files["[Content_Types].xml"] = ct.encode("utf-8")
    doc = files["word/document.xml"].decode("utf-8")
    sect = ('<w:sectPr><w:headerReference w:type="default" r:id="rIdHdr1"/><w:footerReference w:type="default" r:id="rIdFtr1"/>'
            '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1418" w:right="1134" w:bottom="1247" w:left="1134" '
            'w:header="567" w:footer="567" w:gutter="0"/></w:sectPr>')
    doc = re.sub(r"<w:sectPr\b.*?</w:sectPr>|<w:sectPr\b[^>]*/>", sect, doc, count=1, flags=re.S) if "<w:sectPr" in doc \
        else doc.replace("</w:body>", sect + "</w:body>")
    if 'xmlns:r=' not in doc[:600]:
        doc = doc.replace("<w:document ", '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
    files["word/document.xml"] = doc.encode("utf-8")
    out = ESTILOS / "referencia.docx"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b_ in files.items():
            z.writestr(n, b_)
    base.unlink()
    import xml.dom.minidom as md_
    for n in ("word/styles.xml", "word/header1.xml", "word/footer1.xml", "word/document.xml"):
        md_.parseString(files[n])
    print(f"Plantilla de estilos de Word: {out}")


# ----------------------------------------------------------------- nuevo
def cmd_nuevo(repo: Path):
    repo = repo.resolve()
    destino = repo / "docs" / "documento.yaml"
    if destino.exists():
        sys.exit(f"{destino} ya existe.")
    s = (PLANT / "documento-plantilla.yaml").read_text(encoding="utf-8")
    rep = {}
    ficha = repo / "MODEL_CARD.md"
    if ficha.exists():
        m = re.search(r"```yaml\n(.*?)```", ficha.read_text(encoding="utf-8"), re.S)
        mc = (yaml.safe_load(m.group(1)) if m else None) or {}
        rep = {"codigo": mc.get("codigo_inventario"), "nombre": mc.get("nombre"), "tier": mc.get("tier"),
               "tipo_modelo": mc.get("tipo_modelo"), "enfoque": mc.get("enfoque"), "uso": mc.get("uso")}
    man = repo / "evidencias.yaml"
    if man.exists():
        mm = (yaml.safe_load(man.read_text(encoding="utf-8")) or {}).get("modelo") or {}
        for k in ("codigo", "estandar", "tier", "tipo_modelo", "enfoque"):
            if mm.get(k) and not rep.get(k):
                rep[k] = mm[k]
        s = s.replace("evidencias: null", "evidencias: ../evidencias.yaml")
    for k, v in rep.items():
        if v:
            v = {"I": 1, "II": 2, "III": 3, "IV": 4}.get(str(v), v) if k == "tier" else v
            v = v if isinstance(v, int) else json.dumps(str(v), ensure_ascii=False)
            s = re.sub(rf"^(  {k}:)[^#\n]*", lambda x: f"{x.group(1)} {v}".ljust(len(x.group(0))) + " ", s,
                       count=1, flags=re.M)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(s, encoding="utf-8")
    print(f"Datos del documento creados: {destino}\nGenera el documento con: python tools/documento.py render {destino}")


def main():
    ap = argparse.ArgumentParser(description="Documento metodológico dinámico del estándar.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("nuevo")
    n.add_argument("repo", type=Path)
    r = sub.add_parser("render")
    r.add_argument("datos", type=Path)
    r.add_argument("--formatos", default="md,html,docx,pdf")
    r.add_argument("--salida", type=Path)
    sub.add_parser("estilos")
    a = ap.parse_args()
    if a.cmd == "nuevo":
        cmd_nuevo(a.repo)
    elif a.cmd == "estilos":
        crear_referencia_docx()
    else:
        salida = a.salida or a.datos.parent / "salida"
        for p in exportar(a.datos, [f.strip() for f in a.formatos.split(",")], salida):
            print(f"✓ {p}")


if __name__ == "__main__":
    main()
