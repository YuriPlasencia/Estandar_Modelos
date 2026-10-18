---
id: DES-D1
titulo: "D1 · Definición, alcance, diseño y extracción"
estandar: Desarrollo
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 10
---

# D1 · Definición, alcance, diseño y extracción

## Objetivo

Entender el problema de negocio, decidir si un modelo es la solución adecuada y fijar **qué se modela, sobre
quién y con qué datos**. Es, después de Modelamiento, la fase de mayor esfuerzo (<!--DUR:fase:DES-D1-->≈ 3.1–4.0 semanas con 2 personas<!--/DUR-->) porque aquí se
cierran las definiciones que, si cambian después, obligan a rehacer el modelo.

## Entradas

- Solicitud del área de negocio (caso de uso, necesidad, objetivo).
- Políticas de crédito actuales y anteriores; modelos vigentes o previos.
- Acceso a las fuentes (universo de cosechas, buró/RCC, tablones internos).

## Regla de no anticipación del tablón

El tablón de modelamiento se arma **solo con información del pasado** respecto de la fecha de observación
(originación en admisión, foto en comportamiento o buró). No se admiten variables contemporáneas ni del futuro,
porque el futuro no se observa al momento de decidir (U-39, DES-D1-01.03.04).

| Situación | ¿Admitida? |
|---|---|
| Atraso máximo de los 6 meses **previos** a la originación | Sí |
| Saldo del cierre del mes de la originación, si ese cierre es posterior a la fecha de decisión | No (contemporánea) |
| Marca de gestión de cobranza o refinanciación posterior a la observación | No (futura) |
| Variable de buró con desfase de 1 mes, usada con su fecha real de disponibilidad | Sí, documentando el desfase |

Cada variable registra en el diccionario su **fecha de referencia** y el **desfase de disponibilidad** de su fuente, y
una prueba automática verifica que ninguna usa información posterior (DES-D1-01.03.05).

## Decisiones que deben quedar cerradas al salir

1. **Población objetivo** y definición cosechas vs. aprobadas (Project Charter).
2. **Ventana histórica**: mínimo 12 meses Train/Test y, como OOT, solo el **último mes con desempeño completo** (U-01);
   estable según PSI (U-02) y sin quiebres de la tasa del target: si la tasa cambia más de 25 % relativo entre meses
   por una causa operativa, los meses previos al quiebre no se usan para entrenar (U-41, DES-D1-03.01.06).
3. **Exclusiones**: pautas duras, default en foto, desempeño incompleto, indeterminados y cambios de gestión — cada una con su análisis de materialidad (Documento 3).
4. **Default (binario)**: se adopta la definición del estándar (U-17, ver abajo). El proyecto documenta la unidad (cliente u operación) y la materialidad (Documento 4).
5. **Target (continuo)**, cuando aplique: altura, temporalidad y materialidad.
6. **Tier, uso, alcance, limitaciones y criterios de éxito (OKRs)** del modelo.
7. **Fecha de ejecución** considerando desfases de cada fuente.

## Criterios de aceptación

- Project Charter (PPT 1) completo y validado en Reunión 3.
- Kick off realizado con acta (Acta 3).
- Master table inicial (Tabla 1) y master table filtrada (Tabla 2) reproducibles desde scripts.
- Si se usa metodología corporativa, universo y target alineados o desviación justificada (DES-D1-01.04.06).

## Definición de default del estándar (U-17)

> **Default = atraso mayor a 60 días al menos una vez en los 12 meses siguientes a la fecha de observación.**

| Tipo de modelo | Fecha de observación | Población | Ventana de desempeño |
|---|---|---|---|
| **Admisión** (originación) | Fecha de otorgamiento del crédito | Créditos originados en la cosecha | 12 meses desde la originación |
| **Buró** (comportamiento de cliente) | Fecha de corte de la foto | Clientes activos en esa fecha | 12 meses desde la foto |

$$y_i=\mathbb{1}\left[\max_{t\in(t_0,\;t_0+12]}\ \text{días de atraso}_{i,t} > 60\right]$$

