# Cómo proponer un cambio al estándar

Yuri Plasencia — Analytics Pricing & Revenue Management

El estándar crece por **propuestas pequeñas y trazables**. Cualquier analista puede proponer; el custodio aprueba.

## Tipos de cambio y versión

Se usa versionado semántico sobre el estándar completo (`CHANGELOG.md`):

| Cambio | Ejemplo | Versión |
|---|---|---|
| **Mayor** | Nueva obligación para todos los Tier, cambio de un umbral | `3.0.0` |
| **Menor** | Nuevo requisito opcional, nueva plantilla, propuesta de frontera aprobada | `2.1.0` |
| **Parche** | Redacción, ortografía, enlaces | `2.0.1` |

## Proceso

1. **Abrir la propuesta** (rama o carpeta de borrador) con: problema, cambio propuesto, requisito(s) afectados por ID,
   evidencia (piloto, literatura, regulación) e impacto en esfuerzo.
2. **Editar la fuente correcta:**
   - Un requisito → `catalogo/<fase>.yaml`. **Nuevo ID al final de su subtarea**; nunca renumerar ni reutilizar IDs.
   - Un umbral → `catalogo/umbrales.yaml` (con `refs`).
   - Explicación → `docs/...md`. No edites a mano lo que está entre `<!-- CATALOGO:INICIO -->` y `<!-- CATALOGO:FIN -->`.
   - Idea de vanguardia → `docs/frontera/` con `estado: Propuesta`.
3. **Ejecutar** `python tools/build.py`. Debe terminar sin errores.
4. **Revisión:** un par técnico + el custodio. Si cambia obligaciones de segunda línea, también Validación.
5. **Publicar:** actualizar `CHANGELOG.md`, la `version` y `actualizado` del documento.

## Retirar un requisito

No se borra: se marca `retirado: "AAAA-MM-DD — motivo"`. El build lo excluye del planificador pero el ID
queda reservado para la trazabilidad histórica de modelos ya aprobados.
