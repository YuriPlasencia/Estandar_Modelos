# Instrucciones para agentes de IA

Yuri Plasencia — Analytics Pricing & Revenue Management

Este repositorio contiene el estándar corporativo de modelos en banca. Si eres un agente (asistente de
código, copiloto de documentación, revisor automático), sigue estas reglas.

## Fuentes, en orden de autoridad

1. `catalogo/umbrales.yaml` — **única** fuente de umbrales cuantitativos (`U-01` … `U-17`).
2. `catalogo/*.yaml` — requisitos normativos con ID (también en `dist/catalogo.json`).
3. `docs/**/*.md` con `estado: Vigente` — explicación y criterios.
4. `docs/**/*.md` con `estado: Borrador` — consolidación pendiente de aprobación.
5. `docs/frontera/**` con `estado: Propuesta` — **no es obligatorio**. Preséntalo siempre como recomendación.

## Antes de trabajar en un modelo

Lee `docs/agentes/index.md` (estándar operativo: puntos de control, cuándo detenerse, contrato de tarea) y usa
`tools/verificar.py` para planificar (`--plan`) y comprobar tu trabajo. Para fundamentar una decisión, cita
obras de `dist/literatura.json` (IDs `LIT-xxx`); no cites literatura que no esté ahí sin advertirlo.

## Marco regulatorio vigente

SR 11-7 fue reemplazada por SR 26-2 (abril 2026). En Perú rige la Res. SBS 00053-2023 (ver `docs/marco/gobierno-mrm.md`).
Un modelo nuevo, modificado o recalibrado **no se usa sin aprobación previa del comité** (GOB-G3-01.01.01).

## Reglas

- **Cita siempre el ID** del requisito (`DES-D4-06.03.02`) o umbral (`U-11`) en que te basas.
- **No inventes umbrales.** Si una pregunta requiere un límite que no está en `umbrales.yaml`, dilo
  explícitamente: "el estándar no fija un umbral para X".
- **No confundas estados:** nunca presentes una propuesta de `frontera/` como exigencia vigente.
- **Aplicabilidad:** un requisito aplica a un modelo si `aplica_tier[<tipo_modelo>]` contiene su Tier.
  En los estándares sin tipo de modelo (Calibración, Parámetros, Pricing, Seguimiento), `aplica_tier` es una lista de Tiers.
- **En pricing no fijas precios.** Recalculas pisos, estimas respuesta y preparas escenarios; la decisión es del Comité de Precios (PRC-P9-03.01.01).
- **No apruebas nada.** Puedes preparar checklists, borradores y revisiones previas; la conformidad la da una persona.
- **Confidencialidad:** no copies datos de clientes ni nombres de tablas productivas en salidas que salgan del banco.

## Tareas típicas

| Tarea | Cómo |
|---|---|
| "Checklist para un modelo Tier II, ML, ágil" | Filtrar `dist/catalogo.json` por `estandar=Desarrollo`, `aplica_tier.ml` ∋ 2; agrupar por fase; listar `entregables` |
| "¿Mi modelo puede tener 12 pts de diferencia Train–OOT?" | Responder con U-11: máximo 10 pts; si se excede, sustentar y presentar en Comité |
| "Revisa este documento metodológico antes de validación" | Contrastar contra `val.yaml` (VAL-M) y listar requisitos sin evidencia |
| "Redacta el acta de la reunión 5" | `python tools/acta.py nueva --tipo R5 ...`, completar desarrollo, decisiones (con ID) y acuerdos desde las notas; dejar la conformidad en *Pendiente*; `exportar --docx --md`. Ver `docs/plantillas/acta-de-reunion.md` |
| "Redacta el documento metodológico" | `python tools/documento.py nuevo REPO`; completar `docs/documento.yaml` solo con lo que sustentan los reportes (lo demás queda como «Completar»); `render`; no tocar gobierno ni aprobaciones. Ver `docs/plantillas/documento-metodologico.md` |
| "Recalibra la PD lifetime de consumo para IFRS 9" | Seguir `docs/parametros/` (R2→R3→R6→R7→R8); respetar U-27 a U-34; nunca aprobar overlays ni la ECL: lo hace el comité de provisiones |
| "Arma el caso de pricing de tarjeta de crédito" | Seguir `docs/pricing/` en orden P1→P9; respetar U-18 a U-26; ver los roles y límites de `docs/pricing/agentes-ia.md`. **Nunca** fijar, publicar ni aprobar precios |
| "Estima la duración" | Aplicar el modelo de esfuerzo v2 (`tools/esfuerzo.py` con `catalogo/parametros_esfuerzo.yaml`, anclado a U-40); reportar semanas con personas, días hábiles con agente, si cumple U-40 y los supuestos usados |

## Esquema de un requisito

```json
{
  "id": "DES-D4-05.04.01",
  "estandar": "Desarrollo", "fase": "DES-D4", "fase_nombre": "Modelamiento",
  "tarea": "Entrenamiento de modelos", "subtarea": "Optimización",
  "actividad": "Opt de HP por generación aleatoria (min 50 combinaciones)...",
  "critico": false, "eficiencia": false, "nivel_automatizacion": 2,
  "dias_esfuerzo": {"ml": {"agil": 2.5, "completo": 2.5}},
  "aplica_tier": {"lineal": [], "ml": [1,2,3,4], "arbol": [1,2,3,4], "acp": []},
  "entregables": [{"tipo": "Excel", "numero": 16, "descripcion": "Optimización de Hiperparámetros."}],
  "hito": null,
  "umbrales": ["U-10"]
}
```