- Basta **una** ocurrencia en la ventana; no se exige que el atraso persista.
- Se excluyen las operaciones que **no completan los 12 meses** de desempeño (DES-D1-04.01.03) y los
  **indeterminados** (mora cercana pero menor a la altura de default), según DES-D1-04.01.05.
- En buró se excluye quien ya está en default en la foto (*default en foto*, DES-D1-04.01.02).
- Con 12 meses de desempeño, la última cosecha utilizable es la de hace 12 meses. Esto condiciona
  la ventana de modelamiento (U-01): el OOT es justamente esa cosecha, la última madura, y Train/Test son las
  anteriores.
- Cualquier variante (otra altura u otra ventana) es una desviación del estándar: se sustenta con roll rates y la
  curva acumulada de defaults, y se aprueba con acta.

## Análisis de soporte para la definición de default

El análisis de soporte contrasta, por segmento, las fuentes de default disponibles:

| Definición | Personas | Pyme | Mayorista |
|---|---|---|---|
| Default corporativo de la entidad | | | ✓ |
| Default en buró / RCC | ✓ | ✓ | |
| Clasificación regulatoria | ✓ (recomendado) | | |
| Días de atraso | ✓ | ✓ | ✓ |

Análisis que sustentan la decisión: matriz de coincidencias de default cliente–producto (cuántos defaults
adicionales agrega pasar a nivel cliente), distancia temporal entre defaults de productos, **roll rates**
para la altura (30-60-90-120 días), **curva acumulada de defaults** para la temporalidad, y monto fijo para la materialidad.

<!-- CATALOGO:INICIO DES-D1 -->
## Catálogo de requisitos · Definición, alcance, diseño y extracción

