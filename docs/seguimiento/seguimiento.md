---
id: SEG
titulo: "Seguimiento (monitoreo) de modelos"
estandar: Seguimiento
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 35
---

# Seguimiento (monitoreo) de modelos

> **Línea base 2.0.** El seguimiento tiene catálogo propio (SEG-S1 a SEG-S4), alineado con la Res. SBS 00053-2023 (arts. 21–22) y con la
> práctica de los bancos de referencia: indicadores y umbrales aprobados por comité, seguimiento de forzajes,
> sobreajuste en IA, acciones gobernadas e informe al menos anual. Para precios, ver además
> [Pricing · P8](../pricing/p8-seguimiento-gobierno.md); para provisiones, [Parámetros · R9](../parametros/r9-backtesting-clv.md).

## Qué se mide

| Familia | Indicador | Periodicidad | Umbral |
|---|---|---|---|
| Estabilidad | PSI del score y de cada variable | Mensual | U-37 (verde ≤ 10 %, rojo > 25 %) |
| Discriminación | Gini y KS por cosecha madura, global y por segmento | Mensual o trimestral | U-37 (rojo: caída > 10 pts) |
| Calibración | Tasa observada vs. PD por tramo (binomial o Jeffreys); estimadores con ±25 %/±50 % | Trimestral | U-37, U-12 |
| Uso | Volumen y desempeño de los forzajes; uso solo para el propósito aprobado | Mensual | U-36 |
| IA | Sobreajuste en producción (construcción vs. meses recientes) | Trimestral | Según el plan aprobado |
| Datos | Fill rate, duplicados, frescura de fuentes externas | Cada ejecución | Cualquier fallo es rojo |

## Qué se hace ante una alerta

```text
Verde ─▶ continuar
Ámbar ─▶ análisis de causa raíz (drivers, mix, pauta) en ≤ 1 mes
Rojo en calibración, discriminación aceptable ─▶ CALIBRACIÓN (estándar CAL)
Rojo en discriminación ─▶ REDESARROLLO (estándar DES)
Rojo en datos ─▶ plan de contingencia del Documento de Lineamientos (IMP-01.02.01)
Rojo persistente 3 períodos o cambio material de política/población ─▶ comité de riesgos de modelo + mitigación temporal
```

## Requisitos heredados de otros estándares

| Requisito | Origen |
|---|---|
| Reporte de seguimiento preparado en el desarrollo | DES-D4-09.01.02 |
| Muestra mínima mensual para estimadores | DES-D5-01.03.01 |
| Política de forzajes definida antes del uso | DES-D5-01.01.02 |
| Controles de PSI, unicidad y missing en producción | IMP-01.04.01, IMP-01.04.02 |
| Versión del modelo registrada en cada resultado | IMP-01.06.06 |
| La calibración parte de la base de seguimiento | CAL-C1-01.02.01, CAL-C1-01.02.02 |

<!-- CATALOGO:INICIO SEG-S1 -->
## Catálogo de requisitos · Diseño del seguimiento

