---
id: PLT-ACTA
titulo: "Plantilla · Acta de reunión"
estandar: Plantillas
estado: Vigente
version: 2.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 61
---

# Plantilla · Acta de reunión

Las actas son la evidencia principal que pide Validación (VAL-M-01.03 a VAL-M-01.11). Un acta sirve como
evidencia solo si deja **decisiones explícitas, quién las tomó y su conformidad**. Esta plantilla lo asegura con
una estructura fija de 11 secciones y un tipo de acta precargado para cada hito del estándar.

## Dónde se crean

| Quién | Herramienta | Resultado |
|---|---|---|
| **Analista** | Sitio › Herramientas › **Actas de reunión** | Edición en línea con guardado automático; descarga en Word (.docx) y Markdown |
| **Agente de IA o analista en el repositorio** | `python tools/acta.py` | Acta en JSON versionable en Git, exportable a .docx y .md |
| **Agente con acceso al sitio** | Escribe el JSON en la colección `actas` del sitio | Aparece en el editor para que el equipo la complete y apruebe |

Las tres vías usan el **mismo esquema** (`dist/acta.schema.json`) y el mismo diseño de documento.

## Estructura del acta

1. **Datos generales.** N° de acta, modelo (código de inventario, nombre, Tier, tipo), fecha, horario, modalidad, lugar y secretario.
2. **Participantes.** Nombre, área, rol (*Decide, Aprueba, Consultado, Informado, Secretario*) y asistencia.
3. **Objetivo.**
4. **Agenda.**
5. **Desarrollo de la reunión.** Qué se presentó, con qué datos y qué se discutió.
6. **Decisiones.** Cada una enlazada al **requisito o umbral** que la exige, con su responsable y estado.
7. **Excepciones a umbrales.** Umbral (`U-xx`), valor obtenido, justificación y si va a Comité.
8. **Acuerdos y pendientes.** Acción, responsable, fecha compromiso y estado.
9. **Evidencias y entregables revisados.**
10. **Conformidad.** Aprobadores, estado (*Pendiente, Conforme, Observado*), fecha, medio y espacio de firma.
11. **Control de cambios.** Versión, fecha, cambio y autor.

El Word sale en A4, con encabezado (estándar y N° de acta), pie con el sello del custodio y numeración
*Página X de Y*. Las tablas repiten la cabecera si se parten entre páginas, y las propiedades del archivo
llevan título, modelo y palabras clave para encontrarlo en repositorios documentales.

## Ciclo de vida del acta

```text
Borrador ──Enviar a revisión──▶ En revisión ──Aprobar──▶ Aprobada (bloqueada)
    ▲                               │                        │
    └──────Devolver a borrador──────┘                        └──Reabrir──▶ Borrador, versión +1
```

Para **aprobar**, el acta debe tener completo el desarrollo de la reunión, todos los participantes con nombre,
ninguna decisión *Pendiente de aprobación* y **todos los aprobadores en *Conforme***. Cada cambio de estado
queda en el control de cambios con fecha y autor. Una reapertura nunca borra la versión anterior del historial.

## Tipos de acta del estándar

Al crear un acta se elige su tipo. Se precargan el objetivo, la agenda, las decisiones esperadas (con su
requisito), los entregables a revisar, los roles de los participantes y los aprobadores.

