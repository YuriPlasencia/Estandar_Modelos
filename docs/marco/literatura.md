---
id: MARCO-LIT
titulo: Literatura de referencia
estandar: Marco
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 6
---

# Literatura de referencia

Una biblioteca corta y curada. Cada obra está aquí porque **fundamenta un requisito o un umbral concreto** del
estándar, y lo declara. Al abrir un requisito en el sitio, el panel muestra sus lecturas. Los agentes de IA
citan desde esta lista (`dist/literatura.json`) y no inventan referencias.

| Nivel | Qué significa |
|---|---|
| **Canon** | Lectura obligatoria para quien trabaja en el área |
| **Práctica** | Cómo se hace bien en el día a día |
| **Frontera** | Estado del arte; sustenta las propuestas de la sección Frontera |
| **Regulación** | Normas y guías de supervisores |

## Rutas de lectura

| Rol | Empieza por | Después |
|---|---|---|
| Analista nuevo de scoring | LIT-001, LIT-002, LIT-011 | LIT-020, LIT-008, LIT-030 |
| Analista de ML | LIT-020, LIT-021, LIT-027 | LIT-026, LIT-040, LIT-031 |
| Calibración y validación | LIT-006, LIT-008, LIT-043 | LIT-007, LIT-105, LIT-050 |
| Analista de pricing | LIT-071, LIT-070, LIT-060 | LIT-064, LIT-075, LIT-062 |
| Gobierno y agentes de IA | LIT-100, LIT-101, LIT-093 | LIT-094, LIT-090, LIT-102 |

## Cómo proponer una obra

Agrega la entrada en `catalogo/literatura.yaml` con su nivel, el porqué en una frase y los IDs que fundamenta.
El build rechaza obras que no fundamentan ningún requisito existente. Antes de una cita formal, verifica
edición y paginación en la fuente.

<!-- CATALOGO:INICIO LITERATURA -->
105 obras en 10 temas.

## Riesgo de crédito y scoring

- **LIT-001** · *Canon* — Siddiqi, N. (2017). *Intelligent Credit Scoring: Building and Implementing Better Credit Risk Scorecards* (2.ª ed.). Wiley.

  El manual práctico de referencia para construir scorecards: definición de malos, exclusiones, WOE, segmentación e implementación. Fundamenta: `DES-D1-04`, `DES-D1-05`, `DES-D3`, `DES-D4-04`, `DES-D4-11`, `U-38`, `DES-D4-03.03`.

- **LIT-002** · *Canon* — Thomas, L. C., Crook, J. y Edelman, D. (2017). *Credit Scoring and Its Applications* (2.ª ed.). SIAM.

  Fundamentos estadísticos del scoring, incluida la lógica de las ventanas de desempeño y la inferencia de rechazados. Fundamenta: `DES-D1-03`, `DES-D1-05`, `DES-D4-05`.

- **LIT-003** · *Práctica* — Anderson, R. (2007). *The Credit Scoring Toolkit: Theory and Practice for Retail Credit Risk Management and Decision Automation*. Oxford University Press.

  Visión de punta a punta del scoring en la operación del banco, desde los datos hasta la decisión automatizada. Fundamenta: `DES-D1`, `DES-D5`, `IMP`.

- **LIT-004** · *Práctica* — Baesens, B., Rösch, D. y Scheule, H. (2016). *Credit Risk Analytics: Measurement Techniques, Applications, and Examples in SAS*. Wiley.

  PD, LGD y EAD con ejemplos de código; útil para la calibración y la validación de parámetros. Fundamenta: `DES-D4-08`, `CAL-C4`, `VAL-M-03`.

- **LIT-005** · *Práctica* — Bellini, T. (2019). *IFRS 9 and CECL Credit Risk Modelling and Validation*. Academic Press.

  Cómo pasar de scores a PD lifetime y pérdida esperada contable; base del impacto IFRS 9 y de la PD de vida en pricing. Fundamenta: `DES-D5-01.02`, `PRC-P3-01.02`, `PAR-R3-02`, `PAR-R8`.

- **LIT-006** · *Práctica* — Engelmann, B. y Rauhmeier, R. (eds.) (2011). *The Basel II Risk Parameters: Estimation, Validation, Stress Testing* (2.ª ed.). Springer.

  Referencia técnica para estimar y validar PD/LGD/EAD, incluidas pruebas de calibración por tramo. Fundamenta: `DES-D4-08`, `CAL-C4-03.01.04`, `VAL-M-03`, `U-14`, `PAR-R3`, `PAR-R4`, `PAR-R5`.

- **LIT-007** · *Canon* — Vasicek, O. (2002). The distribution of loan portfolio value. *Risk*, 15(12).

  Origen del modelo de un factor que sustenta los intervalos de Vasicek usados para evaluar la precisión por bucket. Fundamenta: `U-14`, `CAL-C4-03.01.04`, `PAR-R3-02.01`.

