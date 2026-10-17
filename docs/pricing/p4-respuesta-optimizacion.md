---
id: PRC-P4
titulo: "Pricing · P4–P5 Respuesta al precio y optimización"
estandar: Pricing
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 27
---

# Pricing · P4–P5 Respuesta al precio y optimización

## P4 · El modelo de respuesta

Estima la probabilidad de que el cliente $i$ acepte la oferta al precio $r$:

$$P_i(r)=\sigma\!\left(\alpha(x_i)+\beta(x_i)\,\big(r - r^{\text{ref}}_i\big)\right),\qquad \beta(x_i)<0$$

donde $r^{\text{ref}}_i$ es la referencia del cliente: tasa de la competencia, tasa de lista o su precio anterior.
La **elasticidad** en el punto $r$ es $\varepsilon_i(r)=\dfrac{\partial \ln P_i}{\partial \ln r}=\beta(x_i)\,r\,\big(1-P_i(r)\big)$.

### El problema central: endogeneidad

El precio histórico se fijó *por* el riesgo y el perfil. Un modelo ingenuo concluye que "los clientes que
pagan más aceptan menos" cuando en realidad mide que "los clientes riesgosos aceptan menos". Ese sesgo tiende
a **exagerar** la sensibilidad y lleva a ceder margen. La estrategia de identificación es un requisito
documentado (PRC-P4-01.01.01):

| Estrategia | Cuándo | Riesgo principal |
|---|---|---|
| **Experimento aleatorio** de precio | Siempre que sea posible (P6) | Costo de oportunidad del piloto; diseño ético |
| **Discontinuidad en la grilla** | Precio salta en un umbral de score o monto | Validez solo cerca del umbral |
| **Variable instrumental** | Cambios del costo de fondos o del tarifario ajenos al cliente | Instrumento débil o no excluible |
| **Double machine learning** | Muchos controles y variación residual suficiente | Variables omitidas |

### Reglas de construcción

- Se sigue DES-D4 (Train/Test/OOT, depuración, selección, documentación).
- Monotonicidad obligatoria: la aceptación decrece con el precio en **todo** segmento (U-20).
- **La calibración manda más que el Gini** (U-21). El optimizador consume probabilidades, no rankings.
- Se declara el **rango de precios válido**: la curva no se extrapola fuera del soporte observado.

<!-- CATALOGO:INICIO PRC-P4 -->
## Catálogo de requisitos · Modelos de respuesta al precio

