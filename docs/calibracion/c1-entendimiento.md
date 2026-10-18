---
id: CAL-C1
titulo: "Calibración · C1–C3 Entendimiento, datos y segmentación"
estandar: Calibración
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 20
---

# Calibración · C1–C3 Entendimiento, datos y segmentación

## Cuándo se calibra

Una calibración corrige el **nivel** (y, si se incorporan drivers, parte del ordenamiento) de un modelo vigente
cuando el seguimiento muestra **descalibración** pero el poder discriminante sigue siendo aceptable. Si el
ordenamiento se ha degradado, corresponde **redesarrollar** (estándar de Desarrollo).

Supuesto de la estimación de esfuerzo: se usa la **base de seguimiento como base de calibración**.
Duración de referencia del proyecto de calibración: <!--DUR:proyecto:Calibración-->≈ 3.3 semanas (Tier I), ≈ 3.1 semanas (Tier II), ≈ 2.4 semanas (Tier III) con 2 personas<!--/DUR-->.

## C1 · Entendimiento

- Entender el modelo actual, su uso y su **status de descalibración**.
- Alinear universo y target con la metodología corporativa, o justificar la desviación.
- Para **segmentos definidos por otros equipos**: revisar su sentido funcional con gerencia, decidir si la
  asignación es única o múltiple con evidencias, y solicitar los archivos de trabajo de los criterios.
- Pedir las bases de seguimiento / universo, los drivers descalibrados identificados por seguimiento y los
  drivers propuestos por negocio o por la pauta actual.
- Analizar **cambios y quiebres poblacionales** y la pauta vigente.

<!-- CATALOGO:INICIO CAL-C1 -->
## Catálogo de requisitos · Entendimiento

