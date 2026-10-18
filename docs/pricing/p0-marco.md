---
id: PRC
titulo: "Pricing analítico · Marco end-to-end"
estandar: Pricing
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 24
---

# Pricing analítico · Marco end-to-end

El precio es la palanca de rentabilidad más potente y la menos industrializada de un banco. Un punto básico
sobre una cartera grande vale más que meses de optimización de costos. Pero un precio mal fijado destruye
valor por partida doble: cede margen donde el cliente habría aceptado más, y pierde volumen bueno donde el
precio está por encima de lo que el riesgo justifica. Este estándar convierte el precio en una decisión
**medible, reproducible, gobernada y auditable**.

## Principios

1. **Ningún precio por debajo de su costo económico.** Todo precio parte de un *piso técnico*: fondeo,
   pérdida esperada, costos y capital (U-18).
2. **El precio se decide con la respuesta del cliente, no solo con el costo.** Sobre el piso, el precio
   óptimo depende de la probabilidad de aceptación y del valor de la operación.
3. **La elasticidad se identifica, no se supone.** El precio histórico no fue aleatorio: sin una estrategia
   causal explícita, el modelo confunde riesgo con sensibilidad al precio (PRC-P4-01.01.01).
4. **Se prueba antes de escalar.** Los cambios materiales se validan con experimentos o despliegues escalonados.
5. **El precio es justo y explicable.** Se explica por riesgo, costo, plazo, canal y relación, nunca por
   atributos protegidos o la vulnerabilidad del cliente (PRC-P9-02.02.01).
6. **Personas deciden; modelos y agentes recomiendan.** Ningún modelo ni agente fija o aprueba precios (PRC-P9-03.01.01).

## Ciclo end-to-end

```text
 P1 Caso y gobierno ─▶ P2 Datos de cotizaciones ─▶ P3 Precio técnico (piso, RAROC)
                                                        │
              ┌─────────────────────────────────────────┘
              ▼
 P4 Respuesta al precio (causal) ─▶ P5 Optimización + escenarios ─▶ Comité de Precios
                                                                          │
              ┌───────────────────────────────────────────────────────────┘
              ▼
 P6 Experimento / piloto ─▶ P7 Motor de precios y facultades ─▶ P8 Seguimiento ─┐
              ▲                                                                  │
              └──────────── recalibrado (insumos trimestral, respuesta anual) ◀──┘
                                  P9 Gobierno, conducta y regulación (transversal)
```

| Fase | Pregunta que responde | Entregable principal |
|---|---|---|
| [P1](p1-definicion-datos.md) | ¿Qué precio decidimos, para qué objetivo y con qué restricciones? | Documento P1 · Ficha del caso |
| [P2](p1-definicion-datos.md) | ¿Tenemos ofertas aceptadas **y rechazadas**, con su costo a la fecha? | Tabla P1 · Base de cotizaciones |
| [P3](p3-precio-tecnico.md) | ¿Cuál es el precio mínimo que crea valor? | Excel P2 · Calculadora de precio técnico |
| [P4](p4-respuesta-optimizacion.md) | ¿Cómo responde cada cliente al precio? | Script P1 · Modelo de respuesta |
| [P5](p4-respuesta-optimizacion.md) | ¿Qué precio maximiza el objetivo respetando las restricciones? | PPT P1 · Escenarios; Acta del Comité |
| [P6](p6-experimentacion-implementacion.md) | ¿Funciona en el mundo real? | Documento P6 · Diseño del experimento |
| [P7](p6-experimentacion-implementacion.md) | ¿Llega al cliente exactamente como se aprobó? | Tarifario, facultades y motor certificado |
| [P8](p8-seguimiento-gobierno.md) | ¿Estamos capturando el valor? | Dashboard P1 · Seguimiento |
| [P9](p8-seguimiento-gobierno.md) | ¿Es legal, justo y está gobernado? | Documento P9 · Política de precios |

## Integración con el resto del estándar

| Pricing usa | De | Para |
|---|---|---|
| PD, LGD, EAD aprobadas | [Desarrollo](../desarrollo/d4-modelamiento.md) y [Calibración](../calibracion/c4-calibrado.md) | Pérdida esperada del piso técnico (PRC-P3-01.02.01) |
| Proceso de construcción de modelos | DES-D4 (muestras, depuración, selección, documentación) | Modelo de respuesta (PRC-P4-02.01.01) |
| Certificación ≥ 99.9 % (U-15) | [Implementación](../implementacion/implementacion.md) | Motor de precios (PRC-P7-02.02.01) |
| Revisión independiente | [Validación](../validacion/validacion.md), ámbito VAL-P | Modelos de precio técnico, respuesta y optimizador |
| Actas por hito | [Actas de reunión](../plantillas/acta-de-reunion.md) | Kick off, modelo de respuesta, Comité de Precios, piloto, revisión post-implementación |
| Estimación de esfuerzo | [Estimación](../marco/estimacion.md) | Plazos con personas y con agentes de IA |

## Qué enfoque de precio usar

| Situación | Enfoque | Requisitos mínimos |
|---|---|---|
| Producto nuevo o sin datos de ofertas rechazadas | **Costo + riesgo** (piso técnico con margen objetivo) | P1, P2, P3, P7, P9 |
| Tarifario por celdas, cartera madura | **Basado en riesgo + respuesta por celda** | P1–P5, despliegue escalonado P6, P7–P9 |
| Precio individual en originación, alto volumen | **Optimización individual con respuesta heterogénea** | Todo el estándar, con experimento P6 obligatorio |
| Depósitos y pasivos | **Beta de traslado + elasticidad de saldos**, piso = valor FTP del fondeo | P1–P5 con modelos de pasivos (PRC-P4-03.01.01) |
| Renovación o repricing de cartera | **Respuesta de retención (fuga) + valor remanente** | P3, P4 (fuga), P5, P8 |

## Indicadores de éxito del programa de pricing

- **Price realization:** tasa efectiva ÷ tasa de lista, por segmento.
- **Margen y RAROC realizados vs. esperados** (U-26).
- **Margen cedido por excepciones** (U-23).
- **Conversión por tramo de precio**, con su curva observada contra la predicha (U-21).
- **% de ofertas bajo el piso técnico** (objetivo: 0 % sin aprobación).
- **Cumplimiento regulatorio de tasas:** 100 % (U-24).
