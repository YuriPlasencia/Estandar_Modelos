---
id: PAR-R8
titulo: "Parámetros · R8 Pérdida esperada y overlays"
estandar: Parámetros
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 36
---

# Parámetros · R8 Pérdida esperada y overlays

## Cálculo

Para una operación en Stage 2, con escenarios $s$ de probabilidad $p_s$, horizonte remanente $T$ y tasa de interés efectiva EIR:

$$\mathrm{ECL}=\sum_{s} p_s \sum_{t=1}^{T}\mathrm{PD}^{\text{marg}}_{s}(t)\cdot \mathrm{LGD}_{s}(t)\cdot \mathrm{EAD}(t)\cdot (1+\mathrm{EIR})^{-t}$$

Para Stage 1, el horizonte se limita a 12 meses. Para Stage 3, la ECL es la LGD en default por la exposición.
El motor se certifica con el estándar de [Implementación](../implementacion/implementacion.md) (U-15) y se
concilia con contabilidad (PAR-R8-01.01.02).

## Movimiento de la ECL

Cada cierre se explica la variación de la ECL, que también exige IFRS 7:

```text
ECL inicial
  + originaciones          − bajas y cancelaciones
  ± transferencias entre stages (1↔2↔3)
  ± cambios de parámetros (recalibraciones)
  ± cambios de escenarios y ponderaciones
  ± overlays (nuevos, recalibrados, liberados)
  − castigos               ± tipo de cambio y otros
= ECL final
```

## Overlays y ajustes post-modelo

Los supervisores reconocen que los overlays se han vuelto parte estructural de la ECL. También advierten que su
calibración tiene demasiado juicio (LIT-113) y que deben basarse en análisis robustos y gobierno sólido (LIT-114).
Este estándar lo traduce en reglas (U-31):

| Requisito | Por qué |
|---|---|
| Causa identificada: qué riesgo no captura el modelo | Sin causa, el overlay es una forma de suavizar resultados |
| Cuantificación reproducible (método, datos y supuestos) | Permite que Validación y Auditoría lo repliquen |
| Cartera afectada y efecto en el staging | Evita aplicarlo "en general" |
| Fecha de revisión o expiración | Impide que se vuelva permanente |
| Aprobación en comité con acta (PAR-OVL) | Responsabilidad clara |
| Plan de absorción en el modelo (PAR-R8-02.01.03) | El objetivo es que el modelo lo capture en el siguiente ciclo |

<!-- CATALOGO:INICIO PAR-R8 -->
## Catálogo de requisitos · Pérdida crediticia esperada (ECL) y overlays

> Bloque generado desde `catalogo/par-r8.yaml` (7 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17).

### 1 · Cálculo de la ECL

#### 1.1 Motor de cálculo

- **`PAR-R8-01.01.01`** Calcular la ECL por operación como la suma, período a período, de PD marginal × LGD × EAD descontada a la tasa de interés efectiva: 12 meses para Stage 1, lifetime para Stage 2 y LGD en default para Stage 3; ponderar por escenario (U-32).

  Aplica: Tier I–IV · Esfuerzo: 3 d · Automatización: 2 · Crítico · Entregable: Script R5: Motor de ECL · Hito: Sprint 6 · Umbrales: U-32

- **`PAR-R8-01.01.02`** Certificar el motor de ECL con el estándar IMP (coincidencia ≥ 95 % con el cálculo de modelamiento, U-15) y conciliar la ECL con contabilidad.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Documento 14: Certificación del modelo

#### 1.2 Análisis de resultados

- **`PAR-R8-01.02.01`** Explicar los movimientos de la ECL entre períodos (originaciones, bajas, cambios de stage, cambios de parámetros, escenarios, castigos) para Contabilidad y para las revelaciones de IFRS 7.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 3 · Crítico · Entregable: Excel R7: Movimiento de la ECL

- **`PAR-R8-01.02.02`** Calcular sensibilidades de la ECL: 100 % en cada escenario, cambios en ponderaciones y en umbrales SICR.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 3 · Entregable: Excel R7: Movimiento de la ECL

### 2 · Overlays y ajustes post-modelo

#### 2.1 Gobierno de overlays

- **`PAR-R8-02.01.01`** Todo overlay o ajuste post-modelo debe tener causa identificada (riesgo no capturado por el modelo), cuantificación reproducible, cartera afectada, fecha de revisión o expiración y aprobación en comité (U-31).

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 1 · Crítico · Entregable: Documento R9: Registro de overlays · Umbrales: U-31

- **`PAR-R8-02.01.02`** Reunión de aprobación de overlays y de los resultados de la ECL del período.

  Aplica: Tier I–IV · Esfuerzo: 0.25 d · Automatización: 1 · Entregable: Acta PAR-OVL: Aprobación de overlays

- **`PAR-R8-02.01.03`** Planificar la absorción de cada overlay recurrente dentro del modelo en el siguiente ciclo de recalibrado, para que no se vuelva permanente.

  Aplica: Tier I–II · Esfuerzo: 1 d · Automatización: 1 · Entregable: Documento R9: Registro de overlays · Umbrales: U-31

<!-- CATALOGO:FIN -->
