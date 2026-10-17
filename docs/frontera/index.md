---
id: FRONTERA
titulo: "Frontera del conocimiento: hoja de ruta"
estandar: Frontera
estado: Propuesta
version: 0.1.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 50
---

# Frontera del conocimiento: hoja de ruta

Esta sección es el **laboratorio** del estándar. Recoge prácticas que la industria y los reguladores están
adoptando y que proponemos incorporar. Nada aquí es obligatorio hasta pasar por el proceso de cambio
(`CONTRIBUTING.md`) y aparecer en el catálogo con estado `Vigente`.

Cada propuesta indica **qué requisito vigente extiende**, para que la incorporación sea quirúrgica.

| ID | Propuesta | Extiende | Prioridad | Esfuerzo |
|---|---|---|---|---|
| FR-01 | [Marco regulatorio de referencia](marco-regulatorio.md) | Marco, VAL | Alta | Bajo |
| FR-02 | [Tiering basado en riesgo](tiering-basado-en-riesgo.md) | DES-D7-01.01.03, VAL-M-01.13 | Alta | Bajo |
| FR-03 | [Explicabilidad y modelos interpretables](explicabilidad.md) | DES-D4-07, DES-D4-05.02 | Alta | Medio |
| FR-04 | [Calibración y cuantificación de incertidumbre](calibracion-e-incertidumbre.md) | DES-D4-08, CAL-C4, SEG | Alta | Medio |
| FR-05 | [Monitoreo de drift moderno](monitoreo-drift.md) | SEG, IMP-01.04 | Media | Medio |
| FR-06 | [Equidad y sesgo](equidad-y-sesgo.md) | DES-D4-10, VAL-M-03.08 | Media | Medio |
| FR-07 | [Reproducibilidad y MLOps](mlops-reproducibilidad.md) | DES-D4-11.01.06, IMP | Alta | Medio |
| FR-08 | [IA generativa y agentes en el ciclo de vida](ia-generativa.md) | Marco, D7 | Media | Medio |

## Criterio para pasar de Propuesta a Vigente

1. Piloto en al menos **un modelo Tier I y uno Tier III**.
2. Script o proceso en el toolkit (nivel de automatización ≥ 3).
3. Umbral, si lo hay, calibrado con datos propios — no copiado de la literatura.
4. Aprobación del custodio y, si cambia obligaciones de segunda línea, de Validación.
