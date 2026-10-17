---
id: INICIO
titulo: Estándares de Modelos en Banca
estandar: Marco
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 0
---

# Estándares de Modelos en Banca

Este repositorio reúne los estándares que rigen el **ciclo de vida completo** de los modelos en banca
(scores de originación, comportamiento y cobranza; estimadores de ingresos; modelos PD/LGD/EAD y calibraciones):
desarrollo, calibración, implementación, seguimiento y validación. Incluye además el estándar de
**Parámetros de riesgo** (PD, LGD, EAD, escenarios, staging y ECL bajo IFRS 9, y CLV) y el de
**Pricing analítico** end-to-end: precio técnico, respuesta al precio, optimización, experimentación, motor de precios y gobierno.

Están escritos como **documentación como código**: texto versionado y revisable, con un catálogo estructurado
que pueden consultar tanto los analistas como los agentes de IA.

> **Línea base 2.0** (octubre 2026): contrastada con la Res. SBS 00053-2023, la SR 26-2, la práctica pública de
> JPMorgan, HSBC, BBVA, Santander y Credicorp, y la literatura reciente de journals de primer nivel.
> Ver [Línea base 2.0 y benchmarking](marco/linea-base.md).

## Cómo está organizado

| Capa | Qué contiene | Quién la usa |
|---|---|---|
| **Catálogo normativo** (`catalogo/*.yaml`) | 340+ requisitos con ID estable, aplicabilidad por Tier y tipo de modelo, esfuerzo, entregable e hito | Analistas, PMO, validadores, agentes |
| **Documentación** (`docs/**/*.md`) | Cada fase explicada: objetivo, entradas, salidas, criterios de aceptación y catálogo de actividades | Analistas, revisores |
| **Umbrales** (`catalogo/umbrales.yaml`) | Los límites cuantitativos vigentes (PSI, Gini, correlaciones...) con su trazabilidad | Todos; es la regla de oro para agentes |
| **Frontera** (`docs/frontera/`) | Prácticas emergentes propuestas para incorporarse al estándar. **No son obligatorias** hasta que se aprueben | Equipo de metodología |
| **Sitio** (`site/index.html`) | Todo lo anterior en un sitio navegable, con buscador y planificador por Tier/modelo | Todos |

## Mapa del ciclo de vida

```text
  ┌────────────┐   ┌────────────┐   ┌──────────────┐   ┌────────────┐   ┌──────────────┐
  │ DESARROLLO │──▶│ VALIDACIÓN │──▶│IMPLEMENTACIÓN│──▶│ SEGUIMIENTO│──▶│ CALIBRACIÓN /│
  │  D1 … D7   │   │ metodológica│   │  + val. impl.│   │  (monitoreo)│   │ REDESARROLLO │
  └────────────┘   └────────────┘   └──────────────┘   └─────┬──────┘   └──────┬───────┘
         ▲                                                    │ alertas         │
         └────────────────────────────────────────────────────┴─────────────────┘
```

## Lectura según tu rol

- **Analista que va a construir un modelo:** empieza en [Ciclo de vida y gobierno](marco/ciclo-de-vida.md), luego
  [Tiering y enfoque](marco/tiering-y-metodologia.md), y usa el **Planificador** del sitio para obtener tu checklist.
- **Analista que va a calibrar:** [Calibración C1–C5](calibracion/c1-entendimiento.md).
- **Implementador:** [Implementación](implementacion/implementacion.md).
- **Validador:** [Validación](validacion/validacion.md) y [Umbrales](marco/umbrales.md).
- **Analista de parámetros (IFRS 9):** [Parámetros de riesgo · Marco](parametros/r0-marco.md).
- **Analista de pricing:** [Pricing analítico · Marco end-to-end](pricing/p0-marco.md) y [Agentes de IA en pricing](pricing/agentes-ia.md).
- **Agente de IA:** lee primero [`AGENTS.md`](../AGENTS.md) y el [estándar operativo de agentes](agentes/index.md); consulta `dist/catalogo.json`.
- **Para profundizar:** [Literatura de referencia](marco/literatura.md), con lecturas enlazadas a cada requisito.

## Convenciones

- **ID de requisito:** `DES-D4-05.04.01` = estándar de Desarrollo · fase D4 · tarea 05 · subtarea 04 · actividad 01.
  Prefijos: `DES` Desarrollo · `CAL` Calibración · `IMP` Implementación · `GOB` Gobierno · `SEG` Seguimiento · `PAR` Parámetros · `PRC` Pricing · `VAL` Validación · `U` Umbral.
  Los IDs no se reutilizan: si un requisito se elimina, su ID queda retirado.
- **Estados de un documento:** `Vigente` (obligatorio) · `Borrador` (en revisión) · `Propuesta` (frontera, no obligatorio).
- **"Debe"** expresa obligación; **"debería"**, recomendación; **"puede"**, opción permitida.

> **Yuri Plasencia — Analytics Pricing & Revenue Management**. Las propuestas de cambio siguen
> el proceso descrito en `CONTRIBUTING.md`.
