# Registro de cambios

Yuri Plasencia — Analytics Pricing & Revenue Management

El proyecto usa versionado semántico sobre el estándar completo (ver `CONTRIBUTING.md`).

## [3.0.1] — 2026-10-17

### Corregido
- «Ficha de nacimiento» pasa a **Ficha técnica del modelo (Model Card)**, el término de la literatura y de la banca;
  su creación se describe como el **registro inicial en el inventario de modelos** (Res. SBS 00053-2023, art. 5).
  La página se mueve a `docs/plantillas/ficha-tecnica.md`.

## [3.0.0] — 2026-10-17

### Cambiado (incompatible)
- **Tres Tiers (I, II, III) en lugar de cuatro.** Tier III y Tier IV tenían exactamente los mismos requisitos,
  umbrales y frecuencia de validación, así que se fusionan en Tier III en todo el estándar: `aplica_tier` del
  catálogo, U-35 (`tier_III_anios`), SEG-S1-01.01.02, PRC-P6-02.02.01, planificador, plantillas y herramientas.
- Se aclara que **el número de Tiers lo aprueba el comité de riesgos de modelo**: ni la Res. SBS 00053-2023 (art. 6)
  ni SR 26-2, PRA SS1/23 u OSFI E-23 fijan un número; la práctica de mercado usa tres o cuatro niveles. Una entidad
  con otra escala documenta su correspondencia con I–III.
- La propuesta de puntaje de tiering (FR-02) pasa a tres cortes: I ≥ 75, II 55–74, III < 55.
- Compatibilidad: `tools/verificar.py`, `tools/documento.py`, el modelo de esfuerzo y el planificador aceptan «4» o
  «IV» de versiones anteriores como Tier III.

## [2.4.0] — 2026-10-17

### Cambiado
- **Ventana OOT (U-01):** el OOT es solo el **último mes con desempeño completo** (la cosecha más reciente que ya
  cumple los 12 meses de U-17), posterior a Train/Test; ya no se acumulan 6 meses. Train/Test sigue con un mínimo de
  12 meses. La estabilidad en el tiempo se evalúa mes a mes dentro de Train/Test y luego en el seguimiento.
- Alineados DES-D1-03.01.02, el acta de ventana, D1, el glosario, la ficha de nacimiento, el MODEL_CARD y el
  documento metodológico (evaluación de U-01, plantilla, gráfico de estabilidad y ejemplo).

## [2.3.1] — 2026-10-17

### Corregido
- Las duraciones citadas en el texto (D1, D4, Implementación y Calibración) se calculan ahora con el modelo de esfuerzo
  anclado a U-40 durante el build (`<!--DUR:...-->`), en lugar de escribirse a mano; quedaban con el modelo anterior.
- D1 ya no se describe como la fase de mayor esfuerzo: lo es Modelamiento (D4).
- Los sprints (Sprint 0 a Sprint 20) se definen como secuencia de paquetes de trabajo de unos 3 días hábiles para
  caber en las 13 semanas de U-40; las revisiones SME 1–13 son semanales.
- README con 541 requisitos y 40 umbrales. El build falla si el README o CITATION.cff no coinciden con el catálogo
  o con la versión.
- `tools/verificar.py` y el documento metodológico evalúan U-40; el documento muestra el enfoque como ágil o completo.
- El estándar de agentes de IA cita la meta de 15 días hábiles y cómo no lograrla saltando controles.

## [2.3.0] — 2026-10-17

### Nuevo
- **Plazo máximo de desarrollo (U-40):** un modelo de Desarrollo se termina con 2 personas en un máximo de 13 semanas
  (3 meses) y, con agentes de IA, en un máximo de 15 días hábiles. Superarlo requiere sustento ante el Comité.
- **Anclaje del modelo de esfuerzo a U-40:** los días del catálogo pasan a ser pesos relativos y el nivel absoluto se
  fija para que el caso más exigente (Desarrollo Tier I, lineal, completo) dure exactamente la meta; el escenario base
  pasa a 2 personas. El planificador muestra si cada caso cumple la meta y la duración con agentes en días hábiles.

### Cambiado
- El enfoque **tradicional** pasa a llamarse **completo** y se redefinen ambos: *ágil* cubre lo esencial con la
  profundidad mínima suficiente; *completo* es el análisis exhaustivo y detallado. Los dos aplican los mismos
  requisitos y umbrales; cambia la profundidad, no lo que se exige.
