---
id: PRC-P8
titulo: "Pricing · P8–P9 Seguimiento, gobierno y conducta"
estandar: Pricing
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 29
---

# Pricing · P8–P9 Seguimiento, gobierno y conducta

## P8 · ¿Estamos capturando el valor?

### Descomposición del margen

Cada mes, la variación del margen del segmento se separa en sus causas, para atribuir resultados a la
estrategia de precios y no al mercado (PRC-P8-01.02.01). Con $M=s\,V$, $s=\bar r-r_{\text{FTP}}$ el spread sobre
el costo de fondos, $V$ el volumen, $w_k$ el peso de la celda $k$ (riesgo, plazo, canal) y $r_k$ su tasa:

$$\Delta M=\underbrace{V_1\sum_k w_{1,k}\,\Delta r_k}_{\text{precio}}+\underbrace{V_1\sum_k \Delta w_k\,r_{0,k}}_{\text{mix}}-\underbrace{V_1\,\Delta r_{\text{FTP}}}_{\text{costo de fondos}}+\underbrace{s_0\,\Delta V}_{\text{volumen}}$$

Los cuatro efectos suman exactamente la variación del margen.

### Tablero mínimo

| Indicador | Umbral |
|---|---|
| Conversión observada vs. predicha por tramo de precio | U-21 |
| Price realization (efectiva ÷ lista) | Tendencia; caída sostenida = fuga |
| Margen y RAROC realizados vs. esperados | U-26 |
| Excepciones y margen cedido | U-23 |
| Ofertas bajo el piso sin aprobación | 0 (U-18) |
| Ofertas sobre el tope regulatorio | 0 (U-24) |
| Brecha con la competencia por celda | Informativo |

<!-- CATALOGO:INICIO PRC-P8 -->
## Catálogo de requisitos · Seguimiento de precios

