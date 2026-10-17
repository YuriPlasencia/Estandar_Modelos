"""
Actas de reunión del estándar: crear, validar y exportar a Word (.docx) y Markdown.

Pensado para analistas y agentes de IA que trabajan desde el repositorio. El editor en línea del sitio
usa el mismo esquema (dist/acta.schema.json) y el mismo diseño de documento: si cambias el formato aquí,
cambia también `actaDocx` en tools/site_template.html.

Uso:
    python tools/acta.py tipos
    python tools/acta.py nueva --tipo R5 --codigo MOD-ORI-001 --nombre "Score de originación TC" \
        --tier II --modelo ml --fecha 2026-10-20 -o actas/MOD-ORI-001/acta-05.json
    python tools/acta.py validar actas/MOD-ORI-001/acta-05.json
    python tools/acta.py exportar actas/MOD-ORI-001/acta-05.json --docx --md

Sin dependencias fuera de la librería estándar (más PyYAML si la entrada es .yaml).
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
CUSTODIO = "Yuri Plasencia — Analytics Pricing & Revenue Management"
NOMBRE_ESTANDAR = "Estándares de Modelos en Banca"

ESTADOS = ["Borrador", "En revisión", "Aprobada"]
ROLES = ["Decide", "Aprueba", "Consultado", "Informado", "Secretario"]
EST_DECISION = ["Acordada", "Pendiente de aprobación", "Rechazada"]
EST_ACUERDO = ["Abierto", "Cerrado"]
EST_CONFORMIDAD = ["Pendiente", "Conforme", "Observado"]
MODELOS = {"lineal": "Lineal", "ml": "ML", "arbol": "Árbol", "acp": "ACP"}

_str = {"type": "string"}
SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "acta.schema.json",
    "title": "Acta de reunión — " + NOMBRE_ESTANDAR,
    "type": "object",
    "required": ["tipo", "numero", "estado", "version", "modelo", "fecha", "objetivo"],
    "properties": {
        "id": _str, "tipo": {"type": "string", "description": "id del tipo en catalogo/actas.yaml"},
        "numero": {"type": "string", "description": "Ej.: ACTA-MOD-ORI-001-05"},
        "estado": {"enum": ESTADOS}, "version": {"type": "integer", "minimum": 1},
        "modelo": {"type": "object", "required": ["codigo", "nombre"], "properties": {
            "codigo": _str, "nombre": _str, "tier": {"enum": ["I", "II", "III", ""]},
            "tipo_modelo": {"enum": list(MODELOS) + [""]}}},
        "fecha": {"type": "string", "format": "date"}, "hora_inicio": _str, "hora_fin": _str,
        "modalidad": {"enum": ["Presencial", "Virtual", "Mixta", ""]}, "lugar": _str, "secretario": _str,
        "objetivo": _str, "agenda": {"type": "array", "items": _str}, "resumen": _str,
        "asistentes": {"type": "array", "items": {"type": "object", "properties": {
            "nombre": _str, "area": _str, "rol": {"enum": ROLES + [""]}, "asistio": {"type": "boolean"}}}},
        "decisiones": {"type": "array", "items": {"type": "object", "properties": {
            "texto": _str, "ref": {"type": ["string", "null"]}, "responsable": _str, "estado": {"enum": EST_DECISION}}}},
        "excepciones": {"type": "array", "items": {"type": "object", "properties": {
            "umbral": _str, "valor": _str, "justificacion": _str, "comite": {"type": "boolean"}}}},
        "acuerdos": {"type": "array", "items": {"type": "object", "properties": {
            "accion": _str, "responsable": _str, "fecha": _str, "estado": {"enum": EST_ACUERDO}}}},
        "evidencias": {"type": "array", "items": _str},
        "conformidad": {"type": "array", "items": {"type": "object", "properties": {
            "nombre": _str, "area": _str, "estado": {"enum": EST_CONFORMIDAD}, "fecha": _str, "medio": _str}}},
        "historial": {"type": "array", "items": {"type": "object", "properties": {
            "fecha": _str, "version": {"type": "integer"}, "cambio": _str, "por": {"type": ["string", "null"]}}}},
        "estandar_version": _str,
    },
}


# ----------------------------------------------------------------- catálogo
def load_tipos():
    import yaml
    with open(ROOT / "catalogo" / "actas.yaml", encoding="utf-8") as f:
        return {t["id"]: t for t in yaml.safe_load(f)["tipos"]}


def nueva(tipo: dict, codigo: str, nombre: str, tier="", modelo="", fecha=None, n=1, secretario="") -> dict:
    hoy = (fecha or date.today().isoformat())
    return {
        "tipo": tipo["id"], "numero": f"ACTA-{codigo}-{n:02d}", "estado": "Borrador", "version": 1,
        "modelo": {"codigo": codigo, "nombre": nombre, "tier": tier, "tipo_modelo": modelo},
        "fecha": hoy, "hora_inicio": "", "hora_fin": "", "modalidad": "Virtual", "lugar": "", "secretario": secretario,
        "objetivo": tipo["objetivo"], "agenda": list(tipo["agenda"]), "resumen": "",
        "asistentes": [{"nombre": "", "area": p["area"], "rol": p["rol"], "asistio": True} for p in tipo["participantes"]],
        "decisiones": [{"texto": d["texto"], "ref": d.get("ref"), "responsable": "", "estado": "Pendiente de aprobación"}
                       for d in tipo["decisiones"]],
        "excepciones": [], "acuerdos": [], "evidencias": list(tipo["entregables"]),
        "conformidad": [{"nombre": "", "area": p["area"], "estado": "Pendiente", "fecha": "", "medio": "Correo"}
                        for p in tipo["participantes"] if p["rol"] in ("Decide", "Aprueba")],
        "historial": [{"fecha": hoy, "version": 1, "cambio": "Creación del acta", "por": None}],
        "estandar_version": "1.2.0",
    }


def validar(a: dict) -> list[str]:
    err = []
    for k in SCHEMA["required"]:
        if not a.get(k):
            err.append(f"falta el campo obligatorio '{k}'")
    if a.get("estado") not in ESTADOS:
        err.append(f"estado inválido: {a.get('estado')}")
    if a.get("estado") == "Aprobada":
        if not a.get("conformidad"):
            err.append("agrega al menos un aprobador")
        if any(d.get("estado") == "Pendiente de aprobación" for d in a.get("decisiones", [])):
            err.append("hay decisiones aún pendientes de aprobación")
        if not a.get("resumen"):
            err.append("un acta aprobada debe tener el desarrollo de la reunión")
        if any(c.get("estado") != "Conforme" for c in a.get("conformidad", [])):
            err.append("un acta aprobada requiere la conformidad de todos los aprobadores")
        if any(not x.get("nombre") for x in a.get("asistentes", [])):
            err.append("hay participantes sin nombre")
    for d in a.get("decisiones", []):
        if d.get("estado") not in EST_DECISION:
            err.append(f"decisión con estado inválido: {d.get('texto')}")
    return err


# ----------------------------------------------------------------- Markdown
def to_md(a: dict, tipos: dict) -> str:
    t = tipos.get(a["tipo"], {})
    m = a["modelo"]
    L = [f"# Acta de reunión · {a['numero']}", "",
         f"**{t.get('nombre', a['tipo'])}** · Estado: **{a['estado']}** · Versión {a['version']}"
         + (f" · Requisito del estándar: `{t['requisito']}`" if t.get("requisito") else ""), "",
         "## 1. Datos generales", "",
         "| | | | |", "|---|---|---|---|",
         f"| **Código de modelo** | {m['codigo']} | **Nombre del modelo** | {m['nombre']} |",
         f"| **Tier** | {m.get('tier') or '—'} | **Tipo de modelo** | {MODELOS.get(m.get('tipo_modelo'), '—')} |",
         f"| **Fecha** | {a['fecha']} | **Horario** | {a.get('hora_inicio') or '—'} – {a.get('hora_fin') or '—'} |",
         f"| **Modalidad** | {a.get('modalidad') or '—'} | **Lugar / enlace** | {a.get('lugar') or '—'} |",
         f"| **Secretario** | {a.get('secretario') or '—'} | **Hito** | {t.get('acta', '—')} |", "",
         "## 2. Participantes", "", "| Nombre | Área | Rol | Asistió |", "|---|---|---|---|"]
    L += [f"| {x['nombre'] or '—'} | {x['area']} | {x['rol']} | {'Sí' if x.get('asistio') else 'No'} |" for x in a["asistentes"]]
    L += ["", "## 3. Objetivo", "", a["objetivo"] or "—", "", "## 4. Agenda", ""]
    L += [f"{i}. {x}" for i, x in enumerate(a["agenda"], 1)] or ["—"]
    L += ["", "## 5. Desarrollo de la reunión", "", a.get("resumen") or "—", "",
          "## 6. Decisiones", "", "| # | Decisión | Requisito | Responsable | Estado |", "|---|---|---|---|---|"]
    L += [f"| {i} | {d['texto']} | {d.get('ref') or '—'} | {d.get('responsable') or '—'} | {d['estado']} |"
          for i, d in enumerate(a["decisiones"], 1)] or ["| — | Sin decisiones registradas | | | |"]
    L += ["", "## 7. Excepciones a umbrales", ""]
    if a["excepciones"]:
        L += ["| Umbral | Valor obtenido | Justificación | ¿Va a Comité? |", "|---|---|---|---|"]
        L += [f"| {e['umbral']} | {e['valor']} | {e['justificacion']} | {'Sí' if e.get('comite') else 'No'} |" for e in a["excepciones"]]
    else:
        L.append("No se registraron excepciones.")
    L += ["", "## 8. Acuerdos y pendientes", ""]
    if a["acuerdos"]:
        L += ["| # | Acción | Responsable | Fecha compromiso | Estado |", "|---|---|---|---|---|"]
        L += [f"| {i} | {x['accion']} | {x['responsable']} | {x['fecha']} | {x['estado']} |" for i, x in enumerate(a["acuerdos"], 1)]
    else:
        L.append("Sin pendientes.")
    L += ["", "## 9. Evidencias y entregables revisados", ""]
    L += [f"- {x}" for x in a["evidencias"]] or ["—"]
    L += ["", "## 10. Conformidad", "", "| Nombre | Área / cargo | Conformidad | Fecha | Medio |", "|---|---|---|---|---|"]
    L += [f"| {c['nombre'] or '—'} | {c['area']} | {c['estado']} | {c.get('fecha') or '—'} | {c.get('medio') or '—'} |" for c in a["conformidad"]]
    L += ["", "## 11. Control de cambios", "", "| Versión | Fecha | Cambio |", "|---|---|---|"]
    L += [f"| {h['version']} | {h['fecha'][:10]} | {h['cambio']} |" for h in a["historial"]]
    L += ["", "---", f"*{NOMBRE_ESTANDAR} v{a.get('estandar_version', '')} · {CUSTODIO}*", ""]
    return "\n".join(L)


# ----------------------------------------------------------------- Word (OOXML)
INK, SEAL, MUTED, RULE, WASH = "1B2A2F", "7A2632", "4A5A60", "C9D1CE", "EAEFEC"


def _r(text, b=False, color=None, sz=None, i=False):
    rpr = ("<w:b/>" if b else "") + ("<w:i/>" if i else "") + (f'<w:color w:val="{color}"/>' if color else "") + \
          (f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>' if sz else "")
    parts = str(text).split("\n")
    inner = "<w:br/>".join(f'<w:t xml:space="preserve">{escape(p)}</w:t>' for p in parts)
    return f"<w:r>{('<w:rPr>' + rpr + '</w:rPr>') if rpr else ''}{inner}</w:r>"


def _p(runs="", style=None, align=None, after=None, keep=False):
    ppr = (f'<w:pStyle w:val="{style}"/>' if style else "") + ("<w:keepNext/>" if keep else "") + \
          (f'<w:spacing w:after="{after}"/>' if after is not None else "") + (f'<w:jc w:val="{align}"/>' if align else "")
    if isinstance(runs, str) and not runs.startswith("<w:r"):
        runs = _r(runs) if runs else ""
    return f"<w:p>{('<w:pPr>' + ppr + '</w:pPr>') if ppr else ''}{runs}</w:p>"


def _tc(content, w, fill=None, bold=False, color=None):
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ""
    paras = "".join(_p(_r(c, b=bold, color=color), after=0) for c in (content if isinstance(content, list) else [content]))
    return f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd}</w:tcPr>{paras}</w:tc>'


def _tbl(rows, widths, header=True, label_cols=()):
    b = f'w:val="single" w:sz="4" w:space="0" w:color="{RULE}"'
    out = [f'<w:tbl><w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:tblBorders><w:top {b}/><w:left {b}/>'
           f'<w:bottom {b}/><w:right {b}/><w:insideH {b}/><w:insideV {b}/></w:tblBorders>'
           '<w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/>'
           '<w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>'
           + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>"]
    for ri, row in enumerate(rows):
        hdr = header and ri == 0
        trpr = "<w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>" if hdr else "<w:trPr><w:cantSplit/></w:trPr>"
        cells = "".join(_tc(c if c not in (None, "") else "—", widths[ci],
                            fill=WASH if hdr or ci in label_cols else None, bold=hdr or ci in label_cols,
                            color=INK if hdr or ci in label_cols else None) for ci, c in enumerate(row))
        out.append(f"<w:tr>{trpr}{cells}</w:tr>")
    return "".join(out) + "</w:tbl>" + _p("", after=120)


def _h(n, text):
    return _p(_r(f"{n}. {text}"), style="Heading1", keep=True)


def to_docx(a: dict, tipos: dict, path: Path):
    t = tipos.get(a["tipo"], {})
    m = a["modelo"]
    W = 9638  # ancho útil A4 con márgenes de 2 cm (twips)
    body = [
        _p(_r("ACTA DE REUNIÓN", b=True, color=SEAL, sz=18), after=40),
        _p(_r(t.get("nombre", a["tipo"])), style="Title"),
        _p(_r(f"{a['numero']}  ·  Estado: ", color=MUTED) + _r(a["estado"], b=True, color=SEAL if a["estado"] == "Aprobada" else INK)
           + _r(f"  ·  Versión {a['version']}" + (f"  ·  Requisito {t['requisito']}" if t.get("requisito") else ""), color=MUTED), after=240),
        _h(1, "Datos generales"),
        _tbl([["Código de modelo", m["codigo"], "Nombre del modelo", m["nombre"]],
              ["Tier", m.get("tier"), "Tipo de modelo", MODELOS.get(m.get("tipo_modelo"), "")],
              ["Fecha", a["fecha"], "Horario", f"{a.get('hora_inicio') or '—'} – {a.get('hora_fin') or '—'}"],
              ["Modalidad", a.get("modalidad"), "Lugar / enlace", a.get("lugar")],
              ["Secretario", a.get("secretario"), "Hito del estándar", t.get("acta")]],
             [1900, 2919, 1900, 2919], header=False, label_cols=(0, 2)),
        _h(2, "Participantes"),
        _tbl([["Nombre", "Área", "Rol", "Asistió"]] +
             [[x["nombre"], x["area"], x["rol"], "Sí" if x.get("asistio") else "No"] for x in a["asistentes"]],
             [3200, 3338, 1900, 1200]),
        _h(3, "Objetivo"), _p(a["objetivo"] or "—", after=160),
        _h(4, "Agenda"),
        *[_p(_r(f"{i}.  ", b=True, color=SEAL) + _r(x), after=40) for i, x in enumerate(a["agenda"], 1)], _p("", after=80),
        _h(5, "Desarrollo de la reunión"),
        *[_p(par, after=120) for par in (a.get("resumen") or "—").split("\n\n")],
        _h(6, "Decisiones"),
        _tbl([["#", "Decisión", "Requisito", "Responsable", "Estado"]] +
             [[str(i), d["texto"], d.get("ref"), d.get("responsable"), d["estado"]] for i, d in enumerate(a["decisiones"], 1)]
             if a["decisiones"] else [["#", "Decisión"], ["—", "Sin decisiones registradas"]],
             [450, 4100, 1700, 1800, 1588] if a["decisiones"] else [450, 9188]),
        _h(7, "Excepciones a umbrales"),
        (_tbl([["Umbral", "Valor obtenido", "Justificación", "¿Va a Comité?"]] +
              [[e["umbral"], e["valor"], e["justificacion"], "Sí" if e.get("comite") else "No"] for e in a["excepciones"]],
              [1300, 1900, 5038, 1400]) if a["excepciones"] else _p(_r("No se registraron excepciones.", i=True, color=MUTED), after=160)),
        _h(8, "Acuerdos y pendientes"),
        (_tbl([["#", "Acción", "Responsable", "Fecha compromiso", "Estado"]] +
              [[str(i), x["accion"], x["responsable"], x["fecha"], x["estado"]] for i, x in enumerate(a["acuerdos"], 1)],
              [450, 4500, 2000, 1588, 1100]) if a["acuerdos"] else _p(_r("Sin pendientes.", i=True, color=MUTED), after=160)),
        _h(9, "Evidencias y entregables revisados"),
        *([_p(_r("▪  ", color=SEAL) + _r(x), after=40) for x in a["evidencias"]] or [_p("—")]), _p("", after=80),
        _h(10, "Conformidad"),
        _tbl([["Nombre", "Área / cargo", "Conformidad", "Fecha", "Medio", "Firma"]] +
             [[c["nombre"], c["area"], c["estado"], c.get("fecha"), c.get("medio"), " "] for c in a["conformidad"]],
             [2000, 2200, 1300, 1200, 1100, 1838]),
        _h(11, "Control de cambios"),
        _tbl([["Versión", "Fecha", "Cambio"]] + [[str(h["version"]), h["fecha"][:10], h["cambio"]] for h in a["historial"]],
             [1000, 1600, 7038]),
    ]
    sect = ('<w:sectPr><w:headerReference w:type="default" r:id="rIdH"/><w:footerReference w:type="default" r:id="rIdF"/>'
            '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1418" w:right="1134" w:bottom="1247" w:left="1134" '
            'w:header="567" w:footer="567" w:gutter="0"/></w:sectPr>')
    NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>{"".join(body)}{sect}</w:body></w:document>'
    bline = f'<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="{SEAL}"/></w:pBdr>'
    header = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}><w:p><w:pPr>{bline}'
              f'<w:tabs><w:tab w:val="right" w:pos="{W}"/></w:tabs></w:pPr>'
              + _r(NOMBRE_ESTANDAR.upper(), b=True, color=SEAL, sz=16) + '<w:r><w:tab/></w:r>'
              + _r(f"{a['numero']}  ·  {m['codigo']}", color=MUTED, sz=16) + "</w:p></w:hdr>")
    fld = lambda code: (f'<w:r><w:rPr><w:color w:val="{MUTED}"/><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
                        f'<w:r><w:rPr><w:color w:val="{MUTED}"/><w:sz w:val="16"/></w:rPr><w:instrText xml:space="preserve"> {code} </w:instrText></w:r>'
                        f'<w:r><w:rPr><w:color w:val="{MUTED}"/><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
                        f'<w:r><w:rPr><w:color w:val="{MUTED}"/><w:sz w:val="16"/></w:rPr><w:t>1</w:t></w:r>'
                        f'<w:r><w:rPr><w:color w:val="{MUTED}"/><w:sz w:val="16"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>')
    footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}><w:p><w:pPr>'
              f'<w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="{RULE}"/></w:pBdr>'
              f'<w:tabs><w:tab w:val="right" w:pos="{W}"/></w:tabs></w:pPr>'
              + _r(CUSTODIO, b=True, color=INK, sz=16) + _r("  ·  Uso interno", color=MUTED, sz=16) + '<w:r><w:tab/></w:r>'
              + _r("Página ", color=MUTED, sz=16) + fld("PAGE") + _r(" de ", color=MUTED, sz=16) + fld("NUMPAGES") + "</w:p></w:ftr>")
    styles = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {NS}>'
              '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>'
              f'<w:color w:val="{INK}"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="es-PE"/></w:rPr></w:rPrDefault>'
              '<w:pPrDefault><w:pPr><w:spacing w:after="80" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
              '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/>'
              '<w:pPr><w:spacing w:after="60"/></w:pPr><w:rPr><w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/>'
              f'<w:color w:val="{INK}"/><w:sz w:val="40"/><w:szCs w:val="40"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
              '<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/>'
              f'<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="2" w:color="{RULE}"/></w:pBdr>'
              '<w:spacing w:before="280" w:after="100"/><w:outlineLvl w:val="0"/></w:pPr>'
              f'<w:rPr><w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:b/><w:color w:val="{SEAL}"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>'
              '</w:styles>')
    settings = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings {NS}>'
                '<w:defaultTabStop w:val="709"/></w:settings>')
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties '
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{escape(a["numero"] + " · " + t.get("nombre", ""))}</dc:title>'
            f'<dc:subject>{escape(m["codigo"] + " · " + m["nombre"])}</dc:subject><dc:creator>{escape(NOMBRE_ESTANDAR)}</dc:creator>'
            f'<cp:keywords>acta; {escape(a["tipo"])}; {escape(m["codigo"])}</cp:keywords>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>')
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties '
           'xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           f'<Application>{escape(NOMBRE_ESTANDAR)}</Application><Company>{escape(CUSTODIO)}</Company></Properties>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
          '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
          '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '<Relationship Id="rIdT" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
             '<Relationship Id="rIdH" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>'
             '<Relationship Id="rIdF" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/_rels/document.xml.rels", drels)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/settings.xml", settings)
        z.writestr("word/header1.xml", header)
        z.writestr("word/footer1.xml", footer)
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)


# ----------------------------------------------------------------- CLI
def _load(p: Path) -> dict:
    if p.suffix in (".yaml", ".yml"):
        import yaml
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser(description="Actas de reunión del " + NOMBRE_ESTANDAR)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tipos", help="lista los tipos de acta")
    n = sub.add_parser("nueva", help="crea un acta precargada desde su tipo")
    n.add_argument("--tipo", required=True)
    n.add_argument("--codigo", required=True, help="código de inventario del modelo")
    n.add_argument("--nombre", required=True)
    n.add_argument("--tier", default="", choices=["", "I", "II", "III"])
    n.add_argument("--modelo", default="", choices=[""] + list(MODELOS))
    n.add_argument("--fecha")
    n.add_argument("--n", type=int, default=1, help="correlativo del acta dentro del modelo")
    n.add_argument("--secretario", default="")
    n.add_argument("-o", "--out", required=True)
    v = sub.add_parser("validar")
    v.add_argument("archivo")
    e = sub.add_parser("exportar")
    e.add_argument("archivo")
    e.add_argument("--docx", action="store_true")
    e.add_argument("--md", action="store_true")
    a = ap.parse_args()
    tipos = load_tipos()
    if a.cmd == "tipos":
        for t in tipos.values():
            print(f"{t['id']:8} {t['acta']:28} {t['nombre']}")
    elif a.cmd == "nueva":
        if a.tipo not in tipos:
            sys.exit(f"Tipo desconocido: {a.tipo}. Usa `python tools/acta.py tipos`.")
        acta = nueva(tipos[a.tipo], a.codigo, a.nombre, a.tier, a.modelo, a.fecha, a.n, a.secretario)
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(acta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Acta creada: {out}")
    elif a.cmd == "validar":
        err = validar(_load(Path(a.archivo)))
        print("Acta válida." if not err else "Observaciones:\n  - " + "\n  - ".join(err))
        sys.exit(1 if err else 0)
    elif a.cmd == "exportar":
        p = Path(a.archivo)
        acta = _load(p)
        if not (a.docx or a.md):
            a.docx = a.md = True
        if a.md:
            p.with_suffix(".md").write_text(to_md(acta, tipos), encoding="utf-8")
            print(f"Markdown: {p.with_suffix('.md')}")
        if a.docx:
            to_docx(acta, tipos, p.with_suffix(".docx"))
            print(f"Word: {p.with_suffix('.docx')}")


if __name__ == "__main__":
    main()
