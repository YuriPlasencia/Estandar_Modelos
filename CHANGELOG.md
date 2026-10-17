# Registro de cambios

Yuri Plasencia — Analytics Pricing & Revenue Management

El proyecto usa versionado semántico sobre el estándar completo (ver `CONTRIBUTING.md`).

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