- **LIT-008** · *Canon* — Basel Committee on Banking Supervision (2005). *Studies on the Validation of Internal Rating Systems* (Working Paper n.º 14). BIS.

  Marco clásico de validación de discriminación (AUC, Gini, KS) y calibración (binomial, Hosmer-Lemeshow, tráfico de luces). Fundamenta: `VAL-M-03`, `DES-D4-06`.

- **LIT-009** · *Práctica* — Hand, D. J. y Henley, W. E. (1997). Statistical classification methods in consumer credit scoring: a review. *Journal of the Royal Statistical Society: Series A*, 160(3), 523–541.

  Revisión de métodos y de sus trampas (sesgo de selección, definición de malos) que sigue vigente. Fundamenta: `DES-D1-05`, `DES-D4-05`.

- **LIT-010** · *Práctica* — Lessmann, S., Baesens, B., Seow, H.-V. y Thomas, L. C. (2015). Benchmarking state-of-the-art classification algorithms for credit scoring: An update of research. *European Journal of Operational Research*, 247(1), 124–136.

  Evidencia comparativa de algoritmos en scoring; sustenta exigir un benchmark interpretable frente al ML. Fundamenta: `DES-D4-05`, `DES-D4-06`.

- **LIT-011** · *Práctica* — Hosmer, D. W., Lemeshow, S. y Sturdivant, R. X. (2013). *Applied Logistic Regression* (3.ª ed.). Wiley.

  La regresión logística bien hecha: selección, bondad de ajuste e interpretación de coeficientes. Fundamenta: `DES-D4-05`, `VAL-M-03.07`, `CAL-C4-04`, `DES-D4-08.01.07`.

- **LIT-012** · *Práctica* — Kaufman, L. y Rousseeuw, P. J. (1990). *Finding Groups in Data: An Introduction to Cluster Analysis*. Wiley.

  Fuente original de PAM y CLARA, citados en la segmentación no supervisada. Fundamenta: `DES-D3-01.01`.

- **LIT-138** · *Práctica* — Verbraken, T., Bravo, C., Weber, R. y Baesens, B. (2014). Development and application of consumer credit scoring models using profit-based classification measures. *European Journal of Operational Research*, 238(2), 505–513.

  Introduce la métrica de máxima ganancia esperada (EMP) para evaluar scorecards por rentabilidad. Fundamenta: `DES-D4-06.01`, `PRC-P5`, `DES-D5-01.01.03`.

- **LIT-139** · *Práctica* — Kozodoi, N., Katsas, P., Lessmann, S., Moreira-Matias, L. y Papakonstantinou, K. (2019). Shallow self-learning for reject inference in credit scoring. En *ECML PKDD 2019*. Springer.

  Inferencia de rechazados con autoaprendizaje y una forma de evaluarla sin etiquetar artificialmente a los rechazados. Fundamenta: `DES-D1-04.01`.

## Machine learning y explicabilidad

- **LIT-020** · *Canon* — Hastie, T., Tibshirani, R. y Friedman, J. (2009). *The Elements of Statistical Learning* (2.ª ed.). Springer.

  Base teórica de regularización, árboles, boosting, validación cruzada y del compromiso sesgo-varianza. Fundamenta: `DES-D4-05`, `DES-D4-04`.

- **LIT-021** · *Práctica* — Chen, T. y Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *Proceedings of KDD '16*, 785–794.

  El algoritmo de boosting de referencia en el estándar; explica sus hiperparámetros y su importancia por gain. Fundamenta: `DES-D4-05.04`, `U-08`, `U-09`, `U-43`, `DES-D4-05.03.04`.

- **LIT-022** · *Práctica* — Ke, G. et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. *Advances in NeurIPS 30*.

  Alternativa eficiente para bases grandes (millones de filas, cientos de columnas). Fundamenta: `DES-D4-05.03`, `U-43`.

- **LIT-023** · *Práctica* — Bergstra, J. y Bengio, Y. (2012). Random Search for Hyper-Parameter Optimization. *Journal of Machine Learning Research*, 13, 281–305.

  Sustento de la búsqueda aleatoria de hiperparámetros con un mínimo de combinaciones. Fundamenta: `DES-D4-05.04`, `U-10`.

- **LIT-024** · *Práctica* — Kursa, M. B. y Rudnicki, W. R. (2010). Feature Selection with the Boruta Package. *Journal of Statistical Software*, 36(11).

  Método Boruta de selección de variables citado en el estándar. Fundamenta: `DES-D4-05.02`.

- **LIT-025** · *Práctica* — Friedman, J. H. y Popescu, B. E. (2008). Predictive learning via rule ensembles. *The Annals of Applied Statistics*, 2(3), 916–954.

  Define el estadístico H de Friedman para detectar interacciones. Fundamenta: `DES-D4-04.06`.

