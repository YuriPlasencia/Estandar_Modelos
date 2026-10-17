---
id: FR-03
titulo: "FR-03 · Explicabilidad y modelos interpretables"
estandar: Frontera
estado: Propuesta
version: 0.1.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 53
---

# FR-03 · Explicabilidad y modelos interpretables

**Hoy:** el estándar pide *Unboxing: SHAP value* para ML (DES-D4-07.01.01) y revisión de sentido económico
(DES-D4-05.02.01).

**Propuesta:**

1. **Restricciones de monotonicidad** en gradient boosting (`monotone_constraints` en XGBoost/LightGBM) para toda
   variable con sentido económico conocido. Convierte la revisión de sentido económico de un control *ex post*
   en una propiedad garantizada del modelo.
2. **Benchmark interpretable obligatorio** para Tier I–II con ML: un modelo *glass-box* (logística WOE o
   *Explainable Boosting Machine* / GAM). Si el ML no supera al benchmark en ≥ 3 pts de Gini OOT, se prefiere el interpretable.
3. **SHAP con cuidado:** reportar SHAP global (importancia y *dependence plots*) y local para casos frontera;
   usar `TreeExplainer` con datos de fondo representativos; documentar que SHAP **no es causal** y que
   variables correlacionadas reparten atribución.
4. **Razones de rechazo** (*reason codes*): para decisiones sobre personas, derivar las 3–4 variables con mayor
   contribución negativa por cliente y verificar su estabilidad.
5. **Contrafactuales accionables** (opcional): "¿qué cambio mínimo cambiaría la decisión?", útil para
   comunicación con clientes y para detectar variables no accionables o sensibles.

**Requisito candidato:** `DES-D4-07.01.02 — Para ML en Tier I–II, documentar restricciones de monotonicidad,
benchmark interpretable y reason codes.`
