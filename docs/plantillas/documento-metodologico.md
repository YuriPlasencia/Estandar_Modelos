---
id: PLT-DOC
titulo: "Plantilla · Documento metodológico"
estandar: Plantillas
estado: Vigente
version: 2.2.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 62
---

# Plantilla · Documento metodológico

El documento metodológico (entregable 11 de DES-D4-11) se escribe **una sola vez, como datos**, y se genera en
todos los formatos que pide el proceso: Markdown para Git y agentes, HTML para leer en pantalla, Word para la
revisión con control de cambios y PDF para Comité y Validación (DES-D4-11.01.07).

La plantilla es **dinámica**: lo que falte no se omite, aparece como un aviso «Completar» que cita el requisito del
estándar que lo exige. Así, un borrador muestra de un vistazo qué le falta para estar listo.

## Cómo se usa

```bash
pip install pyyaml jinja2 pypandoc_binary typst
python tools/documento.py nuevo ../MOD-ORI-001          # crea docs/documento.yaml prellenado
python tools/documento.py render ../MOD-ORI-001/docs/documento.yaml
python tools/documento.py render ../MOD-ORI-001/docs/documento.yaml --formatos md,pdf --salida reports/
```

`nuevo` toma el código, el Tier, el tipo de modelo y el enfoque de `MODEL_CARD.md` y de `evidencias.yaml`, y enlaza
el manifiesto de evidencias para la matriz de cumplimiento. `render` deja los archivos en `docs/salida/`, con el
nombre `CODIGO_documento-metodologico_vX.Y` (Markdown, HTML, Word y PDF; con `--formatos qmd`, también Quarto).

En el repositorio de un modelo basta `make documento`.

## Qué genera automáticamente

| Elemento | Origen |
|---|---|
| **Evaluación de umbrales** (cumple / excepción / no cumple) | Bloque `umbrales` del YAML, con las mismas reglas que `tools/verificar.py`; U-01 se deriva de la ventana |
| **Matriz de cumplimiento** por fase | Requisitos aplicables al estándar, Tier, tipo y enfoque; estado tomado de `evidencias.yaml` |
| **Gráfico de estabilidad** del Gini mensual | `desempeno.mensual`, con la línea de entrenamiento y la banda de U-11 |
| **Alertas de fuga** | Variables finales con IV mayor a 0.50 (U-38) |
| **Desviación de calibración** por tramo | `desempeno.calibracion` |
| **Lecturas recomendadas** | Literatura del catálogo asociada a los requisitos citados en el documento |
| **Control del documento, portada, encabezado y pie** | Bloques `documento` y `control_cambios` |

## Estructura del documento

1. Control del documento y control de cambios
2. Resumen ejecutivo
3. Propósito, uso y alcance (usos no permitidos)
4. Datos: fuentes y no anticipación, universo, ventana, definición de default, exclusiones y calidad
5. Segmentación
6. Variables: embudo de selección y variables finales
7. Metodología: algoritmo, benchmark interpretable, validación cruzada e hiperparámetros
8. Desempeño: muestras, comparación con el modelo vigente, estabilidad mensual y calibración
9. Interpretabilidad, sensibilidad y equidad
10. Integración a la gestión: punto de corte, impactos y forzajes
11. Limitaciones
12. Seguimiento
13. Cumplimiento del estándar: umbrales y matriz de requisitos
14. Gobierno y aprobaciones (actas)
15. Referencias

## Herramientas

| Herramienta | Para qué |
|---|---|
| **Jinja2** | Plantilla `plantillas/documento-metodologico/documento.md.j2` |
| **Pandoc** (`pypandoc_binary`) | Markdown → HTML autocontenido y Word con la plantilla de estilos `estilos/referencia.docx` |
| **Typst** | PDF con portada, índice, encabezado, pie con número de página y sello (`estilos/plantilla.typ.j2`) |
| **Quarto** (opcional) | Salida `.qmd` para quien quiera integrar código ejecutable al documento |

Para ajustar la marca o los estilos de Word: `python tools/documento.py estilos` regenera `referencia.docx`.

## Ejemplo

`plantillas/documento-metodologico/documento-ejemplo.yaml` es un modelo ficticio completo (originación de tarjeta de
crédito, Tier II, machine learning). `ejemplos/documento-metodologico/` tiene su salida en los cuatro formatos.

## Para agentes de IA

Un agente puede completar `docs/documento.yaml` desde los reportes del repositorio y generar el documento. No
completa las secciones de **gobierno y aprobaciones** ni cambia el estado a *Aprobado*: eso lo hace una persona
(AGT). Si una sección no tiene sustento en los reportes, la deja vacía para que aparezca como «Completar».