- **LIT-026** · *Canon* — Lundberg, S. M. y Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in NeurIPS 30*.

  Fundamento de SHAP, exigido para interpretar modelos de ML. Fundamenta: `DES-D4-07`, `FR-03`.

- **LIT-027** · *Canon* — Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. *Nature Machine Intelligence*, 1, 206–215.

  El argumento para preferir modelos interpretables en decisiones de alto impacto como el crédito. Fundamenta: `DES-D4-07`, `DES-D4-06`.

- **LIT-028** · *Frontera* — Lou, Y., Caruana, R., Gehrke, J. y Hooker, G. (2013). Accurate intelligible models with pairwise interactions. *Proceedings of KDD '13*, 623–631.

  Base de los modelos aditivos con interacciones (GA²M / EBM), el benchmark interpretable propuesto en FR-03. Fundamenta: `DES-D4-07`.

- **LIT-029** · *Práctica* — Molnar, C. (2022). *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable* (2.ª ed.). Publicación independiente.

  Guía práctica de interpretabilidad: PDP, ALE, SHAP, contrafactuales y sus limitaciones. Fundamenta: `DES-D4-07`, `PRC-P9-02.03`.

- **LIT-030** · *Canon* — Efron, B. y Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall.

  Fundamento del bootstrap exigido para la estabilidad del desempeño y de los drivers. Fundamenta: `DES-D4-05.05`, `DES-D4-06.03`, `CAL-C4-04.01`, `PRC-P5-02.02`.

- **LIT-031** · *Práctica* — Kapoor, S. y Narayanan, A. (2023). Leakage and the reproducibility crisis in machine-learning-based science. *Patterns*, 4(9).

  Taxonomía de fugas de información (data leakage) que explica muchos Gini "demasiado buenos". Fundamenta: `DES-D4-02`, `DES-D4-06.03.02`, `U-11`, `U-39`, `DES-D1-01.03`, `U-38`, `DES-D4-06.03.05`.

- **LIT-135** · *Práctica* — Gunnarsson, B. R., vanden Broucke, S., Baesens, B., Óskarsdóttir, M. y Lemahieu, W. (2021). Deep learning for credit scoring: Do or don't? *European Journal of Operational Research*, 295(1), 292–305.

  En datos tabulares de crédito, XGBoost supera a las redes profundas a menor costo: sustenta la elección por defecto de boosting. Fundamenta: `DES-D4-05`.

- **LIT-136** · *Frontera* — Chen, Y., Calabrese, R. y Martin-Barragan, B. (2024). Interpretable machine learning for imbalanced credit scoring datasets. *European Journal of Operational Research*, 312(1), 357–372.

  Las explicaciones de SHAP y LIME se vuelven inestables al aumentar el desbalance de clases: obliga a medir su estabilidad. Fundamenta: `DES-D4-07.01`, `VAL-M-05.05`.

- **LIT-137** · *Frontera* — Tu y Wu (2025). Inherently interpretable machine learning for credit scoring: Optimal classification tree with hyperplane splits. *European Journal of Operational Research*, 322(2), 647–664.

  Árboles óptimos interpretables con desempeño competitivo: candidato a benchmark interpretable. Verificar los nombres completos de los autores antes de citar. Fundamenta: `DES-D4-05.03`.

- **LIT-140** · *Práctica* — Dumitrescu, E., Hué, S., Hurlin, C. y Tokpavi, S. (2022). Machine learning for credit scoring: Improving logistic regression with non-linear decision-tree effects. *European Journal of Operational Research*, 297(3).

  Logística penalizada con efectos de árboles: mejora el desempeño sin perder interpretabilidad. Verificar paginación antes de citar. Fundamenta: `DES-D4-05.03`.

- **LIT-145** · *Canon* — Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32.

  Fundamento del ensamble por bagging, una de las cinco familias obligatorias del torneo de modelos. Fundamenta: `DES-D4-05.03.04`, `U-43`.

## Parámetros de riesgo e IFRS 9

- **LIT-110** · *Práctica* — Global Public Policy Committee (2016). *The implementation of IFRS 9 impairment requirements by banks: Considerations for those charged with governance of systemically important banks*. GPPC.

  La guía libre más completa sobre ECL: gobierno, PD, LGD, descuento, staging y forward-looking, escrita por las grandes firmas auditoras. Fundamenta: `PAR`.

- **LIT-111** · *Regulación* — Basel Committee on Banking Supervision (2015). *Guidance on credit risk and accounting for expected credit losses* (d350). BIS.

  Once principios supervisores para medir la pérdida esperada, con un anexo específico para IFRS 9. Fundamenta: `PAR-R1`, `PAR-R8`, `PAR-R9`.

- **LIT-112** · *Regulación* — European Banking Authority (2017). *Guidelines on credit institutions' credit risk management practices and accounting for expected credit losses* (EBA/GL/2017/06).

  Traslada los principios de Basilea a expectativas de supervisión sobre staging, escenarios y gobierno de la ECL. Fundamenta: `PAR-R1`, `PAR-R7`, `PAR-R8`.

