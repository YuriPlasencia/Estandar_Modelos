---
id: DES-D5
titulo: "D5 · Integración a la gestión"
estandar: Desarrollo
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 14
---

# D5 · Integración a la gestión

## Objetivo

Traducir el modelo en **decisiones y valor**: puntos de corte e impacto cuantificado en el negocio, el riesgo
y los estados financieros. Un modelo sin esta fase no está listo para comité.

## Impactos a evaluar

| Impacto | Métrica típica | Evidencia |
|---|---|---|
| Punto de corte | Curvas de sensibilidad / especificidad por segmento | Excel |
| Cobertura (leads) | Variación de aprobados; errores tipo I y II | Excel 20 |
| Indicadores de riesgo | Mora de cosecha esperada | Excel 20 |
| Pricing | Sólo estimadores de ingresos | Excel 20 |
| Provisiones | Provisión / saldo, provisión / margen | Excel 20 |
| Capital económico | Variación del capital asignado | Correo 1 |
| IFRS 9 | Impacto en pérdida esperada | Correo 2 |

El desarrollo, la calibración o el ajuste **deben coordinarse con los modelos PD / LGD / EAD** para armonizar
criterios y supuestos (DES-D5-01.02.07).

Para **estimadores**, se acuerda con el equipo de seguimiento la **muestra mínima mensual** de ingresos/ventas
reales por estrato necesaria para un seguimiento confiable (DES-D5-01.03.01).

<!-- CATALOGO:INICIO DES-D5 -->
## Catálogo de requisitos · Integración a la gestión

> Bloque generado desde `catalogo/des-d5.yaml` (11 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Desarrollo v1.0.

### 1 · Evaluación de Impactos

#### 1.1 Definición de punto de corte teórico

- **`DES-D5-01.01.01`** Definición de punto de corte teórico / segmentos

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 3 · Entregable: Excel: Curvas de especificidad y sensibilidad. · Hito: Sprint 18

- **`DES-D5-01.01.02`** Definir la política de forzajes (overrides): quién puede forzar, motivos válidos, registro obligatorio y límite de materialidad; el seguimiento medirá su volumen y desempeño (U-36).

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 1 · Crítico · Umbrales: U-36 · Nota: Línea base 2.0 (2026-10-17). Res. SBS 00053-2023 arts. 19 y 22.

#### 1.2 Evaluación de impactos en el negocio y valorización de ganancias del modelo

- **`DES-D5-01.02.01`** Impacto en variación de leads (cobertura).

  Aplica: Lineal/ML/Árbol I · ACP I–IV · Esfuerzo: 1.5–2 d ágil / 2–3 d completo · Automatización: -1 · Entregable: Excel 20: Análisis de Impactos en error tipo I y II · Hito: SME 11

- **`DES-D5-01.02.02`** Impacto en los indicadores de riesgo según tipo modelo (ej. Cosecha mora)

  Aplica: Lineal/ML/Árbol I · Esfuerzo: 1.5–2 d ágil / 2–3 d completo · Automatización: -1 · Entregable: Excel 20: Análisis de Impactos en error tipo I y II

- **`DES-D5-01.02.03`** Impacto en pricing (solo para estimadores de ingresos).

  Aplica: Lineal/ML/Árbol I–IV · Esfuerzo: 1.5 d ágil / 2 d completo · Automatización: 0 · Entregable: Excel 20: Análisis de Impactos en Pricing.

- **`DES-D5-01.02.04`** Impacto en provisiones. (provisión/saldo, provisión/margen)

  Aplica: Todos los tipos, Tier I–II · Esfuerzo: 1.5 d ágil / 2 d completo · Automatización: 0 · Entregable: Excel 20: Análisis de Impactos en provisiones.

- **`DES-D5-01.02.05`** Impacto en asignación de capital económico.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Correo 1: Impactos en CE.

- **`DES-D5-01.02.06`** Impacto en IFRS.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Correo 2: Impactos en IFRS. · Hito: SME 12

- **`DES-D5-01.02.07`** Coordinar la construcción/ calibración/ ajuste con PD/ LGD/ EAD, armonizando los crieterios y/o supuestos

  Aplica: Lineal/ML/Árbol I–IV · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Correo 2: Impactos en IFRS.

#### 1.3 (estimadores) Definición de muestra mínima de ingresos/ventas reales para el seguimiento

- **`DES-D5-01.03.01`** Coordinar con el equipo de seguimiento la muestra mínima de ingresos/ventas por estratos que serán necesarias mensualmente para asegurar la confiabilidad del seguimiento de cada modelo de estimador. Esta será compartida al usuario encargado de disponibilizar la información.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Documentacion metodológica y de implementación · Hito: Sprint 19

- **`DES-D5-01.03.02`** ñ

  Aplica: Todos los tipos, Tier I–IV

<!-- CATALOGO:FIN -->
