---
id: FR-04
titulo: "FR-04 · Calibración y cuantificación de incertidumbre"
estandar: Frontera
estado: Propuesta
version: 0.1.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 54
---

# FR-04 · Calibración y cuantificación de incertidumbre

**Hoy:** se calibra con drivers micro/macro y se evalúa precisión por tramo con intervalos de Vasicek (U-14).
Los modelos ML entregan *scores* cuya probabilidad no siempre está bien calibrada.

## Propuestas

**1. Métricas de calibración estándar** reportadas junto al Gini en la selección del modelo (DES-D4-06):

$$\text{Brier}=\frac1n\sum_{i}(p_i-y_i)^2,\qquad
\text{ECE}=\sum_{b=1}^{B}\frac{n_b}{n}\left|\bar y_b-\bar p_b\right|$$

y el **test de Jeffreys** por tramo (estándar en backtesting de PD): con $d$ defaults en $n$ casos,
el p-valor es $F_{\text{Beta}(d+\frac12,\,n-d+\frac12)}(\mathrm{PD})$; valores bajos indican subestimación.

**2. Recalibración post-hoc para ML**: Platt (logística sobre el score) o regresión isotónica, ajustadas en una
muestra distinta a la de entrenamiento; documentar la elegida y su efecto en Brier.

**3. Margen de conservadurismo (MoC)** para modelos regulatorios: cuantificar por separado la incertidumbre
de datos, de metodología y de estimación, en vez de un ajuste único.

**4. Predicción conforme para estimadores** (target continuo): intervalos con cobertura garantizada en
muestra finita, sin supuestos distribucionales. Con residuos de calibración $r_i=|y_i-\hat y_i|$, el intervalo
es $\hat y\pm q_{1-\alpha}$, con $q_{1-\alpha}$ el cuantil $\lceil (n+1)(1-\alpha)\rceil/n$ de los $r_i$.
Complementa la métrica vigente de "% dentro de ±25 % / ±50 %" (U-12) con una promesa de cobertura explícita.
Usar la versión *conformalized quantile regression* si la dispersión depende del cliente.
