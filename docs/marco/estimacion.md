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
revisan, deciden y firman, y siguen yendo a las **mismas reuniones**:

$$T_{\text{agente}}=\sum_i d_i f_i\,g_i\,(1+s)+B_{\text{agente}}+R$$

| Tipo de actividad | Esfuerzo humano que queda ($g$) | Qué hace el agente |
|---|---:|---|
| Datos (extracción, calidad, PSI, feature engineering, entrenamiento) | 25 % | Escribe y ejecuta scripts; la persona revisa salidas |
| Documentación | 30 % | Redacta desde logs y resultados; la persona corrige y firma |
| Análisis (sentido económico, segmentación, elección del modelo) | 60 % | Prepara alternativas; la decisión es humana |
| Gobierno (aprobaciones, solicitudes, evidencias) | 100 % | No acelera trámites formales |
| Supervisión del agente ($s$) | +15 % sobre el trabajo asistido | Instruir, verificar, corregir |

Cada requisito tiene su tipo en `dist/catalogo.json` (campo `naturaleza`). Si una clasificación automática no es
correcta, se corrige agregando `naturaleza:` al requisito en su YAML.

No incluye esperas que no son esfuerzo, como la agenda del Comité de Modelos o la cola de Validación.

## Resultado · 3 millones de registros × 1 000 columnas

<!-- CATALOGO:INICIO ESFUERZO -->
**Escenario:** 3.000.000 registros × 1.000 columnas · 4 segmentos · 1.5 personas · 30 % del tiempo en reuniones. Semanas de **calendario** (esfuerzo ÷ personas ÷ 5 días).

### Desarrollo (incluye Implementación y Gobierno)

| Tier | Modelo | Personas ágil | Personas trad. | Con agente ágil | Con agente trad. | Ahorro |
|---|---|---:|---:|---:|---:|---:|
| I | Lineal | 36.6 | 40.0 | 21.5 | 23.7 | 41% |
| I | ML | 33.3 | 37.0 | 19.7 | 22.1 | 41% |
| I | Árbol | 31.4 | 34.9 | 18.7 | 20.9 | 41% |
| I | ACP | 24.5 | 27.2 | 14.1 | 15.7 | 42% |
| II | Lineal | 33.9 | 36.8 | 20.0 | 21.8 | 41% |
| II | ML | 31.3 | 34.5 | 18.6 | 20.6 | 40% |
| II | Árbol | 29.4 | 32.3 | 17.5 | 19.3 | 40% |
| II | ACP | 23.0 | 25.6 | 13.4 | 15.0 | 42% |
| III | Lineal | 30.1 | 32.6 | 17.7 | 19.2 | 41% |
| III | ML | 29.5 | 32.4 | 17.4 | 19.1 | 41% |
| III | Árbol | 27.8 | 30.3 | 16.4 | 17.9 | 41% |
| III | ACP | 21.5 | 23.8 | 12.4 | 13.8 | 42% |
| IV | Lineal | 30.1 | 32.6 | 17.7 | 19.2 | 41% |
| IV | ML | 29.5 | 32.4 | 17.4 | 19.1 | 41% |
| IV | Árbol | 27.6 | 30.1 | 16.3 | 17.8 | 41% |
| IV | ACP | 21.5 | 23.8 | 12.4 | 13.8 | 42% |

### Calibración, Parámetros, Pricing, Seguimiento e Implementación

| Proyecto | Personas | Con agente | Ahorro |
|---|---:|---:|---:|
| Calibración Tier I | 10.6 | 6.3 | 40% |
| Calibración Tier II | 9.7 | 5.9 | 39% |
| Calibración Tier III | 7.6 | 4.5 | 41% |
| Calibración Tier IV | 7.6 | 4.5 | 41% |
| Parámetros de riesgo Tier I | 20.8 | 11.5 | 45% |
| Parámetros de riesgo Tier II | 20.8 | 11.5 | 45% |
| Parámetros de riesgo Tier III | 16.3 | 9.0 | 45% |
| Parámetros de riesgo Tier IV | 16.2 | 8.9 | 45% |
| Pricing end-to-end Tier I | 20.4 | 12.0 | 41% |
| Pricing end-to-end Tier II | 20.4 | 12.0 | 41% |
| Pricing end-to-end Tier III | 16.1 | 9.5 | 41% |
| Pricing end-to-end Tier IV | 15.0 | 8.8 | 41% |
| Seguimiento anual de un modelo Tier I | 2.4 | 1.5 | 38% |
| Seguimiento anual de un modelo Tier III | 2.4 | 1.5 | 38% |
| Implementación (proyecto independiente) | 2.7 | 1.8 | 33% |

### Desglose de referencia · Tier I, ML, ágil (días-persona)

| Fase | Catálogo | Reuniones del catálogo (\*) | Trabajo ajustado por volumen | Trabajo con agente |
|---|---:|---:|---:|---:|
| DES-D1 · Definición, alcance, diseño y extracción | 44.3 | 8.0 | 58.8 | 23.3 |
| DES-D2 · Preparación, calidad y entendimiento de los datos | 4.2 | 0.0 | 6.3 | 2.8 |
| DES-D3 · Segmentación | 2.4 | 0.8 | 2.1 | 0.7 |
| DES-D4 · Modelamiento | 61.4 | 1.2 | 77.7 | 29.1 |
| DES-D5 · Integración a la gestión | 12.5 | 0.0 | 12.5 | 8.0 |
| DES-D7 · Gobierno | 1.5 | 0.0 | 1.5 | 1.5 |
| IMP · Implementación | 14.6 | 0.5 | 14.1 | 7.5 |
| Bloqueo por tiempo de máquina (36.0 h) | | | 1.8 | 0.5 |
| Reuniones (30 % del tiempo de las personas) | | | 74.9 | 74.9 |
| **Total días-persona** | **140.9** | | **249.6** | **148.1** |
| **Semanas de calendario con 1.5 personas** | | | **33.3** | **19.7** |

(\*) Se excluyen del trabajo directo porque su tiempo ya está dentro del % de reuniones.

<!-- CATALOGO:FIN -->

## Notas para un proyecto de este tamaño

- **Memoria:** 3 M × 1 000 columnas son unos 12 GB en `float32` (24 GB en `float64`). Se necesita un servidor
  con ≥ 64 GB de RAM, o un motor distribuido. Para la exploración se puede trabajar sobre una muestra
  si cumple la representatividad (U-03).
- **Tiempo de máquina:** con ML, ~120 ajustes por segmento (≥ 50 de hiperparámetros, U-10), 4 segmentos y
  150 variables, son unas 36 horas de cómputo. Corren de noche, pero conviene planificarlas por sprint.
- **El agente no reduce las reuniones.** Con agente, las reuniones pasan de ser el 30 % del tiempo a cerca de la mitad.
  La siguiente palanca es acortar ceremonias, por ejemplo con actas preparadas por el agente y decisiones por escrito.
