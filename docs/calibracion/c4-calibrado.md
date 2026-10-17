---
id: CAL-C4
titulo: "Calibración · C4 Calibrado"
estandar: Calibración
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 21
---

# Calibración · C4 Calibrado

## Flujo iterativo

```text
Depuración de drivers (estabilidad, fill rate, quiebres, correlación)
   ─▶ Feature engineering (dummies, transformación toolkit, convoluciones)
   ─▶ Evaluación del score a calibrar (estabilidad y discriminación, ventanas)
   ─▶ Iteración 1 ─▶ Reunión preliminar 1 ─▶ Iteración 2 ─▶ Reunión preliminar 2   (Tier 1–2)
   ─▶ Calibrado final (drivers significativos, signos, bootstrap, migración, granularidad)
   ─▶ Tabla puntuada a seguimiento ─▶ Reunión de cierre con acta
```

## Reglas para incluir un driver de calibración

1. **Trameado** del driver por cortes recomendados o de interés de negocio.
2. Precisión de cada tramo con **intervalos de Vasicek** (ver [Glosario](../marco/glosario.md)):
   tramos en rojo deben incluirse en la calibración; los que estén en los límites se evalúan y aprueba gerencia (U-14).
3. **Significancia** de los coeficientes añadidos y **sentido económico** de los signos.
4. **Aporte marginal** a la discriminación del modelo.
5. Tratamiento de **missing y valores especiales** documentado.
6. Ejes de segmentación con materialidad ≤ 5 % se revisan con negocio y gerencia (U-13).

## Correlación

Pearson para continuas; V de Cramér, Spearman u otros para cualitativas. Superar el umbral es posible por
necesidad de negocio, con excepción documentada (CAL-C4-01.02.01).

## Ventanas

Para calibraciones con fases diferenciadas por ventana, se debe usar la información **más reciente y confiable**;
de lo contrario se documenta como **limitación** (CAL-C4-03.01.03).

<!-- CATALOGO:INICIO CAL-C4 -->
## Catálogo de requisitos · Calibrado