- La clave `tradicional` de `dias_esfuerzo` se renombra a `completo` en el catálogo y en `dist/catalogo.json`.
  `tools/verificar.py`, `tools/documento.py`, el modelo de esfuerzo y el planificador del sitio siguen aceptando
  `tradicional` como alias.

## [2.2.0] — 2026-10-17

### Nuevo
- **Plantilla dinámica del documento metodológico** (DES-D4-11.01.07): los datos del modelo se registran en
  `docs/documento.yaml` y `tools/documento.py` genera Markdown, HTML, Word y PDF (y Quarto, opcional) desde la
  misma fuente, con Jinja2, Pandoc y Typst.
- El documento evalúa los umbrales obtenidos con las reglas de `tools/verificar.py`, arma la matriz de
  cumplimiento desde `evidencias.yaml`, grafica la estabilidad del Gini, alerta variables con IV mayor a 0.50 y
  marca como «Completar» lo que falta, citando el requisito que lo exige.
- Página `docs/plantillas/documento-metodologico.md`, ejemplo ficticio completo y objetivo `make documento` en la
  plantilla del repositorio de un modelo.

## [2.1.0] — 2026-10-17

### Nuevo
- **No anticipación temporal del tablón** (U-39): toda variable se construye solo con información anterior a la fecha
  de observación; cada variable documenta su fecha de referencia y el desfase de su fuente, con prueba automática
  (DES-D1-01.03.04, DES-D1-01.03.05).
- **Orden obligatorio antes de entrenar**: análisis univariado (DES-D4-03.02.02) y bivariado con WOE/IV (DES-D4-03.03.02),
  sospecha de fuga para variables con IV mayor a 0.50 (DES-D4-03.03.03, U-38) y filtro de variables confiables con
  embudo documentado (DES-D4-03.03.04).
- Validación verifica no anticipación y fuga (VAL-M-05.07, bloqueante). `tools/verificar.py` comprueba U-38 y U-39.

## [2.0.0] — 2026-10-17 · Línea base (primera versión pública)

Primera publicación del estándar como documentación como código. Constituye la **línea base** contra la que se
medirán los cambios futuros. El detalle del benchmarking está en `docs/marco/linea-base.md`.

### Estándares
- **Gobierno del riesgo de modelo (GOB)**, 21 requisitos a nivel de entidad, mapeados artículo por artículo a la
  Res. SBS 00053-2023 y alineados con SR 26-2 y PRA SS1/23.
- **Desarrollo (DES)**, **Calibración (CAL)** e **Implementación (IMP)**, con controles de benchmark interpretable,
  validación cruzada, sensibilidad, equidad, forzajes, inferencia de rechazados y aprobación previa al uso.
- **Seguimiento (SEG)**: indicadores y umbrales aprobados por comité, forzajes, sobreajuste en IA, árbol de decisión e informe periódico.
- **Validación (VAL)**: metodológica, de implementación, de parámetros (VAL-R) y de pricing (VAL-P), con réplica,
  challenger, periodicidad por categoría y severidad de hallazgos.
- **Parámetros de riesgo (PAR)**: PD 12 meses y lifetime, LGD, EAD/CCF, escenarios, staging, ECL, overlays, backtesting y CLV.
- **Pricing analítico (PRC)**: precio técnico y RAROC, respuesta al precio con identificación causal, optimización,
  experimentación, motor de precios, seguimiento y conducta.
- **Agentes de IA (AGT)**: principios, puntos de control humanos, condiciones de detención, contrato de tarea y evaluación.
- **Frontera**: propuestas no obligatorias (marco regulatorio, tiering, explicabilidad, calibración e incertidumbre,
  drift, equidad, MLOps e IA generativa).

### Datos y herramientas
- 37 umbrales cuantitativos (U-01 a U-37) enlazados a sus requisitos.
- 103 obras de literatura enlazadas a requisitos y umbrales.
- 27 tipos de acta precargados por hito; editor en línea y exportación a Word y Markdown (`tools/acta.py`).
- Modelo de esfuerzo con volumen de datos, reuniones, equipo y escenario con agente de IA.
- Verificador de evidencias (`tools/verificar.py`) y plantilla de repositorio de modelo.
- Sitio autocontenido con buscador, planificador y editor de actas; JSON y `llms.txt` para agentes.
