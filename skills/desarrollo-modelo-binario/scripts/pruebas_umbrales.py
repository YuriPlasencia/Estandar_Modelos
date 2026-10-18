"""Métricas y pruebas de umbrales para modelos binarios bajo el Estándar de Desarrollo.

Yuri Plasencia — Analytics Pricing & Revenue Management.

Solo depende de numpy y pandas. Cada prueba devuelve un dict
{"umbral": "U-xx", "valor": ..., "cumple": bool, "detalle": str}
que se copia tal cual al manifiesto `evidencias.yaml` (campo `umbrales`).

Los valores de corte se copiaron de `catalogo/umbrales.yaml`. Esa es la única fuente de verdad: si el YAML
cambia, este módulo se actualiza. Uso:

    python pruebas_umbrales.py --autotest
"""
from __future__ import annotations

import argparse
import sys

import numpy as np
import pandas as pd

# Cortes de catalogo/umbrales.yaml
U02_PSI_MAX, U02_PSI_MAX_EXCEPCION = 0.10, 0.20
U03_MIN, U03_MAX = 0.95, 1.05
U09_MAX, U09_DESEABLE = 0.40, 0.25
U10_MIN_COMBINACIONES = 50
U11_BRECHA_MAX_PTS, U11_CAIDA_REL_MAX = 5.0, 0.10
U38_IV_FUGA, U38_IV_BAJO = 0.50, 0.02
U41_CAMBIO_REL_MAX = 0.25
U42_PARSIMONIA_PTS = 1.5
U43_MIN_FAMILIAS = 5

# Complejidad por familia, para la regla de parsimonia (U-42). Menor = más simple y explicable.
COMPLEJIDAD = {"logistica": 1, "arbol": 2, "random_forest": 3, "hist_boosting": 4, "xgboost": 5}


def _resultado(umbral, valor, cumple, detalle):
    return {"umbral": umbral, "valor": valor, "cumple": bool(cumple), "detalle": detalle}


# ---------------------------------------------------------------- métricas

def auc(y, score, peso=None):
    """AUC por rangos (Mann–Whitney), con empates promediados y pesos opcionales."""
    y = np.asarray(y, dtype=float)
    s = np.asarray(score, dtype=float)
    w = np.ones_like(y) if peso is None else np.asarray(peso, dtype=float)
    orden = np.argsort(s, kind="mergesort")
    s, y, w = s[orden], y[orden], w[orden]
    # suma ponderada de "buenos con score menor" para cada malo, empates a la mitad
    _, inicio = np.unique(s, return_index=True)
    fin = np.append(inicio[1:], len(s))
    w_pos, w_neg = w * y, w * (1 - y)
    neg_acum, num = 0.0, 0.0
    for a, b in zip(inicio, fin):
        pos_g, neg_g = w_pos[a:b].sum(), w_neg[a:b].sum()
        num += pos_g * (neg_acum + 0.5 * neg_g)
        neg_acum += neg_g
    total_pos, total_neg = w_pos.sum(), w_neg.sum()
    if total_pos == 0 or total_neg == 0:
        raise ValueError("El target necesita ambas clases para calcular el AUC")
    return num / (total_pos * total_neg)


def gini(y, score, peso=None):
    """Gini = 2·AUC − 1, en puntos (0–100). El score debe crecer con la probabilidad del evento."""
    return 100.0 * (2.0 * auc(y, score, peso) - 1.0)


def ks(y, score):
    """KS = máx |F_malos(s) − F_buenos(s)|, en puntos (0–100)."""
    y = np.asarray(y, dtype=float)
    s = np.asarray(score, dtype=float)
    orden = np.argsort(s, kind="mergesort")
    y = y[orden]
    malos = np.cumsum(y) / y.sum()
    buenos = np.cumsum(1 - y) / (1 - y).sum()
    # evaluar solo al final de cada grupo de empates
    ultimo = np.append(np.diff(s[orden]) != 0, True)
    return 100.0 * np.max(np.abs(malos[ultimo] - buenos[ultimo]))


def brier(y, prob):
    y = np.asarray(y, dtype=float)
    p = np.asarray(prob, dtype=float)
    return float(np.mean((p - y) ** 2))