> Bloque generado desde `catalogo/seg-s1.yaml` (3 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Línea base 2.0 (2026-10-17): consolidación de requisitos vigentes, Res. SBS 00053-2023 y práctica de bancos de referencia.

### 1 · Plan de seguimiento

#### 1.1 Indicadores y umbrales

- **`SEG-S1-01.01.01`** Definir para cada modelo los indicadores de seguimiento (estabilidad, discriminación, calibración, forzajes, calidad de datos y, para IA, sobreajuste) con umbrales y alertas aprobados por el comité de riesgos de modelo (SBS art. 21; U-37).

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 2 · Crítico · Entregable: Documento S1: Plan de seguimiento · Hito: Sprint 0 · Umbrales: U-37

- **`SEG-S1-01.01.02`** Fijar la periodicidad por categoría (Tier I mensual o trimestral; Tier III–IV al menos semestral) y la fecha en que cada cosecha madura lo suficiente para medir desempeño.

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 1 · Entregable: Documento S1: Plan de seguimiento

- **`SEG-S1-01.01.03`** Asegurar los datos de seguimiento: tabla productiva con versión del modelo, scores, decisiones, forzajes y desempeño posterior; para estimadores, la muestra mínima acordada en DES-D5-01.03.01.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Tabla S1: Base de seguimiento

<!-- CATALOGO:FIN -->

<!-- CATALOGO:INICIO SEG-S2 -->
## Catálogo de requisitos · Ejecución del seguimiento

> Bloque generado desde `catalogo/seg-s2.yaml` (6 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Línea base 2.0 (2026-10-17): consolidación de requisitos vigentes, Res. SBS 00053-2023 y práctica de bancos de referencia.

### 1 · Indicadores

#### 1.1 Estabilidad y datos

- **`SEG-S2-01.01.01`** Medir el PSI del score y de cada variable frente a la población de construcción, y los controles de calidad de los datos productivos (missings, duplicados, fuentes desactualizadas).

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 4 · Crítico · Entregable: Dashboard S1: Tablero de seguimiento

#### 1.2 Desempeño

- **`SEG-S2-01.02.01`** Medir la discriminación (Gini, KS) por cosecha madura, global y por segmento, frente a la de construcción (U-37).

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 4 · Crítico · Entregable: Dashboard S1: Tablero de seguimiento · Umbrales: U-37

- **`SEG-S2-01.02.02`** Medir la calibración: tasa observada vs. PD por tramo con intervalos binomiales o de Jeffreys; para estimadores, el % de casos dentro de ±25 % y ±50 % (U-12).

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 4 · Crítico · Entregable: Dashboard S1: Tablero de seguimiento

- **`SEG-S2-01.02.03`** Para modelos de IA, medir el sobreajuste en producción: brecha de desempeño entre construcción y los meses recientes (SBS art. 22).

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 3 · Entregable: Dashboard S1: Tablero de seguimiento

#### 1.3 Uso y forzajes

- **`SEG-S2-01.03.01`** Medir el volumen de forzajes (overrides) y el desempeño de los casos forzados frente a los no forzados, por motivo y por nivel que forzó (U-36).

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 3 · Crítico · Entregable: Dashboard S1: Tablero de seguimiento · Umbrales: U-36

- **`SEG-S2-01.03.02`** Verificar que el modelo se usa solo para el propósito y la población aprobados; un uso nuevo es un cambio de uso que requiere aprobación (GOB-G3-01.01.01).

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 1 · Crítico

<!-- CATALOGO:FIN -->

<!-- CATALOGO:INICIO SEG-S3 -->
## Catálogo de requisitos · Acciones ante alertas

> Bloque generado desde `catalogo/seg-s3.yaml` (2 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Línea base 2.0 (2026-10-17): consolidación de requisitos vigentes, Res. SBS 00053-2023 y práctica de bancos de referencia.

### 1 · Respuesta

#### 1.1 Árbol de decisión

- **`SEG-S3-01.01.01`** Aplicar el árbol de decisión: verde, continuar; ámbar, análisis de causa raíz en un mes; rojo en calibración con discriminación aceptable, calibrar (CAL); rojo en discriminación, redesarrollar (DES); rojo en datos, plan de contingencia (IMP-01.02.01).

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 1 · Crítico · Entregable: Documento S2: Informe de seguimiento

- **`SEG-S3-01.01.02`** Escalar al comité un rojo que persista tres períodos o un cambio material de política o de población, con medidas temporales de mitigación mientras se corrige (SBS art. 7).

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 1 · Crítico · Entregable: Acta CRM: Comité de riesgos de modelo

<!-- CATALOGO:FIN -->

<!-- CATALOGO:INICIO SEG-S4 -->
## Catálogo de requisitos · Reporte del seguimiento

> Bloque generado desde `catalogo/seg-s4.yaml` (2 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Línea base 2.0 (2026-10-17): consolidación de requisitos vigentes, Res. SBS 00053-2023 y práctica de bancos de referencia.

### 1 · Informes

#### 1.1 Informe periódico

- **`SEG-S4-01.01.01`** Emitir el informe de seguimiento al menos una vez al año (más frecuente según categoría) con desviaciones de indicadores, backtesting, sensibilidad, forzajes, cumplimiento de acciones y, para IA, sobreajuste; aprobarlo en el comité (SBS art. 22).

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Documento S2: Informe de seguimiento

- **`SEG-S4-01.01.02`** Actualizar el inventario con el estado del modelo y sus debilidades abiertas después de cada informe (GOB-G2-01.01.01).

  Aplica: Tier I–IV · Esfuerzo: 0.25 d · Automatización: 2

<!-- CATALOGO:FIN -->

## Frontera *(propuesta)*

Ver [FR-05 · Monitoreo de drift moderno](../frontera/monitoreo-drift.md): Jensen–Shannon y Wasserstein además del
PSI, validación adversarial y estimación de desempeño sin etiquetas mientras maduran las cosechas.
