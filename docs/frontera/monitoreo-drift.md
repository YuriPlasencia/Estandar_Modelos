---
id: FR-05
titulo: "FR-05 · Monitoreo de drift moderno"
estandar: Frontera
estado: Propuesta
version: 0.1.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 55
---

# FR-05 · Monitoreo de drift moderno

**Hoy:** el PSI es el indicador único de estabilidad (U-02, IMP-01.04).

**Limitaciones del PSI:** depende del número y corte de los tramos, no es simétrico respecto a la elección de
la referencia en tramos pequeños, es sensible al tamaño de muestra (con $n$ grande todo "se mueve" y con $n$
chico nada) y no dice si el cambio afecta al desempeño.

## Propuestas

1. **Complementar, no sustituir, el PSI**:
   - Divergencia de **Jensen–Shannon** (simétrica, acotada en $[0,1]$) para variables con muchos tramos.
   - **Wasserstein / KS** para continuas sin depender del binning.
   - Umbrales ajustados por tamaño de muestra (bootstrap del PSI bajo la hipótesis de no cambio).
2. **Drift multivariado — validación adversarial:** entrenar un clasificador que distinga *referencia* vs.
   *actual*; un AUC ≈ 0.5 indica que no hay drift; AUC > 0.6 es alerta y su importancia de variables dice qué cambió.
3. **Estimación de desempeño sin etiquetas:** mientras maduran las cosechas, estimar el Gini esperado con
   métodos tipo CBPE (*confidence-based performance estimation*), válidos si el modelo está calibrado (ver FR-04).
4. **Separar drift de datos y drift de concepto:** el primero se ve en las variables; el segundo sólo en el
   desempeño. El plan de acción es distinto (calibrar vs. redesarrollar).
