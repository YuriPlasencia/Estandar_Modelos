---
id: DES-D2
titulo: "D2 · Preparación, calidad y entendimiento de los datos"
estandar: Desarrollo
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 11
---

# D2 · Preparación, calidad y entendimiento de los datos

## Objetivo

Certificar que los datos son **válidos, completos, únicos, precisos y consistentes** antes de modelar.
El resultado es la *certificación de calidad de datos* (Documento 6): sin ella no se avanza a D3/D4.

## Dimensiones de calidad evaluadas

| Dimensión | Pregunta | Evidencia |
|---|---|---|
| Documental | ¿Existe diccionario de datos e informe de calidad del proveedor? | Excel 4, Documento 5 |
| Validez | ¿Lo recibido coincide con la petición formal? | — |
| Completitud | ¿Qué % de registros están vacíos, sólo con llaves o sin target? ¿Cuál es el *fill rate* por variable, total y mensual? ¿Es estable en el tiempo (Mann–Kendall)? | Script 5, Excel 5 |
| Unicidad | ¿Hay duplicados? | Script 6 |
| Descriptiva | Máx., mín., media, mediana, percentiles; estabilidad PSI incluyendo meses recientes (U-02) | Excel 6 |
| Precisión | ¿Los descriptivos cuadran con la información de negocio? | Excel 7 |
| Consistencia | ¿Hay coherencia interna y externa con criterios funcionales y de segmentación? | Script 7 |

## Criterios de aceptación

- Variables con PSI > 10 % (o > 20 % en excepción justificada) quedan fuera del set candidato (U-02).
- Toda incidencia de calidad queda documentada con su decisión (usar, corregir, excluir).
- Documento 6 firmado por el líder del proyecto.

<!-- CATALOGO:INICIO DES-D2 -->
## Catálogo de requisitos · Preparación, calidad y entendimiento de los datos

> Bloque generado desde `catalogo/des-d2.yaml` (18 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Desarrollo v1.0.

### 1 · Revisión documental y control review

#### 1.1 Revisión del diccionario de datos

- **`DES-D2-01.01.01`** Garantizar la existencia de un diccionario de datos sobre la base disponible

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0 d ágil / 0 d trad. · Automatización: 1 · Entregable: Excel 4: Diccionario de datos. · Hito: Sprint 6

#### 1.2 Revisión del reporte de calidad de datos del proveedor

- **`DES-D2-01.02.01`** Revisar detalladamente el informe de calidad de datos entregado por el proveedor de información

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1 · Entregable: Documento 5: Informe de calidad de datos.

#### 1.3 Análisis de validez

- **`DES-D2-01.03.01`** Comparar información recibida con la petición formal de información

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1

#### 1.4 Análisis de completitud

- **`DES-D2-01.04.01`** % de registros sin ninguna información

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1 d ágil / 1 d trad. · Automatización: 1 · Entregable: Script 5: Análisis de completitud: Registros sin información.

- **`DES-D2-01.04.02`** % de registros sólo con información de llaves

  Aplica: Todos los tipos, Tier I–IV · Automatización: 1 · Entregable: Script 5: Análisis de completitud: Análisis de registros con solo información de llaves.

- **`DES-D2-01.04.03`** % de registros sin información de la variable target (total)

  Aplica: Todos los tipos, Tier I–IV · Automatización: 1 · Entregable: Script 5: Análisis de completitud: Análisis de registros sin la variable target.

- **`DES-D2-01.04.04`** % de registros sin información de la variable target (mensual)

  Aplica: Todos los tipos, Tier I–II · Automatización: 1 · Entregable: Script 5: Análisis de completitud: Análisis de registros sin la variable target mensual.

- **`DES-D2-01.04.05`** % de datos faltantes por variable independiente (total)

  Aplica: Todos los tipos, Tier I–IV · Automatización: 1 · Entregable: Excel 5: Fill Rate (total).

- **`DES-D2-01.04.06`** % de datos faltantes por variable independiente (mensual)

  Aplica: Todos los tipos, Tier I–II · Automatización: 1 · Entregable: Excel 5: Fill Rate (mensual).

- **`DES-D2-01.04.07`** Análisis de estabilidad de valores faltantes en cada variable

  Aplica: Todos los tipos, Tier I–II · Automatización: 1 · Entregable: Excel 5: Resultados del test de Mann-Kendall de tendencia para % de missing por mes.

#### 1.5 Análisis de Unicidad

- **`DES-D2-01.05.01`** % de registros duplicados

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1 · Entregable: Script 6: Análisis de unicidad.

#### 1.6 Análisis descriptivo de variables

- **`DES-D2-01.06.01`** Análisis descriptivo de todas las variables (automático)

  Aplica: Todos los tipos, Tier I–II · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1 · Entregable: Excel 6: Análisis descriptivo de variables: Máximo, mínimo, promedio, mediana, percentiles.

- **`DES-D2-01.06.02`** Análisis descriptivo de las variables definidas como mínimas

  Aplica: Lineal/Árbol I–II · ML I–IV · ACP III–IV · Automatización: 1 · Entregable: Excel 6: Análisis descriptivo de variables: Máximo, mínimo, promedio, mediana, percentiles.

- **`DES-D2-01.06.03`** Análisis de estabilidad de las variables a través del PSI (incluyendo meses recientes) con un umbral minimo de aceptación del 10%; en caso dicho nivel reduzca considerablemente el set disponible de variables para el modelamiento se evaluará un nivel de aceptación mayor que no supere el 20%.

  Aplica: Lineal/Árbol I–II · ML/ACP I–IV · Automatización: 1 · Entregable: Excel 6: Analisis de estabilidad · Umbrales: U-02

### 2 · Control de Calidad y entendimiento de los datos

#### 2.1 Análisis de Precisión

- **`DES-D2-02.01.01`** Comparación de descriptivos de la base de datos con información de negocio

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1 · Entregable: Excel 7: Comparación de evolutivos con datos del negocio.

#### 2.2 Análisis de consistencia

- **`DES-D2-02.02.01`** Consistencia y coherencia interna y externa con criterios funcionales o de negocio (criterios y def de segmentación)

  Aplica: Todos los tipos, Tier I–II · Esfuerzo: 1.4875 d ágil / 1.75 d trad. · Automatización: 1 · Entregable: Script 7: Analisis de consistencia: Criterios funcionales y de negocio.

#### 2.3 Reporte final de caildad de datos

- **`DES-D2-02.03.01`** Revisión del conjunto de análisis y decisión sobre calidad de datos

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.5 d ágil / 0.5 d trad. · Automatización: 1

- **`DES-D2-02.03.02`** Documentación de los análisis y certificación de calidad

  Aplica: Todos los tipos, Tier I–IV · Automatización: 1 · Entregable: Documento 6: Analisis y certificación de calidad.

<!-- CATALOGO:FIN -->
