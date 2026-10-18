---
id: DES-D4
titulo: "D4 · Modelamiento"
estandar: Desarrollo
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 13
---

# D4 · Modelamiento

## Objetivo

Construir, seleccionar, calibrar y documentar el modelo final, y llevarlo a aprobación del Comité de Modelos.
Es la fase con más requisitos del estándar (<!--DUR:fase:DES-D4-->≈ 2.8–5.7 semanas con 2 personas<!--/DUR-->).

## Flujo

```text
Exclusiones del target ─▶ Muestreo (representatividad) ─▶ Train/Test/OOT
      ─▶ Depuración (PSI, fill rate, Gini univariado) ─▶ Feature engineering
      ─▶ Entrenamiento ─▶ Optimización HP ─▶ Bootstrap ─▶ Selección del modelo final
      ─▶ Interpretación (SHAP) ─▶ Calibración y regla de transición
      ─▶ Performance por drivers ─▶ Limitaciones ─▶ Documentación ─▶ Cierre cuanti/cuali ─▶ Comité
```

## Antes de entrenar: el orden es obligatorio

Ningún modelo se entrena sobre variables que no hayan pasado, en este orden, por:

```text
 1 No anticipación        cada variable usa solo información anterior a la observación      U-39 · DES-D1-01.03.04
 2 Univariado             distribución, faltantes, especiales, categorías raras, extremos   DES-D4-03.02.02
 3 Fill rate y PSI        poblamiento global y mensual; estabilidad temporal                DES-D4-03.02.01 · U-02
 4 Bivariado              WOE e IV por tramo, tendencia y monotonicidad del riesgo          DES-D4-03.03.02
 5 Sospecha de fuga       IV > 0.50 se excluye (cuasi-determinismo)                         U-38 · DES-D4-03.03.03
 6 Filtro de confiables   IV ≤ 0.50, fill rate del plan, PSI; luego correlación             DES-D4-03.03.04 · U-06 · U-07
 ──────────────────────────────────────────────────────────────────────────────────────────────────────────
 Embudo de variables documentado ─▶ Feature engineering ─▶ Entrenamiento
```

**Por qué la no anticipación es la regla número uno.** En producción el modelo decide con lo que se sabe *antes*
de la fecha de observación. Una variable contemporánea o del futuro (un saldo de fin de mes posterior a la
originación, una marca de cobranza o un campo que se actualiza tras el default) no existe en el momento de decidir.
Infla el Gini en construcción y hace que el modelo falle al implementarse. Cada variable documenta su fecha de
referencia y el desfase de su fuente (DES-D1-01.03.05).

**Por qué un IV demasiado alto es una alarma.** En crédito, un IV mayor a 0.50 casi siempre indica que la variable
contiene información del target (fuga) y no poder predictivo genuino. Es la regla clásica de la práctica de scoring
(LIT-001), y la experiencia lo confirma: una sola variable de este tipo puede concentrar casi toda la importancia del
modelo y abrir una brecha Train–OOT de más de 10 pts, que se cierra al excluirla. Por eso se excluye sin excepción.

**Por qué el filtro de IV es asimétrico.** El límite superior (0.50) protege contra la fuga; el inferior (0.02) no se
aplica a ciegas. Un filtro univariado que descarta todo lo que tiene IV bajo puede eliminar los bloques
sociodemográficos y financieros y dejar un modelo apoyado en dos o tres variables operativas. Esos bloques se
preservan como línea base de control (DES-D4-05.02.09) y es el análisis multivariado el que decide si aportan.

## Reglas clave (resumen de umbrales)

| Tema | Regla | Umbral |
|---|---|---|
| No anticipación | Cero variables contemporáneas o futuras | U-39 |
| Fuga por IV | IV > 0.50 se excluye; IV < 0.02 no excluye por sí solo | U-38 |
| Representatividad | $0.95 \le TM/TG \le 1.05$; si no, ponderar | U-03 |
| Estabilidad de variables | PSI ≤ 10 % (≤ 20 % excepción) | U-02 |
| Outliers | Percentiles 1-5-95-99 | U-04 |
| Correlación continuas | < 60 % (hasta < 95 % por tradeoff) | U-06 |
| Asociación categóricas | p-valor χ² ≥ 0.0001 o V de Cramér < 0.4 | U-07 |
| Selección de variables | Top 100 sin fuga / 80 % del gain, luego paso a paso | U-08 |
| Concentración de importancia | Máximo 40 % por variable (deseable ≤ 25 %) | U-09 |
| Hiperparámetros | ≥ 50 combinaciones, semilla fija | U-10 |
| Sobreajuste | \|Gini Train − Gini OOT\| ≤ 10 pts y caída relativa ≤ 10 %; si no, descalifica | U-11 |
| Torneo | Al menos 5 familias de algoritmos en clasificación binaria | U-43 |
| Parsimonia | Si el más simple está a < 1.5 pts de Gini, gana el más simple | U-42 |
| Desempeño por deciles | Cero inversiones de la tasa observada en el OOT | U-44 |