> Bloque generado desde `catalogo/prc-p4.yaml` (9 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Pricing Analítico v1.0 (nuevo, 2026-10-17).

### 1 · Identificación causal

#### 1.1 Estrategia de identificación

- **`PRC-P4-01.01.01`** Documentar cómo se separa el efecto del precio del efecto del riesgo y del perfil del cliente, dado que el precio histórico no fue asignado al azar: experimento aleatorio (preferido), discontinuidad en la grilla de precios, variable instrumental (por ejemplo, cambios del costo de fondos o del tarifario ajenos al cliente) o double machine learning con controles completos.

  Aplica: Tier I–III · Esfuerzo: 2 d · Automatización: 1 · Crítico · Entregable: Documento P4: Modelo de respuesta y elasticidad · Hito: Sprint 3

- **`PRC-P4-01.01.02`** Pruebas de robustez de la identificación: placebo en periodos sin cambio de precio, balance de covariables entre grupos de precio, sensibilidad a variables omitidas y estabilidad de la elasticidad entre submuestras temporales.

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 2 · Entregable: Documento P4: Modelo de respuesta y elasticidad

### 2 · Modelo de aceptación

#### 2.1 Construcción

- **`PRC-P4-02.01.01`** Estimar la probabilidad de aceptación de la oferta en función del precio relativo (precio ofrecido frente a referencia o competencia) y de las características del cliente, siguiendo DES-D4 para muestras (Train/Test/OOT), depuración y selección de variables.

  Aplica: Tier I–III · Esfuerzo: 5 d · Automatización: 2 · Crítico · Entregable: Script P1: Modelo de respuesta

- **`PRC-P4-02.01.02`** Imponer la restricción de monotonicidad decreciente de la aceptación en el precio (U-20), incluso en modelos de machine learning (restricciones monotónicas en gradient boosting) y permitir elasticidades heterogéneas por segmento.

  Aplica: Tier I–III · Esfuerzo: 1 d · Automatización: 2 · Crítico · Entregable: Script P1: Modelo de respuesta · Umbrales: U-20

#### 2.2 Desempeño

- **`PRC-P4-02.02.01`** Validar discriminación (Gini/AUC) y, sobre todo, calibración: aceptación observada vs. predicha por decil y por tramo de precio (U-21). En pricing un modelo descalibrado optimiza mal aunque ordene bien.

  Aplica: Tier I–III · Esfuerzo: 1.5 d · Automatización: 3 · Crítico · Entregable: Excel P3: Curvas de respuesta por segmento · Umbrales: U-21

### 3 · Comportamiento posterior

#### 3.1 Modelos de valor

- **`PRC-P4-03.01.01`** Estimar los modelos que determinan el valor de la operación según el precio: prepago y cancelación (activos), sensibilidad de saldo y fuga ante cambios de tasa (depósitos: beta de traslado y elasticidad de saldos), uso de línea (TC).

  Aplica: Tier I–II · Esfuerzo: 4 d · Automatización: 2 · Entregable: Script P1: Modelo de respuesta

- **`PRC-P4-03.01.02`** Evaluar si el precio afecta el riesgo (selección adversa); si la PD observada cambia con el precio para un mismo score, incorporarlo en el valor esperado.

  Aplica: Tier I–II · Esfuerzo: 1.5 d · Automatización: 2 · Entregable: Documento P4: Modelo de respuesta y elasticidad

### 4 · Cierre del modelo de respuesta

#### 4.1 Revisión

- **`PRC-P4-04.01.01`** Reunión de revisión del modelo de respuesta con el dueño del precio: elasticidades por segmento, su sentido de negocio y sus límites de uso.

  Aplica: Tier I–III · Esfuerzo: 0.5 d · Automatización: 1 · Entregable: Acta PRC-ELA: Revisión del modelo de respuesta

#### 4.2 Documentación

- **`PRC-P4-04.02.01`** Documentar el modelo de respuesta con la estructura de DES-D4-11 (memoria metodológica, limitaciones, rango de precios en que la elasticidad es válida).

  Aplica: Tier I–III · Esfuerzo: 2 d · Automatización: 1 · Entregable: Documento P4: Modelo de respuesta y elasticidad

<!-- CATALOGO:FIN -->

## P5 · Optimización

Para cada oferta (o celda) se elige el precio que maximiza el valor esperado:

$$\max_{r_i}\ \sum_i P_i(r_i)\cdot V_i(r_i)\quad\text{s.a.}\quad
\begin{cases}
r_{\min,i}\le r_i\le r_{\max} & \text{(U-18, U-24)}\\
\sum_i P_i(r_i)\,\mathrm{EAD}_i \ge \text{Volumen objetivo}\\
r_i \text{ no decreciente en el riesgo dentro de la celda} & \text{(U-19)}\\
|r_i - r_i^{\text{actual}}| \le \Delta & \text{(U-25)}
\end{cases}$$

con $V_i(r)$ el valor presente de la operación: margen sobre el piso, ajustado por prepago, fuga, uso de
línea y, si la entidad lo gestiona, venta cruzada. Para un objetivo solo de margen y respuesta logística,
el óptimo sin restricciones cumple

$$r^{*}_i = r_{\min,i} + \frac{1}{|\beta_i|\,\big(1-P_i(r^{*}_i)\big)}$$

Es decir, el margen óptimo sobre el piso es inversamente proporcional a la sensibilidad del cliente.

### Buenas prácticas

- **Robustez:** optimiza con el intervalo de la elasticidad, no solo con su punto central (PRC-P5-02.02.01).
  Una elasticidad sobreestimada cede margen; una subestimada pierde volumen. Ambos errores tienen costo asimétrico.
- **Granularidad comercial:** redondea a la grilla (p.ej. 25 pb) y reporta el valor perdido por redondeo.
- **Escenarios, no un número:** el comité decide entre alternativas con volumen, margen, RAROC, pérdida
  esperada, capital y provisiones a 12 meses.

<!-- CATALOGO:INICIO PRC-P5 -->
## Catálogo de requisitos · Optimización y propuesta de precios

> Bloque generado desde `catalogo/prc-p5.yaml` (7 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Pricing Analítico v1.0 (nuevo, 2026-10-17).

### 1 · Formulación

#### 1.1 Problema de optimización

- **`PRC-P5-01.01.01`** Formular el problema: maximizar la función objetivo de P1 sumando, por oferta, la probabilidad de aceptación por el valor de la operación al precio propuesto, sujeto a precio ≥ piso técnico (U-18), precio ≤ tope regulatorio (U-24), metas de volumen y riesgo, monotonicidad en el riesgo (U-19) y gradualidad (U-25).

  Aplica: Tier I–III · Esfuerzo: 2 d · Automatización: 1 · Crítico · Entregable: Documento P5: Propuesta de precios · Hito: Sprint 4 · Umbrales: U-19, U-25

- **`PRC-P5-01.01.02`** Definir la granularidad de la decisión (celda de tarifario o precio individual) y la regla de redondeo a la grilla comercial (por ejemplo, múltiplos de 25 pb), evaluando el valor perdido por redondeo.

  Aplica: Tier I–III · Esfuerzo: 1 d · Automatización: 1 · Entregable: Documento P5: Propuesta de precios

### 2 · Resolución

#### 2.1 Optimizador

- **`PRC-P5-02.01.01`** Implementar el optimizador (búsqueda en grilla, programación no lineal o entera) con semilla y versiones fijadas, y verificar que la solución respeta todas las restricciones.

  Aplica: Tier I–III · Esfuerzo: 3 d · Automatización: 2 · Crítico · Entregable: Script P2: Optimizador de precios

#### 2.2 Robustez

- **`PRC-P5-02.02.01`** Optimizar con incertidumbre: propagar el intervalo de la elasticidad (bootstrap o posterior) a la propuesta y preferir precios cuyo resultado sea bueno en todo el rango plausible, no solo en el punto central.

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 2 · Entregable: Script P2: Optimizador de precios

#### 2.3 Escenarios

- **`PRC-P5-02.03.01`** Construir escenarios para el comité: precio actual, propuesta óptima, propuesta con restricción de volumen y alternativas del negocio, con impacto en volumen, margen, RAROC, pérdida esperada, capital y provisiones a 12 meses.

  Aplica: Tier I–III · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: PPT P1: Escenarios de precio

### 3 · Validación de la propuesta

#### 3.1 Controles

- **`PRC-P5-03.01.01`** Controlar la propuesta antes de llevarla a comité: 100 % de precios dentro de [piso, tope], monotonicidad, cambios mayores al umbral de gradualidad identificados, y análisis de equidad de precios por grupos: las diferencias deben explicarse por riesgo, costo, plazo o canal (PRC-P9-02.02.01).

  Aplica: Tier I–III · Esfuerzo: 1.5 d · Automatización: 3 · Crítico · Entregable: Documento P5: Propuesta de precios

#### 3.2 Comité de Precios

- **`PRC-P5-03.02.01`** Presentar la propuesta y sus escenarios al Comité de Precios para su aprobación, con las excepciones a umbrales explícitas.

  Aplica: Tier I–III · Esfuerzo: 0.5 d · Automatización: 1 · Crítico · Entregable: Acta PRC-CP: Comité de Precios · Hito: Comité de Precios

<!-- CATALOGO:FIN -->

## Frontera *(propuesta, no obligatoria)*

- **Bandits contextuales** para el precio individual en canales digitales de alto volumen: equilibran aprender
  la elasticidad y explotarla, siempre dentro de [piso, tope] y con exploración acotada y registrada.
- **Causal ML** (*causal forests*, *meta-learners*) para estimar elasticidades heterogéneas por cliente con
  intervalos de confianza honestos.
- **Optimización de cartera con capital:** asignación conjunta de precio y límite cuando el capital es la restricción vinculante.