def psi(referencia, actual, tramos=10):
    """PSI = Σ (a_i − e_i)·ln(a_i / e_i), con tramos por cuantiles de la referencia.

    Para variables categóricas pasa tramos=None: cada categoría es un tramo.
    """
    ref = pd.Series(referencia)
    act = pd.Series(actual)
    if tramos is None or not pd.api.types.is_numeric_dtype(ref):
        e = ref.astype(str).value_counts(normalize=True, dropna=False)
        a = act.astype(str).value_counts(normalize=True, dropna=False)
    else:
        cortes = np.unique(np.nanquantile(ref.dropna(), np.linspace(0, 1, tramos + 1)))
        cortes[0], cortes[-1] = -np.inf, np.inf
        e = pd.cut(ref, cortes).value_counts(normalize=True, dropna=False)
        a = pd.cut(act, cortes).value_counts(normalize=True, dropna=False)
    e, a = e.align(a, fill_value=0.0)
    eps = 1e-6
    e, a = e.clip(lower=eps), a.clip(lower=eps)
    return float(((a - e) * np.log(a / e)).sum())


def iv_woe(x, y, tramos=10):
    """WOE_i = ln(g_i / b_i), IV = Σ (g_i − b_i)·WOE_i. Devuelve (iv, tabla por tramo).

    Los faltantes forman su propio tramo. Las categóricas usan cada categoría como tramo.
    """
    x = pd.Series(x).reset_index(drop=True)
    y = pd.Series(y).reset_index(drop=True).astype(int)
    if pd.api.types.is_numeric_dtype(x) and x.nunique(dropna=True) > tramos:
        grupo = pd.qcut(x, tramos, duplicates="drop").astype(object)
    else:
        grupo = x.astype(object)
    grupo = grupo.where(x.notna(), "FALTANTE").astype(str)
    t = pd.crosstab(grupo, y)
    t = t.reindex(columns=[0, 1], fill_value=0)
    eps = 0.5  # corrección de Laplace para tramos sin buenos o sin malos
    g = (t[0] + eps) / (t[0].sum() + eps * len(t))
    b = (t[1] + eps) / (t[1].sum() + eps * len(t))
    woe = np.log(g / b)
    tabla = pd.DataFrame({"n": t.sum(axis=1), "malos": t[1], "tasa": t[1] / t.sum(axis=1), "woe": woe})
    return float(((g - b) * woe).sum()), tabla


def tasa_por_decil(y, score, deciles=10):
    """Tasa observada por decil de score; decil 1 = score más bajo."""
    df = pd.DataFrame({"y": np.asarray(y, dtype=float), "s": np.asarray(score, dtype=float)})
    df["decil"] = pd.qcut(df["s"].rank(method="first"), deciles, labels=range(1, deciles + 1))
    return df.groupby("decil", observed=True)["y"].agg(["count", "mean"]).rename(columns={"mean": "tasa"})


# ---------------------------------------------------------------- pruebas

def prueba_u02(valor_psi, excepcion_sustentada=False):
    """U-02: PSI ≤ 10 % para aceptar una variable; hasta 20 % solo con excepción sustentada."""
    tope = U02_PSI_MAX_EXCEPCION if excepcion_sustentada else U02_PSI_MAX
    return _resultado("U-02", round(valor_psi, 4), valor_psi <= tope,
                      f"PSI {valor_psi:.2%} vs tope {tope:.0%}" + (" (excepción sustentada)" if excepcion_sustentada else ""))


def prueba_u03(tasa_muestra, tasa_poblacion):
    """U-03: 95 % ≤ TM/TG ≤ 105 %. Si falla, ponderar la muestra y usar los pesos en todo lo posterior."""
    r = tasa_muestra / tasa_poblacion
    return _resultado("U-03", round(r, 4), U03_MIN <= r <= U03_MAX,
                      f"TM/TG = {r:.3f}" + ("" if U03_MIN <= r <= U03_MAX else "; ponderar la muestra"))


def prueba_u38(valor_iv):
    """U-38: IV > 0.50 se excluye por sospecha de fuga. IV < 0.02 NO excluye; pasa al multivariado."""
    if valor_iv > U38_IV_FUGA:
        return _resultado("U-38", round(valor_iv, 4), False, "IV > 0.50: excluir por sospecha de fuga e investigar su origen")
    nota = "IV < 0.02: no se excluye por sí solo (DES-D4-05.02.09)" if valor_iv < U38_IV_BAJO else "IV en rango"
    return _resultado("U-38", round(valor_iv, 4), True, nota)


def prueba_u41(tasas_mensuales):
    """U-41: la tasa del target no cambia más de 25 % relativo entre meses consecutivos de Train.

    `tasas_mensuales`: pd.Series indexada por mes, en orden. Devuelve los meses con quiebre en `detalle`;
    la causa (operativa, de política, de proceso) la determina una persona.
    """
    t = pd.Series(tasas_mensuales).astype(float)
    cambio = (t / t.shift(1) - 1).abs().dropna()
    quiebres = cambio[cambio > U41_CAMBIO_REL_MAX]
    detalle = "sin quiebres" if quiebres.empty else "quiebres en: " + ", ".join(f"{m} ({v:.0%})" for m, v in quiebres.items())
    return _resultado("U-41", round(float(cambio.max()), 4) if len(cambio) else 0.0, quiebres.empty, detalle)


