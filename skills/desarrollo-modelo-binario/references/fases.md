# Fases del desarrollo binario: qué hacer, con qué ID y qué entregar

Esta guía recorre el camino crítico de un modelo binario. **No es la lista completa de requisitos**: la lista
exacta para tu Tier, tipo y enfoque sale de `python tools/verificar.py --plan <REPO> --fase <FASE>`. Si un requisito
del plan no aparece aquí, igual se cumple. Las marcas *crítico* vienen del catálogo: su incumplimiento invalida el entregable.

Convención: **L** = `lineal`, **M** = `ml`, **A** = `arbol`. Si no se indica, aplica a los tres tipos y a los Tiers I–III.

---

## D1 · Definición, alcance, diseño y extracción (`docs/desarrollo/d1-definicion.md`)

**Objetivo:** fijar qué se modela, sobre quién y con qué datos. Lo que cambie después obliga a rehacer el modelo.

1. **Caso de uso y factibilidad** (DES-D1-01.01.01 a .07): necesidad, materialidad del universo y del target, políticas actuales y anteriores, modelos previos, supuestos económicos de las variables. Reunión 1 (DES-D1-01.01.08, *crítico*) → acta **R1**.
2. **Universo y filtros básicos** (DES-D1-01.02.01 a .05): base universo, evolutivos por montos y cuentas por driver (Excel 1), script de filtros con conteos antes y después.
3. **Tabla única** (DES-D1-01.03.01 a .05): Reunión 2 de fuentes y variables (*crítico*, acta **R2**), Script 2 de tabla única, Tabla 1 (master table inicial), Script 3 de nuevas variables.
   - **No anticipación (U-39, DES-D1-01.03.04, *crítico*):** toda variable usa solo información anterior a la fecha de observación (originación en admisión; foto en comportamiento o buró).
   - **Diccionario con fecha de referencia y desfase de la fuente** + prueba automática de no anticipación (DES-D1-01.03.05, *crítico*). Esta prueba vive en `src/` y su salida en `reports/D1/`.
4. **Project Charter (PPT 1)** (DES-D1-01.04.01 a .08): población objetivo, cosechas vs. aprobadas, OKRs, **Tier y uso**, alcance y limitaciones, alineamiento corporativo, ficha técnica (`MODEL_CARD.md`). Reunión 3 → acta **R3**.
5. **Kick off** (DES-D1-02.01.01, DES-D1-02.02.01 *crítico*): PPT 2 con el plazo (U-40) → acta **KO**.
6. **Ventana de modelamiento** (DES-D1-03.01.01 a .06):
   - **U-01:** al menos 12 meses de Train/Test; el OOT es **solo el último mes con desempeño completo** (la cosecha más reciente con 12 meses de maduración), posterior a Train/Test. No se acumulan meses en el OOT.
   - **U-41 (DES-D1-03.01.06, *crítico*):** audita la serie mensual de la tasa del target. Si cambia más de 25 % relativo entre meses consecutivos por un quiebre operativo, de política o de proceso, los meses previos al quiebre no entran a Train. Si así quedan menos de 12 meses, es una excepción a U-01 con acta.
   - **U-02:** estabilidad de la ventana con PSI (Excel 2).
7. **Exclusiones** (DES-D1-04.01.01 a .08), cada una con materialidad (Excel 3, Documento 3, Tabla 2 filtrada): pautas duras, default en foto, desempeño incompleto (< 12 meses), indeterminados, cambios de gestión. En admisión entrenada solo con aprobados: **sesgo de selección e inferencia de rechazados** (DES-D1-04.01.08; L/M/A, Tier I–II).
8. **Definición de default (U-17)** (DES-D1-05.01.01 a 05.04.01): atraso **mayor a 60 días** al menos una vez en los **12 meses siguientes** a la fecha de observación. Documenta unidad (cliente u operación) y materialidad (Documento 4). Tier I–II: roll rates (DES-D1-05.02.02), incidencia operación–cliente, análisis de materialidad. Otra altura u otra ventana es una **desviación** con roll rates, curva acumulada y acta.
   - Para targets binarios que no son default (propensión, fraude, contactabilidad), el estándar no fija la definición en U-17: documenta altura, temporalidad y materialidad en el Documento 4 (DES-D1-06.03.01) y llévalo a acta.
9. **Metodología propuesta** (DES-D1-07.01.01).