- **LIT-113** · *Práctica* — European Banking Authority (2023). *IFRS 9 implementation by EU institutions: Monitoring report* (EBA/Rep/2023/36).

  Hallazgos de benchmarking: los overlays se volvieron estructurales, el backtesting es insuficiente y la variabilidad entre bancos es alta. Fundamenta: `PAR-R8-02`, `PAR-R9-01`, `U-31`.

- **LIT-114** · *Práctica* — European Central Bank (2024). *IFRS 9 overlays and model improvements for novel risks*. ECB Banking Supervision.

  Buenas y malas prácticas para incorporar riesgos nuevos (clima, energía, geopolítica) vía modelo u overlay gobernado. Fundamenta: `PAR-R6-02.01.03`, `PAR-R8-02`, `U-31`.

- **LIT-115** · *Regulación* — European Central Bank (2024, actualizada en 2025). *ECB guide to internal models*. ECB Banking Supervision.

  Expectativas de estimación y calibración de PD y LGD (largo plazo, downturn) que sirven de referencia también para parámetros de gestión. Fundamenta: `PAR-R3`, `PAR-R4`, `U-27`.

- **LIT-116** · *Regulación* — European Banking Authority (2016). *Guidelines on the application of the definition of default* (EBA/GL/2016/07).

  Criterios de default, períodos de prueba para salir de él y tratamiento de reestructurados. Fundamenta: `PAR-R1-02`, `U-33`.

- **LIT-117** · *Frontera* — Bellotti, T. y Crook, J. (2013). Forecasting and stress testing credit card default using dynamic models. *International Journal of Forecasting*, 29(4), 563–574.

  Modelos de supervivencia en tiempo discreto con variables de comportamiento y macro: base de la PD lifetime con forward-looking. Fundamenta: `PAR-R3-02`, `PAR-R6-02`.

- **LIT-118** · *Frontera* — Botha, A. y Verster, T. (2025). *Approaches for modelling the term-structure of default risk under IFRS 9: A tutorial using discrete-time survival analysis*. arXiv:2507.15441.

  Tutorial reciente que compara enfoques de estructura temporal de la PD bajo IFRS 9, con código en R. Fundamenta: `PAR-R3-02`.

- **LIT-119** · *Frontera* — Bellotti, A., Brigo, D., Gambetti, P. y Vrins, F. (2021). Forecasting recovery rates on non-performing loans with machine learning. *International Journal of Forecasting*, 37(1), 428–444.

  Evidencia del uso de machine learning para proyectar recuperaciones de cartera en default. Fundamenta: `PAR-R4-01`, `PAR-R4-02`.

- **LIT-120** · *Práctica* — Loterman, G., Brown, I., Martens, D., Mues, C. y Baesens, B. (2012). Benchmarking regression algorithms for loss given default modeling. *International Journal of Forecasting*, 28(1), 161–170.

  Comparación sistemática de técnicas de regresión para LGD; punto de partida para elegir el modelo. Fundamenta: `PAR-R4-01.02`.

- **LIT-121** · *Frontera* — Kellner, R., Nagl, M. y Rösch, D. (2022). Opening the black box – Quantile neural networks for loss given default prediction. *Journal of Banking & Finance*, 134.

  Modela la distribución completa de la LGD (no solo su media) con redes de cuantiles, útil para escenarios y downturn. Fundamenta: `PAR-R4-01.02`.

- **LIT-122** · *Práctica* — Credicorp Ltd. (varios años). *Annual Report on Form 20-F*, notas sobre pérdida crediticia esperada. U.S. Securities and Exchange Commission.

  Práctica pública del grupo al que pertenece el BCP: PD × LGD × EAD descontada, tres escenarios revisados trimestralmente y SICR mensual. Fundamenta: `PAR-R6-01`, `PAR-R7`, `PAR-R8-01`, `GOB`.

- **LIT-123** · *Regulación* — Superintendencia de Banca, Seguros y AFP (2008). *Reglamento para la Evaluación y Clasificación del Deudor y la Exigencia de Provisiones* (Resolución SBS n.º 11356-2008), y modificatorias.

  Marco de provisiones regulatorias en Perú que convive con IFRS 9; verificar la versión consolidada vigente. Fundamenta: `PAR-R1-01`, `PAR-R9-02.01`.

- **LIT-124** · *Regulación* — IASB (2005, con modificaciones). *IFRS 7 Financial Instruments: Disclosures*. IFRS Foundation.

  Revelaciones exigidas sobre riesgo de crédito y movimientos de la ECL. Fundamenta: `PAR-R8-01.02`.

