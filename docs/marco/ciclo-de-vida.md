---
id: MARCO-CV
titulo: Ciclo de vida y gobierno del modelo
estandar: Marco
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 1
---

# Ciclo de vida y gobierno del modelo

## Etapas

| # | Etapa | Estándar | Resultado de salida (gate) |
|---|---|---|---|
| 1 | Definición, alcance, diseño y extracción | [DES-D1](../desarrollo/d1-definicion.md) | Project Charter aprobado, Kick off, definición de default/target documentada |
| 2 | Preparación, calidad y entendimiento de datos | [DES-D2](../desarrollo/d2-calidad-datos.md) | Certificación de calidad de datos (Documento 6) |
| 3 | Segmentación | [DES-D3](../desarrollo/d3-segmentacion.md) | Segmentación final documentada (Documento 7) |
| 4 | Modelamiento | [DES-D4](../desarrollo/d4-modelamiento.md) | Modelo final seleccionado, calibrado y documentado; presentación en Comité de Modelos |
| 5 | Integración a la gestión | [DES-D5](../desarrollo/d5-integracion-gestion.md) | Punto de corte e impactos (riesgo, pricing, provisiones, capital, IFRS) |
| 6 | Implementación | [IMP](../implementacion/implementacion.md) | Certificación ≥ 95 % de coincidencia y conformidad del usuario |
| 7 | Gobierno | [DES-D7](../desarrollo/d7-gobierno.md) | Evidencias, Tier asignado, alta en inventario |
| — | Validación | [VAL](../validacion/validacion.md) | Dictamen de validación metodológica y de implementación |
| — | Seguimiento | [SEG](../seguimiento/seguimiento.md) | Reportes periódicos y alertas |
| — | Calibración | [CAL](../calibracion/c1-entendimiento.md) | Calibrado aprobado e implementado |
| — | Parámetros de riesgo | [PAR](../parametros/r0-marco.md) | Parámetros y ECL aprobados en comité de provisiones, motor certificado y backtesting anual |
| — | Pricing analítico | [PRC](../pricing/p0-marco.md) | Tarifario aprobado en Comité de Precios, motor certificado y seguimiento de margen |

## Hitos y ceremonias

El estándar se ejecuta en **sprints** (Sprint 0 a Sprint 20) con reuniones formales que dejan **acta**. Los sprints
marcan la **secuencia** de los paquetes de trabajo, no una duración fija: para cumplir el plazo máximo de U-40
(13 semanas con 2 personas), cada sprint dura en promedio unos 3 días hábiles, y las revisiones SME 1–13 son semanales.
Con agentes de IA, la misma secuencia se recorre en 15 días hábiles.

> Cada acta se crea en el sitio (**Herramientas › Actas de reunión**) o con `tools/acta.py`, ya precargada para su hito.
> Ver [Plantilla · Acta de reunión](../plantillas/acta-de-reunion.md).

| Hito | Momento | Evidencia |
|---|---|---|
| Reunión 1–2 | Levantamiento de expectativas (población, fuentes) | Acta 1, Acta 2 |
| Reunión 3 | Enriquecimiento de la propuesta / diseño funcional | Acta de reunión |
| Kick off | Arranque formal con stakeholders | PPT 2, Acta 3 |
| Reunión 4 | Segmentación | Acta 4 |
| Reunión 5 | Selección del modelo final | Acta 5 |
| Reunión 6 | Presentación del calibrado | Acta 6 |
| Reunión 7–8 | Resultados cuantitativos y enfoque cualitativo con la banca | Acta 7, Acta 8 |
| Comité de Modelos | Aprobación | Acta del comité |
| SME 1–13 | Revisiones con expertos de negocio (*subject matter experts*) | Según fase |

## Gobierno de la entidad

Todo el ciclo opera bajo el [Gobierno del riesgo de modelo](gobierno-mrm.md): comité de riesgos de modelo trimestral,
inventario, categorización, aprobación previa al uso (GOB-G3-01.01.01) e informe anual, según la Res. SBS 00053-2023.

## Tres líneas de defensa

| Línea | Rol | Responsabilidad en este estándar |
|---|---|---|
| 1ª | Equipo desarrollador / dueño del modelo | Ejecuta D1–D7, CAL e IMP; genera las evidencias; el líder del proyecto revisa la aplicación del estándar (DES-D7-01.01.01) |
| 2ª | Validación de modelos | Ejecuta VAL-M y VAL-I de forma independiente |
| 3ª | Auditoría interna | Revisa que el marco se cumpla |

## Reglas de gobierno transversales

1. **Todo modelo debe estar registrado en el inventario** con código único antes de su implementación (IMP-01.01, VAL-M-01.12).
2. **Toda decisión metodológica relevante debe quedar evidenciada** (correo, acta o documento) — DES-D7-01.01.02.
3. **Todo documento técnico lleva un cuadro de control de cambios** (DES-D4-11.01.03).
4. Si se usa una **metodología corporativa**, las definiciones de universo y target deben alinearse con ella;
   cualquier desviación se justifica con análisis metodológico o de negocio (DES-D1-01.04.06, CAL-C1-01.01.04).
5. Las desviaciones a un umbral (ver [Umbrales](umbrales.md)) se **sustentan por escrito** y, cuando el estándar
   lo indica, se presentan en Comité de Modelos.
