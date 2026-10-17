---
id: DES-D3
titulo: "D3 · Segmentación"
estandar: Desarrollo
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 12
---

# D3 · Segmentación

## Objetivo

Decidir si conviene construir **un modelo único o varios modelos por segmento**, y con qué ejes. Un segmento
se justifica sólo si mejora el desempeño frente al modelo unisegmento y es estable y material.

## Enfoque

1. **Propuesta de ejes** con stakeholders (Reunión 4). Si los drivers no son claros, usar árboles de decisión
   para identificar candidatos y cortes.
2. **Materialidad y target por segmento**: tasa de default, volumen, estabilidad en el tiempo.
3. **Segmentación supervisada**: comparar modelos *naive* por segmento vs. modelo unisegmento.
4. **Segmentación no supervisada** (opcional): k-medias, k-modas, k-medoides, jerárquico, CLARA, PAM; número
   de clusters por gráfico de sedimentación (codo).
5. **Contraste estadístico** de homogeneidad intra-segmento y heterogeneidad entre segmentos, y contraste con el negocio.

## Criterios de aceptación

- La segmentación elegida supera al unisegmento en desempeño (PPT 3).
- Cada segmento tiene materialidad suficiente y target estable (Excel 8).
- Documento 7 aprobado en SME 3.
- Supuesto de estimación: máximo 4–5 segmentos (ver [Estimación](../marco/estimacion.md)).

<!-- CATALOGO:INICIO DES-D3 -->
## Catálogo de requisitos · Segmentación

> Bloque generado desde `catalogo/des-d3.yaml` (9 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Desarrollo v1.0.

### 1 · Segmentación

#### 1.1 Brainstorming sobre propuestas de segmentación y análisis

- **`DES-D3-01.01.01`** Reunión stakeholder para determinar propuesta de ejes de segmentación, en caso no tenga claridad de los posibles drivers de segmentación se utilizar técnicas como árboles de decisión para la identificar de potenciales drivers, así como cortes propuestos

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.85 d ágil / 1 d completo · Automatización: 1 · Entregable: Acta 4: Reunión de segmentación. · Hito: Reunión 4

- **`DES-D3-01.01.02`** Análisis de ratio de default y materialidad/Análisis de target ( Estabilidad de Segmentos)

  Aplica: Lineal/ML/Árbol I–IV · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 1 · Entregable: Excel 8: Analisis de materialidad y target por segmento. · Hito: Sprint 7

- **`DES-D3-01.01.03`** Segmentación por metodología supervisada (modelos naive) / Modelo Segmentado VS Modelo Unisegmento

  Aplica: Lineal I–II · Esfuerzo: 2 d ágil / 2 d completo · Automatización: 1 · Entregable: Excel 8: Analisis comparativo entre modelos.

- **`DES-D3-01.01.04`** Segmentación con ejes adicionales

  Aplica: Lineal/ACP I–II · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Tabla 3: Master table por segmento.

- **`DES-D3-01.01.05`** Segmentación por metodología no supervisada (opcional): Evaluar diversos tipos de clustering de acuerdo con el tipo de datos utilizados (k-medias, k-modas, k-medoids, clustering jerárquico, CLARA, PAM). Definir el número óptimo de clusters mediante gráfico de sedimentación.

  Aplica: Lineal I–II · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Tabla 3: Master table por segmento.

#### 1.2 Análisis final y Documentación

- **`DES-D3-01.02.01`** Comparación del desempeño de las segmentaciones con el modelo unisegmento

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Ppt 3: Análisis de segmentación.

- **`DES-D3-01.02.02`** Análisis de estabilidad del target y materialidad, contraste estadístico (homogeneidad y/o heterogeneidad), contraste con el negocio

  Aplica: Lineal/ML/Árbol I–IV · Esfuerzo: 1 d ágil / 1 d completo · Automatización: 1 · Entregable: Excel 8: Analisis de materialidad y target por segmento.

- **`DES-D3-01.02.03`** Elaboración de presentación de segmentación final.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.5 d ágil / 0.5 d completo · Automatización: 1 · Entregable: Ppt 3: Análisis de segmentación.

- **`DES-D3-01.02.04`** Documentación y definición de la segmentación final

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.5–1.5 d ágil / 0.5–1.5 d completo · Automatización: 1 · Entregable: Documento 7: Análisis de segmentación. · Hito: SME 3

<!-- CATALOGO:FIN -->