<!-- CATALOGO:INICIO ACTAS -->
| Tipo (`--tipo`) | Reunión / hito | Evidencia | Requisito | Decisiones precargadas |
|---|---|---|---|---:|
| `R1` | Reunión 1 · Levantamiento de expectativas: población objetivo | Acta 1 | `DES-D1-01.01.08` | 3 |
| `R2` | Reunión 2 · Levantamiento de expectativas: fuentes y variables | Acta 2 | `DES-D1-01.03.01` | 2 |
| `R3` | Reunión 3 · Enriquecimiento de la propuesta y diseño funcional | Acta de reunión | `DES-D1-01.04.07` | 4 |
| `KO` | Kick off del desarrollo | Acta 3 | `DES-D1-02.02.01` | 2 |
| `R4` | Reunión 4 · Segmentación | Acta 4 | `DES-D3-01.01.01` | 1 |
| `R5` | Reunión 5 · Selección del modelo final | Acta 5 | `DES-D4-06.03.01` | 3 |
| `R6` | Reunión 6 · Presentación del calibrado | Acta 6 | `DES-D4-08.01.05` | 1 |
| `R7` | Reunión 7 · Resultados del modelo final | Acta 7 | `DES-D4-12.01.01` | 2 |
| `R8` | Reunión 8 · Enfoque cualitativo con la banca | Acta 8 | `DES-D4-13.01.01` | 3 |
| `CM` | Comité de Modelos · Aprobación | ACTA-CM | `DES-D4-14.01.01` | 2 |
| `IMP-E` | Entrega al equipo implementador | Acta 9 | `IMP-01.01.05` | 1 |
| `IMP-C` | Cierre de la implementación | Acta 10 | `IMP-01.07.01` | 2 |
| `CAL-KO` | Kick off de la calibración | Acta de kick off | `CAL-C2-02.01.01` | 1 |
| `CAL-PR` | Reunión preliminar de resultados de calibración | Acta preliminar | `CAL-C4-03.03.01` | 2 |
| `CAL-CI` | Cierre del calibrado | Acta de cierre del calibrado | `CAL-C4-05.01.01` | 1 |
| `PRC-KO` | Kick off del proyecto de pricing | Acta PRC-KO | `PRC-P1-02.02.01` | 3 |
| `PRC-ELA` | Revisión del modelo de respuesta al precio | Acta PRC-ELA | `PRC-P4-04.01.01` | 3 |
| `PRC-CP` | Comité de Precios · Aprobación de la propuesta | Acta PRC-CP | `PRC-P5-03.02.01` | 4 |
| `PRC-PIL` | Aprobación del piloto o experimento de precio | Acta PRC-PIL | `PRC-P6-01.02.01` | 2 |
| `PRC-PIR` | Revisión post-implementación de precios | Acta PRC-PIR | `PRC-P8-02.01.02` | 2 |
| `PAR-KO` | Kick off del proyecto de parámetros | Acta PAR-KO | `PAR-R1-03.01.01` | 3 |
| `PAR-ESC` | Revisión trimestral de escenarios macroeconómicos | Acta PAR-ESC | `PAR-R6-03.01.01` | 2 |
| `PAR-OVL` | Aprobación de overlays y de la ECL del período | Acta PAR-OVL | `PAR-R8-02.01.02` | 2 |
| `PAR-BT` | Resultados del backtesting de parámetros | Acta PAR-BT | `PAR-R9-01.01.03` | 2 |
| `PAR-CP` | Comité de provisiones · Aprobación de parámetros | Acta PAR-CP | `PAR-R9-02.01.01` | 3 |
| `CRM` | Comité de riesgos de modelo (sesión trimestral) | Acta CRM | `GOB-G1-01.02.01` | 4 |
| `SME` | Revisión con experto de negocio (SME) | Acta SME | — | 0 |
| `LIBRE` | Otra reunión del proyecto | Acta de reunión | — | 0 |

<!-- CATALOGO:FIN -->

## Uso desde el repositorio (analistas y agentes)

```bash
python tools/acta.py tipos
python tools/acta.py nueva --tipo R5 --codigo MOD-ORI-001 --nombre "Score de originación TC" --tier II --modelo ml --n 5 -o actas/MOD-ORI-001/acta-05.json
python tools/acta.py validar actas/MOD-ORI-001/acta-05.json
python tools/acta.py exportar actas/MOD-ORI-001/acta-05.json --docx --md
```

Hay un acta de ejemplo ya aprobada, con datos ficticios, en `ejemplos/actas/` (.docx, .md y .json).

`validar` aplica las mismas reglas que el botón *Aprobar* del sitio. Se recomienda guardar las actas en
`actas/<código de modelo>/` dentro del repositorio del modelo, junto a su `MODEL_CARD.md`.

## Reglas para agentes de IA

- Un agente **puede redactar** el acta (desarrollo, decisiones, acuerdos) a partir de la transcripción o las notas de la reunión.
- Un agente **nunca marca una conformidad como *Conforme* ni aprueba un acta**: eso lo hace cada persona.
- Cada decisión debe citar el ID del requisito o umbral (`DES-D4-06.03.01`, `U-11`). Si no existe, se deja vacío; no se inventa.
- No se copian datos de clientes ni nombres de tablas productivas en el acta.