**G0 · Caso y Tier** — conformidad de Negocio + jefatura de modelos. Actas: R3 y KO.
**Detente si:** default ambiguo o distinto de U-17; variables posteriores a la observación; quiebre del target que deje la ventana corta sin acta.

---

## D2 · Calidad de datos (`docs/desarrollo/d2-calidad-datos.md`)

**Objetivo:** certificar validez, completitud, unicidad, precisión y consistencia. Sin Documento 6 no se pasa a D3/D4.

| Dimensión | IDs | Entregable |
|---|---|---|
| Documental | DES-D2-01.01.01, .02.01 | Excel 4 (diccionario), Documento 5 |
| Validez | DES-D2-01.03.01 | Comparación con la petición formal |
| Completitud | DES-D2-01.04.01 a .07 | Script 5, Excel 5 (fill rate total y mensual; Mann–Kendall del % de missing, Tier I–II) |
| Unicidad | DES-D2-01.05.01 | Script 6 |
| Descriptiva y estabilidad | DES-D2-01.06.01 a .03 | Excel 6; PSI ≤ 10 % (≤ 20 % solo si 10 % reduce mucho el set) — **U-02** |
| Precisión | DES-D2-02.01.01 | Excel 7 (cuadre con cifras de negocio) |
| Consistencia | DES-D2-02.02.01 (Tier I–II) | Script 7 |
| Certificación | DES-D2-02.03.01, .02 | **Documento 6** firmado por el líder |

Toda incidencia queda con su decisión: usar, corregir o excluir.

**G1 · Datos certificados** — conformidad de la jefatura de modelos.

---

## D3 · Segmentación (`docs/desarrollo/d3-segmentacion.md`)

1. Reunión 4 de ejes (DES-D3-01.01.01) → acta **R4**. Si los drivers no son claros, árbol de decisión para candidatos.
2. Tasa de default y materialidad por segmento, estabilidad (DES-D3-01.01.02; Excel 8).
3. Supervisada: modelos *naive* por segmento vs. unisegmento (DES-D3-01.01.03; **L** Tier I–II). No supervisada opcional (DES-D3-01.01.05).
4. Comparación final con el unisegmento (DES-D3-01.02.01, PPT 3), contraste estadístico y de negocio (DES-D3-01.02.02), Documento 7 (DES-D3-01.02.04).

Un segmento se justifica solo si **supera al unisegmento**, es material y estable. Supuesto de estimación: máximo 4–5 segmentos.

**G2 · Segmentación** — conformidad de Negocio.

---

## D4 · Modelamiento (`docs/desarrollo/d4-modelamiento.md`)

### D4.1 Muestra y particiones

- Outliers del target por percentiles (DES-D4-01.01.01, U-04); materialidad de exclusiones (DES-D4-02.01.01).
- **Representatividad (U-03, DES-D4-02.02.01):** 0.95 ≤ TM/TG ≤ 1.05. Si no cumple, pondera la muestra y usa los pesos en **todo** lo posterior.
- Train / Test / OOT (DES-D4-02.03.01): Train y Test del mismo periodo (secuencial o estratificado por target y mes); OOT según U-01. **Guarda las tres bases** (DES-D4-05.03.01) con hash en `data/`.

### D4.2 Embudo de variables — el orden es obligatorio

```text
1 No anticipación  U-39           4 Bivariado WOE/IV, tendencia, monotonicidad  DES-D4-03.03.02 (crítico)
2 Univariado       DES-D4-03.02.02 (crítico)   5 Fuga: IV > 0.50 se excluye      U-38 · DES-D4-03.03.03 (crítico)
3 Fill rate y PSI  DES-D4-03.02.01 · U-02     6 Filtro de confiables → correlación  DES-D4-03.03.04 (crítico) · U-06 · U-07
```

- Reporta el **embudo**: cuántas variables entran y salen en cada filtro y por qué (DES-D4-03.03.04).
- IV < 0.02 **no excluye** por sí solo; los bloques sociodemográfico y financiero se preservan como control (DES-D4-05.02.09). Si el modelo final los descarta, documenta la evidencia multivariada.
- La variable excluida por fuga se investiga y su origen se documenta como aprendizaje (DES-D4-03.03.03).
- Correlación entre continuas < 60 % (hasta < 95 % evaluando el tradeoff; U-06). Categóricas: p-valor χ² ≥ 0.0001 o V de Cramér < 0.4 (U-07). El estándar no exige un tamaño mínimo de celda para χ²; si lo usas, dilo como criterio propio.

