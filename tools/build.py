"""
Build del estándar.

1. Carga catalogo/*.yaml (fuente de verdad) y valida: IDs únicos, referencias de umbrales,
   y que todo ID citado en docs/ y archivos raíz exista.
2. Regenera los bloques <!-- CATALOGO:INICIO X --> ... <!-- CATALOGO:FIN --> de docs/.
3. Escribe dist/catalogo.json, dist/umbrales.json, dist/estimacion.json, dist/llms-full.txt y llms.txt.
4. Genera site/index.html (autocontenido) desde tools/site_template.html.

Uso:  python tools/build.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import esfuerzo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CAT, DOCS, DIST, SITE = ROOT / "catalogo", ROOT / "docs", ROOT / "dist", ROOT / "site"
ROOT_MD = ["AGENTS.md", "CONTRIBUTING.md", "CHANGELOG.md", "README.md"]
CUSTODIO = "Yuri Plasencia — Analytics Pricing & Revenue Management"

MODEL_LABEL = {"lineal": "Lineal", "ml": "ML", "arbol": "Árbol", "acp": "ACP"}
ROMAN = {1: "I", 2: "II", 3: "III"}
ID_RE = re.compile(r"\b(?:(?:DES-D\d|CAL-C\d|PRC-P\d|PAR-R\d{1,2}|SEG-S\d|GOB-G\d)-\d{2}(?:\.\d{2}){0,2}|IMP-\d{2}(?:\.\d{2}){0,2}|VAL-[MIPR]-\d{2}(?:\.\d{2})?|U-\d{2})\b")
MARK_RE = re.compile(r"(<!-- CATALOGO:INICIO (\S+) -->)(.*?)(<!-- CATALOGO:FIN -->)", re.S)

errors: list[str] = []


# ------------------------------------------------------------------ carga
def load_yaml(p: Path):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_catalog():
    fases, reqs = [], []
    for p in sorted(CAT.glob("*.yaml")):
        if p.stem in ("umbrales", "estimacion", "parametros_esfuerzo", "actas", "literatura"):
            continue
        d = load_yaml(p)
        fase = {"fase": d["fase"], "nombre": d["nombre"], "estandar": d["estandar"],
                "origen": d.get("origen"), "archivo": f"catalogo/{p.name}"}
        if d["fase"] == "VAL":
            fase["ambitos"] = d["ambitos_validacion"]
            amb = {a["id"]: a["nombre"] for a in d["ambitos_validacion"]}
            for r in d["requisitos"]:
                reqs.append({"id": r["id"], "estandar": d["estandar"], "fase": "VAL", "fase_nombre": d["nombre"],
                             "tarea": amb[r["ambito"]], "subtarea": r["bloque"], "actividad": r["requisito"],
                             "killer": bool(r.get("killer", False)), "aplica_tier": [1, 2, 3]})
        else:
            for a in d["actividades"]:
                if a.get("retirado"):
                    continue
                r = {"id": a["id"], "estandar": d["estandar"], "fase": d["fase"], "fase_nombre": d["nombre"]}
                r.update(a)
                reqs.append(r)
        fases.append(fase)
    return fases, reqs


# --------------------------------------------------------------- formateo
def tiers_txt(ts):
    ts = sorted(ts)
    if not ts:
        return "—"
    if ts == list(range(ts[0], ts[-1] + 1)) and len(ts) > 1:
        return f"{ROMAN[ts[0]]}–{ROMAN[ts[-1]]}"
    return ", ".join(ROMAN[t] for t in ts)


def aplica_txt(r):
    ap = r.get("aplica_tier")
    if isinstance(ap, list):
        return f"Tier {tiers_txt(ap)}"
    groups: dict[str, list[str]] = {}
    for m, ts in ap.items():
        if ts:
            groups.setdefault(tiers_txt(ts), []).append(MODEL_LABEL.get(m, m))
    if not groups:
        return "—"
    if len(groups) == 1 and len(next(iter(groups.values()))) == len([m for m in ap if m in MODEL_LABEL]):
        return f"Todos los tipos, Tier {next(iter(groups))}"
    return " · ".join(f"{'/'.join(ms)} {t}" for t, ms in groups.items())


def fmt_n(x):
    return f"{x:g}"


def esfuerzo_txt(r):
    d = r.get("dias_esfuerzo")
    if d is None:
        return None
    if isinstance(d, (int, float)):
        return f"{fmt_n(d)} d" if d else None
    ag = sorted({v["agil"] for v in d.values() if v.get("agil") is not None})
    tr = sorted({v["completo"] for v in d.values() if v.get("completo") is not None})

    def rng(vs):
        return fmt_n(vs[0]) if len(vs) == 1 else f"{fmt_n(vs[0])}–{fmt_n(vs[-1])}"
    parts = []
    if ag:
        parts.append(f"{rng(ag)} d ágil")
    if tr:
        parts.append(f"{rng(tr)} d completo")
    return " / ".join(parts) or None


def ent_txt(e):
    n = f" {e['numero']}" if e.get("numero") else ""
    return f"{e['tipo']}{n}: {e['descripcion']}" if e["tipo"] != "Otro" else e["descripcion"]


def activity_md(r):
    lines = r["actividad"].split("\n")
    out = [f"- **`{r['id']}`** {lines[0]}"]
    for ln in lines[1:]:
        if ln.startswith("  - "):
            out.append("    " + ln.strip())
        elif ln.startswith("- "):
            out.append("  " + ln)
        else:
            out[-1] += "  "
            out.append("  " + ln)
    meta = [f"Aplica: {aplica_txt(r)}"]
    if r.get("killer"):
        meta.insert(0, "**KILLER**")
    if (e := esfuerzo_txt(r)):
        meta.append(f"Esfuerzo: {e}")
    if r.get("nivel_automatizacion") is not None:
        meta.append(f"Automatización: {r['nivel_automatizacion']}")
    if r.get("critico"):
        meta.append("Crítico")
    if r.get("eficiencia"):
        meta.append("Eficiencia")
    if r.get("entregables"):
        meta.append("Entregable: " + "; ".join(ent_txt(e) for e in r["entregables"]))
    if r.get("hito"):
        meta.append(f"Hito: {r['hito']}")
    if r.get("umbrales"):
        meta.append("Umbrales: " + ", ".join(r["umbrales"]))
    if r.get("nota_origen"):
        meta.append(f"Nota: {r['nota_origen']}")
    out += ["", "  " + " · ".join(meta)]
    return "\n".join(out)


def block_fase(code, fases, reqs):
    fase = next(f for f in fases if f["fase"] == code)
    rs = [r for r in reqs if r["fase"] == code]
    out = [f"## Catálogo de requisitos · {fase['nombre']}", "",
           f"> Bloque generado desde `{fase['archivo']}` ({len(rs)} requisitos). Para modificarlo, edita el YAML "
           f"y ejecuta `python tools/build.py`. Fuente: {fase['origen']}.", ""]
    cur_t = cur_s = None
    for r in rs:
        parts = r["id"].split("-")[-1].split(".")
        t_key = (r["tarea"], parts[0])
        if t_key != cur_t:
            cur_t, cur_s = t_key, None
            out += [f"### {int(parts[0])} · {r['tarea']}", ""]
        s_key = (r["subtarea"], parts[1] if len(parts) > 1 else "")
        if s_key != cur_s:
            cur_s = s_key
            out += [f"#### {int(parts[0])}.{int(parts[1])} {r['subtarea']}", ""]
        out += [activity_md(r), ""]
    return "\n".join(out)


def block_umbrales(umb, req_doc):
    out = ["| ID | Tema | Regla | Establecido en |", "|---|---|---|---|"]
    for u in umb:
        refs = ", ".join(f"[`{x}`]({req_doc.get(x, '')})" if req_doc.get(x) else f"`{x}`" for x in u["refs"])
        regla = u["regla"].replace("|", "\\|")
        if u.get("nota"):
            regla += f" *Nota: {u['nota']}*"
        out.append(f"| **{u['id']}** | {u['tema']} | {regla} | {refs} |")
    return "\n".join(out) + "\n"


def block_esfuerzo(reqs, P):
    esc = P["escenario_base"]
    an = P.get("anclaje") or {}
    f1 = lambda x: f"{x:.1f}"
    f0 = lambda x: f"{x:.0f}"
    sem = lambda r: f1(r["personas"]["semanas_calendario"])
    dag = lambda r: f0(r["agente"]["dias_habiles"])
    out = [f"**Escenario:** {esc['registros']:,} registros × {esc['columnas']:,} columnas".replace(",", ".")
           + f" · {esc['segmentos']} segmentos · {esc['fte']} personas · {int(esc['pct_reuniones'] * 100)} % del tiempo en reuniones. "
           "Con personas, semanas de **calendario**; con agentes, **días hábiles** con las mismas personas.", ""]
    if an:
        c = an["caso_referencia"]
        out += [f"**Meta U-40:** {an['fte']} personas, máximo {an['meta']['semanas_personas']} semanas; con agentes, máximo "
                f"{an['meta']['dias_habiles_agente']} días hábiles. Caso de referencia del anclaje: {c['std']} Tier {ROMAN[c['tier']]}, "
                f"{MODEL_LABEL[c['model']]}, {'ágil' if c['enf'] == 'agil' else 'completo'}.", ""]
    out += ["### Desarrollo (incluye Implementación y Gobierno)", "",
            "| Tier | Modelo | Personas ágil (sem.) | Personas completo (sem.) | Agente ágil (días) | Agente completo (días) | Ahorro |",
            "|---|---|---:|---:|---:|---:|---:|"]
    for t in (1, 2, 3):
        for m in ("lineal", "ml", "arbol", "acp"):
            r = {e: esfuerzo.estimar(reqs, P, {"std": "Desarrollo", "tier": t, "model": m, "enf": e}) for e in ("agil", "completo")}
            if r["agil"]["dias_catalogo"] == 0:
                continue
            out.append(f"| {ROMAN[t]} | {MODEL_LABEL[m]} | {sem(r['agil'])} | {sem(r['completo'])} | {dag(r['agil'])} | "
                       f"{dag(r['completo'])} | {r['agil']['agente']['ahorro_pct']:.0%} |")
    out += ["", "### Calibración, Parámetros, Pricing, Seguimiento e Implementación", "",
            "| Proyecto | Personas (semanas) | Con agente (días hábiles) | Ahorro |", "|---|---:|---:|---:|"]
    filas = ([(f"Calibración Tier {ROMAN[t]}", {"std": "Calibración", "tier": t, "model": "lineal", "enf": "completo"}) for t in (1, 2, 3)]
             + [(f"Parámetros de riesgo Tier {ROMAN[t]}", {"std": "Parámetros", "tier": t, "model": "ml", "enf": "completo"}) for t in (1, 2, 3)]
             + [(f"Pricing end-to-end Tier {ROMAN[t]}", {"std": "Pricing", "tier": t, "model": "ml", "enf": "completo"}) for t in (1, 2, 3)]
             + [(f"Seguimiento anual de un modelo Tier {ROMAN[t]}", {"std": "Seguimiento", "tier": t, "model": "lineal", "enf": "completo"}) for t in (1, 3)]
             + [("Implementación (proyecto independiente)", {"std": "Implementación", "tier": 1, "model": "lineal", "enf": "agil"})])
    for nombre, cfg in filas:
        r = esfuerzo.estimar(reqs, P, cfg)
        out.append(f"| {nombre} | {sem(r)} | {dag(r)} | {r['agente']['ahorro_pct']:.0%} |")
    # desglose de referencia
    cfg = {"std": "Desarrollo", "tier": 1, "model": "ml", "enf": "agil"}
    r = esfuerzo.estimar(reqs, P, cfg)
    out += ["", "### Desglose de referencia · Tier I, ML, ágil (días-persona)", "",
            "| Fase | Trabajo con personas | Trabajo con agente |", "|---|---:|---:|"]
    for f in r["fases"]:
        out.append(f"| {f['fase']} · {f['nombre']} | {f1(f['trabajo'])} | {f1(f['trabajo_agente'])} |")
    tp, ta = r["personas"]["dias_persona"], r["agente"]["dias_persona"]
    out += [f"| Reuniones y bloqueo por tiempo de máquina ({f1(r['horas_maquina'])} h) | {f1(tp - sum(f['trabajo'] for f in r['fases']))} | "
            f"{f1(ta - sum(f['trabajo_agente'] for f in r['fases']))} |",
            f"| **Total días-persona** | **{f1(tp)}** | **{f1(ta)}** |",
            f"| **Duración con {esc['fte']} personas** | **{sem(r)} semanas** | **{dag(r)} días hábiles** |", ""]
    return "\n".join(out)


DUR_RE = re.compile(r"(<!--DUR:(\S+?)-->).*?(<!--/DUR-->)", re.S)


def _sem(x):
    return f"{x:.1f}" if x < 10 else f"{x:.0f}"


def texto_duracion(clave, reqs, P):
    """Duraciones citadas en el texto de docs/, calculadas con el modelo de esfuerzo anclado a U-40.
    fase:CODIGO  → rango de semanas de esa fase en Desarrollo (de Tier III ágil a Tier I completo).
    proyecto:ESTANDAR → semanas del proyecto por Tier.  Así el texto nunca se desalinea del modelo."""
    esc = P["escenario_base"]
    fte, m = esc["fte"], esc["pct_reuniones"]
    tipo, cod = clave.split(":", 1)
    if tipo == "fase":
        vals = []
        for t in (1, 2, 3):
            for mod in ("lineal", "ml", "arbol", "acp"):
                for e in ("agil", "completo"):
                    r = esfuerzo.estimar(reqs, P, {"std": "Desarrollo", "tier": t, "model": mod, "enf": e})
                    f = next((x for x in r["fases"] if x["fase"] == cod), None)
                    if f and f["trabajo"]:
                        vals.append(f["trabajo"] / (1 - m) / fte / 5)
        lo, hi = min(vals), max(vals)
        rango = _sem(lo) if _sem(lo) == _sem(hi) else f"{_sem(lo)}–{_sem(hi)}"
        return f"≈ {rango} semanas con {fte} personas"
    std = cod
    cfgs = {1: None, 2: None, 3: None}
    for t in cfgs:
        mod = {"Calibración": "lineal", "Seguimiento": "lineal", "Implementación": "lineal"}.get(std, "ml")
        enf = "agil" if std == "Implementación" else "completo"
        cfgs[t] = esfuerzo.estimar(reqs, P, {"std": std, "tier": t, "model": mod, "enf": enf})["personas"]["semanas_calendario"]
    grupos = []
    for t, v in cfgs.items():
        if grupos and _sem(grupos[-1][1]) == _sem(v):
            grupos[-1][0].append(t)
        else:
            grupos.append(([t], v))
    if len(grupos) == 1:
        return f"≈ {_sem(grupos[0][1])} semanas con {fte} personas"
    partes = [f"≈ {_sem(v)} semanas (Tier {ROMAN[ts[0]]}{'–' + ROMAN[ts[-1]] if len(ts) > 1 else ''})" for ts, v in grupos]
    return ", ".join(partes) + f" con {fte} personas"


def block_literatura(lit):
    out = [f"{len(lit['obras'])} obras en {len(lit['temas'])} temas.", ""]
    for t in lit["temas"]:
        obras = [o for o in lit["obras"] if o["tema"] == t["id"]]
        if not obras:
            continue
        out += [f"## {t['nombre']}", ""]
        for o in obras:
            refs = ", ".join(f"`{a}`" for a in o["aplica"])
            out += [f"- **{o['id']}** · *{o['nivel']}* — {o['cita']}", "",
                    f"  {o['por_que']} Fundamenta: {refs}.", ""]
    return "\n".join(out) + "\n"


def block_actas(act):
    out = ["| Tipo (`--tipo`) | Reunión / hito | Evidencia | Requisito | Decisiones precargadas |", "|---|---|---|---|---:|"]
    for t in act["tipos"]:
        req = f"`{t['requisito']}`" if t.get("requisito") else "—"
        out.append(f"| `{t['id']}` | {t['nombre']} | {t['acta']} | {req} | {len(t['decisiones'])} |")
    return "\n".join(out) + "\n"


def block_val(reqs):
    rs = [r for r in reqs if r["fase"] == "VAL"]
    out = [f"## Catálogo de requisitos · Validación", "",
           f"> Bloque generado desde `catalogo/val.yaml` ({len(rs)} requisitos).", ""]
    cur_a = cur_b = None
    for r in rs:
        if r["tarea"] != cur_a:
            cur_a, cur_b = r["tarea"], None
            out += [f"### {r['tarea']}", ""]
        if r["subtarea"] != cur_b:
            cur_b = r["subtarea"]
            out += [f"#### {r['subtarea']}", ""]
        k = " **KILLER**" if r.get("killer") else ""
        u = f" · Umbrales: {', '.join(r['umbrales'])}" if r.get("umbrales") else ""
        out.append(f"- [ ] **`{r['id']}`**{k} {r['actividad']}{u}")
        if r is rs[-1] or rs[rs.index(r) + 1]["subtarea"] != r["subtarea"]:
            out.append("")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------- docs
def split_front(text):
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        return yaml.safe_load(fm) or {}, body.lstrip("\n")
    return {}, text


def main():
    fases, reqs = load_catalog()
    umb = load_yaml(CAT / "umbrales.yaml")["umbrales"]
    P = load_yaml(CAT / "parametros_esfuerzo.yaml")
    ACT = load_yaml(CAT / "actas.yaml")
    LIT = load_yaml(CAT / "literatura.yaml")

    # ---- validaciones
    ids = [r["id"] for r in reqs]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errors.append(f"IDs duplicados: {sorted(dup)}")
    idset = set(ids) | {u["id"] for u in umb}

    def exists(x):
        return x in idset or any(i.startswith(x + ".") or i.startswith(x + "-") for i in idset)

    by_id = {r["id"]: r for r in reqs}
    for t in ACT["tipos"]:
        for ref in [t.get("requisito")] + [d.get("ref") for d in t["decisiones"]]:
            if ref and ref not in idset:
                errors.append(f"actas.yaml · {t['id']} referencia {ref}, que no existe")
    for u in umb:
        for ref in u["refs"]:
            if ref not in by_id:
                errors.append(f"{u['id']} referencia {ref}, que no existe")
            else:
                by_id[ref].setdefault("umbrales", []).append(u["id"])

    # ---- regenerar bloques en docs
    doc_files = sorted(DOCS.rglob("*.md"))
    req_doc: dict[str, str] = {}
    for p in doc_files:
        for m in MARK_RE.finditer(p.read_text(encoding="utf-8")):
            code = m.group(2)
            for r in reqs:
                if r["fase"] == code:
                    req_doc[r["id"]] = p.relative_to(DOCS).as_posix()
    for p in doc_files:
        txt = p.read_text(encoding="utf-8")

        def repl(m):
            code = m.group(2)
            if code == "UMBRALES":
                rel = {k: "../" + v for k, v in req_doc.items()} if p.parent != DOCS else req_doc
                body = block_umbrales(umb, rel)
            elif code == "LITERATURA":
                body = block_literatura(LIT)
            elif code == "ACTAS":
                body = block_actas(ACT)
            elif code == "ESFUERZO":
                body = block_esfuerzo(reqs, P)
            elif code == "VAL":
                body = block_val(reqs)
            elif any(f["fase"] == code for f in fases):
                body = block_fase(code, fases, reqs)
            else:
                errors.append(f"{p.name}: bloque desconocido {code}")
                return m.group(0)
            return f"{m.group(1)}\n{body}\n{m.group(4)}"
        new = MARK_RE.sub(repl, txt)
        new = DUR_RE.sub(lambda m: f"{m.group(1)}{texto_duracion(m.group(2), reqs, P)}{m.group(3)}", new)
        if new != txt:
            p.write_text(new, encoding="utf-8")

    # ---- validar referencias citadas en texto
    pages = []
    for p in sorted(DOCS.rglob("*.md")):
        fm, body = split_front(p.read_text(encoding="utf-8"))
        pages.append({"path": "docs/" + p.relative_to(DOCS).as_posix(), "meta": fm, "md": body})
    for name in ROOT_MD:
        p = ROOT / name
        if p.exists():
            pages.append({"path": name, "meta": {"titulo": name.replace(".md", ""), "estandar": "Repositorio",
                                                  "orden": 90}, "md": p.read_text(encoding="utf-8")})
    for pg in pages:
        clean = re.sub(r"<!-- CATALOGO:INICIO.*?CATALOGO:FIN -->", "", pg["md"], flags=re.S)
        for m in ID_RE.finditer(clean):
            x = m.group(0)
            if not exists(x) and not pg["path"].startswith("docs/frontera") and pg["path"] != "AGENTS.md":
                errors.append(f"{pg['path']}: cita {x}, que no existe en el catálogo")
        if pg["path"].startswith("docs/") and pg["meta"].get("custodio") != CUSTODIO:
            errors.append(f"{pg['path']}: falta el sello de custodio en el front matter")

    page_ids = {pg["meta"].get("id") for pg in pages if pg["meta"].get("id")}

    def cubre(a, x):
        return x == a or x.startswith(a + ".") or x.startswith(a + "-")
    for o in LIT["obras"]:
        if not o.get("aplica"):
            errors.append(f"literatura.yaml · {o['id']} no fundamenta ningún requisito")
        for a in o.get("aplica", []):
            if not (exists(a) or a in page_ids):
                errors.append(f"literatura.yaml · {o['id']} referencia {a}, que no existe")
    for r in reqs:
        ls = [o["id"] for o in LIT["obras"] if any(cubre(a, r["id"]) for a in o["aplica"])]
        if ls:
            r["lecturas"] = ls
    for u in umb:
        ls = [o["id"] for o in LIT["obras"] if u["id"] in o["aplica"] or any(cubre(a, ref) for a in o["aplica"] for ref in u["refs"])]
        if ls:
            u["lecturas"] = ls

    if errors:
        print("ERRORES:\n  - " + "\n  - ".join(errors))
        sys.exit(1)

    # ---- dist
    DIST.mkdir(exist_ok=True)
    for r in reqs:
        if r["fase"] != "VAL":
            r["naturaleza"] = esfuerzo.naturaleza(r)
    meta = {"nombre": "Estándares de Modelos en Banca", "custodio": CUSTODIO, "version": "3.0.1",
            "generado": date.today().isoformat(), "n_requisitos": len(reqs),
            "licencia": "CC-BY-4.0 (contenido) · MIT (código en tools/)"}
    # ---- cifras del README y de CITATION.cff alineadas con el catálogo
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for patron, valor, que in ((r"\*\*(\d+) requisitos\*\*", len(reqs), "requisitos"),
                               (r"\*\*(\d+) umbrales\*\*", len(umb), "umbrales")):
        m = re.search(patron, readme)
        if m and int(m.group(1)) != valor:
            errors.append(f"README.md dice {m.group(1)} {que}; el catálogo tiene {valor}")
    for archivo, patron in (("README.md", r"Versión \*\*([\d.]+)\*\*"), ("CITATION.cff", r"^version: ([\d.]+)")):
        m = re.search(patron, (ROOT / archivo).read_text(encoding="utf-8"), re.M)
        if m and m.group(1) != meta["version"]:
            errors.append(f"{archivo} dice versión {m.group(1)}; el estándar es {meta['version']}")
    if errors:
        print("ERRORES:\n  - " + "\n  - ".join(errors))
        sys.exit(1)
    for r in reqs:
        r["doc"] = "docs/" + req_doc[r["id"]] if r["id"] in req_doc else None
    (DIST / "catalogo.json").write_text(json.dumps({"meta": meta, "fases": fases, "requisitos": reqs},
                                                    ensure_ascii=False, indent=1), encoding="utf-8")
    (DIST / "umbrales.json").write_text(json.dumps({"meta": meta, "umbrales": umb}, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    (DIST / "estimacion.json").write_text(json.dumps({"parametros_esfuerzo": P},
                                                     ensure_ascii=False, indent=1), encoding="utf-8")


    pages.sort(key=lambda x: (x["meta"].get("orden", 99), x["path"]))
    full = [f"# {meta['nombre']} — texto completo para LLMs\n# Custodio: {CUSTODIO} · v{meta['version']} · {meta['generado']}\n"]
    for pg in pages:
        st = pg["meta"].get("estado", "")
        full.append(f"\n\n========== {pg['path']} [{st}] ==========\n\n{pg['md']}")
    (DIST / "llms-full.txt").write_text("".join(full), encoding="utf-8")

    idx = [f"# {meta['nombre']}", "",
           f"> Estándar de desarrollo, calibración, implementación, seguimiento y validación de modelos en banca. "
           f"{CUSTODIO}. Leer AGENTS.md antes de responder: citar IDs, no inventar umbrales, "
           f"distinguir Vigente / Borrador / Propuesta.", "",
           "## Datos estructurados", "",
           "- [Catálogo de requisitos](dist/catalogo.json): todos los requisitos con ID, aplicabilidad por Tier y tipo de modelo",
           "- [Umbrales](dist/umbrales.json): lista cerrada de límites cuantitativos",
           "- [Modelo de esfuerzo](dist/estimacion.json): parámetros para estimar semanas por estándar, Tier, modelo y enfoque",
           "- [Texto completo](dist/llms-full.txt)", "", "## Documentos", ""]
    for pg in pages:
        if pg["path"].startswith("docs/"):
            idx.append(f"- [{pg['meta'].get('titulo')}]({pg['path']}): {pg['meta'].get('estado')}")
    (ROOT / "llms.txt").write_text("\n".join(idx) + "\n", encoding="utf-8")

    # ---- sitio
    tpl = (ROOT / "tools" / "site_template.html").read_text(encoding="utf-8")
    tpl = tpl.replace("/*__ACTAS_CSS__*/", (ROOT / "tools" / "site_actas.css").read_text(encoding="utf-8"))
    tpl = tpl.replace("/*__ACTAS_JS__*/", (ROOT / "tools" / "site_actas.js").read_text(encoding="utf-8"))
    import acta as acta_mod
    (DIST / "acta.schema.json").write_text(json.dumps(acta_mod.SCHEMA, ensure_ascii=False, indent=1), encoding="utf-8")
    (DIST / "literatura.json").write_text(json.dumps(LIT, ensure_ascii=False, indent=1), encoding="utf-8")
    (DIST / "actas.json").write_text(json.dumps(ACT, ensure_ascii=False, indent=1), encoding="utf-8")
    data = {"meta": meta, "pages": pages, "fases": fases, "requisitos": reqs, "umbrales": umb,
            "parametros_esfuerzo": P, "actas": ACT, "literatura": LIT, "naturaleza": {r["id"]: esfuerzo.naturaleza(r) for r in reqs}}
    payload = json.dumps(data, ensure_ascii=False, default=str).replace("</", "<\\/")
    SITE.mkdir(exist_ok=True)
    page = tpl.replace("/*__DATA__*/null", payload)
    # artifact.html: contenido para publicar como Artifact (el host añade el esqueleto HTML)
    (SITE / "artifact.html").write_text(page, encoding="utf-8")
    # index.html: documento completo para abrir localmente con doble clic
    head = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n</head>\n<body>\n')
    (SITE / "index.html").write_text(head + page + "\n</body>\n</html>\n", encoding="utf-8")

    print(f"OK · {len(reqs)} requisitos · {len(umb)} umbrales · {len(pages)} páginas")


if __name__ == "__main__":
    main()
