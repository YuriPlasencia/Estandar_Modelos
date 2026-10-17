---
id: MARCO-TIER
titulo: Tiering, tipo de modelo y enfoque de trabajo
estandar: Marco
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 2
---

# Tiering, tipo de modelo y enfoque de trabajo

Cada requisito del catálogo se activa según **tres dimensiones**. Antes de empezar, el proyecto debe fijarlas
en el Project Charter (DES-D1-01.04.04 *Definición del Tier y uso del modelo*).

## 1. Tier del modelo (I – III)

El Tier refleja la **materialidad y criticidad** del modelo. Determina cuántas actividades son obligatorias:
un Tier I exige el conjunto completo; el Tier III permite omitir análisis marcados como no aplicables
(por ejemplo, el análisis mensual de completitud del target o la segmentación supervisada).

| Tier | Riesgo del modelo | Tratamiento |
|---|---|---|
| **I** | Alto | Conjunto completo de requisitos; validación periódica anual con réplica completa (U-35) |
| **II** | Medio | Omite algunos análisis de profundidad; validación cada dos años |
| **III** | Bajo | Solo lo necesario para sustentar el uso; validación cada tres años |

> **El número de Tiers lo aprueba el comité.** La Res. SBS 00053-2023 (art. 6) exige categorizar los modelos por
> materialidad, uso y complejidad, con criterios aprobados por el comité de riesgos de modelo (GOB-G2-02.01.01), y
> fijar por categoría el alcance, la profundidad y la frecuencia del seguimiento y la validación. **No fija un número
> de categorías**, como tampoco lo hacen la guía SR 26-2 (EE. UU.), la PRA SS1/23 (Reino Unido) ni la OSFI E-23
> (Canadá). La práctica de mercado usa tres o cuatro niveles; este estándar adopta **tres**, porque cada nivel debe
> cambiar de verdad los controles que se exigen: en la versión anterior, Tier III y Tier IV tenían exactamente los
> mismos requisitos, umbrales y frecuencia de validación. Si el comité de una entidad aprueba otra escala, debe
> documentar su correspondencia con I–III. Las herramientas aceptan «4» o «IV» de versiones anteriores como Tier III.

- El Tier se asigna con participación del equipo desarrollador (DES-D7-01.01.03) y se aprueba con acta (VAL-M-01.13).
- El catálogo indica, para cada actividad, en qué Tiers aplica (`aplica_tier`).

> **Criterios de categoría.** Los aprueba el comité de riesgos de modelo (GOB-G2-02.01.01). Ver la propuesta de
> puntaje en [Frontera › Tiering basado en riesgo](../frontera/tiering-basado-en-riesgo.md).

## 2. Tipo de modelo

| Clave | Tipo | Ejemplos |
|---|---|---|
| `lineal` | Modelos lineales / lineales generalizados | Regresión logística con WOE, regresión lineal |
| `ml` | Machine Learning | Gradient boosting (XGBoost, LightGBM), redes |
| `arbol` | Árboles de regresión / decisión | CART, árboles de segmentación |
| `acp` | Modelos basados en ACP (componentes principales) | Índices sintéticos, *scorecards* expertos |

Algunas actividades son exclusivas de un tipo. Por ejemplo, la optimización de hiperparámetros (DES-D4-05.04) sólo
aplica a ML; la transformación WOE de continuas (DES-D4-04.03.02) sólo a modelos lineales.

## 3. Enfoque de trabajo: Ágil vs Completo

El catálogo estima el esfuerzo (días-persona) para dos enfoques:

- **Ágil:** cubre lo esencial. Se ejecutan todas las actividades aplicables, pero con la profundidad mínima suficiente
  para sustentar cada decisión: análisis acotados a lo material, iteraciones cortas y entregables incrementales. Cada
  actividad requiere en torno a un 15 % menos de esfuerzo, lo que acorta la duración total en cerca de un 10 % (ver
  [Estimación](estimacion.md)).
- **Completo:** análisis exhaustivo y documentación detallada de cada actividad: más alternativas evaluadas, pruebas de
  sensibilidad y robustez más amplias y entregables cerrados al final de cada etapa.

Los dos enfoques aplican **los mismos requisitos y umbrales**; cambia la profundidad, no lo que se exige. Los requisitos
críticos y los umbrales nunca se relajan por elegir el enfoque ágil. Calibración, Parámetros, Pricing y Seguimiento se
estiman siempre con el enfoque completo. En versiones anteriores, el enfoque completo se llamaba *tradicional*; las
herramientas aceptan ambos nombres.

## 4. Nivel de automatización

Cada actividad declara su nivel de automatización actual (0–4). Es la palanca principal de eficiencia: subir una
actividad de nivel 2 a 4 la convierte en un proceso del *toolkit*.

| Nivel | Significado |
|---|---|
| 0 | El análisis no se ha realizado previamente |
| 1 | No se cuenta con códigos |
| 2 | Scripts particulares |
| 3 | Scripts estándar |
| 4 | Procesos industrializados dentro del toolkit |

## 5. Marcas de criticidad

- **Crítico:** actividad cuyo incumplimiento invalida el entregable.
- **Eficiencia:** actividad priorizada para automatización.
- **KILLER** (validación de implementación): requisito cuyo incumplimiento bloquea la conformidad.