### D4.3 Feature engineering (según tipo)

| Tema | Lineal | ML | Árbol |
|---|---|---|---|
| Outliers de variables | Percentiles por Tier (DES-D4-04.01.01 a .03; U-04) | — | Igual que lineal |
| Categóricas | Árboles/experto (T1), dummies acumulativas (T2), media del target/one-hot/WOE (T3) (DES-D4-04.02.01 a .03) | — | Igual que lineal |
| Transformaciones | Funcionales (T1–2, DES-D4-04.03.01); WOE (T3, DES-D4-04.03.03) | — | — |
| Imputación | Target equivalente (DES-D4-04.04.01); media/mediana solo con missing < 1 % o < 30 casos (U-05) | No exigida por el catálogo; documenta el tratamiento de faltantes que use el algoritmo | Igual que lineal |
| Convoluciones e interacciones | DES-D4-04.06.01 a .03; XGBFir y H de Friedman opcionales | Igual | Opcionales |

En todos: **sin banderas de corte duro** («sin historia», «saturado») que inviertan la monotonicidad en la validación temporal; prefiere ratios continuos acumulados y aplica la prueba de U-44 antes de aceptar la variable (DES-D4-04.03.04). Cierra con matriz final de correlaciones y base final documentada (DES-D4-04.07.01 a .03).

### D4.4 Selección de variables

- Modelo inicial de insights (DES-D4-05.01.01); revisión de **sentido económico** con el usuario (DES-D4-05.02.01, .02).
- **Dos fases** (DES-D4-05.02.08): (1) ranking automatizado de todas las variables que pasaron el filtro, hasta el tope de U-08 (top 100 sin fuga u 80 % del gain); (2) paso a paso adelante y atrás con función objetivo compuesta (discriminación, error absoluto por decil y violaciones de monotonicidad) evaluada en la **validación temporal**. El OOT no interviene.
- ML/Árbol: Boruta opcional (T1), curva de poder por gain (T2), top 100 / 80 % del gain (DES-D4-05.02.03 a .05).
- **Concentración (U-09, DES-D4-05.02.06):** ninguna variable > 40 % de la importancia (deseable ≤ 25 %). Si se excede en árboles: colsample_bytree ≤ 0.60 y L2.
- Reporte de estabilidad de la discriminación por variable (DES-D4-05.02.07).

### D4.5 Torneo de modelos (U-43, DES-D4-05.03.04, *crítico*)

Al menos **cinco familias** con los mismos datos, la misma validación temporal y la misma semilla:

| # | Familia | Ejemplo |
|---|---|---|
| 1 | Logística regularizada — **línea base obligatoria** | L2 o ElasticNet |
| 2 | Árbol podado | CART profundidad 4–6 |
| 3 | Bagging | Random forest |
| 4 | Boosting por histogramas **con restricciones de monotonicidad** | HistGradientBoosting / LightGBM |
| 5 | Boosting extremo regularizado | XGBoost con γ, α, λ |

- ML: **benchmark interpretable** (logística con WOE, GAM/EBM o árbol óptimo); si el ML elegido no lo supera en al menos **3 pts de Gini OOT**, justifícalo (DES-D4-05.03.02, *crítico*).
- ML: validación cruzada **temporal** cuando hay dependencia en el tiempo, con la brecha esperada entrenamiento–validación (DES-D4-05.03.03, *crítico*).
- Hiperparámetros: búsqueda aleatoria de **≥ 50 combinaciones** con semilla fija (U-10, DES-D4-05.04.01). Si no se completan, sustenta. Registra cuántas combinaciones probaste.
- Lineal: bootstrap (DES-D4-05.05.02). Todos: scripts de tratamiento de variables en OOT (DES-D4-05.05.01).

### D4.6 Evaluación y elección del campeón