- **LIT-125** · *Frontera* — European Banking Authority (2025). *Consultation paper on draft Guidelines on the methodology for estimating and applying credit conversion factors* (EBA/CP/2025/10).

  Estado del arte supervisor en CCF: CCF realizado, revolventes y downturn. Verificar si ya se publicó la versión final. Fundamenta: `PAR-R5-02`.

## Calibración e incertidumbre

- **LIT-040** · *Canon* — Niculescu-Mizil, A. y Caruana, R. (2005). Predicting good probabilities with supervised learning. *Proceedings of ICML 2005*, 625–632.

  Muestra que el boosting ordena bien pero calibra mal, y compara Platt con la regresión isotónica. Fundamenta: `DES-D4-08`, `PRC-P4-02.02`, `U-21`.

- **LIT-041** · *Práctica* — Platt, J. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. En *Advances in Large Margin Classifiers*. MIT Press.

  Origen del escalado de Platt para recalibrar scores. Fundamenta: `DES-D4-08`.

- **LIT-042** · *Práctica* — Guo, C., Pleiss, G., Sun, Y. y Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *Proceedings of ICML 2017*.

  Popularizó el ECE y la calibración por temperatura; útil para cualquier modelo complejo. Fundamenta: `DES-D4-08`, `U-21`.

- **LIT-043** · *Práctica* — Brown, L. D., Cai, T. T. y DasGupta, A. (2001). Interval Estimation for a Binomial Proportion. *Statistical Science*, 16(2), 101–133.

  Por qué el intervalo de Jeffreys es preferible al de Wald para tasas de default pequeñas. Fundamenta: `CAL-C4-03.01.04`, `U-14`, `U-21`, `U-30`.

- **LIT-044** · *Frontera* — Angelopoulos, A. N. y Bates, S. (2023). Conformal Prediction: A Gentle Introduction. *Foundations and Trends in Machine Learning*, 16(4), 494–591.

  La introducción más clara a la predicción conforme para estimadores con cobertura garantizada. Fundamenta: `U-12`, `DES-D4-06.01`.

- **LIT-045** · *Frontera* — Romano, Y., Patterson, E. y Candès, E. (2019). Conformalized Quantile Regression. *Advances in NeurIPS 32*.

  Intervalos conformes que se adaptan a la dispersión de cada cliente. Fundamenta: `U-12`.

- **LIT-046** · *Canon* — Vovk, V., Gammerman, A. y Shafer, G. (2005). *Algorithmic Learning in a Random World*. Springer.

  Fundamento teórico de la predicción conforme. Fundamenta: `U-12`.

- **LIT-144** · *Canon* — Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3.

  Origen del Brier score, la medida de exactitud de probabilidades que se exige reportar en el torneo y en la calibración. Fundamenta: `DES-D4-06.03.05`, `DES-D4-08.01.07`.

## Estabilidad, monitoreo y MLOps

- **LIT-050** · *Práctica* — Yurdakul, B. (2018). *Statistical Properties of Population Stability Index* (tesis doctoral). Western Michigan University.

  Estudia la distribución del PSI y su dependencia del tamaño muestral y del binning; sustenta umbrales ajustados por muestra. Fundamenta: `U-02`, `DES-D2-01.06`, `IMP-01.04`.

- **LIT-051** · *Práctica* — Lin, J. (1991). Divergence measures based on the Shannon entropy. *IEEE Transactions on Information Theory*, 37(1), 145–151.

  Define la divergencia de Jensen–Shannon, complemento simétrico y acotado del PSI. Fundamenta: `U-02`.

- **LIT-052** · *Práctica* — Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M. y Bouchachia, A. (2014). A survey on concept drift adaptation. *ACM Computing Surveys*, 46(4).

  Distingue drift de datos y de concepto, clave para decidir entre calibrar y redesarrollar. Fundamenta: `CAL-C1-01.01`, `PRC-P8-01.03`.

- **LIT-053** · *Canon* — Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning Systems. *Advances in NeurIPS 28*.

  Por qué el modelo es la parte pequeña del sistema; fundamenta los controles de implementación. Fundamenta: `IMP`, `PRC-P7-02`.

- **LIT-054** · *Práctica* — Breck, E., Cai, S., Nielsen, E., Salib, M. y Sculley, D. (2017). The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction. *IEEE International Conference on Big Data*.

  Lista de pruebas de datos, modelo e infraestructura que inspira la certificación automatizada. Fundamenta: `IMP-01.06`, `PRC-P7-02.02`.

- **LIT-055** · *Canon* — Mann, H. B. (1945). Nonparametric tests against trend. *Econometrica*, 13(3), 245–259.

  Prueba de Mann–Kendall usada para la estabilidad de los valores faltantes. Fundamenta: `DES-D2-01.04`.

- **LIT-056** · *Práctica* — Basel Committee on Banking Supervision (2013). *Principles for effective risk data aggregation and risk reporting* (BCBS 239). BIS.

  Principios de calidad, trazabilidad y oportunidad de los datos de riesgo. Fundamenta: `DES-D2`, `PRC-P2-02`.

