---
id: MARCO-GLOS
titulo: Glosario y fórmulas de referencia
estandar: Marco
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 5
---

# Glosario y fórmulas de referencia

## Términos

| Término | Definición |
|---|---|
| **Universo** | Conjunto de operaciones/clientes elegibles antes de exclusiones. |
| **Cosecha** | Cohorte de operaciones originadas en un mismo periodo, seguida en su maduración. |
| **Target** | Variable objetivo. Binaria (default) o continua (p.ej. ingreso estimado). |
| **Default** | Evento de incumplimiento definido por altura (días de atraso), temporalidad (ventana de desempeño) y materialidad (monto mínimo). |
| **Indeterminado** | Operación con mora menor a la altura de default al cierre de la ventana; se excluye del entrenamiento. |
| **Train / Test / OOT** | Muestra de entrenamiento, de prueba (mismo periodo) y *out-of-time* (periodo posterior). |
| **Roll rate** | Probabilidad de transitar de un tramo de mora al siguiente; sustenta la altura de default. |
| **Driver** | Variable explicativa, en especial las usadas para calibrar. |
| **Convolución** | Variable construida combinando otras (interacciones, ratios) con criterio de negocio. |
| **Applicant / Behavior** | Score de originación vs. score de comportamiento; la *regla de transición* define cuándo pasar de uno a otro. |
| **Matriz CAR** | Enfoque cualitativo (dimensiones, preguntas y pesos) que complementa al score cuantitativo. |
| **Pauta** | Política de crédito (reglas duras de admisión). |
| **SME** | *Subject Matter Expert*: revisión con experto de negocio. |
| **Toolkit** | Herramienta estándar corporativa de modelamiento. |
| **Comité de Modelos (CM)** | Instancia que aprueba modelos y excepciones. |

## Fórmulas

**Population Stability Index (PSI)** — estabilidad entre una distribución de referencia $e$ y una actual $a$ en $k$ tramos:

$$\mathrm{PSI}=\sum_{i=1}^{k}\left(a_i-e_i\right)\ln\frac{a_i}{e_i}$$

Umbral vigente: ver U-02.

**Gini y AUC** — poder discriminante de un score binario:

$$\mathrm{Gini}=2\,\mathrm{AUC}-1$$

**Kolmogorov–Smirnov (KS)**: $\mathrm{KS}=\max_s\left|F_{\text{malos}}(s)-F_{\text{buenos}}(s)\right|$.

**Weight of Evidence e Information Value** — para el tramo $i$ con proporción de buenos $g_i$ y malos $b_i$:

$$\mathrm{WOE}_i=\ln\frac{g_i}{b_i},\qquad \mathrm{IV}=\sum_i\left(g_i-b_i\right)\mathrm{WOE}_i$$

**V de Cramér** — asociación entre categóricas, con $\chi^2$ de la tabla $r\times c$ y $n$ observaciones:

$$V=\sqrt{\frac{\chi^2/n}{\min(r-1,\;c-1)}}$$

**Representatividad de la muestra**: $\dfrac{TM}{TG}\in[0.95,\;1.05]$, con $TM$ y $TG$ la tasa del target en muestra y población (U-03).

**Intervalo de Vasicek** (precisión de PD por tramo, con correlación de activos $\rho$ y nivel de confianza $q$):

$$\mathrm{DR}_{q}=\Phi\!\left(\frac{\Phi^{-1}(\mathrm{PD})+\sqrt{\rho}\,\Phi^{-1}(q)}{\sqrt{1-\rho}}\right)$$

Si la tasa de default observada de un tramo cae fuera de $[\mathrm{DR}_{1-q},\mathrm{DR}_{q}]$, el tramo se marca en rojo (U-14).

**Prueba de Mann–Kendall** — tendencia monótona en una serie (p.ej. % de missing mensual, DES-D2-01.04.07):
$S=\sum_{i<j}\operatorname{sgn}(x_j-x_i)$; se rechaza "sin tendencia" si $|Z|>z_{1-\alpha/2}$.
