---
id: MARCO-EST
titulo: Estimación de esfuerzo
estandar: Marco
estado: Vigente
version: 2.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 4
---

# Estimación de esfuerzo

La estimación se calcula desde el catálogo de requisitos con el modelo de esfuerzo.
Los parámetros están en `catalogo/parametros_esfuerzo.yaml` y la lógica en `tools/esfuerzo.py`.
El Planificador del sitio usa exactamente el mismo cálculo y permite cambiar el escenario.

## Cómo se calcula

Para cada requisito aplicable según Tier, tipo de modelo y enfoque:

$$W=\sum_{i\notin\text{reuniones}} d_i\cdot f_i,\qquad
f_i=\left(\frac{N}{N_0}\right)^{0.15}\left(\frac{C}{C_0}\right)^{e_i}$$

- $d_i$: días del catálogo. $N, C$: registros y columnas del proyecto. $N_0=1\,000\,000$ y $C_0=300$ son el
  volumen de referencia al que corresponden los días del catálogo.
- $f_i$ se aplica sólo a las actividades de **datos** de D1–D4 y C1–C4. Se usa $e_i=0.5$ si la actividad es
  manual (nivel de automatización 0–2) y $e_i=0.25$ si está automatizada (3–4). En entrenamiento y calibración
  sólo pesa el número de registros, porque se trabaja con ~150 variables preseleccionadas (U-08) o con pocos drivers.
- Las actividades de **reunión** del catálogo no se suman al trabajo directo: su tiempo queda dentro del
  porcentaje de reuniones.

**Con personas**, si una fracción $m$ del tiempo se va en reuniones y $B$ es el bloqueo por tiempo de máquina:

$$T_{\text{personas}}=\frac{W+B}{1-m},\qquad R=m\,T_{\text{personas}},\qquad \text{semanas}=\frac{T}{\text{FTE}\times 5}$$

**Con un agente de IA**, el agente escribe y ejecuta los scripts y redacta los borradores. Las personas
revisan, deciden y firman (antes del anclaje, con las mismas reuniones):

$$T_{\text{agente}}=\sum_i d_i f_i\,g_i\,(1+s)+B_{\text{agente}}+R$$

| Tipo de actividad | Esfuerzo humano que queda ($g$) | Qué hace el agente |
|---|---:|---|
| Datos (extracción, calidad, PSI, feature engineering, entrenamiento) | 25 % | Escribe y ejecuta scripts; la persona revisa salidas |
| Documentación | 30 % | Redacta desde logs y resultados; la persona corrige y firma |
| Análisis (sentido económico, segmentación, elección del modelo) | 60 % | Prepara alternativas; la decisión es humana |
| Gobierno (aprobaciones, solicitudes, evidencias) | 100 % | No acelera trámites formales |
| Supervisión del agente ($s$) | +15 % sobre el trabajo asistido | Instruir, verificar, corregir |

### Anclaje a la meta de plazo (U-40)

La meta del estándar es que un modelo de Desarrollo se termine con **2 personas en un máximo de 13 semanas (3 meses)**
y, con agentes de IA, en **un máximo de 15 días hábiles** con las mismas personas. Los días del catálogo se usan como
**pesos relativos** entre actividades, y el nivel absoluto se ancla a esa meta: el caso más exigente de Desarrollo
(Tier I, lineal, completo) dura exactamente la meta con el escenario base.

$$k_{\text{personas}}=\frac{13\times5\times2}{T_{\text{personas}}(\text{ref})},\qquad
k_{\text{agente}}=\frac{15\times2}{T_{\text{agente}}(\text{ref})}$$

Todas las estimaciones, de todos los estándares, se multiplican por $k_{\text{personas}}$ o $k_{\text{agente}}$, de modo
que conservan sus proporciones y los demás casos quedan por debajo de la meta. Si el volumen, los segmentos o el
porcentaje de reuniones de un proyecto lo llevan por encima de U-40, el planificador lo marca y el exceso se sustenta
ante el Comité. Con agentes, también las reuniones se acortan, porque el proyecto dura menos.

Cada requisito tiene su tipo en `dist/catalogo.json` (campo `naturaleza`). Si una clasificación automática no es
correcta, se corrige agregando `naturaleza:` al requisito en su YAML.

No incluye esperas que no son esfuerzo, como la agenda del Comité de Modelos o la cola de Validación.

## Resultado · 3 millones de registros × 1 000 columnas

<!-- CATALOGO:INICIO ESFUERZO -->
**Escenario:** 3.000.000 registros × 1.000 columnas · 4 segmentos · 2 personas · 30 % del tiempo en reuniones. Con personas, semanas de **calendario**; con agentes, **días hábiles** con las mismas personas.