- Métricas **global, por mes y por segmento**, en meses de construcción y en los más recientes con desempeño; alerta |Gini construcción − Gini último mes| (DES-D4-06.01.01).
- Tier I–II: métrica basada en rentabilidad (p. ej. EMP) junto al Gini (DES-D4-06.01.03).
- **Desempeño por deciles** con cero inversiones en el OOT (U-44, DES-D4-06.01.04). No es calibración.
- Comparación con el **modelo vigente** por mes en cosechas o aprobados (DES-D4-06.02.01).
- **Tabla oficial** (DES-D4-06.03.05, *crítico*): por candidato, Gini Train, Gini/KS/AUC en validación y en OOT, brecha absoluta y relativa, Brier y concentración máxima. Reglas en orden: (1) descalifica U-11; (2) nadie supera U-09; (3) parsimonia U-42 (más simple a < 1.5 pts gana); (4) Brier reportado y comparado. Ver `scripts/pruebas_umbrales.py` → `tabla_torneo`, `elegir_campeon`.
- **U-11 (DES-D4-06.03.02):** cumple si brecha Train–OOT ≤ 5 pts **o** caída relativa ≤ 10 %. Si no cumple ninguna, descalificado y sin excepción.
- Si se modeló sobre muestra: Gini muestra vs. población por bootstrap (DES-D4-06.03.03).
- Reunión 5 de selección (DES-D4-06.03.01) → acta **R5**.

**G3 · Modelo final** — conformidad de Negocio + jefatura.

### D4.7 Interpretación, calibración y transición

- ML: SHAP (DES-D4-07.01.01, Tier I) y estabilidad de las explicaciones ante remuestreo y desbalance (DES-D4-07.01.02).
- L/M: base de calibración, drivers micro, variables macro (T1–2), calibración y puntuación calibrada (DES-D4-08.01.01 a .06); presentación → acta **R6**.
- Todos: **calibración probabilística formal** — Hosmer-Lemeshow, o binomial o Jeffreys por tramo — y Brier (DES-D4-08.01.07).
- Matriz y regla de transición applicant/behavior; Gini por mes de maduración (DES-D4-08.02.01 a .03). Documento de calibración (DES-D4-08.03.01).

**G4 · Calibración** — conformidad de Negocio.

### D4.8 Limitaciones, documentación y cierre

- Debilidades de discriminación, calibración, estabilidad (matriz de migración) y desempeño en subpoblaciones (DES-D4-10.01.01 a .05) → capítulo obligatorio.
- **Sensibilidad** del score a sus variables principales y supuestos (DES-D4-10.01.06, *crítico*).
- Personas naturales Tier I–II: **equidad** (variables sensibles, proxies, métricas por grupo; DES-D4-10.01.07). El marco detallado de FR-06 es *Propuesta*: úsalo como recomendación.
- Documentación funcional y técnica, control de cambios, usos, versiones y rutas de herramientas (DES-D4-11.01.01 a .06).
- Documento metodológico con `tools/documento.py` (DES-D4-11.01.07); consolidada (DES-D4-11.02.01, U-40).
- Reunión de resultados (DES-D4-12.01.01 → **R7**); enfoque cualitativo con la banca si aplica (DES-D4-13.x → **R8**); presentación de aprobación (DES-D4-14.01.01).

---

## D5 · Integración a la gestión (`docs/desarrollo/d5-integracion-gestion.md`)

- **Punto de corte** por función de utilidad con costo asimétrico y estratos de gestión (DES-D5-01.01.01, .03).
- **Política de forzajes** (DES-D5-01.01.02, *crítico*): quién fuerza, motivos válidos, registro obligatorio y límite (U-36 para el seguimiento).
- Impactos: cobertura y riesgo (Tier I; DES-D5-01.02.01, .02), provisiones (Tier I–II), capital, IFRS 9, coordinación con PD/LGD/EAD (DES-D5-01.02.04 a .07).
- Muestra mínima para el seguimiento, coordinada con el equipo de Seguimiento (DES-D5-01.03.01).

---

## D7 · Gobierno (`docs/desarrollo/d7-gobierno.md`)

- Revisión de aplicación del estándar por el líder (DES-D7-01.01.01, *crítico*) y evidencias de correos, actas y conformidades (DES-D7-01.01.02, *crítico*): todo en `evidencias.yaml`.
- Participación en la asignación de Tier e inventario (DES-D7-01.01.03, .04); variables críticas (DES-D7-01.01.06).
- **Aprobación previa del comité** antes de cualquier uso (DES-D7-01.01.07, *crítico*; GOB-G3-01.01.01).

**G5 · Aprobación** — Comité de Modelos, acta **CM**. El agente prepara el borrador; nunca la aprueba.