## Torneo de modelos (champion–challenger)

En clasificación binaria (admisión, comportamiento, propensión, contactabilidad, fraude) **no se elige un algoritmo
a criterio**. Compiten al menos cinco familias con los mismos datos, la misma validación temporal y la misma semilla
(DES-D4-05.03.04, U-43):

| Familia | Ejemplo | Para qué está en el torneo |
|---|---|---|
| Lineal regularizada (**línea base obligatoria**) | Regresión logística L2 o ElasticNet | Piso de defensibilidad e interpretabilidad |
| Árbol simple podado | CART con profundidad 4 a 6 | Ganancia no lineal básica, explicable |
| Ensamble por bagging | Random forest | Estabilidad ante la varianza de la muestra |
| Boosting por histogramas | HistGradientBoosting / LightGBM con **restricciones de monotonicidad** | Discriminación con sentido económico |
| Boosting extremo regularizado | XGBoost con γ, α y λ | Referencia de frontera en discriminación |

**Selección de variables en dos fases** (DES-D4-05.02.08): un ranking automatizado de todas las variables que pasaron
el filtro previo (hasta el tope de U-08) y luego una selección paso a paso con una función objetivo compuesta
(discriminación, error por decil y violaciones de monotonicidad). Partir de un puñado de variables elegidas a criterio
pone un techo artificial al modelo.

**Tabla oficial y reglas de coronación** (DES-D4-06.03.05). Cada candidato reporta Gini de entrenamiento, Gini, KS y
AUC en validación y en OOT, brecha absoluta y relativa, Brier score y concentración máxima de importancia. Gana quien
cumple las reglas, en este orden:

1. **Descalificación por sobreajuste:** brecha Train–OOT mayor a 10 pts o caída relativa mayor a 10 % (U-11).
2. **Concentración:** ninguna variable con más del 40 % de la importancia (U-09).
3. **Parsimonia:** si un modelo más simple queda a menos de 1.5 pts de Gini del más complejo, se elige el simple (U-42).
4. **Calibración:** el Brier score se reporta y se compara; la calibración formal se prueba aparte (DES-D4-08.01.07).

> **El OOT no se usa para elegir.** Variables, hiperparámetros y función objetivo se optimizan en Train/Test con
> validación temporal. El OOT se evalúa **una sola vez**, sobre los candidatos finales, para confirmar. Si se itera
> mirando el OOT, deja de ser una prueba independiente y el Gini reportado sobrestima el que se verá en producción.

**Desempeño por deciles no es calibración.** La curva de tasa observada por decil mide el **ordenamiento** y se exige
monótona en el OOT (U-44, DES-D4-06.01.04). La **calibración probabilística** compara la probabilidad estimada con la
observada mediante una prueba formal, como Hosmer-Lemeshow o binomial por tramo (DES-D4-08.01.07). Son dos reportes
distintos y se nombran así.

## Selección del modelo final

Las métricas se evalúan **global, por mes y por segmento**, tanto en los meses de construcción como en los
**meses más recientes con desempeño**:

- Target binario: AUC / Gini, y la alerta $\left|\mathrm{Gini}_{\text{construcción}}-\mathrm{Gini}_{\text{último mes}}\right|$.
- Target continuo: $R^2$, % de real dentro de ±25 % y ±50 % del proyectado, ECM (U-12).
- Comparación contra el **modelo vigente** en cosechas / solicitudes aprobadas.
- Si se modeló sobre muestra: consistencia Gini muestra vs. población por bootstrap (DES-D4-06.03.03).

## Reproducibilidad (obligatorio)

Guardar las bases **Train, Test y OOT** (DES-D4-05.03.01), fijar semillas (DES-D4-05.04.01) y documentar
versiones y rutas de las herramientas (DES-D4-11.01.06).

## Limitaciones

Todo modelo cierra con un reporte de debilidades de **discriminación, calibración y estabilidad**, incluyendo
el desempeño en subpoblaciones distintas a la de modelamiento (PPT 14). Este reporte es un capítulo obligatorio
del documento metodológico.

<!-- CATALOGO:INICIO DES-D4 -->
## Catálogo de requisitos · Modelamiento