> Bloque generado desde `catalogo/prc-p8.yaml` (6 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Pricing Analítico v1.0 (nuevo, 2026-10-17).

### 1 · Tablero de seguimiento

#### 1.1 Indicadores

- **`PRC-P8-01.01.01`** Construir el tablero mensual: conversión por tramo de precio, price realization, margen y RAROC realizados vs. esperados, mix de riesgo de lo colocado, excepciones de precio y margen cedido, brecha con la competencia y cumplimiento de topes.

  Aplica: Tier I–IV · Esfuerzo: 3 d · Automatización: 3 · Crítico · Entregable: Dashboard P1: Seguimiento de precios · Hito: Sprint 7

#### 1.2 Descomposición de resultados

- **`PRC-P8-01.02.01`** Descomponer cada mes la variación del margen en efecto precio, efecto volumen, efecto mix (riesgo, plazo, canal) y efecto costo de fondos, para atribuir resultados a la estrategia de precios y no al mercado.

  Aplica: Tier I–III · Esfuerzo: 1.5 d · Automatización: 3 · Entregable: Dashboard P1: Seguimiento de precios

#### 1.3 Alertas

- **`PRC-P8-01.03.01`** Activar alertas: margen realizado fuera de ±15 % del esperado por dos meses (U-26), excepciones por encima del umbral de leakage (U-23), deriva de la elasticidad (calibración del modelo de respuesta fuera de U-21) y cualquier oferta sobre el tope regulatorio (U-24).

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 3 · Crítico · Entregable: Dashboard P1: Seguimiento de precios · Umbrales: U-21, U-23, U-26

### 2 · Revisión post-implementación

#### 2.1 Revisión

- **`PRC-P8-02.01.01`** Revisión post-implementación entre 3 y 6 meses después del lanzamiento: valor capturado frente al caso de negocio de P1, aprendizajes y decisión de recalibrar el precio técnico, el modelo de respuesta o ambos.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 2 · Entregable: Documento P8: Revisión post-implementación

- **`PRC-P8-02.01.02`** Reunión de revisión post-implementación con el dueño del precio y Finanzas.

  Aplica: Tier I–IV · Esfuerzo: 0.25 d · Automatización: 1 · Entregable: Acta PRC-PIR: Revisión post-implementación

#### 2.2 Ciclo de recalibrado

- **`PRC-P8-02.02.01`** Actualizar los insumos del precio técnico cuando cambian FTP, costos, capital o PD/LGD (al menos trimestralmente), y recalibrar el modelo de respuesta al menos una vez al año o ante alerta.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 3 · Entregable: Excel P2: Calculadora de precio técnico

<!-- CATALOGO:FIN -->

## P9 · Gobierno, conducta y regulación

### Comité de Precios

Aprueba tarifarios, pisos, matrices de facultades, experimentos y excepciones a umbrales de pricing.
Lo integran el dueño del precio, Finanzas/ALM, Riesgos y Cumplimiento, con Analytics Pricing como secretaría
técnica. Cada sesión deja acta (tipo **PRC-CP** del [editor de actas](../plantillas/acta-de-reunion.md)).

### Marco regulatorio y de conducta

- **Topes de tasa** donde la regulación los fije. Por ejemplo, en Perú el BCRP fija tasas máximas para
  ciertos créditos de consumo y pequeña empresa. **Verificar la norma y los valores vigentes** antes de cada
  revisión de tarifario. El motor los controla en forma preventiva (U-24).
- **Transparencia:** cálculo y publicación de la TCEA (créditos) y la TREA (depósitos), y comunicación
  anticipada de cambios de condiciones, según la normativa de transparencia del supervisor local.
- **Trato justo:** el precio se explica por riesgo, costo, plazo, canal y relación comercial. Está prohibido
  usar como palanca la baja sensibilidad de clientes vulnerables. Se prueban proxies de atributos protegidos
  como en [FR-06](../frontera/equidad-y-sesgo.md) (PRC-P9-02.02.01).
- **Modelos de pricing = modelos:** precio técnico, respuesta y optimizador se inventarían, se asignan a un
  Tier y se validan (ámbito VAL-P de [Validación](../validacion/validacion.md)).

<!-- CATALOGO:INICIO PRC-P9 -->
## Catálogo de requisitos · Gobierno, conducta y regulación de precios

> Bloque generado desde `catalogo/prc-p9.yaml` (6 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Pricing Analítico v1.0 (nuevo, 2026-10-17).

### 1 · Gobierno de precios

#### 1.1 Comité de Precios

- **`PRC-P9-01.01.01`** Operar un Comité de Precios con mandato escrito: aprueba tarifarios, pisos, matrices de facultades, experimentos y excepciones a umbrales de pricing. Integra al dueño del precio, Finanzas/ALM, Riesgos y Cumplimiento; cada sesión deja acta (PRC-CP).

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 1 · Crítico · Entregable: Documento P9: Política de precios y conducta

#### 1.2 Política de precios

- **`PRC-P9-01.02.01`** Mantener una política de precios aprobada que establezca principios, metodología de piso técnico, gradualidad, facultades, uso de modelos y de agentes de IA, y frecuencia de revisión.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 1 · Entregable: Documento P9: Política de precios y conducta

### 2 · Conducta y regulación

#### 2.1 Cumplimiento regulatorio

- **`PRC-P9-02.01.01`** Verificar el cumplimiento de la normativa vigente de tasas y transparencia: topes de tasa donde existan (U-24), cálculo y publicación de TCEA/TREA, comunicación de cambios de condiciones con la anticipación exigida y prohibición de cobros no permitidos.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 2 · Crítico · Entregable: Documento P9: Política de precios y conducta · Umbrales: U-24

#### 2.2 Trato justo

- **`PRC-P9-02.02.01`** Asegurar que el precio se explique por riesgo, costo, plazo, canal y relación comercial, y no por atributos protegidos o por la vulnerabilidad del cliente. Prohibido usar como palanca de precio la baja sensibilidad de clientes vulnerables (p.ej. menor alfabetización financiera). Probar proxies como en FR-06.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 2 · Crítico · Entregable: Documento P9: Política de precios y conducta

#### 2.3 Explicabilidad al cliente

- **`PRC-P9-02.03.01`** Poder explicar a un cliente, a un ejecutivo o al supervisor por qué una oferta tiene ese precio, a partir de los componentes del piso técnico y de los ajustes comerciales registrados.

  Aplica: Tier I–II · Esfuerzo: 1 d · Automatización: 2 · Entregable: Documento P9: Política de precios y conducta

### 3 · Agentes de IA en pricing

#### 3.1 Controles

- **`PRC-P9-03.01.01`** Si se usan agentes de IA en el ciclo de pricing, registrar cada agente (rol, herramientas permitidas, datos a los que accede), conservar el log de sus acciones y asegurar que ningún agente fije, publique ni apruebe precios: toda decisión de precio la toma y firma una persona con facultad.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 2 · Crítico · Entregable: Documento P9: Política de precios y conducta

<!-- CATALOGO:FIN -->
