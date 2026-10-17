---
id: PAR-R6
titulo: "Parámetros · R6–R7 Escenarios y staging"
estandar: Parámetros
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 35
---

# Parámetros · R6–R7 Escenarios y staging

## R6 · Forward-looking

**Responsabilidades.** Estudios Económicos produce los escenarios y sus probabilidades; Parámetros los traduce a
tasas de default y LGD con **modelos satélite**; el comité los aprueba cada trimestre (U-32).

**La no linealidad importa.** Las pérdidas crecen más que proporcionalmente en recesión. Por eso la ECL se pondera
**después** de calcularla en cada escenario:

| Escenario | Probabilidad | ECL (ejemplo, millones) |
|---|---:|---:|
| Optimista | 25 % | 100 |
| Base | 50 % | 120 |
| Pesimista | 25 % | 220 |
| **ECL ponderada** $\sum_s p_s\,\mathrm{ECL}_s$ | | **140** |
| ECL de un "escenario promedio" (incorrecto) | | ≈ 125 |

Usar el escenario promedio **subestima** la provisión, aquí en unos 15 millones.

**Riesgos que la macro no ve.** Clima, energía, cadenas de suministro, geopolítica o concentraciones sectoriales
no siempre se reflejan en el PBI. El BCE considera mala práctica tratarlos solo vía variables macro generales
(LIT-114). Se evalúan explícitamente y, si el modelo no los captura, se cubren con un overlay gobernado (R8).

<!-- CATALOGO:INICIO PAR-R6 -->
## Catálogo de requisitos · Escenarios macroeconómicos y forward-looking

> Bloque generado desde `catalogo/par-r6.yaml` (6 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17).

### 1 · Escenarios

#### 1.1 Diseño y probabilidades

- **`PAR-R6-01.01.01`** Recibir de Estudios Económicos al menos tres escenarios (base, optimista y pesimista) con sus probabilidades y su sustento, revisados como mínimo cada trimestre (U-32).

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 1 · Crítico · Entregable: Documento R7: Escenarios y probabilidades · Hito: Sprint 4 · Umbrales: U-32

- **`PAR-R6-01.01.02`** Definir el horizonte de proyección explícito y la regla de reversión a la media de largo plazo de las variables macro y de los parámetros.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 1 · Crítico · Entregable: Documento R7: Escenarios y probabilidades

### 2 · Modelos satélite

#### 2.1 Vínculo macro–parámetros

- **`PAR-R6-02.01.01`** Estimar los modelos satélite que vinculan las variables macro con la tasa de default (y con la LGD cuando aplique): selección de variables con sentido económico y signo esperado, rezagos, y estabilidad fuera de muestra.

  Aplica: Tier I–IV · Esfuerzo: 3 d · Automatización: 2 · Crítico · Entregable: Script R4: Modelos satélite

- **`PAR-R6-02.01.02`** Probar la no linealidad: la ECL ponderada se calcula como el promedio de las ECL de cada escenario, nunca como la ECL de un escenario promedio (U-32).

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 3 · Crítico · Entregable: Excel R5: ECL por escenario · Umbrales: U-32

- **`PAR-R6-02.01.03`** Evaluar riesgos que la macro no captura (clima, energía, cadenas de suministro, geopolítica, sectores concentrados) y decidir si requieren un ajuste del modelo o un overlay gobernado (R8).

  Aplica: Tier I–II · Esfuerzo: 1.5 d · Automatización: 1 · Entregable: Documento R7: Escenarios y probabilidades

### 3 · Gobierno de escenarios

#### 3.1 Revisión trimestral

- **`PAR-R6-03.01.01`** Reunión trimestral de revisión de escenarios y probabilidades con Estudios Económicos, Riesgos y Contabilidad.

  Aplica: Tier I–IV · Esfuerzo: 0.25 d · Automatización: 1 · Entregable: Acta PAR-ESC: Revisión de escenarios

<!-- CATALOGO:FIN -->

## R7 · Staging

| Stage | Condición | ECL |
|---|---|---|
| **1** | Sin aumento significativo del riesgo desde el origen | 12 meses |
| **2** | Aumento significativo (SICR), sin default | Lifetime |
| **3** | En default (deterioro crediticio) | Lifetime con LGD en default |

**Criterio cuantitativo** (U-29), por operación, con PD lifetime en el reconocimiento inicial y hoy, para el plazo remanente:

$$\frac{\mathrm{PD}^{\text{LT}}_{\text{hoy}}}{\mathrm{PD}^{\text{LT}}_{\text{origen}}}\ \ge\ k\qquad\text{y}\qquad \mathrm{PD}^{\text{LT}}_{\text{hoy}}-\mathrm{PD}^{\text{LT}}_{\text{origen}}\ \ge\ a$$

El umbral absoluto $a$ evita que operaciones de muy bajo riesgo pasen a Stage 2 por variaciones mínimas; el
relativo $k$ capta el deterioro en riesgos medios.

**Backstops y criterios cualitativos** (U-28): más de 30 días de atraso implica Stage 2; default implica Stage 3.
A esto se suman refinanciados, lista de vigilancia y alertas tempranas.

**Cómo saber si el staging funciona:** la mayoría de los defaults deberían haber pasado antes por Stage 2, con
anticipación suficiente (PAR-R7-01.01.02). Si muchos defaults saltan directo de Stage 1 a Stage 3, los umbrales
son demasiado laxos.

<!-- CATALOGO:INICIO PAR-R7 -->
## Catálogo de requisitos · Staging y aumento significativo del riesgo (SICR)

> Bloque generado desde `catalogo/par-r7.yaml` (4 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17).

### 1 · Criterios de staging

#### 1.1 Criterios cuantitativos

- **`PAR-R7-01.01.01`** Comparar la PD lifetime actual con la PD lifetime en el reconocimiento inicial, por operación, con umbrales relativos y absolutos calibrados por cartera (U-29).

  Aplica: Tier I–IV · Esfuerzo: 2.5 d · Automatización: 2 · Crítico · Entregable: Documento R8: Criterios de staging · Hito: Sprint 5 · Umbrales: U-29

- **`PAR-R7-01.01.02`** Calibrar los umbrales SICR para que Stage 2 anticipe el default: proporción de defaults que pasaron antes por Stage 2, tiempo de permanencia y estabilidad de las transiciones.

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Excel R6: Calibración de umbrales SICR · Umbrales: U-29

#### 1.2 Criterios cualitativos y backstops

- **`PAR-R7-01.02.01`** Aplicar el backstop de 30 días de atraso para Stage 2 y el de default para Stage 3 (U-28), además de criterios cualitativos: refinanciados, lista de vigilancia y alertas tempranas.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 2 · Crítico · Entregable: Documento R8: Criterios de staging · Umbrales: U-28

- **`PAR-R7-01.02.02`** Definir el retorno de Stage 2 a Stage 1 y de Stage 3 a Stage 2 con períodos de prueba (U-33), y documentar el tratamiento de activos adquiridos u originados con deterioro (POCI).

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 1 · Entregable: Documento R8: Criterios de staging · Umbrales: U-33

<!-- CATALOGO:FIN -->
