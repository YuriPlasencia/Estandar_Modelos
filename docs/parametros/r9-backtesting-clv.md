---
id: PAR-R9
titulo: "Parámetros · R9–R10 Backtesting, gobierno y CLV"
estandar: Parámetros
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 37
---

# Parámetros · R9–R10 Backtesting, gobierno y CLV

## R9 · Backtesting

El informe de monitoreo de la EBA identifica el backtesting como el área que más inversión requiere (LIT-113).
Este estándar exige un backtesting anual con cinco frentes:

| Frente | Prueba | Umbral |
|---|---|---|
| PD | Jeffreys por grado; tasa observada vs. PD a 12 meses y por horizonte | U-30 |
| LGD | LGD realizada vs. estimada por año de default, con los procesos ya cerrados | Desvío documentado |
| CCF | CCF realizado vs. estimado en los defaults del año | Desvío documentado |
| Staging | % de defaults que estaban en Stage 2; meses de anticipación; transiciones | Tendencia y comparación entre carteras |
| ECL | Pérdidas realizadas vs. ECL constituida por cohorte; escenario que se materializó | Explicación de diferencias |

## Gobierno

- **Comité de provisiones** (acta PAR-CP): aprueba parámetros, escenarios, staging, overlays y ECL, y revisa el puente con las provisiones regulatorias locales cuando coexisten.
- **Validación** independiente con el ámbito VAL-R de [Validación](../validacion/validacion.md).
- **Ciclo de recalibrado:** escenarios cada trimestre; parámetros al menos una vez al año o ante una alerta del backtesting.

<!-- CATALOGO:INICIO PAR-R9 -->
## Catálogo de requisitos · Backtesting, seguimiento y gobierno

> Bloque generado desde `catalogo/par-r9.yaml` (5 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17).

### 1 · Backtesting

#### 1.1 Backtesting de parámetros

- **`PAR-R9-01.01.01`** Backtesting anual de PD (Jeffreys por grado, U-30), LGD (estimada vs. realizada), CCF y staging (proporción de defaults que estaban en Stage 2; transiciones entre stages).

  Aplica: Tier I–IV · Esfuerzo: 3 d · Automatización: 3 · Crítico · Entregable: Excel R8: Backtesting de parámetros · Hito: Sprint 7 · Umbrales: U-30

- **`PAR-R9-01.01.02`** Backtesting de la ECL: comparar pérdidas realizadas con la ECL constituida por cohorte, y explicar las diferencias (escenario materializado vs. probabilidades asignadas).

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 3 · Entregable: Excel R8: Backtesting de parámetros

- **`PAR-R9-01.01.03`** Reunión de resultados del backtesting y decisión de recalibrar o redesarrollar.

  Aplica: Tier I–IV · Esfuerzo: 0.25 d · Automatización: 1 · Entregable: Acta PAR-BT: Resultados del backtesting

### 2 · Gobierno de provisiones

#### 2.1 Comité de provisiones

- **`PAR-R9-02.01.01`** Presentar al comité de provisiones los parámetros, escenarios, staging, overlays y la ECL resultante, con el puente frente a las provisiones regulatorias locales cuando ambas coexistan.

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 1 · Crítico · Entregable: Acta PAR-CP: Comité de provisiones · Hito: Comité de provisiones

- **`PAR-R9-02.01.02`** Mantener la documentación del ciclo de cálculo (insumos, versiones, controles, aprobaciones) para auditoría externa y supervisión, con cuadro de control de cambios.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 2 · Crítico · Entregable: Documento R10: Manual del ciclo de provisiones

<!-- CATALOGO:FIN -->

## R10 · CLV: los mismos parámetros para gestionar

El valor de vida del cliente usa **la misma supervivencia** que la ECL. Así, provisiones, pricing y gestión
comercial comparten una sola visión del riesgo:

$$\mathrm{CLV}=\sum_{t=1}^{T} S(t)\,\frac{\text{margen}_t-\mathrm{PD}^{\text{marg}}(t)\,\mathrm{LGD}\,\mathrm{EAD}_t-\text{costos}_t-\text{costo de capital}_t}{(1+r)^t}$$

donde $S(t)$ incluye la supervivencia frente a default, prepago y fuga. La diferencia con la ECL está en el uso:
la ECL usa parámetros PIT con forward-looking; el CLV para decisiones de largo plazo puede usar parámetros TTC.
La diferencia se documenta (PAR-R10-01.01.02). El precio técnico de [Pricing](../pricing/p3-precio-tecnico.md)
consume la misma PD lifetime anualizada.

<!-- CATALOGO:INICIO PAR-R10 -->
## Catálogo de requisitos · Valor de vida del cliente (CLV) y usos de gestión

> Bloque generado desde `catalogo/par-r10.yaml` (3 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17).

### 1 · CLV

#### 1.1 Modelo de valor

- **`PAR-R10-01.01.01`** Construir el valor de vida del cliente con los mismos parámetros lifetime (supervivencia por default, prepago y fuga, margen esperado, costo de riesgo y costo de capital) para que gestión, pricing y provisiones usen una sola visión del riesgo.

  Aplica: Tier I–II · Esfuerzo: 3 d · Automatización: 2 · Entregable: Script R6: Modelo de CLV · Hito: Sprint 8

- **`PAR-R10-01.01.02`** Documentar las diferencias entre los parámetros contables (PIT con forward-looking) y los de gestión (por ejemplo, TTC para pricing de largo plazo) y en qué uso aplica cada uno.

  Aplica: Tier I–III · Esfuerzo: 1 d · Automatización: 1 · Entregable: Documento R1: Mapa de parámetros y usos

### 2 · Entrega a usuarios

#### 2.1 Consumo de parámetros

- **`PAR-R10-02.01.01`** Publicar los parámetros vigentes en una tabla versionada con fecha de vigencia para sus consumidores (motor de ECL, pricing PRC-P3, capital, stress testing), con el registro de qué versión usó cada proceso.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 2 · Crítico · Entregable: Tabla R5: Parámetros vigentes versionados

<!-- CATALOGO:FIN -->

## Frontera *(propuesta, no obligatoria)*

- **Supervivencia dinámica con macro** para PD lifetime y stress testing (LIT-117), y tutoriales reproducibles recientes (LIT-118).
- **ML para recuperaciones y LGD** con la distribución completa, no solo la media: redes de cuantiles (LIT-121), ensambles y benchmarks (LIT-119, LIT-120).
- **Filtros de estado** (Kalman) anclados al largo plazo para estabilizar las proyecciones PIT a varios años.
- **Riesgos nuevos en la ECL:** clima y geopolítica mediante ajustes de modelo antes que overlays (LIT-114).
- **CCF:** seguir la versión final de las guías de la EBA sobre CCF (LIT-125).