def prueba_u09(importancias):
    """U-09: ninguna variable > 40 % de la importancia relativa (deseable ≤ 25 %)."""
    imp = pd.Series(importancias, dtype=float).abs()
    rel = imp / imp.sum()
    top, var = float(rel.max()), rel.idxmax()
    detalle = f"máx {var} = {top:.1%}"
    if top > U09_MAX:
        detalle += "; en árboles forzar colsample_bytree ≤ 0.60 y L2; revisar fuga"
    elif top > U09_DESEABLE:
        detalle += "; cumple, pero sobre el 25 % deseable"
    return _resultado("U-09", round(top, 4), top <= U09_MAX, detalle)


def prueba_u10(n_combinaciones, semilla):
    """U-10: ≥ 50 combinaciones en búsqueda aleatoria y semilla fija."""
    ok = n_combinaciones >= U10_MIN_COMBINACIONES and semilla is not None
    return _resultado("U-10", int(n_combinaciones), ok,
                      f"{n_combinaciones} combinaciones, semilla={semilla}" + ("" if ok else "; sustentar si no se completa"))


def prueba_u11(gini_train, gini_oot):
    """U-11: cumple si brecha ≤ 5 pts O caída relativa ≤ 10 %. Si no cumple ninguna, descalificado (sin excepción).

    También alerta si el Gini OOT supera al de Train (posible fuga; condición de escalamiento).
    """
    brecha = gini_train - gini_oot
    caida = brecha / gini_train if gini_train else float("inf")
    cumple = brecha <= U11_BRECHA_MAX_PTS or caida <= U11_CAIDA_REL_MAX
    detalle = f"brecha {brecha:.2f} pts, caída relativa {caida:.1%}"
    if not cumple:
        detalle += "; DESCALIFICADO"
    if gini_oot > gini_train:
        detalle += "; ALERTA: Gini OOT > Gini Train, revisar fuga y escalar"
    return _resultado("U-11", round(brecha, 2), cumple, detalle)


def prueba_u44(y_oot, score_oot, deciles=10):
    """U-44: tasa observada por decil monótona en el OOT, cero inversiones (score creciente con el riesgo)."""
    tabla = tasa_por_decil(y_oot, score_oot, deciles)
    tasas = tabla["tasa"].to_numpy()
    inversiones = [int(tabla.index[i + 1]) for i in range(len(tasas) - 1) if tasas[i + 1] < tasas[i]]
    detalle = "sin inversiones" if not inversiones else f"inversiones en deciles {inversiones}"
    return _resultado("U-44", len(inversiones), not inversiones, detalle)


def prueba_u43(familias):
    """U-43: al menos 5 familias con la logística regularizada como línea base obligatoria."""
    fam = set(familias)
    ok = len(fam) >= U43_MIN_FAMILIAS and "logistica" in fam
    falta = [] if "logistica" in fam else ["logistica (línea base obligatoria)"]
    return _resultado("U-43", len(fam), ok, f"familias: {sorted(fam)}" + (f"; falta {falta}" if falta else ""))


# ---------------------------------------------------------------- torneo

def tabla_torneo(candidatos):
    """Tabla oficial del torneo (DES-D4-06.03.05).

    `candidatos`: lista de dicts con
      nombre, familia (clave de COMPLEJIDAD), y_train, p_train, y_val, p_val, y_oot, p_oot, importancias (dict)
    """
    filas = []
    for c in candidatos:
        g_tr = gini(c["y_train"], c["p_train"])
        g_va = gini(c["y_val"], c["p_val"])
        g_oot = gini(c["y_oot"], c["p_oot"])
        u11 = prueba_u11(g_tr, g_oot)
        u09 = prueba_u09(c["importancias"])
        u44 = prueba_u44(c["y_oot"], c["p_oot"])
        filas.append({
            "nombre": c["nombre"], "familia": c["familia"],
            "gini_train": g_tr,
            "gini_val": g_va, "ks_val": ks(c["y_val"], c["p_val"]), "auc_val": auc(c["y_val"], c["p_val"]),
            "gini_oot": g_oot, "ks_oot": ks(c["y_oot"], c["p_oot"]), "auc_oot": auc(c["y_oot"], c["p_oot"]),
            "brecha_pts": g_tr - g_oot, "caida_rel": (g_tr - g_oot) / g_tr if g_tr else np.nan,
            "brier_oot": brier(c["y_oot"], c["p_oot"]),
            "concentracion_max": u09["valor"],
            "cumple_u11": u11["cumple"], "cumple_u09": u09["cumple"], "cumple_u44": u44["cumple"],
        })
    return pd.DataFrame(filas)


