---
id: FR-06
titulo: "FR-06 · Equidad y sesgo"
estandar: Frontera
estado: Propuesta
version: 0.1.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 56
---

# FR-06 · Equidad y sesgo

**Hoy:** se analiza el desempeño por subpoblaciones (DES-D4-10.01.04, VAL-M-03.08) con foco en riesgo, no en trato justo.

**Propuesta:** para modelos sobre personas naturales (Tier I–II), un análisis de equidad documentado en el
capítulo de limitaciones:

1. **Variables sensibles y proxies:** no usar atributos protegidos (sexo, edad cuando la norma lo restrinja,
   etnia, discapacidad…) y probar si alguna variable los aproxima (AUC de predecir el atributo con las variables del modelo).
2. **Métricas por grupo** (donde la información exista legalmente):
   - Razón de aprobación entre grupos (*disparate impact*), alerta si < 0.8.
   - Diferencia de tasa de verdaderos positivos (*equal opportunity*).
   - Calibración por grupo: misma PD debe significar el mismo riesgo observado.
3. **Decisión documentada:** las métricas de equidad son en parte incompatibles entre sí; el documento debe
   decir cuál se prioriza y por qué, y qué *trade-off* de Gini se acepta.

La disponibilidad legal de atributos sensibles varía por jurisdicción; coordinar con Legal y Cumplimiento antes de recolectarlos.
