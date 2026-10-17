---
id: PRC-P1
titulo: "Pricing · P1–P2 Caso, gobierno y datos"
estandar: Pricing
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 25
---

# Pricing · P1–P2 Caso, gobierno y datos

## P1 · El caso de pricing

La mitad de los proyectos de pricing que fracasan lo hacen por un objetivo mal definido. "Subir margen" sin
decir a costa de cuánto volumen lleva a una propuesta que el negocio rechaza en el comité. El caso debe dejar escrito:

- **La decisión:** tarifario por celdas, precio individual, renovación, repricing o tasa de depósitos.
- **La función objetivo y su horizonte:** por ejemplo, *maximizar el margen esperado a 12 meses con un volumen
  no inferior al 95 % del actual*.
- **Las restricciones duras:** tope regulatorio (U-24), piso técnico (U-18), gradualidad (U-25), apetito de riesgo.
- **El valor en juego:** margen cedido hoy por excepciones y operaciones bajo el piso. Es la línea base
  contra la que se mide el éxito en la revisión post-implementación (PRC-P8-02.01.01).

<!-- CATALOGO:INICIO PRC-P1 -->
## Catálogo de requisitos · Definición del caso de pricing y gobierno inicial

> Bloque generado desde `catalogo/prc-p1.yaml` (8 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Pricing Analítico v1.0 (nuevo, 2026-10-17).

### 1 · Caso de negocio

#### 1.1 Objetivo y alcance

- **`PRC-P1-01.01.01`** Definir el producto (activo o pasivo), los segmentos, los canales y el tipo de decisión de precio: tarifario de lista, precio individual en originación, renovación, repricing de cartera o tasa de depósitos.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 1 · Crítico · Entregable: Documento P1: Ficha del caso de pricing · Hito: Sprint 0

- **`PRC-P1-01.01.02`** Fijar la función objetivo y su horizonte: margen financiero, NIM, RAROC, valor de vida del cliente (CLV), volumen o una combinación ponderada. Documentar explícitamente el trade-off volumen–margen que acepta el negocio.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 1 · Crítico · Entregable: Documento P1: Ficha del caso de pricing

- **`PRC-P1-01.01.03`** Inventariar las restricciones: topes regulatorios de tasa (U-24), apetito de riesgo, metas de volumen y de colocación, política comercial, compromisos con clientes, gradualidad máxima de cambios (U-25) y restricciones de conducta.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 1 · Crítico · Entregable: Documento P1: Ficha del caso de pricing · Umbrales: U-25

#### 1.2 Diagnóstico del precio actual

- **`PRC-P1-01.02.01`** Diagnosticar el esquema de precios vigente: tarifario, bandas de negociación, facultades de descuento, dispersión de tasas por segmento de riesgo, price realization (tasa efectiva vs. tasa de lista) y brecha frente a la competencia.

  Aplica: Tier I–IV · Esfuerzo: 3 d · Automatización: 2 · Entregable: Excel P1: Diagnóstico del precio actual · Hito: Sprint 1

- **`PRC-P1-01.02.02`** Estimar el valor en juego: margen cedido por excepciones (leakage), clientes con precio por debajo del piso técnico (U-18) y oportunidad por segmento. Es la base para priorizar el proyecto y medir su éxito.

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 2 · Entregable: Excel P1: Diagnóstico del precio actual

### 2 · Gobierno inicial

#### 2.1 Clasificación y responsables

- **`PRC-P1-02.01.01`** Registrar en el inventario los modelos que intervendrán (precio técnico, respuesta, optimizador) y asignar su Tier. Un modelo de pricing es un modelo sujeto a este estándar y a Validación.

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 1 · Crítico · Entregable: Documento P1: Ficha del caso de pricing

- **`PRC-P1-02.01.02`** Definir la matriz RACI: dueño del precio (negocio), Finanzas/ALM (costo de fondos y capital), Riesgos (PD/LGD y apetito), Analytics Pricing (modelos y optimización), Cumplimiento y Legal (conducta y transparencia), Tecnología (motor de precios).

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 1 · Entregable: Documento P1: Ficha del caso de pricing

#### 2.2 Kick off

- **`PRC-P1-02.02.01`** Reunión de kick off del proyecto de pricing con el dueño del precio, Finanzas, Riesgos y Cumplimiento.

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 1 · Entregable: Acta PRC-KO: Kick off de pricing · Hito: Kick Off

<!-- CATALOGO:FIN -->

## P2 · La base de cotizaciones

El error de datos más caro en pricing es **modelar solo las operaciones desembolsadas**. Quien aceptó revela
poco sobre quien rechazó; sin las ofertas rechazadas, la elasticidad no se puede estimar. La unidad de la base es la **oferta**:

| Bloque | Campos mínimos |
|---|---|
| Oferta | id de oferta, fecha, producto, monto, plazo, canal, ejecutivo, precio de lista, precio ofrecido, excepción y aprobador |
| Resultado | aceptó (sí/no), precio final, fecha de desembolso, motivo de no aceptación |
| Costo a la fecha | FTP por plazo, PD, LGD, EAD, costo operativo, capital consumido (versionados a la fecha de la oferta) |
| Contexto | tasa de la competencia, tasa de referencia, campaña, saturación del canal |
| Comportamiento posterior | prepago, cancelación, uso de línea, saldo, default |

**Variación exógena del precio.** Antes de modelar, mide cuánta variación del precio no depende del cliente:
cambios de tarifario, campañas, saltos de la grilla. Si casi todo el precio se explica por el riesgo, no hay
identificación posible. Entonces el experimento (P6) es un **requisito previo**, no un extra (PRC-P2-02.01.02).

<!-- CATALOGO:INICIO PRC-P2 -->
## Catálogo de requisitos · Datos de pricing y calidad

> Bloque generado desde `catalogo/prc-p2.yaml` (7 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Pricing Analítico v1.0 (nuevo, 2026-10-17).

### 1 · Base de cotizaciones

#### 1.1 Construcción

- **`PRC-P2-01.01.01`** Construir la base a nivel de oferta o cotización, no solo de operaciones desembolsadas: precio ofrecido, precio final, aceptación (sí/no), monto, plazo, canal, ejecutivo, fecha y motivo de no aceptación. Sin las ofertas rechazadas por el cliente no se puede estimar la respuesta al precio.

  Aplica: Tier I–IV · Esfuerzo: 4 d · Automatización: 2 · Crítico · Entregable: Tabla P1: Base de cotizaciones · Hito: Sprint 1

- **`PRC-P2-01.01.02`** Enriquecer cada oferta con los insumos del precio técnico vigentes a la fecha de la oferta: PD y LGD del modelo de riesgo aprobado (definición de default U-17), curva FTP, costo operativo y consumo de capital.

  Aplica: Tier I–IV · Esfuerzo: 3 d · Automatización: 2 · Crítico · Entregable: Tabla P1: Base de cotizaciones

- **`PRC-P2-01.01.03`** Incorporar variables de contexto: tasas de la competencia por producto y plazo, tasa de referencia de política monetaria, campañas vigentes, estacionalidad y saturación del canal.

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 2 · Entregable: Tabla P1: Base de cotizaciones

- **`PRC-P2-01.01.04`** Para productos con comportamiento posterior (TC, consumo, hipotecario, depósitos), unir el desempeño: prepago, cancelación, uso de línea, saldo promedio y default, para calcular el valor de la operación y no solo su aceptación.

  Aplica: Tier I–III · Esfuerzo: 3 d · Automatización: 2 · Entregable: Tabla P1: Base de cotizaciones

### 2 · Calidad de datos de pricing

#### 2.1 Controles

- **`PRC-P2-02.01.01`** Aplicar los controles de calidad de DES-D2 (validez, completitud, unicidad, precisión, consistencia) y los específicos de pricing: precio ofrecido registrado antes de la decisión del cliente, cotizaciones duplicadas por re-cotización, tasas fuera de rango y fechas de oferta coherentes con la de desembolso.

  Aplica: Tier I–IV · Esfuerzo: 2.5 d · Automatización: 3 · Crítico · Entregable: Documento P2: Diccionario y certificación de datos de pricing

- **`PRC-P2-02.01.02`** Medir la variación exógena del precio disponible para identificar la elasticidad: cambios de tarifario, campañas, saltos de la grilla, pruebas previas. Si no existe variación suficiente, el diseño de un experimento (P6) pasa a ser requisito previo para el modelo de respuesta.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 1 · Crítico · Entregable: Documento P2: Diccionario y certificación de datos de pricing

- **`PRC-P2-02.01.03`** Certificar la base de pricing con acta de conformidad de las fuentes (Finanzas para FTP y costos; Riesgos para PD/LGD).

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 1 · Entregable: Documento P2: Diccionario y certificación de datos de pricing

<!-- CATALOGO:FIN -->