def elegir_campeon(tabla, metrica="gini_val"):
    """Aplica las reglas de coronación en orden: U-11, U-09, U-42; el Brier se reporta.

    `metrica`: Gini con el que se compara la parsimonia. Por defecto el de validación, porque el OOT no se usa
    para elegir. El estándar no precisa qué Gini usa U-42; si el equipo decide otro, documéntalo en el acta R5.
    Devuelve (nombre del campeón o None, lista de motivos). No incumplir U-44 no descalifica aquí: si el campeón
    tiene inversiones, es un umbral fallado y hay que escalar.
    """
    motivos = []
    t = tabla.copy()
    t["complejidad"] = t["familia"].map(COMPLEJIDAD).fillna(99)
    for regla, col in (("U-11", "cumple_u11"), ("U-09", "cumple_u09")):
        fuera = t.loc[~t[col], "nombre"].tolist()
        if fuera:
            motivos.append(f"{regla} descalifica: {fuera}")
        t = t[t[col]]
    if "logistica" not in set(tabla["familia"]):
        motivos.append("U-43: falta la logística regularizada como línea base")
    if t.empty:
        motivos.append("Ningún candidato elegible: detenerse y escalar")
        return None, motivos
    mejor = t.loc[t[metrica].idxmax()]
    cercanos = t[t[metrica] >= mejor[metrica] - U42_PARSIMONIA_PTS].sort_values(["complejidad", metrica], ascending=[True, False])
    campeon = cercanos.iloc[0]
    if campeon["nombre"] != mejor["nombre"]:
        motivos.append(f"U-42: {campeon['nombre']} está a {mejor[metrica] - campeon[metrica]:.2f} pts de "
                       f"{mejor['nombre']} y es más simple; se elige el simple")
    if not campeon["cumple_u44"]:
        motivos.append(f"U-44 falla en {campeon['nombre']}: inversiones por decil en el OOT; escalar")
    motivos.append(f"Brier OOT del campeón: {campeon['brier_oot']:.4f} (reportar y comparar)")
    return campeon["nombre"], motivos


# ---------------------------------------------------------------- autotest

def _autotest():
    rng = np.random.default_rng(20261017)
    n = 20000
    x = rng.normal(size=n)
    p = 1 / (1 + np.exp(-(-2.5 + 1.2 * x)))
    y = rng.binomial(1, p)

    assert abs(auc([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]) - 0.75) < 1e-12
    assert abs(gini([0, 1], [0.2, 0.9]) - 100) < 1e-9
    assert abs(auc([0, 1, 0, 1], [0.5, 0.5, 0.5, 0.5]) - 0.5) < 1e-12
    g = gini(y, p)
    assert 50 < g < 70, g
    assert 0 < ks(y, p) <= 100
    assert psi(x, x) < 1e-9
    assert psi(x, x + 0.5) > 0.10
    iv, _ = iv_woe(x, y)
    assert 0.3 < iv < 1.5, iv
    assert prueba_u38(iv_woe(y + rng.normal(0, 0.01, n), y)[0])["cumple"] is False  # fuga plantada
    assert prueba_u38(0.01)["cumple"] is True

    assert prueba_u11(70, 64)["cumple"] is True      # 6 pts, caída 8.6 %: cumple por la relativa
    assert prueba_u11(70, 58)["cumple"] is False     # 12 pts: descalificado
    assert "ALERTA" in prueba_u11(60, 62)["detalle"]
    assert prueba_u03(0.051, 0.050)["cumple"] and not prueba_u03(0.040, 0.050)["cumple"]
    assert not prueba_u41(pd.Series([0.05, 0.051, 0.08], index=["m1", "m2", "m3"]))["cumple"]
    assert not prueba_u09({"a": 0.5, "b": 0.3, "c": 0.2})["cumple"]
    assert prueba_u44(y, p)["cumple"]
    assert not prueba_u43(["arbol", "random_forest", "hist_boosting", "xgboost", "otro"])["cumple"]

    def cand(nombre, familia, ruido):
        s = p + rng.normal(0, ruido, n)
        return {"nombre": nombre, "familia": familia, "y_train": y, "p_train": s, "y_val": y, "p_val": s,
                "y_oot": y, "p_oot": s, "importancias": {"x": 0.3, "z": 0.3, "w": 0.4}}
    t = tabla_torneo([cand("LR", "logistica", 0.001), cand("XGB", "xgboost", 0.0005)])
    campeon, motivos = elegir_campeon(t)
    assert campeon == "LR", (campeon, motivos)  # parsimonia
    print("autotest OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--autotest", action="store_true")
    if ap.parse_args().autotest:
        _autotest()
    else:
        ap.print_help()
        sys.exit(0)
