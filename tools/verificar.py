"""
Verificador de evidencias de un modelo contra el estándar.

Compara el manifiesto `evidencias.yaml` del repositorio de un modelo con el catálogo normativo: requisitos
aplicables sin evidencia, archivos faltantes o modificados, excepciones sin acta, umbrales en falla e IDs
inexistentes. Pensado para analistas, agentes de IA e integración continua (sale con código 1 si hay brechas).

Uso:
    python tools/verificar.py --init  RUTA_REPO --estandar Desarrollo --tier 2 --modelo ml --enfoque agil
    python tools/verificar.py --plan  RUTA_REPO --fase DES-D4
    python tools/verificar.py         RUTA_REPO [--hash]
    python tools/verificar.py --sellar RUTA_REPO          # registra el sha256 de los archivos citados
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
import esfuerzo  # noqa: E402

ESTADOS = {"cumplido", "pendiente", "no_aplica", "excepcion"}
ROMAN = {1: "I", 2: "II", 3: "III"}

# Regla numérica de cada umbral sobre el valor que reporta el manifiesto. None = revisión manual.
# El significado del valor reportado se indica en el texto de cada regla.
REGLAS = {
    "U-02": ("PSI máximo de las variables del modelo ≤ 0.10 (≤ 0.20 con excepción)", lambda v: v <= 0.10),
    "U-03": ("Ratio TM/TG entre 0.95 y 1.05", lambda v: 0.95 <= v <= 1.05),
    "U-06": ("Correlación máxima entre continuas < 0.60 (≤ 0.95 con sustento)", lambda v: v < 0.60),
    "U-07": ("V de Cramér máxima entre categóricas < 0.4", lambda v: v < 0.4),
    "U-10": ("Combinaciones de hiperparámetros probadas ≥ 50", lambda v: v >= 50),
    "U-11": ("|Gini Train − Gini OOT| ≤ 10 pts", lambda v: abs(v) <= 10),
    "U-13": ("Materialidad mínima de los ejes de segmentación > 0.05", lambda v: v > 0.05),
    "U-15": ("Coincidencia modelamiento vs. implementación ≥ 0.95", lambda v: v >= 0.95),
    "U-16": ("Meses de certificación con proveedor externo ≥ 3", lambda v: v >= 3),
    "U-38": ("IV máximo de las variables del modelo ≤ 0.50 (salvo investigación de fuga documentada)", lambda v: v <= 0.50),
    "U-39": ("Variables con información posterior a la observación = 0", lambda v: v == 0),
    "U-40": ("Duración del desarrollo con 2 personas ≤ 13 semanas (con agentes de IA ≤ 15 días hábiles)", lambda v: v <= 13),
    "U-21": ("Desvío relativo máximo de la aceptación por decil ≤ 0.10", lambda v: abs(v) <= 0.10),
    "U-22": ("Potencia del experimento ≥ 0.80", lambda v: v >= 0.80),
    "U-23": ("Proporción de operaciones con excepción de precio ≤ 0.15", lambda v: v <= 0.15),
    "U-24": ("Proporción de ofertas dentro del tope regulatorio = 1.0", lambda v: v >= 1.0),
    "U-25": ("Cambio máximo de tasa de lista sin comité ≤ 100 pb", lambda v: abs(v) <= 100),
    "U-26": ("Desvío del margen realizado vs. esperado ≤ 0.15", lambda v: abs(v) <= 0.15),
}


def cargar_catalogo():
    _, reqs = build.load_catalog()
    umbrales = build.load_yaml(build.CAT / "umbrales.yaml")["umbrales"]
    by_id = {r["id"]: r for r in reqs}
    for u in umbrales:
        for ref in u["refs"]:
            if ref in by_id:
                by_id[ref].setdefault("umbrales", []).append(u["id"])
    return [r for r in reqs if r["fase"] != "VAL"], {u["id"] for u in umbrales}


def cfg_de(modelo: dict) -> dict:
    std = modelo["estandar"]
    return {"std": std, "tier": esfuerzo.tier(modelo["tier"]),
            "model": modelo.get("tipo_modelo") or "lineal",
            "enf": "completo" if std in ("Calibración", "Pricing", "Parámetros", "Seguimiento")
            else esfuerzo.enfoque(modelo.get("enfoque") or "agil")}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def cmd_init(repo: Path, a):
    reqs, _ = cargar_catalogo()
    modelo = {"codigo": a.codigo or repo.name, "estandar": a.estandar, "tier": esfuerzo.tier(a.tier),
              "tipo_modelo": a.modelo or "", "enfoque": esfuerzo.enfoque(a.enfoque) if a.enfoque else ""}
    aplicables = [r for r in reqs if esfuerzo.aplica(r, cfg_de(modelo))]
    L = ["# Manifiesto de evidencias. Generado por tools/verificar.py --init el " + date.today().isoformat(),
         "# Estados: cumplido | pendiente | no_aplica | excepcion (con justificación y acta).",
         "modelo:"] + [f"  {k}: {v}" for k, v in modelo.items()] + ["evidencias:"]
    fase = None
    for r in aplicables:
        if r["fase"] != fase:
            fase = r["fase"]
            L.append(f"# ---- {fase} · {r['fase_nombre']}")
        L.append(f"- requisito: {r['id']}   # {r['actividad'].splitlines()[0][:90]}")
        L.append("  estado: pendiente")
        L.append("  archivos: []")
    out = repo / "evidencias.yaml"
    if out.exists() and not a.forzar:
        sys.exit(f"{out} ya existe. Usa --forzar para sobrescribirlo.")
    repo.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Manifiesto creado con {len(aplicables)} requisitos aplicables: {out}")


def cargar_manifiesto(repo: Path) -> dict:
    p = repo / "evidencias.yaml"
    if not p.exists():
        sys.exit(f"No existe {p}. Créalo con --init.")
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def cmd_plan(repo: Path, a):
    reqs, _ = cargar_catalogo()
    man = cargar_manifiesto(repo)
    est = {e["requisito"]: e.get("estado", "pendiente") for e in man.get("evidencias", [])}
    cfg = cfg_de(man["modelo"])
    rs = [r for r in reqs if esfuerzo.aplica(r, cfg) and (not a.fase or r["fase"].startswith(a.fase))]
    print(f"# Plan · {man['modelo']['codigo']} · {a.fase or 'todas las fases'} · {len(rs)} requisitos\n")
    for r in rs:
        e = ", ".join(f"{x['tipo']} {x.get('numero') or ''}".strip() for x in r.get("entregables", []))
        u = f" · umbrales {', '.join(r['umbrales'])}" if r.get("umbrales") else ""
        print(f"- [{'x' if est.get(r['id']) in ('cumplido', 'no_aplica', 'excepcion') else ' '}] {r['id']} "
              f"{r['actividad'].splitlines()[0]}" + (f" → {e}" if e else "") + u)


def cmd_verificar(repo: Path, a):
    reqs, umb = cargar_catalogo()
    ids = {r["id"] for r in reqs}
    man = cargar_manifiesto(repo)
    cfg = cfg_de(man["modelo"])
    aplicables = {r["id"]: r for r in reqs if esfuerzo.aplica(r, cfg)}
    ev = {e["requisito"]: e for e in man.get("evidencias", []) if "requisito" in e}
    falt, arch, hashes, exc, umb_f, desconocidos, est_inv = [], [], [], [], [], [], []
    for i in aplicables:
        if i not in ev:
            falt.append(i)
    for i, e in ev.items():
        if i not in ids:
            desconocidos.append(i)
            continue
        if e.get("estado") not in ESTADOS:
            est_inv.append(i)
        if e.get("estado") == "excepcion" and not (e.get("justificacion") and e.get("acta")):
            exc.append(i)
        for f in e.get("archivos") or []:
            p = repo / f
            if not p.exists():
                arch.append(f"{i}: {f}")
            elif a.hash and (e.get("sha256") or {}).get(f) and sha256(p) != e["sha256"][f]:
                hashes.append(f"{i}: {f}")
        for u, v in (e.get("umbrales") or {}).items():
            if u not in umb:
                desconocidos.append(u)
            elif u in REGLAS and isinstance(v, (int, float)) and not REGLAS[u][1](v) and e.get("estado") != "excepcion":
                umb_f.append(f"{u} = {v} en {i} — regla: {REGLAS[u][0]}")
    cuenta = {s: sum(1 for i in aplicables if ev.get(i, {}).get("estado") == s) for s in ESTADOS}
    pend = [i for i in aplicables if ev.get(i, {}).get("estado", "pendiente") == "pendiente"]
    m = man["modelo"]
    tipo = f" · {m.get('tipo_modelo')} · {cfg['enf']}" if cfg["std"] in ("Desarrollo", "Implementación") else ""
    L = [f"# Verificación de evidencias · {m['codigo']}", "",
         f"{m['estandar']} · Tier {ROMAN.get(cfg['tier'], cfg['tier'])}{tipo} · {date.today().isoformat()}", "",
         "| Estado | Requisitos |", "|---|---:|"]
    L += [f"| {s} | {cuenta[s]} |" for s in ("cumplido", "excepcion", "no_aplica", "pendiente")]
    L += [f"| **aplicables** | **{len(aplicables)}** |", ""]

    def sec(t, xs):
        if xs:
            L.extend([f"## {t} ({len(xs)})", ""] + [f"- {x}" for x in xs] + [""])
    sec("Requisitos aplicables sin entrada en el manifiesto", falt)
    sec("Requisitos pendientes", pend)
    sec("Archivos citados que no existen", arch)
    sec("Archivos modificados desde que se sellaron", hashes)
    sec("Excepciones sin justificación o sin acta", exc)
    sec("Umbrales en falla", umb_f)
    sec("Estados no válidos", est_inv)
    sec("IDs que no existen en el catálogo", desconocidos)
    brechas = falt or arch or hashes or exc or umb_f or desconocidos or est_inv
    L.append("**Resultado:** " + ("hay brechas por cerrar." if brechas or pend else "sin brechas. Listo para Validación."))
    (repo / "reports").mkdir(exist_ok=True)
    (repo / "reports" / "verificacion.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    sys.exit(1 if brechas else 0)


def cmd_sellar(repo: Path, a):
    p = repo / "evidencias.yaml"
    txt = p.read_text(encoding="utf-8")
    man = yaml.safe_load(txt)
    n = 0
    for e in man.get("evidencias", []):
        fs = [f for f in e.get("archivos") or [] if (repo / f).exists()]
        if fs:
            e["sha256"] = {f: sha256(repo / f) for f in fs}
            n += len(fs)
    cab = "".join(l + "\n" for l in txt.splitlines() if l.startswith("#") and not re.match(r"#\s*-{4}", l))
    p.write_text(cab + yaml.safe_dump(man, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    print(f"Sellados {n} archivos en {p}")


def main():
    ap = argparse.ArgumentParser(description="Verifica las evidencias de un modelo contra el estándar.")
    ap.add_argument("repo", type=Path)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--init", action="store_true", help="crea evidencias.yaml con los requisitos aplicables")
    g.add_argument("--plan", action="store_true", help="lista los requisitos de una fase y su estado")
    g.add_argument("--sellar", action="store_true", help="registra el sha256 de los archivos citados")
    ap.add_argument("--estandar", default="Desarrollo", choices=["Desarrollo", "Calibración", "Implementación", "Parámetros", "Pricing", "Seguimiento"])
    ap.add_argument("--tier", type=int, default=2, choices=[1, 2, 3, 4],
                    help="1 | 2 | 3 (4 se acepta como alias de 3, de versiones anteriores)")
    ap.add_argument("--modelo", default="", choices=["", "lineal", "ml", "arbol", "acp"])
    ap.add_argument("--enfoque", default="", choices=["", "agil", "completo", "tradicional"],
                    help="agil: lo esencial con la profundidad mínima suficiente · completo: análisis exhaustivo (tradicional = alias de completo)")
    ap.add_argument("--codigo", default="")
    ap.add_argument("--fase", default="")
    ap.add_argument("--hash", action="store_true", help="comprueba los sha256 registrados")
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()
    if a.init:
        cmd_init(a.repo, a)
    elif a.plan:
        cmd_plan(a.repo, a)
    elif a.sellar:
        cmd_sellar(a.repo, a)
    else:
        cmd_verificar(a.repo, a)


if __name__ == "__main__":
    main()