- **LIT-133** · *Práctica* — Kiritz, N., Ravitz, M. y Levonian, M. (2019). Model risk tiering: an exploration of industry practices and principles. *Journal of Risk Model Validation*, 13(2).

  Prácticas de la industria para categorizar modelos, escrito por exsupervisores (uno de ellos lideró SR 11-7). Fundamenta: `GOB-G2`, `FR-02`.

## Inferencia causal y experimentación

- **LIT-060** · *Canon* — Angrist, J. D. y Pischke, J.-S. (2009). *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press.

  Variables instrumentales, discontinuidad de regresión y diferencias en diferencias aplicadas a la identificación de la elasticidad. Fundamenta: `PRC-P4-01`.

- **LIT-061** · *Canon* — Imbens, G. W. y Rubin, D. B. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences: An Introduction*. Cambridge University Press.

  El marco de resultados potenciales que ordena cualquier discusión sobre el efecto del precio. Fundamenta: `PRC-P4-01`, `PRC-P6`.

- **LIT-062** · *Frontera* — Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E., Hansen, C., Newey, W. y Robins, J. (2018). Double/debiased machine learning for treatment and structural parameters. *The Econometrics Journal*, 21(1), C1–C68.

  Double ML para estimar la elasticidad con muchos controles sin sesgo de regularización. Fundamenta: `PRC-P4-01.01`.

- **LIT-063** · *Frontera* — Wager, S. y Athey, S. (2018). Estimation and Inference of Heterogeneous Treatment Effects using Random Forests. *Journal of the American Statistical Association*, 113(523), 1228–1242.

  Causal forests para elasticidades heterogéneas por cliente con intervalos de confianza. Fundamenta: `PRC-P4-02.01`.

- **LIT-064** · *Canon* — Kohavi, R., Tang, D. y Xu, Y. (2020). *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*. Cambridge University Press.

  Diseño, potencia, métricas de resguardo y errores frecuentes (mirar antes de tiempo) en experimentos. Fundamenta: `PRC-P6`, `U-22`.

- **LIT-065** · *Práctica* — Cunningham, S. (2021). *Causal Inference: The Mixtape*. Yale University Press.

  Introducción aplicada y accesible a los métodos de identificación, con código. Fundamenta: `PRC-P4-01`.

## Pricing y revenue management

- **LIT-070** · *Canon* — Phillips, R. L. (2021). *Pricing and Revenue Optimization* (2.ª ed.). Stanford University Press.

  El texto de referencia en optimización de precios: curvas de respuesta, segmentación y precio personalizado. Fundamenta: `PRC-P4`, `PRC-P5`.

- **LIT-071** · *Canon* — Phillips, R. L. (2018). *Pricing Credit Products*. Stanford University Press.

  El único tratado específico de pricing de crédito al consumo: riesgo, respuesta, regulación y ejecución. Fundamenta: `PRC`.

- **LIT-072** · *Canon* — Talluri, K. T. y van Ryzin, G. J. (2004). *The Theory and Practice of Revenue Management*. Springer.

  Fundamentos de revenue management y de la optimización con restricciones de capacidad. Fundamenta: `PRC-P5-01`.

- **LIT-073** · *Práctica* — Gallego, G. y Topaloglu, H. (2019). *Revenue Management and Pricing Analytics*. Springer.

  Modelos de elección y optimización de precios con enfoque analítico moderno. Fundamenta: `PRC-P4-02`, `PRC-P5`.

- **LIT-074** · *Práctica* — Bodea, T. y Ferguson, M. (2014). *Segmentation, Revenue Management and Pricing Analytics*. Routledge.

  Puente práctico entre segmentación, respuesta y optimización, con casos. Fundamenta: `PRC-P4`, `PRC-P5`.

- **LIT-075** · *Práctica* — Matten, C. (2000). *Managing Bank Capital: Capital Allocation and Performance Measurement* (2.ª ed.). Wiley.

  Asignación de capital y RAROC, base del cargo por capital del precio técnico. Fundamenta: `PRC-P3-01.04`, `PRC-P3-02.01`, `U-18`.

- **LIT-076** · *Práctica* — Hull, J. C. (2018). *Risk Management and Financial Institutions* (5.ª ed.). Wiley.

  Capital económico, precios de transferencia y medidas de rentabilidad ajustada por riesgo en contexto bancario. Fundamenta: `PRC-P3-01.01`, `PRC-P3-01.04`.

- **LIT-077** · *Frontera* — den Boer, A. V. (2015). Dynamic pricing and learning: Historical origins, current research, and new directions. *Surveys in Operations Research and Management Science*, 20(1), 1–18.

  Revisión del precio con aprendizaje (explorar vs. explotar), base de los bandits de precio. Fundamenta: `PRC-P6`, `PRC-P4-02`.

