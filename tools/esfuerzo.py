"""
Modelo de esfuerzo v2. La misma lógica está replicada en tools/site_template.html (función `estimar`);
si cambias una, cambia la otra.

Pasos, para un proyecto (estándar, Tier, tipo de modelo, enfoque) y un escenario (volumen, FTE, reuniones):
  1. Trabajo directo W = Σ días_catálogo × factor_volumen, sin las actividades de tipo "reunión"
     (su tiempo queda dentro del % de reuniones).
  2. Tiempo de máquina K (horas) y la parte que bloquea a quien trabaja.
  3. Personas:  T = (W + bloqueo) / (1 − %reuniones).  Reuniones R = %reuniones × T.
  4. Agente:    T = W × factor_agente × (1 + supervisión) + bloqueo_agente + R   (mismas reuniones).
  5. Duración en semanas = T / FTE / 5.
"""
from __future__ import annotations

import re

NAT_RULES = [
    ("reunion", re.compile(r"\breuni[oó]n|kick ?off|\bacta\b|presentaci[oó]n en (reuni|cm)|comit[eé]", re.I)),
    ("datos", re.compile(r"revisi[oó]n de diferencias|controles? de calidad|desarrollo de (script|controles)|"
                         r"[aá]rboles de decisi|segmentaci[oó]n (con|por)|construir la tabla", re.I)),
    ("gobierno", re.compile(r"conformidad|aprobaci|^solicit|solicitud|env[ií]o de|evidenci|registrar modelo|"
                            r"participar|cooperar|revisar la aplicaci", re.I)),
    ("documentacion", re.compile(r"^documenta|documentaci[oó]n|documento|manual|memoria|bit[aá]cora|"
                                 r"elaboraci[oó]n de (la )?(ppt|presentaci)|^reporte|cap[ií]tulo|registo|registro al cuadro|especificar las versiones", re.I)),
    ("datos", re.compile(r"\bpsi\b|fill rate|percentil|imputa|correlaci|muestreo|muestra|train|entrenam|optimiz|"
                         r"bootstrap|extracci|\bbase\b|tabla|completitud|unicidad|duplicad|descriptiv|transformaci|"
                         r"\bwoe\b|convoluci|script|ejecuci|calibra|gini|clustering|outlier|evolutivo|pegado|"
                         r"crear variables|puntuaci|% de |missing|estabilidad|matriz|cuadre|performance|boruta|"
                         r"hp |interacci|dummies|encoder|categor", re.I)),
]
VOL_PHASES = {"DES-D1", "DES-D2", "DES-D3", "DES-D4", "CAL-C1", "CAL-C2", "CAL-C3", "CAL-C4", "PRC-P2", "PRC-P4", "PAR-R2", "PAR-R3", "PAR-R4", "PAR-R5"}


def naturaleza(r: dict) -> str:
    if r.get("naturaleza"):
        return r["naturaleza"]
    if r["fase"] == "DES-D7":
        return "gobierno"
    txt = r["actividad"]
    for nat, rx in NAT_RULES:
        if rx.search(txt):
            return nat
    return "analisis"


def aplica(r, cfg):
    if cfg["std"] in ("Calibración", "Pricing", "Parámetros", "Seguimiento"):
        return r["estandar"] == cfg["std"] and cfg["tier"] in r["aplica_tier"]
    ok = ["Desarrollo", "Implementación"] if cfg["std"] == "Desarrollo" else ["Implementación"]
    return r["estandar"] in ok and cfg["tier"] in (r["aplica_tier"].get(cfg["model"]) or [])


def dias_base(r, cfg):
    d = r.get("dias_esfuerzo")
    if d is None:
        return 0.0
    if isinstance(d, (int, float)):
        return float(d)
    v = d.get(cfg["model"]) or {}
    return float(v.get(cfg["enf"]) or 0)


def factor_volumen(r, P, esc):
    if naturaleza(r) != "datos" or r["fase"] not in VOL_PHASES:
        return 1.0
    ref, el = P["volumen_referencia"], P["elasticidad"]
    f_reg = (esc["registros"] / ref["registros"]) ** el["registros"]
    tarea = int(r["id"].split("-")[-1].split(".")[0])
    if r["fase"].startswith(("CAL", "PRC", "PAR")) or (r["fase"] == "DES-D4" and tarea >= 5):
        # calibración: pocos drivers; entrenamiento: variables ya preseleccionadas (U-08)
        return f_reg
    e_col = el["columnas_automatizado"] if (r.get("nivel_automatizacion") or 0) >= 3 else el["columnas_manual"]
    return f_reg * (esc["columnas"] / ref["columnas"]) ** e_col


def horas_maquina(P, esc, cfg):
    if cfg["std"] in ("Implementación", "Seguimiento"):
        return 0.0
    c = P["computo"]
    escala = (esc["registros"] / 1e6) * (P["columnas_modelo"] / 100)
    if cfg["std"] == "Calibración":
        return c["ajustes_calibracion"] * c["minutos_por_ajuste_ref"]["lineal"] * escala / 60
    if cfg["std"] == "Pricing":
        return c["ajustes_pricing"] * c["minutos_por_ajuste_ref"]["ml"] * escala / 60
    if cfg["std"] == "Parámetros":
        return c["ajustes_parametros"] * c["minutos_por_ajuste_ref"]["ml"] * escala / 60
    m = cfg["model"]
    return esc["segmentos"] * c["ajustes_por_segmento"][m] * c["minutos_por_ajuste_ref"][m] * escala / 60


def estimar(reqs, P, cfg, esc=None):
    esc = {**P["escenario_base"], **(esc or {})}
    g, sup = P["agente"]["factor_trabajo"], P["agente"]["supervision"]
    fases: dict[str, dict] = {}
    for r in reqs:
        if not aplica(r, cfg):
            continue
        b = dias_base(r, cfg)
        nat = naturaleza(r)
        f = fases.setdefault(r["fase"], {"fase": r["fase"], "nombre": r["fase_nombre"], "base": 0.0,
                                         "reuniones_catalogo": 0.0, "trabajo": 0.0, "trabajo_agente": 0.0})
        f["base"] += b
        if nat == "reunion":
            f["reuniones_catalogo"] += b
            continue
        w = b * factor_volumen(r, P, esc)
        f["trabajo"] += w
        f["trabajo_agente"] += w * g[nat] * ((1 + sup) if g[nat] < 1 else 1)
    W = sum(f["trabajo"] for f in fases.values())
    Wa = sum(f["trabajo_agente"] for f in fases.values())
    K = horas_maquina(P, esc, cfg)
    bl = P["computo"]["bloqueo"]
    hd = esc["horas_dia"]
    m = esc["pct_reuniones"]
    T_p = (W + K * bl["personas"] / hd) / (1 - m)
    R = m * T_p
    T_a = Wa + K * bl["agente"] / hd + R
    sem = lambda t: t / esc["fte"] / 5
    base = sum(f["base"] for f in fases.values())
    return {
        "escenario": esc, "cfg": cfg, "fases": list(fases.values()),
        "dias_catalogo": base, "trabajo_directo": W, "horas_maquina": K, "dias_reuniones": R,
        "personas": {"dias_persona": T_p, "semanas_calendario": sem(T_p), "meses": sem(T_p) / 4.33},
        "agente": {"dias_persona": T_a, "semanas_calendario": sem(T_a), "meses": sem(T_a) / 4.33,
                   "ahorro_pct": 1 - T_a / T_p if T_p else 0},
    }