**Meta U-40:** 2 personas, máximo 13 semanas; con agentes, máximo 15 días hábiles. Caso de referencia del anclaje: Desarrollo Tier I, Lineal, completo.

### Desarrollo (incluye Implementación y Gobierno)

| Tier | Modelo | Personas ágil (sem.) | Personas completo (sem.) | Agente ágil (días) | Agente completo (días) | Ahorro |
|---|---|---:|---:|---:|---:|---:|
| I | Lineal | 11.9 | 13.0 | 14 | 15 | 77% |
| I | ML | 10.8 | 12.0 | 13 | 14 | 77% |
| I | Árbol | 10.2 | 11.3 | 12 | 13 | 77% |
| I | ACP | 7.9 | 8.8 | 9 | 10 | 78% |
| II | Lineal | 11.0 | 12.0 | 13 | 14 | 77% |
| II | ML | 10.2 | 11.2 | 12 | 13 | 77% |
| II | Árbol | 9.6 | 10.5 | 11 | 12 | 77% |
| II | ACP | 7.5 | 8.3 | 8 | 9 | 77% |
| III | Lineal | 9.8 | 10.6 | 11 | 12 | 77% |
| III | ML | 9.6 | 10.5 | 11 | 12 | 77% |
| III | Árbol | 9.0 | 9.8 | 10 | 11 | 77% |
| III | ACP | 7.0 | 7.7 | 8 | 9 | 78% |
| IV | Lineal | 9.8 | 10.6 | 11 | 12 | 77% |
| IV | ML | 9.6 | 10.5 | 11 | 12 | 77% |
| IV | Árbol | 9.0 | 9.8 | 10 | 11 | 77% |
| IV | ACP | 7.0 | 7.7 | 8 | 9 | 78% |

### Calibración, Parámetros, Pricing, Seguimiento e Implementación

| Proyecto | Personas (semanas) | Con agente (días hábiles) | Ahorro |
|---|---:|---:|---:|
| Calibración Tier I | 3.4 | 4 | 77% |
| Calibración Tier II | 3.2 | 4 | 76% |
| Calibración Tier III | 2.5 | 3 | 77% |
| Calibración Tier IV | 2.5 | 3 | 77% |
| Parámetros de riesgo Tier I | 6.8 | 7 | 78% |
| Parámetros de riesgo Tier II | 6.8 | 7 | 78% |
| Parámetros de riesgo Tier III | 5.3 | 6 | 78% |
| Parámetros de riesgo Tier IV | 5.2 | 6 | 78% |
| Pricing end-to-end Tier I | 6.6 | 8 | 77% |
| Pricing end-to-end Tier II | 6.6 | 8 | 77% |
| Pricing end-to-end Tier III | 5.2 | 6 | 77% |
| Pricing end-to-end Tier IV | 4.9 | 6 | 77% |
| Seguimiento anual de un modelo Tier I | 0.8 | 1 | 76% |
| Seguimiento anual de un modelo Tier III | 0.8 | 1 | 76% |
| Implementación (proyecto independiente) | 0.9 | 1 | 74% |

### Desglose de referencia · Tier I, ML, ágil (días-persona)

| Fase | Trabajo con personas | Trabajo con agente |
|---|---:|---:|
| DES-D1 · Definición, alcance, diseño y extracción | 25.5 | 3.9 |
| DES-D2 · Preparación, calidad y entendimiento de los datos | 2.7 | 0.5 |
| DES-D3 · Segmentación | 0.9 | 0.1 |
| DES-D4 · Modelamiento | 33.7 | 4.9 |
| DES-D5 · Integración a la gestión | 5.4 | 1.3 |
| DES-D7 · Gobierno | 0.6 | 0.3 |
| IMP · Implementación | 6.1 | 1.3 |
| Reuniones y bloqueo por tiempo de máquina (36.0 h) | 33.2 | 12.7 |
| **Total días-persona** | **108.1** | **25.0** |
| **Duración con 2 personas** | **10.8 semanas** | **13 días hábiles** |

<!-- CATALOGO:FIN -->

## Notas para un proyecto de este tamaño

- **Memoria:** 3 M × 1 000 columnas son unos 12 GB en `float32` (24 GB en `float64`). Se necesita un servidor
  con ≥ 64 GB de RAM, o un motor distribuido. Para la exploración se puede trabajar sobre una muestra
  si cumple la representatividad (U-03).
- **Tiempo de máquina:** con ML, ~120 ajustes por segmento (≥ 50 de hiperparámetros, U-10), 4 segmentos y
  150 variables, son unas 36 horas de cómputo. Corren de noche, pero conviene planificarlas por sprint.
- **Cumplir 15 días con agentes exige acortar ceremonias:** actas preparadas por el agente, decisiones por escrito y
  reuniones de hito cortas. Las aprobaciones formales no se aceleran; se agendan desde el kick-off.