> Bloque generado desde `catalogo/des-d1.yaml` (57 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Desarrollo v1.0.

### 1 · Definición del objetivo del modelo

#### 1.1 Entendimiento del problema de negocio

- **`DES-D1-01.01.01`** Entendimiento origen del desarrollo (entendimiento del caso de uso, necesidad del negocio, objetivo del modelo)

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 2–2.125 d ágil / 2.5–3.5 d completo · Automatización: 1 · Hito: Sprint 0

- **`DES-D1-01.01.02`** Evaluar la factibilidad para la construcción del modelo, analizando materialidad (universo y target), impacto en la gestión, información disponible para el desarrollo y posible uso de modelos vigentes.

  Aplica: Todos los tipos, Tier I–III · Automatización: 1

- **`DES-D1-01.01.03`** Características de la población

  Aplica: Todos los tipos, Tier I–III · Automatización: 1

- **`DES-D1-01.01.04`** Políticas actuales y anteriores

  Aplica: Todos los tipos, Tier I–III · Automatización: 1

- **`DES-D1-01.01.05`** Modelos anteriores

  Aplica: Todos los tipos, Tier I–III · Automatización: 1

- **`DES-D1-01.01.06`** Información disponible (data disponible, data nueva)

  Aplica: Todos los tipos, Tier I–III · Automatización: 1

- **`DES-D1-01.01.07`** Definición de supuestos económicos que sustenten la racionalidad/sentido del modelo en su conjunto y de las variables

  Aplica: Todos los tipos, Tier I–III

- **`DES-D1-01.01.08`** Reunión de levantamiento de expectativas: Población objetivo/cosechas (exclusiones, inclusiones).

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1 · Crítico · Entregable: Acta 1: Reunión Levantamiento de Expectativas II. · Hito: Reunion 1

#### 1.2 Elaboración de la base universo y filtros básicos (todas estas actividades asumen la disponibilidad de la data input)

- **`DES-D1-01.02.01`** Elaboración de base universo

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 5 d ágil / 5 d completo · Automatización: 1 · Entregable: Correo 1: Petición de datos universo. · Hito: Sprint 1

- **`DES-D1-01.02.02`** Elaboración de evolutivos total por montos

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Excel 1: Evolutivos por montos, tabla y gráfico.

- **`DES-D1-01.02.03`** Elaboración de evolutivos por cuentas de principales drivers del negocio

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Excel 1: Evolutivos de cuentas por drivers, tablas y gráficos

- **`DES-D1-01.02.04`** Elaboración de evolutivos por montos de principales drivers del negocio

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Excel 1: Evolutivos de montos por drivers, tablas y gráficos

- **`DES-D1-01.02.05`** Análisis y validación de filtros básicos para el universo de modelamiento

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Script: de filtros básicos.; Excel 1: Número de cuentas antes y despues de filtrar.

#### 1.3 Extracción de tabla única y creación de nuevas variables

- **`DES-D1-01.03.01`** Reunión de levantamiento de expectativas: Fuentes, variables

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.25 d ágil / 0.25 d completo · Automatización: 1 · Crítico · Entregable: Acta 2: Reunión Levantamiento de Expectativas II. · Hito: Reunión 2

- **`DES-D1-01.03.02`** Pegado de las variables de los tablones

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 2.5–3 d ágil / 2.5–3 d completo · Automatización: 1 · Entregable: Script 2: Creación de tabla única; Tabla 1: Master table inicial. · Hito: Sprint 2*

- **`DES-D1-01.03.03`** Crear variables post BrainStorming

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 8.5 d ágil / 10 d completo · Automatización: 1 · Entregable: Script 3: Creación de nuevas variables. · Hito: SME 1

- **`DES-D1-01.03.04`** Regla de no anticipación: toda variable del tablón de modelamiento se construye solo con información disponible antes de la fecha de observación (originación o foto). Están prohibidas las variables contemporáneas o del futuro, porque en producción el futuro no se observa (U-39).

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 1 · Crítico · Entregable: Script 2: Creación de tabla única · Umbrales: U-39 · Nota: Línea base 2.1 (2026-10-17): criterio del custodio.

- **`DES-D1-01.03.05`** Documentar en el diccionario, para cada variable, su fecha de referencia y el desfase de disponibilidad de su fuente, y verificar con una prueba automática que ninguna variable usa información posterior a la fecha de observación menos ese desfase.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1 d ágil / 1.5 d completo · Automatización: 3 · Crítico · Entregable: Script 2: Creación de tabla única · Umbrales: U-39 · Nota: Línea base 2.1 (2026-10-17): criterio del custodio.

#### 1.4 Requerimientos y propuesta de solución (inception)

- **`DES-D1-01.04.01`** Definición población objetivo

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 2–2.55 d ágil / 2.5–3 d completo · Automatización: 1 · Entregable: Ppt 1: Project Charter: Población. · Hito: Sprint 3

- **`DES-D1-01.04.02`** Definiciones, criterios y supuestos

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Ppt 1: Project Charter: Definición cosechas vs Aprobadas.

- **`DES-D1-01.04.03`** Definiciones de criterios de éxito

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Ppt 1: Project Charter: OKRs.

- **`DES-D1-01.04.04`** Definición del TIER y uso del modelo

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Ppt 1: Project Charter: Definición del uso de modelo.

- **`DES-D1-01.04.05`** Definición de alcance y limitaciones

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Ppt 1: Project Charter: Definición de alcances, limitaciones.

- **`DES-D1-01.04.06`** En el caso se utilice una metodología corporativa, se debe alienar las principales definiciones a utilizar en el modelamiento (Universo y Target). En caso no aplique, se debería justificar el cambio en las definiciones con análisis metodológicos y/o de negocio.

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Ppt 1: Project Charter: Alineamiento Corporativo

- **`DES-D1-01.04.07`** Reunión - Enriquecimiento de la propuesta y diseño funcional del modelo

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Acta: de reunión. · Hito: Reunión 3

- **`DES-D1-01.04.08`** Documentación del project charter (ficha técnica del modelo, técnicas a usar y otros)

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Ppt 1: Project Charter · Hito: Sprint 4

#### 1.5 Sesión de ideación de variables

- **`DES-D1-01.05.01`** Reuniones con los usuarios/ bancas para revisar variables sugeridas por el negocio (ideación)

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 2 d ágil / 3 d completo · Automatización: 1 · Entregable: Acta: de reunión entre el equipo de modelos y los equipos de negocio

#### 1.6 Evaluación de la dispobilidad de información y accesos

- **`DES-D1-01.06.01`** Reuniones con los encargados de la extracción de información

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 2 d ágil / 3 d completo · Automatización: 1 · Entregable: Acta: de reunión entre el equipo de modelos y el equipo de tecnología y datos

#### 1.7 Definir fecha de ejecución del modelo, considerando los desfases a asumir por cada fuente utilizada y en función a las expectativas de los equipos Stakeholders

- **`DES-D1-01.07.01`** Reuniones con los encargados de la extracción de información y creación de variables

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 2 d ágil / 3 d completo · Automatización: 1 · Entregable: Acta: de reunión entre el equipo de modelos y el equipo de tecnología y datos

### 2 · Reunión Kick off

#### 2.1 Análisis pendientes previos al kick off

- **`DES-D1-02.01.01`** Presentación (PPT) del kick off

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1–2 d ágil / 1.5–3 d completo · Automatización: 1 · Entregable: Ppt 2: Kick off · Umbrales: U-40

#### 2.2 Reunión Kick off

- **`DES-D1-02.02.01`** Reunión kick off

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 1 · Crítico · Entregable: Acta 3: Reunión Kick off · Hito: Kick Off

### 3 · Definición de ventana de modelación

#### 3.1 Ventana Modelamiento - Definición de la ventana histórica de modelación

- **`DES-D1-03.01.01`** Análisis de estabilidad de la variable objetivo

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 2.975–3 d ágil / 3.5 d completo · Automatización: 1 · Entregable: Excel 2: Evolutivos de cuentas y montos por drivers. · Hito: Sprint 5

- **`DES-D1-03.01.02`** Selección de la ventana histórica de modelación, en caso de modelos de originación, comportamentales y cobranzas, considerar como mínimo 12 meses para el modelamiento (Train/Test) y, como OOT, solo el último mes con desempeño completo (U-01), esto sujeto a la disponibilidad de información en cada proyecto.

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Excel 2: Evolutivos del promedio de la variable objetivo por segmento. · Umbrales: U-01

- **`DES-D1-03.01.03`** Análisis de estabilidad de la ventana de modelamiento, utilizar el PSI como indicar de estabilidad población, en caso sea necesario complementar con algún análisis adicional (Intervalos de confianza)

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Excel 2: Número de cuentas por mes en la ventana de modelación · Umbrales: U-02

- **`DES-D1-03.01.04`** Evaluar los meses con ciertas alertas de inestabilidad, con justificacion metodologica y/o negocio

  Aplica: Todos los tipos, Tier I–III

- **`DES-D1-03.01.05`** Documentación de la generación de la población de modelamiento

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 1 · Entregable: Documento 2: Pedido de datos.

- **`DES-D1-03.01.06`** Antes de fijar la ventana de Train, auditar la serie mensual de la tasa del target. Si la tasa cambia más de 25 % relativo entre meses por un quiebre operativo, de política o de proceso (U-41), los meses previos al quiebre no se usan para entrenar. Si así quedan menos de 12 meses de Train/Test, es una excepción a U-01 que se sustenta y se aprueba con acta.

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 3 · Crítico · Umbrales: U-41 · Nota: Versión 4.0.0 (2026-10-17). Lecciones de proyectos de desarrollo; ver CHANGELOG.

### 4 · Criterios de exclusión

#### 4.1 Definición de exclusiones

- **`DES-D1-04.01.01`** Exclusiones por pautas duras (actuales y futuras)

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 0.85 d ágil / 1 d completo · Automatización: 1 · Entregable: Excel 3: Número de cuentas y promedio antes y después de pautas duras.

- **`DES-D1-04.01.02`** Exclusiones por default en foto (análisis materialidad)

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Excel 3: Número de cuentas y promedio antes y después de default en foto.

- **`DES-D1-04.01.03`** Exclusiones por operaciones con desempeño < ventana de default y mora reciente (análisis impacto)

  Aplica: Todos los tipos, Tier I–II · Automatización: 1 · Entregable: Script 4: Análisis filtros: Operaciones sin desempeño completo.

- **`DES-D1-04.01.04`** Exclusiones por operaciones con desempeño < ventana de default y mora reciente (análisis materialidad)

  Aplica: Lineal/ML/Árbol I–III · Automatización: 1 · Entregable: Excel 3: Número de cuentas y promedio del target de las cuentas sin desempeño.

- **`DES-D1-04.01.05`** Exclusiones por operaciones con mora < altura del default: indeterminados (análisis materialidad)

  Aplica: Lineal/ML/Árbol I–III · Automatización: 1 · Entregable: Excel 3: Número de cuentas y promedio del target de las cuentas de indetermindos.

- **`DES-D1-04.01.06`** Exclusiones por cambios de gestión (Cobranzas)

  Aplica: Lineal/ML/Árbol I–III · Automatización: 1 · Entregable: Excel 3: Número de cuentas y promedio del target de las cuentas excluidas por cambios de gestión

- **`DES-D1-04.01.07`** Documentación de las exclusiones

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Documento 3: Filtros y exclusiones.; Tabla 2: Master table filtrada.

- **`DES-D1-04.01.08`** Evaluar el sesgo de selección de los modelos de originación entrenados solo con solicitudes aprobadas y documentar la estrategia de inferencia de rechazados aplicada, o por qué no aplica.

  Aplica: Lineal/ML/Árbol I–II · Esfuerzo: 1.5 d ágil / 2 d completo · Automatización: 1 · Entregable: Documento 3: Filtros y exclusiones. · Nota: Línea base 2.0 (2026-10-17). Thomas et al. (2017); Kozodoi et al. (2019).

### 5 · Definición del default (binario)

#### 5.1 Definición de cliente - operación

- **`DES-D1-05.01.01`** Adopción de definición del estándar

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 5 d ágil / 5 d completo · Automatización: 1 · Umbrales: U-17

- **`DES-D1-05.01.02`** Análisis de incidencia de default operación en comportamiento cliente

  Aplica: Lineal/ML/Árbol I–II · Automatización: 1

#### 5.2 Definición altura y temporalidad

- **`DES-D1-05.02.01`** Adopción de definición del estándar

  Aplica: Lineal/ML/Árbol I–III · Automatización: 1 · Umbrales: U-17

- **`DES-D1-05.02.02`** Análisis de roll rates

  Aplica: Lineal/ML/Árbol I–II · Automatización: 1

#### 5.3 Definición de materialidad

- **`DES-D1-05.03.01`** Adopción de definición del estándar

  Aplica: Lineal/ML/Árbol I–III · Automatización: 1

- **`DES-D1-05.03.02`** Análisis asociados a la definición de la materialidad

  Aplica: Lineal/ML/Árbol I–II · Automatización: 1

#### 5.4 Documentación final

- **`DES-D1-05.04.01`** Documentación final definición de default

  Aplica: Lineal/ML/Árbol I–III · Automatización: 1 · Entregable: Documento 4: Definición de default. · Umbrales: U-17

### 6 · Definición del target (continuo)

#### 6.1 Definición altura y temporalidad

- **`DES-D1-06.01.01`** Adopción de definición del estándar

  Aplica: Lineal/ML/Árbol I–III · Esfuerzo: 3 d ágil / 3 d completo · Automatización: 1

#### 6.2 Definición de materialidad

- **`DES-D1-06.02.01`** Adopción de definición del estándar

  Aplica: Lineal/ML/Árbol I–III · Automatización: 1

- **`DES-D1-06.02.02`** Análisis asociados a la definición de la materialidad

  Aplica: Lineal/ML/Árbol I–II · Automatización: 1

#### 6.3 Documentación final

- **`DES-D1-06.03.01`** Documentación final definición del target

  Aplica: Todos los tipos, Tier I–III · Automatización: 1 · Entregable: Documento 4: Definición del target. · Hito: SME 2

### 7 · Definición Metodología para modelar

#### 7.1 Identificar la mejor metodología para modelar el target específico

- **`DES-D1-07.01.01`** Identificar la mejor metodología para modelar el target específico

  Aplica: Todos los tipos, Tier I–III · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Propuestas de las metodologías para modelar el target

<!-- CATALOGO:FIN -->
