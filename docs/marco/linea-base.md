---
id: MARCO-LB
titulo: "Línea base 2.0 y benchmarking"
estandar: Marco
estado: Vigente
version: 2.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 1
---

# Línea base 2.0 y benchmarking

La versión 2.0 es la **línea base** del estándar: el punto de referencia contra el que se medirán los cambios
futuros. Se construyó contrastando cada estándar con tres fuentes: la regulación vigente, la práctica pública de
bancos de referencia y la literatura reciente de journals de primer nivel.

## Método y límites

- **Los bancos no publican sus estándares internos de modelos.** Lo que sí es público son sus informes anuales y
  regulatorios (10-K, 20-F, Pillar 3), sus principios de IA y su investigación aplicada. Este benchmarking usa solo
  esas fuentes y las cita. Para cualquier banco concreto, sus documentos internos aprobados prevalecen.
- La regulación se verificó en la fuente primaria cuando fue posible (Fed, El Peruano, EBA, BCE, BIS).
- Las referencias de journals se verificaron en sus bases bibliográficas. Las que tienen datos pendientes lo dicen en la propia cita.

## Hallazgos principales

1. **Perú tiene norma propia de riesgo de modelo** (Res. SBS 00053-2023). Exige comité trimestral, aprobación
   previa de todo modelo nuevo o modificado (incluida una recalibración), réplica en alta categoría, seguimiento de
   forzajes, informe anual, reglas para terceros y requisitos específicos de IA. Se incorporó en el nuevo estándar de
   [Gobierno](gobierno-mrm.md) y en Desarrollo, Calibración, Implementación, Validación y Seguimiento.
2. **SR 11-7 ya no está vigente:** fue reemplazada el 17 de abril de 2026 por **SR 26-2**, más basada en riesgo y con
   una sección de terceros. Excluye explícitamente la IA generativa y agéntica, un vacío que este estándar cubre
   con [AGT](../agentes/index.md).
3. **El seguimiento es donde la norma y la práctica exigen más disciplina.** Tiene estándar propio ([Seguimiento](../seguimiento/seguimiento.md)).
4. **La literatura reciente confirma decisiones del estándar y agrega controles:** el boosting es preferible al deep
   learning en datos tabulares de crédito (LIT-135); las explicaciones SHAP/LIME se vuelven inestables con desbalance
   (LIT-136); la equidad puede mejorarse a bajo costo (LIT-134); la evaluación por rentabilidad complementa al Gini (LIT-138).

## Cambios por estándar

| Estándar | Brecha detectada | Enriquecimiento en 2.0 | Fuente |
|---|---|---|---|
| **Gobierno** (nuevo) | No existía un estándar a nivel de entidad | GOB-G1 a GOB-G5: comité, inventario, categorización, aprobación previa, terceros, IA, informe anual | SBS 53-2023, SR 26-2, SS1/23, JPMorgan, HSBC, BBVA |
| **Desarrollo** | Sin control del sesgo de selección | DES-D1-04.01.08 inferencia de rechazados | LIT-002, LIT-139 |
| | ML sin benchmark ni validación cruzada obligatorios | DES-D4-05.03.02, DES-D4-05.03.03 | SBS art. 16, LIT-135, LIT-132 |
| | Solo métricas estadísticas | DES-D4-06.01.03 métrica de rentabilidad (EMP) | LIT-138 |
| | Explicabilidad sin prueba de estabilidad | DES-D4-07.01.02 | LIT-136 |
| | Sin análisis de sensibilidad ni de equidad | DES-D4-10.01.06, DES-D4-10.01.07 | SBS art. 16, LIT-134 |
| | Forzajes no normados | DES-D5-01.01.02, U-36 | SBS arts. 19 y 22 |
| | Aprobación previa implícita | DES-D7-01.01.07 | SBS art. 17 |
| **Calibración** | No se exigía justificar calibrar vs. redesarrollar | CAL-C1-01.01.07 | Práctica de bancos |
| | Recalibrar no se trataba como modificación | CAL-C5-01.01.05 | SBS art. 17 |
| **Implementación** | Sin pruebas de escenarios de error | IMP-01.06.05 | SBS art. 18 |
| | Sin trazabilidad de versión por resultado | IMP-01.06.06 | FR-07, práctica de bancos |
| **Validación** | Sin réplica, challenger, periodicidad ni severidad de hallazgos | VAL-M-05.01 a VAL-M-05.06, U-35 | SBS arts. 7, 20 y 25; Santander |
| **Seguimiento** | Borrador | SEG-S1 a SEG-S4, U-36, U-37 | SBS arts. 21–22 |
| **Parámetros, Pricing, Agentes** | Construidos con benchmarking propio (GPPC, BCBS, EBA, BCE, literatura de pricing e IA) | Agentes cubre el vacío de SR 26-2 en IA generativa | — |

## Cómo se mantiene la línea base

- **Revisión anual** del benchmarking (regulación, práctica pública de bancos y literatura), con un informe de
  brechas que alimenta la versión menor siguiente.
- **Cambio regulatorio:** se incorpora como versión mayor si cambia obligaciones (como en 2.0 con la SBS y SR 26-2).
- Cada requisito nuevo lleva `nota_origen` con su fuente, para auditar por qué existe.

## Fuentes públicas consultadas

- Federal Reserve, [SR 26-2: Revised Guidance on Model Risk Management](https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm) (abril 2026).
- SBS, [Reglamento de Gestión de Riesgos de Modelo, Res. SBS N° 00053-2023](https://busquedas.elperuano.pe/dispositivo/NL/2141173-1) (El Peruano).
- JPMorgan Chase & Co., [Form 10-K 2024](https://www.sec.gov/Archives/edgar/data/19617/000001961725000270/jpm-20241231.htm), sección de riesgo de modelo.
- BBVA, [Eight responsible AI principles](https://www.bbva.com/en/innovation/bbvas-eight-responsible-ai-principles/) y [Responsible innovation](https://www.bbva.com/en/innovation/responsible-innovation-how-bbva-ensures-safe-use-of-artificial-intelligence/).
- HSBC, descripciones públicas de su función de Model Risk Management (portal de empleo, [ejemplo](https://mycareer.hsbc.com/fr_FR/external/PipelineDetail/Senior-Manager-Independent-Model-Review-f-m-d/253184)).
- Credicorp, [Form 20-F 2025](https://www.sec.gov/Archives/edgar/data/0001001290/000100129026000008/bap-20251231.htm).
- EBA, [Follow-up report on machine learning for IRB models](https://www.eba.europa.eu/eba-publishes-follow-report-use-machine-learning-internal-ratings-based-models) (2023).
- Kiritz, Ravitz y Levonian (2019), [Model risk tiering](https://www.risk.net/journal-of-risk-model-validation/6710566/model-risk-tiering-an-exploration-of-industry-practices-and-principles), *Journal of Risk Model Validation*.
- Artículos de EJOR 2014–2025 citados en la [literatura](literatura.md) (LIT-134 a LIT-140).