> Bloque generado desde `catalogo/cal-c4.yaml` (32 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Calibración v1.0.

### 1 · Depuración de variables

#### 1.1 Análisis de estabilidad y fill rate

- **`CAL-C4-01.01.01`** Análisis de tendencia de los posibles drivers de calibrado (estabilidad temporal)

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

- **`CAL-C4-01.01.02`** Análisis de porcentaje de casos poblados para los posibles drivers de calibrado

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

- **`CAL-C4-01.01.03`** Análisis de tendencias y quiebres

  Aplica: Tier I–II · Esfuerzo: 0.5 d

#### 1.2 Análisis Inicial de Correlación de Variables

- **`CAL-C4-01.02.01`** Análisis de la correlación de los drivers objeto de análisis, para el caso de variables continuas se medirá el indicador de correlación pearson, y para el caso de variables cualitativas se evaluaran diferentes indicador (V-Carmer, Spearman, etc), sin embargo en el caso de superar el umbral se pueden hacer excepciones según las necesidades del negocio.

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

### 2 · Feature Engineering

#### 2.1 Tratamiento de variables

- **`CAL-C4-02.01.01`** Transformación de variables: Evaluación de posibles transformaciones de las variables (Categorización Dummies, Transformación toolkie, sin transformación)

  Aplica: Tier I · Esfuerzo: 3 d

- **`CAL-C4-02.01.02`** Evaluación de convolución de variables

  Aplica: Tier I · Esfuerzo: 1 d

### 3 · Ejecución de calibración

#### 3.1 Modelo a Calibrar

- **`CAL-C4-03.01.01`** Evaluación de la estabilidad poblacional y del poder de discriminación del score a calibrarir, aplica tanto para los modelos base como para los modelos calibrados previamente

  Aplica: Tier I–IV · Esfuerzo: 3 d

- **`CAL-C4-03.01.02`** Evaluación de las ventanas de construcción de los componentes de la calibración, incluyendo al score base o score calibrado, verificando el performance actual para delimitar el uso de estos.

  Aplica: Tier I–IV

- **`CAL-C4-03.01.03`** Para calibraciones que contemplen fases diferenciadas por las ventanas de análisis, se debe de incluir la información más reciente y confiable, caso contario se debe de documentar como una limitación.

  Aplica: Tier I–IV

- **`CAL-C4-03.01.04`** Para la inclusion de los drivers:
  - Trameado (bucketización) del driver por cortes recomendados u objetos de interés de negocio.
  - Evaluación de la precisión por cada tramo o bucket según los intervalos de Vasicek.
  - Buckets que se encuentren en semáforo rojo deberán de incluirse en el proceso de calibración.
  - Buckets que se encuentren dentro de los límites rojos, deberán de evaluarse y aprobarse por la gerencia.
  - Verificación de la significancia de los coeficientes añadidos
  - Evaluación del aporte marginal en la discriminación del modelo por la inclusión de los drivers de calibración. Sin embargo, el tener un aporte muy bajo no será determinante para excluir el driver. Llevar discucion a la gerencia.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Umbrales: U-14

- **`CAL-C4-03.01.05`** Dependiendo del tipo de calibración e inclusión de los drivers:  
  Evaluación y esclarecimiento en la documentación el tratamiento de valores missing y especiales.

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

- **`CAL-C4-03.01.06`** Dependiendo de la necesidad del proyecto de calibración:
  - Evaluación de la materialidad de los ejes de segmentación, en el caso que no tengan materialidad superior a 5%, revisar la inclusión con los usuarios de negocio y la gerencia.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Umbrales: U-13

#### 3.2 Calibrado con drivers - 1era iteración

- **`CAL-C4-03.02.01`** Ejecución del calibrado para validar significancia e ingreso de los drivers del backlog al calibrado

  Aplica: Tier I–IV · Esfuerzo: 1.5 d

- **`CAL-C4-03.02.02`** Revisión por sentido económico

  Aplica: Tier I–IV · Esfuerzo: 1.5 d

- **`CAL-C4-03.02.03`** Análisis de correlación según el tipo de transformación de la variable.

  Aplica: Tier I–IV

- **`CAL-C4-03.02.04`** Matriz de migración / performance del modelo por driver / granularidad

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

- **`CAL-C4-03.02.05`** Entendimiento inicial de los resultados

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

#### 3.3 1era renión preliminar de resultados

- **`CAL-C4-03.03.01`** Reunión y elaboración de acta

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

#### 3.4 Calibrado con drivers - 2da iteración

- **`CAL-C4-03.04.01`** Ejecución del calibrado para validar significancia e ingreso de los drivers al calibrado

  Aplica: Tier I–II · Esfuerzo: 1.5 d

- **`CAL-C4-03.04.02`** Revisión por sentido económico

  Aplica: Tier I–II · Esfuerzo: 1.5 d

- **`CAL-C4-03.04.03`** Análisis de correlación según el tipo de transformación de la variable.

  Aplica: Tier I–IV

- **`CAL-C4-03.04.04`** Matriz de migración / performance del modelo por driver / granularidad

  Aplica: Tier I–II · Esfuerzo: 0.5 d

- **`CAL-C4-03.04.05`** Entendimiento inicial de los resultados

  Aplica: Tier I–II · Esfuerzo: 0.5 d

#### 3.5 2da reunión preliminar de resultados

- **`CAL-C4-03.05.01`** Reunión y elaboración de acta

  Aplica: Tier I–II · Esfuerzo: 0.5 d

### 4 · Calibrado final

#### 4.1 Ejecución del modelo final

- **`CAL-C4-04.01.01`** Selección de drivers significativos

  Aplica: Tier I–II · Esfuerzo: 1 d

- **`CAL-C4-04.01.02`** Conclusiones del sentido de los coeficientes.

  Aplica: Tier I–II · Esfuerzo: 1 d

- **`CAL-C4-04.01.03`** Ejecución final del calibrado

  Aplica: Tier I–IV · Esfuerzo: 1 d

- **`CAL-C4-04.01.04`** Bootstrap driver finales / Matriz de migración / performance del modelo por driver(general y mensual) / granularidad (rangos de pd, rangos de ventas)

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

- **`CAL-C4-04.01.05`** Envio de tabla puntuada al equipo de seguimiento

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

#### 4.2 Analisis previos a la reunión de cierre

- **`CAL-C4-04.02.01`** Elaboración de la PPT

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

### 5 · Reunión presentación del calibrado

#### 5.1 Reunión presentación de calibrado

- **`CAL-C4-05.01.01`** Reunión calibrado final

  Aplica: Tier I–IV · Esfuerzo: 0.5 d

- **`CAL-C4-05.01.02`** Acta del cirre del calibrado

  Aplica: Tier I–IV

<!-- CATALOGO:FIN -->