- **LIT-078** · *Frontera* — Lattimore, T. y Szepesvári, C. (2020). *Bandit Algorithms*. Cambridge University Press.

  Teoría de bandits contextuales para el precio individual en canales digitales. Fundamenta: `PRC-P6`.

## Equidad y conducta

- **LIT-080** · *Canon* — Barocas, S., Hardt, M. y Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press.

  El marco completo de criterios de equidad y sus límites. Fundamenta: `DES-D4-10`, `PRC-P9-02.02`, `VAL-P-04.02`.

- **LIT-081** · *Práctica* — Hardt, M., Price, E. y Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in NeurIPS 29*.

  Define igualdad de oportunidades, una de las métricas propuestas en FR-06. Fundamenta: `DES-D4-10`.

- **LIT-082** · *Práctica* — Kleinberg, J., Mullainathan, S. y Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*.

  Demuestra que calibración e igualdad de errores no pueden cumplirse a la vez: obliga a elegir y documentar. Fundamenta: `DES-D4-10`, `PRC-P9-02.02`.

- **LIT-083** · *Frontera* — Fuster, A., Goldsmith-Pinkham, P., Ramadorai, T. y Walther, A. (2022). Predictably Unequal? The Effects of Machine Learning on Credit Markets. *The Journal of Finance*, 77(1), 5–47.

  Evidencia de cómo el ML redistribuye acceso y precio del crédito entre grupos. Fundamenta: `DES-D4-10`, `PRC-P9-02.02`.

- **LIT-134** · *Práctica* — Kozodoi, N., Jacob, J. y Lessmann, S. (2022). Fairness in credit scoring: Assessment, implementation and profit implications. *European Journal of Operational Research*, 297(3), 1083–1094.

  Muestra que la discriminación puede reducirse a costo bajo y propone la separación como criterio de equidad para scorecards. Fundamenta: `DES-D4-10.01`, `PRC-P9-02.02`.

## IA generativa, agentes y gobierno de la IA

- **LIT-090** · *Canon* — Mitchell, M. et al. (2019). Model Cards for Model Reporting. *Proceedings of FAT\* 2019*, 220–229.

  Origen de las model cards; base de la ficha técnica del modelo. Fundamenta: `DES-D1-01.04.08`, `DES-D7-01.01`.

- **LIT-091** · *Práctica* — Gebru, T. et al. (2021). Datasheets for Datasets. *Communications of the ACM*, 64(12), 86–92.

  Documentar el origen, la composición y los límites de cada base, como en el diccionario de datos. Fundamenta: `DES-D2-01.01`, `PRC-P2-02`.

- **LIT-092** · *Frontera* — Yao, S. et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. *ICLR 2023*.

  El patrón razonar-actuar sobre herramientas que siguen los agentes que ejecutan este estándar. Fundamenta: `FR-08`, `PRC-P9-03`.

- **LIT-093** · *Práctica* — Schluntz, E. y Zhang, B. (2024). *Building effective agents*. Anthropic.

  Patrones simples y componibles para agentes (flujos, orquestador-trabajadores, evaluador-optimizador) y cuándo no usar agentes. Fundamenta: `PRC-P9-03`, `FR-08`.

- **LIT-094** · *Regulación* — NIST (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)* (NIST AI 100-1).

  Marco de gestión de riesgos de IA (gobernar, mapear, medir, gestionar) aplicable a agentes. Fundamenta: `FR-08`, `PRC-P9-03`.

- **LIT-095** · *Regulación* — NIST (2024). *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile* (NIST AI 600-1).

  Riesgos específicos de la IA generativa (confabulación, seguridad de la información) y controles sugeridos. Fundamenta: `FR-08`.

- **LIT-096** · *Regulación* — ISO/IEC 42001:2023. *Information technology — Artificial intelligence — Management system*.

  Norma certificable de sistema de gestión de IA; útil para formalizar el gobierno de agentes. Fundamenta: `FR-08`.

- **LIT-141** · *Frontera* — Beas y Díaz (2024). Documento de trabajo sobre modelos de lenguaje para predecir riesgo de crédito de consumo en Chile. Comisión para el Mercado Financiero (CMF).

  Evidencia temprana: LLMs ajustados alcanzan un desempeño cercano a LightGBM, pero sus explicaciones no siempre se alinean con los datos. Verificar título y publicación. Fundamenta: `FR-08`.

- **LIT-142** · *Práctica* — BBVA (s. f.). *BBVA's eight responsible AI principles* y *Responsible innovation: how BBVA ensures safe use of artificial intelligence*. bbva.com.

  Práctica pública de un banco de referencia: inventario y monitoreo de sistemas de IA y principios traducidos en controles. Fundamenta: `GOB-G4-02`.

## Regulación y supervisión