> Bloque generado desde `catalogo/des-d4.yaml` (104 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Desarrollo v1.0.

### 1 · Exclusiones del target (contínuo)

#### 1.1 Exclusión de outliers del target

- **`DES-D4-01.01.01`** Excluir outliers del target por percentiles

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0.25 d ágil / 0.5 d completo · Automatización: 1 · Entregable: Script 8: Exclusión de outliers del target. · Hito: Sprint 8 · Umbrales: U-04

### 2 · Muestreo y estratificación

#### 2.1 Muestreo aleatorio para la reducción de registros

- **`DES-D4-02.01.01`** Examinar la materialidad para definir el porcentaje de exclusión.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1 · Entregable: Script 9: Muestreo y Estratificación

#### 2.2 Análisis de representatividad de la muestra

- **`DES-D4-02.02.01`** Examinar la representatividad a través de la exactitud target a nivel global en la población (TG) y en la muestra (TM).  
  95%<=TM/TG<=105%  
  En caso la muestra no sea representativa ponderar la muestra. La ponderación de la muestra será utilizada para el modelamiento y todos los análisis posteriores incluyendo el cálculo de pesos.

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Gráficos: resultado de representatividad · Umbrales: U-03

#### 2.3 Selección de muestras

- **`DES-D4-02.03.01`** Selección train, test y OOT (secuencial / estrat por target y mes)

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1 · Entregable: Tabla 4: Master table por muestra.

### 3 · Depuración de variables

#### 3.1 Análisis de estabilidad

- **`DES-D4-03.01.01`** Análisis de tendencia de las variables independientes calculando el indicador PSI (estabilidad temporal) incluyendo meses recientes, justificación de la permanencia o depuración de variables inestables.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 2 · Entregable: Excel 9: Resultados del test de estabilidad · Umbrales: U-02

#### 3.2 Fill rate

- **`DES-D4-03.02.01`** Análisis de porcentaje de casos poblados (global/por mes)

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 3 · Entregable: Excel 10: Univariate analysis I

- **`DES-D4-03.02.02`** Análisis univariado de cada variable sobre la muestra de entrenamiento: distribución, valores especiales y faltantes, categorías raras y valores extremos. Es requisito previo del análisis bivariado.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 3 · Crítico · Entregable: Excel 10: Univariate analysis I · Nota: Línea base 2.1 (2026-10-17): criterio del custodio.

#### 3.3 Gini por variables

- **`DES-D4-03.03.01`** Análisis de discriminación por variables (global/por mes)

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 3 · Hito: SME 4

- **`DES-D4-03.03.02`** Análisis bivariado de cada variable frente al target: WOE e IV por tramo, tendencia y monotonicidad del riesgo, y estabilidad del IV entre períodos.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1.5 d ágil / 1.5 d completo · Automatización: 3 · Crítico · Entregable: Excel 10: Univariate analysis I · Nota: Línea base 2.1 (2026-10-17): criterio del custodio.

- **`DES-D4-03.03.03`** Excluir por sospecha de fuga de información (cuasi-determinismo) toda variable con IV mayor a 0.50: no entra al modelamiento (U-38). Se documenta la investigación de su origen como aprendizaje del proyecto.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 2 · Crítico · Entregable: Excel 9: Resultados del test de estabilidad · Umbrales: U-38 · Nota: Línea base 2.1 (2026-10-17): criterio del custodio.

- **`DES-D4-03.03.04`** Filtro de variables confiables antes del entrenamiento: solo pasan las variables que cumplen no anticipación (U-39), fill rate mínimo del plan del modelo, estabilidad (U-02) e IV no mayor a 0.50 (U-38; un IV menor a 0.02 no excluye por sí solo); después se aplican las reglas de correlación (U-06, U-07). Se reporta el embudo de variables (cuántas entran y salen en cada filtro y por qué).

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 3 · Crítico · Entregable: Tabla 1: Base de variables finalistas. · Umbrales: U-38, U-39 · Nota: Línea base 2.1 (2026-10-17): criterio del custodio.

### 4 · Feature engineering

#### 4.1 Detección y tratamiento de outliers

- **`DES-D4-04.01.01`** Análisis de percentiles automático (revisión variables críticas & revisión por criterio de tipo de variable)

  Aplica: Lineal/Árbol/ACP I · Esfuerzo: 2 d ágil / 2 d completo · Automatización: 3 · Entregable: Excel 10: Univariate analysis I · Hito: Sprint 9

- **`DES-D4-04.01.02`** Análisis de percentiles automático (revisión variables críticas)

  Aplica: Lineal/Árbol/ACP II · Esfuerzo: 1.5 d ágil / 1.5 d completo · Automatización: 3

- **`DES-D4-04.01.03`** Análisis de percentiles automático / experto (1%-5%-95%-99%)

  Aplica: Lineal/Árbol/ACP III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 4 · Umbrales: U-04

#### 4.2 Transformación de variables categóricas

- **`DES-D4-04.02.01`** Árboles de decisión/ corrección experta (reducir categorías)

  Aplica: Lineal/Árbol/ACP I · Esfuerzo: 2 d ágil / 2 d completo · Automatización: 1 · Entregable: Script 10: Tratamiento de variables categóricas

- **`DES-D4-04.02.02`** Agrupación por dummies acumulativas

  Aplica: Lineal/Árbol/ACP II · Esfuerzo: 1.5 d ágil / 1.5 d completo · Automatización: 4

- **`DES-D4-04.02.03`** Transformación a media / mediana del target / One hot encoder / class / WOE

  Aplica: Lineal/Árbol/ACP III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 4

#### 4.3 Transformación de variables continuas

- **`DES-D4-04.03.01`** Transformaciones funcionales vs el target (ej. Lineal, polinomica, exponencial, etc).

  Aplica: Lineal I–II · Esfuerzo: 2 d ágil / 2 d completo · Automatización: 4 · Entregable: Ppt 4: Resumen de transformaciones realizadas.

- **`DES-D4-04.03.02`** Estandarizacion de variables/normalizacion

  Aplica: ACP I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1

- **`DES-D4-04.03.03`** Tranformación WOE

  Aplica: Lineal/ACP III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1

- **`DES-D4-04.03.04`** No usar banderas binarias de corte duro (por ejemplo, «sin historia» o «saturado») cuando invierten la monotonicidad del riesgo en la validación temporal; priorizar ratios continuos acumulados, que degradan con suavidad. La prueba de monotonicidad por deciles (U-44) se aplica antes de aceptar la variable.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 2 · Umbrales: U-44 · Nota: Versión 4.0.0 (2026-10-17). Lecciones de proyectos de desarrollo; ver CHANGELOG.

#### 4.4 Imputación de missings

- **`DES-D4-04.04.01`** Imputación por target equivalente

  Aplica: Lineal/Árbol I–III · Esfuerzo: 1.5 d ágil / 1.5 d completo · Automatización: 4 · Entregable: Excel 11: Univariate analysis III

- **`DES-D4-04.04.02`** Imputación por mediana/media poblacional (para variables con materialidad de missing <1%/ 30 casos / defaults) (opcional)

  Aplica: Lineal/Árbol/ACP I–III · Esfuerzo: 0–1 d ágil / 0–1.5 d completo · Automatización: 4 · Umbrales: U-05

- **`DES-D4-04.04.03`** Probar técnica de imputación multivariada en variables core (opcional)

  Aplica: Lineal/Árbol/ACP I · Esfuerzo: 1 d ágil / 1–1.5 d completo · Automatización: 1 · Entregable: Ppt 5: Imputación multivariada de variables

#### 4.5 Preselección de variables

- **`DES-D4-04.05.01`** Preselección por correlaciones (<60% | <95%) Tradeoff poder predictivo

  Aplica: Lineal/ML/Árbol I · Esfuerzo: 2 d ágil / 2 d completo · Automatización: 1 · Entregable: Ppt 6: Análisis de correlaciones y poder predictivo. · Umbrales: U-06

- **`DES-D4-04.05.02`** Preselección por correlaciones (<60%) para variables continuas

  Aplica: Lineal/ML/Árbol II–III · Esfuerzo: 1.5 d ágil / 1.5 d completo · Automatización: 4 · Umbrales: U-06

- **`DES-D4-04.05.03`** Preselección por asociaciones para variables categóricas (se acepta variables categóricas según prueba chi cuadrado >=0.0001 o la V de cramer sea menor a 0.4).

  Aplica: Lineal/ML/Árbol II–III · Esfuerzo: 1.5 d ágil / 1.5 d completo · Automatización: 4 · Hito: SME 5 · Umbrales: U-07

#### 4.6 Convolución de variables

- **`DES-D4-04.06.01`** Árboles de decisión + criterio de negocio

  Aplica: Lineal/ML/ACP I · Esfuerzo: 3.4 d ágil / 4 d completo · Automatización: 1 · Entregable: Ppt 7: Convolución de variables. · Hito: Sprint 10

- **`DES-D4-04.06.02`** Convoluciones basado en bitácora de convolución de variables

  Aplica: Lineal/ML/ACP II · Esfuerzo: 2.55 d ágil / 3 d completo · Automatización: 1

- **`DES-D4-04.06.03`** Convoluciones basado en bitácora de convolución de variables (5 convoluciones por segmento).

  Aplica: Lineal/ML/ACP III · Esfuerzo: 1.7 d ágil / 2 d completo · Automatización: 1

- **`DES-D4-04.06.04`** Creación de interacciones XGBFir (opcional)

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1.7 d ágil / 2 d completo · Automatización: 1

- **`DES-D4-04.06.05`** Detección interacciones Friedman's H Statistic (opcional)

  Aplica: Todos los tipos, Tier I–III

#### 4.7 Construcción de la base final

- **`DES-D4-04.07.01`** Elaboración de matriz final de correlaciones

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 4 · Entregable: Excel 12: Model Parameters.

- **`DES-D4-04.07.02`** Entrega de la base final

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 1 · Entregable: Tabla 1: Base de variables finalistas.

- **`DES-D4-04.07.03`** Documentación de los procedimientos realizados y las decisiones finales

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Documento 8: Feature Engenieering.; Tabla 5: Master table final · Hito: SME 6

### 5 · Entrenamiento de modelos

#### 5.1 Ejecución del modelo inicial

- **`DES-D4-05.01.01`** Ejecución de un modelo incial para primeros insights

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 2 · Entregable: Excel 13: Importancia de variables modelo Inicial. · Hito: Sprint 11

#### 5.2 Selección de variables

- **`DES-D4-05.02.01`** Revisión por sentido económico

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1.275–2.55 d ágil / 1.5–3 d completo · Automatización: 1 · Entregable: Excel 14: Revisión de Sentido Económico.

- **`DES-D4-05.02.02`** Reunión con usuario para revisión de sentido económico / depuración de variables

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 1 · Entregable: Excel 15: Selección de variables.

- **`DES-D4-05.02.03`** Selección de variables: Boruta (opcional)

  Aplica: ML/Árbol I · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 2

- **`DES-D4-05.02.04`** Selección de variables: Curva de Poder predictivo por Gain.

  Aplica: ML/Árbol II · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 3

- **`DES-D4-05.02.05`** Selección de variables: Top 100 variables sin fuga / 80% del gain (U-08).

  Aplica: ML III · Árbol I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 3 · Umbrales: U-08

- **`DES-D4-05.02.06`** Los pesos de las variables en la construcción de modelos tradicionales se calcularán según la lógica de la herramienta estandarizada: toolkit de modelamiento, con un peso maximo recomendado del 25%. En la construcción de modelos machine learning utilizarán para el cálculo de pesos el gain, con un peso recomendado del 10%. Para calibraciones se utiliza la métrica de Chi-Wald

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 2 · Umbrales: U-09

- **`DES-D4-05.02.07`** Elaboración del reporte de estabilidad de los indicadores de discriminación por variable.  
  Sin embargo en el caso de que las variables cuyos indicadores no sean estables , no será determinante para su exclusión. Llevar discusion a gerencia.

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 1 d ágil / 1–2 d completo · Automatización: 3

- **`DES-D4-05.02.08`** Seleccionar variables en dos fases: (1) ranking automatizado de todas las variables que pasaron el filtro previo, hasta el tope de U-08; (2) selección paso a paso hacia adelante y hacia atrás con una función objetivo compuesta (discriminación, error absoluto por decil y violaciones de monotonicidad), evaluada en la validación temporal. El OOT no interviene en la selección: se reserva para la confirmación final (DES-D4-06.03.05).

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 1 d ágil / 1.25 d completo · Automatización: 3 · Umbrales: U-08 · Nota: Versión 4.0.0 (2026-10-17). Lecciones de proyectos de desarrollo; ver CHANGELOG.

- **`DES-D4-05.02.09`** Preservar como línea base de control los bloques estructurales de negocio (sociodemográfico y financiero, incluido el endeudamiento en el sistema): un IV bajo no los excluye por sí solo (U-38). Si el modelo final los descarta, se documenta la evidencia multivariada que lo justifica.

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 2 · Umbrales: U-38 · Nota: Versión 4.0.0 (2026-10-17). Lecciones de proyectos de desarrollo; ver CHANGELOG.

#### 5.3 Entrenamiento

- **`DES-D4-05.03.01`** Entrenamiento de posibles modelos con las variables preseleccionadas

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 3 d ágil / 3 d completo · Automatización: 4 · Entregable: Excel 12: Model Parameters. · Hito: SME 7

- **`DES-D4-05.03.02`** Para modelos de ML, construir un benchmark interpretable (logística con WOE, GAM/EBM o árbol óptimo) y justificar el modelo elegido si no lo supera en al menos 3 pts de Gini OOT.

  Aplica: ML/Árbol I–III · Esfuerzo: 1.5 d ágil / 2 d completo · Automatización: 2 · Crítico · Entregable: Excel 12: Model Parameters. · Nota: Línea base 2.0 (2026-10-17). Res. SBS 00053-2023 art. 16; Gunnarsson et al. (2021); Rudin (2019).

- **`DES-D4-05.03.03`** Ajustar los modelos de ML con validación cruzada (temporal cuando exista dependencia en el tiempo) y reportar la brecha esperada entre entrenamiento y validación.

  Aplica: ML/Árbol I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 3 · Crítico · Entregable: Excel 16: Optimización de Hiperparámetros. · Nota: Línea base 2.0 (2026-10-17). Res. SBS 00053-2023 art. 16; EBA/REP/2023/28.

- **`DES-D4-05.03.04`** En clasificación binaria, enfrentar al menos cinco familias de algoritmos con los mismos datos, la misma validación temporal y la misma semilla (U-43): (1) regresión logística regularizada (L2 o ElasticNet) como línea base obligatoria; (2) árbol de decisión podado; (3) ensamble por bagging (random forest); (4) boosting por histogramas con restricciones de monotonicidad; (5) boosting extremo regularizado. No se elige un algoritmo sin torneo.

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 1.5 d ágil / 2 d completo · Automatización: 3 · Crítico · Entregable: Excel: Tabla del torneo de modelos (leaderboard). · Umbrales: U-43 · Nota: Versión 4.0.0 (2026-10-17). Lecciones de proyectos de desarrollo; ver CHANGELOG.

#### 5.4 Optimización

- **`DES-D4-05.04.01`** Opt de HP por generación aleatoria (min 50 combinaciones), en caso de no completar el mínimo combinaciones se darán los sustentos necesarios.  
  Ejecución con HP óptimos (eta, max_depth, subsample, colsample, gamma, alpha, lambda, scale_pos_weight y otros parámetros), Además de agregar una semilla para su replica

  Aplica: ML/Árbol I–III · Esfuerzo: 3 d ágil / 3 d completo · Automatización: 2 · Entregable: Excel 16: Optimización de Hiperparámetros. · Umbrales: U-10

- **`DES-D4-05.04.02`** Opt de HP Grid search (opcional)

  Aplica: ML/Árbol I–III · Automatización: 2

- **`DES-D4-05.04.03`** Opt de HP Random Search (opcional)

  Aplica: ML/Árbol I–III · Automatización: 2

- **`DES-D4-05.04.04`** Opt de HP Bayesian Search (opcional)

  Aplica: Todos los tipos, Tier I–III · Automatización: 1

- **`DES-D4-05.04.05`** Ejecución con HP óptimos

  Aplica: ML/Árbol I–III · Esfuerzo: 1.5 d ágil / 1.5 d completo · Automatización: 1 · Entregable: Script 11: Ejecución del modelo final.

- **`DES-D4-05.04.06`** Analisis diferencias en gini train vs gini test/gini oot

  Aplica: ML/Árbol I–III · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 1

#### 5.5 Bootstrap

- **`DES-D4-05.05.01`** Tratamiento de variables en OOT, generación de scripts.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.5–2 d ágil / 0.5–2 d completo · Automatización: 3 · Entregable: Script 12: Script de Implementación.

- **`DES-D4-05.05.02`** Bootstrap.

  Aplica: Lineal/ACP I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 3 · Entregable: Excel 17: Analisis Bootstrap.

### 6 · Selección del modelo final

#### 6.1 Análisis de métricas y tendencia en las diferentes muestras (cosechas, solicitudes, etc).

- **`DES-D4-06.01.01`** AUC/Gini/R2 (Global/por mes/segmento) - Default (binario) / Dichas métricas deben ser evaluadas en meses de construcción del modelo y en meses recientes / Analizar posibles alertas de inestabilidad comparando variaciones de desempeño |Gini Construcción - Gini Último Mes Con Desempeño|

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 2 · Entregable: Ppt 9: Resumen de indicadores del modelo final.

- **`DES-D4-06.01.02`** R2, % de real entre proyectado +/-25%, +/- 50%, Error cuadrático medio - Target (continuo) / Dichas métricas deben ser evaluadas en meses de construcción del modelo y en meses recientes / Analizar posibles alertas de inestabilidad comparando variaciones de desempeño |R2 Construcción – R2 Último Mes Con Desempeño|

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 2 · Umbrales: U-12

- **`DES-D4-06.01.03`** Para Tier I–II, reportar junto al Gini una métrica de evaluación basada en rentabilidad (por ejemplo, la máxima ganancia esperada, EMP) que refleje el costo asimétrico de los errores.

  Aplica: Todos los tipos, Tier I–II · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 2 · Nota: Línea base 2.0 (2026-10-17). Verbraken et al. (2014).

- **`DES-D4-06.01.04`** Reportar el desempeño por deciles de score (ordenamiento y tasa observada por decil) con su prueba de monotonicidad: cero inversiones en el OOT (U-44). Este reporte se llama «desempeño por deciles», no «calibración»: la calibración probabilística es un análisis distinto (DES-D4-08.01.07).

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 3 · Umbrales: U-44 · Nota: Versión 4.0.0 (2026-10-17). Lecciones de proyectos de desarrollo; ver CHANGELOG.

#### 6.2 Comparación con modelo vigente

- **`DES-D4-06.02.01`** Comparación con modelo vigente en cosechas / solicitudes aprobadas (por mes).

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 2 · Entregable: Ppt 10: Comparación con el modelo vigente.

#### 6.3 Selección del modelo final

- **`DES-D4-06.03.01`** Selección del modelo final (reunión con usuario)

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 0 · Entregable: Acta 5: Selección del modelo final. · Hito: Reunión 5

- **`DES-D4-06.03.02`** El modelo elegido debe tener una diferencia máxima de 10 puntos de performance entre la base de Train y OOT. En caso se tenga una diferencia mayor, se deberá sustentar en la documentación y presentar el caso en comité de modelos.

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 0 · Entregable: Documento 9: Entrenamiento y selección de modelos. · Hito: Sprint 13 · Umbrales: U-11

- **`DES-D4-06.03.03`** En caso el modelo sea construido utilizando un muestreo, se deberá evaluar la consistencia del performance del moldeo ( Gini Muestra vs Gini Población), a través de un ejercicio de bootstrapping

  Aplica: Todos los tipos, Tier I–III

- **`DES-D4-06.03.04`** Documentación del modelo final

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 2.125 d ágil / 2.5 d completo · Automatización: 1 · Entregable: Documento 9: Entrenamiento y selección de modelos.

- **`DES-D4-06.03.05`** Elegir el campeón con la tabla oficial del torneo: por candidato, Gini de entrenamiento, Gini, KS y AUC en validación y en OOT, brecha absoluta y relativa, Brier score y concentración máxima de importancia. Reglas: (1) queda descalificado quien incumpla U-11; (2) si uno más simple está a menos de 1.5 pts de Gini del más complejo, se elige el más simple (U-42); (3) nadie supera U-09; (4) el Brier score se reporta y se compara. El OOT se evalúa una sola vez, sobre los candidatos finales.

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 2 · Crítico · Umbrales: U-09, U-11, U-42, U-43 · Nota: Versión 4.0.0 (2026-10-17). Lecciones de proyectos de desarrollo; ver CHANGELOG.

### 7 · Interpretación del modelo de ordenamiento

#### 7.1 Reporte de interpretación del modelo

- **`DES-D4-07.01.01`** Unboxing: SHAP Value

  Aplica: ML I · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 1 · Entregable: Excel 18: Simulador.

- **`DES-D4-07.01.02`** Evaluar la estabilidad de las explicaciones (SHAP o LIME) ante remuestreo y desbalance de clases, y documentar las variables cuya contribución es inestable.

  Aplica: ML/Árbol I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 2 · Nota: Línea base 2.0 (2026-10-17). Chen, Calabrese y Martin-Barragan (2024).

### 8 · Calibración y regla de transición de scores

#### 8.1 Calibración

- **`DES-D4-08.01.01`** Extracción de base de calibración

  Aplica: Lineal/ML I–III · Esfuerzo: 2 d ágil / 2 d completo · Automatización: 1 · Entregable: Script 13: Análisis de calibración. · Hito: SME 8

- **`DES-D4-08.01.02`** Definición de drivers micro

  Aplica: Lineal/ML I–III · Esfuerzo: 1.7 d ágil / 2 d completo · Automatización: 1 · Hito: Sprint 14

- **`DES-D4-08.01.03`** Análisis de variables macro

  Aplica: Lineal/ML I–II · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1

- **`DES-D4-08.01.04`** Calibración

  Aplica: Lineal/ML I–III · Esfuerzo: 1.5 d ágil / 1.5 d completo · Automatización: 1

- **`DES-D4-08.01.05`** Reunión con usuario para presentación del calibrado

  Aplica: Lineal/ML I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1 · Entregable: Acta 6: de reunión. · Hito: Reunión 6

- **`DES-D4-08.01.06`** Puntuación de base calibrada

  Aplica: Lineal/ML I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Script 14: Implementación del calibrado.; Tabla 6: Base puntuada (oracle). · Hito: Sprint 15

- **`DES-D4-08.01.07`** Evaluar la calibración probabilística con una prueba formal (Hosmer-Lemeshow, o binomial o Jeffreys por tramo) y el Brier score. Una curva de tasa observada por decil sin bandas de confianza ni prueba no es una calibración.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 3 · Nota: Versión 4.0.0 (2026-10-17). Lecciones de proyectos de desarrollo; ver CHANGELOG.

#### 8.2 Análisis de transición applicant-behavior

- **`DES-D4-08.02.01`** Matriz de transición applicant / behavior

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 2 · Entregable: Excel 19: Matriz de transición

- **`DES-D4-08.02.02`** Temporalidad del applicant/behavior (gini por mes de maduración)

  Aplica: Lineal/ML/Árbol I–III · Entregable: Excel 19: Gini por mes de maduración.

- **`DES-D4-08.02.03`** Regla de transición de score

  Aplica: Lineal/ML/Árbol I–III · Entregable: Script 15: Implementación de la regla de transición.

#### 8.3 Documentación

- **`DES-D4-08.03.01`** Documento final de calibración

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Documento 10: Calibración.

### 9 · Evaluación del performance por drivers

#### 9.1 Evaluación del performance por drivers

- **`DES-D4-09.01.01`** Ejecución del performance del modelo

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 4 · Entregable: Script 16: Performance del modelo.

- **`DES-D4-09.01.02`** Reporte del seguimiento del modelo y acciones a desarrollar

  Aplica: Todos los tipos, Tier I–III · Entregable: Ppt 13: Presentación del performance del modelo. · Hito: SME 9

### 10 · Limitaciones del modelo

#### 10.1 Identificación de debilidades

- **`DES-D4-10.01.01`** Debilidades de discriminación

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 4.25 d ágil / 5 d completo · Automatización: 1 · Entregable: Ppt 14: Debilidades del modelo. · Hito: Sprint 16

- **`DES-D4-10.01.02`** Debilidades de calibración.

  Aplica: Todos los tipos, Tier I–III

- **`DES-D4-10.01.03`** Debilidades de estabilidad / Matriz de migración temporal

  Aplica: Todos los tipos, Tier I–III

- **`DES-D4-10.01.04`** En en caso el modelo se utilice en subpoblaciones distintas a la de modelamiento se debera evaluar el performece (Gini) en dichas subpoblacion.

  Aplica: Lineal/ML/Árbol I–III

- **`DES-D4-10.01.05`** Reporte de debilidades del modelo

  Aplica: Lineal/ML/Árbol I–III · Hito: SME 10

- **`DES-D4-10.01.06`** Realizar un análisis de sensibilidad del score ante variaciones de sus variables principales y de los supuestos del modelo.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 2 · Crítico · Nota: Línea base 2.0 (2026-10-17). Res. SBS 00053-2023 art. 16.

- **`DES-D4-10.01.07`** Para modelos sobre personas naturales Tier I–II, analizar la equidad: variables sensibles y sus proxies, métricas por grupo (separación) y decisión documentada sobre el criterio priorizado y su costo (FR-06).

  Aplica: Todos los tipos, Tier I–II · Esfuerzo: 1.5 d ágil / 2 d completo · Automatización: 2 · Nota: Línea base 2.0 (2026-10-17). Kozodoi, Jacob y Lessmann (2022); Barocas et al. (2023).

### 11 · Documentación Metodológica

#### 11.1 Elaboaración de la documentación

- **`DES-D4-11.01.01`** Documentación funcional

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1.275 d ágil / 1.5 d completo · Automatización: 1 · Entregable: Documento 11: Memoria metodológica del modelo. · Hito: Sprint 17

- **`DES-D4-11.01.02`** Documentación técnica

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 2.55 d ágil / 3 d completo · Automatización: 1 · Entregable: Documento 12: Manual de extracción.

- **`DES-D4-11.01.03`** Agregar un registo al cuadro de control de cambios con cada modificación

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 1 · Entregable: En caso exista algun cambio en el documento metodológico se agregará un registro al cuadro de control de cambios.

- **`DES-D4-11.01.04`** Agregar un cápitulo que detalle el reporte debilidades encontradas en el modelo

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 1

- **`DES-D4-11.01.05`** Agregar un cápitulo que detalle los usos del modelo

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 1

- **`DES-D4-11.01.06`** Especificar las versiones y rutas de las herramientas de procesamiento estadístico usadas y la funcionalidad de estas en cuanto al uso dado, así como las rutas productivas deonde se almacenará todo el desarrollo del proyecto

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 1

- **`DES-D4-11.01.07`** Elaborar el documento metodológico con la plantilla dinámica del estándar: registrar los datos del modelo en docs/documento.yaml y generar el documento con tools/documento.py (Markdown, HTML, Word y PDF desde la misma fuente). El documento evalúa los umbrales obtenidos, incluye la matriz de cumplimiento tomada de evidencias.yaml y no se presenta a Comité ni a Validación con secciones «Completar» pendientes.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 3 · Eficiencia · Entregable: Documento 11: Documento metodológico generado desde docs/documento.yaml (.md, .html, .docx y .pdf). · Nota: Versión 2.2.0 (2026-10-17). Documentación como código: una sola fuente versionada para todos los formatos.

#### 11.2 Consolidación

- **`DES-D4-11.02.01`** Documentación consolidada

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.425 d ágil / 0.5 d completo · Automatización: 1 · Entregable: Ppt 15: Cierre del modelo. · Umbrales: U-40

### 12 · Cierre Cuantitativo

#### 12.1 Cierre de modelo final

- **`DES-D4-12.01.01`** Reunión de resultados del modelo final cuantitativo

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1 · Entregable: Acta 7: Reunión de resultados del modelo final. · Hito: Reunión 7

### 13 · Cierre Cualitativo

#### 13.1 Enfoque Caulitativo (matrix CAR)

- **`DES-D4-13.01.01`** Reunión con la banca para revisión del enfoque cualitativo

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1 · Entregable: Acta 8: Acta de reunión con la banca · Hito: Reunión 8

- **`DES-D4-13.01.02`** Revisión, análisis y actualización de dimensiones en caso amerite

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1

- **`DES-D4-13.01.03`** Revisión, análisis y actualización de preguntas en caso amerite

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1

- **`DES-D4-13.01.04`** Revisión, análisis y actualización de pesos en caso amerite

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1

#### 13.2 Documentación cualitativa

- **`DES-D4-13.02.01`** Documentación consolidado Cualitativo

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1 · Entregable: Documento 11: Memoria metodológica del modelo.

### 14 · Presentación en CM

#### 14.1 Presentación

- **`DES-D4-14.01.01`** El modelo elegido no supera 10 puntos de diferencia de Gini entre Train y OOT ni una caída relativa de 10 % (U-11). Un candidato que exceda cualquiera de los dos queda descalificado; no admite excepción.

  Aplica: Lineal/ML/Árbol I–III · ACP I–II · Esfuerzo: 0 d ágil / 0 d completo · Automatización: 1 · Entregable: Acta 8: Acta del comité de modelos. · Hito: Comité de modelos

<!-- CATALOGO:FIN -->