> Bloque generado desde `catalogo/cal-c1.yaml` (12 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Calibración v1.0.

### 1 · Definición del objetivo del calibrado

#### 1.1 Entendimiento del modelo y usos

- **`CAL-C1-01.01.01`** Entendimiento del modelo actual

  Aplica: Tier I–III · Esfuerzo: 1 d

- **`CAL-C1-01.01.02`** Entendimiento del uso

  Aplica: Tier I–III · Esfuerzo: 0.5 d

- **`CAL-C1-01.01.03`** Status descalibrado del modelo

  Aplica: Tier I–III · Esfuerzo: 0.5 d

- **`CAL-C1-01.01.04`** En el caso se utilice una metodología corporativa para la calibración, se debe alienar las principales definiciones a utilizar en el modelamiento (Universo y Target). En caso no aplique, se debería justificar el cambio en las definiciones con análisis metodológicos y/o de negocio.

  Aplica: Tier I–III · Esfuerzo: 0.5 d

- **`CAL-C1-01.01.05`** Para la inclusión de segmentos definidos por otros equipos:
  - Revision del sentido funcional de los ejes propuestas con la gerencia.
  - Evaluación en función de los resultados de la revisión, si la asignación del segmento será única o múltiple, solicitar las evidencias y respaldos de esto.
  - Solicitud archivos de trabajo sobre los criterios definidos.

  Aplica: Tier I–III · Esfuerzo: 2 d

- **`CAL-C1-01.01.06`** Dependiendo de la necesidad del proyecto de calibración, para el caso en el que se requiere de alguna acción para estimar impactos coyunturales en la cartera y el uso de estos:  
  Listar y Evaluar con la gerencia y usuarios, alternativas que no requieran aplicar medidas directas en los resultados de los modelos.

  Aplica: Tier I–III · Esfuerzo: 2 d

- **`CAL-C1-01.01.07`** Documentar por qué se calibra y no se redesarrolla: discriminación vigente aceptable y descalibración como causa principal, según el árbol de decisión de Seguimiento (SEG-S3-01.01.01).

  Aplica: Tier I–III · Esfuerzo: 0.5 d · Automatización: 1 · Crítico · Nota: Línea base 2.0 (2026-10-17). Práctica de bancos de referencia.

#### 1.2 Petición y elaboración de la base universo y filtros básicos (todas estas actividades asumen la disponibilidad de la data input)

- **`CAL-C1-01.02.01`** Petición de bases de seguimiento / universo

  Aplica: Tier I–III · Esfuerzo: 0.5 d

- **`CAL-C1-01.02.02`** Elaboración de los principales drivers descalibrados proporcionados por seguimiento

  Aplica: Tier I–II · Esfuerzo: 0.5 d

- **`CAL-C1-01.02.03`** Elaboración de posibles drivers de calibrado proporcionado por los stakeholders del negocio / Pauta actual

  Aplica: Tier I–II · Esfuerzo: 0.5 d

### 2 · Población y Pauta actual

#### 2.1 Análisis de la población y pauta actual

- **`CAL-C1-02.01.01`** Análisis de los cambios poblacionales / quiebres de población

  Aplica: Tier I–III · Esfuerzo: 0.5 d

- **`CAL-C1-02.01.02`** Conocimiento de las pauta actual

  Aplica: Tier I–II · Esfuerzo: 0.5 d

<!-- CATALOGO:FIN -->

## C2 · Preparación y calidad de datos

- **Cuadrar** la base con los informes de seguimiento (total mensual, tasa de default mensual y PD actual mensual).
- Duplicados, descriptivos de drivers candidatos (global y mensual) y contraste con negocio.
- Propuesta inicial de cambio de nivel y **Kick off** con el área solicitante (con acta).

<!-- CATALOGO:INICIO CAL-C2 -->
## Catálogo de requisitos · Preparación y calidad de datos

> Bloque generado desde `catalogo/cal-c2.yaml` (8 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Calibración v1.0.

### 1 · Control de Calidad y entendimiento de los datos

#### 1.1 Análisis de completitud y unicidad

- **`CAL-C2-01.01.01`** Cuadre de la infromación con los informes de seguimeinto (Total mensual, rd mensual y pd actual mensual)

  Aplica: Tier I–III · Esfuerzo: 0.5 d

- **`CAL-C2-01.01.02`** % de registros duplicados

  Aplica: Tier I–III · Esfuerzo: 0.5 d

- **`CAL-C2-01.01.03`** Análisis descriptivo de los posibles drivers de calibrado (global y mensual)

  Aplica: Tier I–III · Esfuerzo: 0.5 d

- **`CAL-C2-01.01.04`** Comparación de descriptivos de la base de datos con información de negocio

  Aplica: Tier I–III · Esfuerzo: 0.5 d

- **`CAL-C2-01.01.05`** Propuesta inicial de cambio de nivel en el modelo (generico)

  Aplica: Tier I–II · Esfuerzo: 1 d

#### 1.2 Análisis previos al kick off

- **`CAL-C2-01.02.01`** Elaboración de la PPT

  Aplica: Tier I–II · Esfuerzo: 0.5 d

### 2 · Reunión Kick off

#### 2.1 Reunión Kick off

- **`CAL-C2-02.01.01`** Reunión kick off  
  (Se tiene que convocar al area Solicitante)

  Aplica: Tier I–II · Esfuerzo: 0.5 d

- **`CAL-C2-02.01.02`** Acta de la reunión

  Aplica: Tier I–II · Esfuerzo: 0.5 d

<!-- CATALOGO:FIN -->

## C3 · Segmentación

Tasa de default y materialidad de los segmentos candidatos, y performance del modelo actual por segmento
en los **12 últimos meses con desempeño** (o según disponibilidad).

<!-- CATALOGO:INICIO CAL-C3 -->
## Catálogo de requisitos · Segmentación

> Bloque generado desde `catalogo/cal-c3.yaml` (2 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Calibración v1.0.

### 1 · Segmentación

#### 1.1 Segmentación a probar

- **`CAL-C3-01.01.01`** Análisis de ratio de default y materialidad para posibles segmentos de calibrado

  Aplica: Tier I–II · Esfuerzo: 0.5 d

- **`CAL-C3-01.01.02`** Performance del modelo actual según los los segmentos para el calibrado (12 ulitmos meses con desempeño y/o según disponibilidad de información)

  Aplica: Tier I–II · Esfuerzo: 0.5 d

<!-- CATALOGO:FIN -->
