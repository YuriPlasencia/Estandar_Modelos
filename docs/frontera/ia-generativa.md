---
id: FR-08
titulo: "FR-08 · IA generativa y agentes en el ciclo de vida"
estandar: Frontera
estado: Propuesta
version: 0.1.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 58
---

# FR-08 · IA generativa y agentes en el ciclo de vida

Dos frentes distintos:

## A. Los LLM como **modelos** sujetos a este estándar

Un LLM que clasifica reclamos, extrae datos de estados financieros o sugiere decisiones de crédito **es un
modelo** y debe estar en el inventario. Diferencias con un score clásico:

| Aspecto | Score clásico | LLM |
|---|---|---|
| Desarrollo | Entrenamiento propio | Selección de proveedor + *prompt* / RAG / *fine-tuning* |
| Validación | Gini, KS, calibración | Conjuntos de evaluación etiquetados, exactitud por tarea, tasa de alucinación, robustez a *prompts* adversarios |
| Estabilidad | PSI de variables | Cambios de versión del proveedor, deriva de los textos de entrada |
| Implementación | Script productivo | *Prompt* versionado, *guardrails*, registro de entradas/salidas |
| Seguimiento | Desempeño de cosechas | Muestreo humano periódico de salidas |

**Propuesta:** un perfil de estándar "Modelos de IA generativa" que reutilice D1 (caso de uso, factibilidad),
D2 (calidad de documentos fuente), D5 (impactos) e IMP, y reemplace D3–D4 por *diseño de evaluación*.
Tier mínimo II si decide sobre clientes.

## B. Los agentes como **asistentes** del equipo de modelos

Este repositorio está preparado para eso (ver `AGENTS.md`). Usos de alto valor y bajo riesgo:

1. **Checklist automático:** dado Tier, tipo y enfoque, generar la lista de actividades y entregables.
2. **Revisión previa a validación:** contrastar el documento metodológico contra los IDs de `val.yaml` y listar faltantes.
3. **Redacción asistida** de documentación técnica a partir de logs y salidas de scripts.
4. **Consulta de umbrales** con cita obligatoria del ID (`U-xx`).

**Reglas:** el agente cita IDs, no inventa umbrales, no aprueba nada, y su salida la firma una persona.