- **LIT-100** · *Regulación* — Board of Governors of the Federal Reserve System y Office of the Comptroller of the Currency (2011). *Supervisory Guidance on Model Risk Management* (SR 11-7). Reemplazada en abril de 2026 por SR 26-2 (LIT-130).

  La guía fundacional de riesgo de modelo: desarrollo, validación con effective challenge y gobierno. Fundamenta: `VAL`, `DES-D7`, `FR-01`.

- **LIT-101** · *Regulación* — Prudential Regulation Authority (2023). *Model risk management principles for banks* (SS1/23). Bank of England.

  Principios modernos de MRM que incluyen explícitamente ML y modelos de terceros. Fundamenta: `VAL`, `DES-D7`, `FR-01`, `FR-02`.

- **LIT-102** · *Regulación* — Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, de 13 de junio de 2024, por el que se establecen normas armonizadas en materia de inteligencia artificial.

  Clasifica el scoring de personas naturales como IA de alto riesgo y fija obligaciones de datos, documentación y supervisión humana. Fundamenta: `FR-01`, `FR-06`, `PRC-P9-02`.

- **LIT-103** · *Regulación* — IASB (2014). *IFRS 9 Financial Instruments*. IFRS Foundation.

  Pérdida esperada contable; define el impacto en provisiones de cada modelo. Fundamenta: `DES-D5-01.02`, `PAR-R7`, `PAR-R8`.

- **LIT-104** · *Regulación* — European Banking Authority (2017). *Guidelines on PD estimation, LGD estimation and the treatment of defaulted exposures* (EBA/GL/2017/16).

  Criterios de estimación y margen de conservadurismo para parámetros regulatorios. Fundamenta: `DES-D4-08`, `FR-04`, `PAR-R3`, `PAR-R4`.

- **LIT-105** · *Regulación* — European Central Bank (2019). *Instructions for reporting the validation results of internal models: IRB Pillar I models for credit risk*.

  Batería estándar de pruebas de validación, incluido el test de Jeffreys por grado. Fundamenta: `VAL-M-03`, `FR-04`, `U-14`, `PAR-R3-03`, `U-30`.

- **LIT-106** · *Regulación* — Basel Committee on Banking Supervision (2017). *Basel III: Finalising post-crisis reforms*. BIS.

  Requerimientos de capital que determinan el consumo de capital en el precio técnico. Fundamenta: `PRC-P3-01.04`.

- **LIT-107** · *Regulación* — Superintendencia de Banca, Seguros y AFP (2017). *Reglamento de Gobierno Corporativo y de la Gestión Integral de Riesgos* (Resolución SBS n.º 272-2017), y modificatorias.

  Marco local de gestión integral de riesgos; verificar la versión vigente y las normas específicas de riesgo de modelo. Fundamenta: `DES-D7`, `VAL`.

- **LIT-108** · *Regulación* — Congreso de la República del Perú (2021). *Ley n.º 31143, Ley que protege de la usura a los consumidores de los servicios financieros*.

  Faculta al BCRP a fijar tasas máximas en ciertos créditos; origen del control U-24 en Perú. Verificar la reglamentación vigente. Fundamenta: `U-24`, `PRC-P9-02.01`.

- **LIT-130** · *Regulación* — Board of Governors of the Federal Reserve System, OCC y FDIC (2026). *Revised Guidance on Model Risk Management* (SR 26-2; OCC Bulletin 2026-13; FDIC FIL-15-2026).

  Reemplaza a SR 11-7 con un enfoque basado en riesgo y una sección de modelos de terceros; excluye la IA generativa y agéntica, que este estándar cubre con AGT. Fundamenta: `GOB`, `VAL`, `FR-01`.

- **LIT-131** · *Regulación* — Superintendencia de Banca, Seguros y AFP (2023). *Reglamento de Gestión de Riesgos de Modelo* (Resolución SBS n.º 00053-2023).

  La norma peruana de riesgo de modelo: categorización, comité trimestral, aprobación previa, réplica, forzajes, terceros y requisitos de IA. Base obligatoria de la línea base 2.0 en Perú. Fundamenta: `GOB`, `VAL-M-05`, `SEG`, `DES-D7`, `U-35`.

- **LIT-132** · *Regulación* — European Banking Authority (2023). *Follow-up report on the use of machine learning for internal ratings-based models* (EBA/REP/2023/28).

  Recomendaciones para un uso prudente del ML en modelos de crédito: explicabilidad, sobreajuste e interacción con el AI Act y el GDPR. Fundamenta: `DES-D4-05`, `DES-D4-07`, `VAL-M-05.05`.

- **LIT-143** · *Práctica* — JPMorgan Chase & Co. (2025). *Annual Report on Form 10-K 2024*, sección de gestión del riesgo de modelo. U.S. Securities and Exchange Commission.

  Práctica pública: función independiente de gobierno y revisión de modelos (MRGR), riesgo de modelo a cargo del usuario e inclusión de modelos de ML/IA. Fundamenta: `GOB-G1`.


<!-- CATALOGO:FIN -->
