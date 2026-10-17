# Estándares de Modelos en Banca

[![Publicar sitio](https://github.com/YuriPlasencia/estandares-modelos/actions/workflows/pages.yml/badge.svg)](https://github.com/YuriPlasencia/estandares-modelos/actions/workflows/pages.yml)

**Sitio:** https://yuriplasencia.github.io/estandares-modelos/

**Un estándar abierto, versionado y legible por máquinas para el ciclo de vida completo de los modelos en banca:
desarrollo, calibración, implementación, seguimiento, validación, parámetros de riesgo (IFRS 9), pricing analítico
y trabajo con agentes de IA.**

Autor y custodio: **Yuri Plasencia — Analytics Pricing & Revenue Management** · Versión **2.2.0** (sobre la línea base 2.0) · Octubre 2026 · Licencia CC BY 4.0 (contenido) y MIT (código)

---

## Por qué existe

Los estándares de modelos suelen vivir en documentos difíciles de mantener, de auditar y de consultar. Este
repositorio los trata como **código**: cada requisito tiene un ID estable, cada umbral está en una lista cerrada y
trazable, cada cambio pasa por control de versiones, y todo se publica a la vez para personas (un sitio navegable) y
para agentes de IA (JSON y `llms.txt`).

| | |
|---|---|
| **540 requisitos** con ID estable, aplicabilidad por Tier y tipo de modelo, esfuerzo, entregables e hitos | **39 umbrales** cuantitativos, cada uno enlazado a los requisitos que lo establecen |
| **103 obras** de literatura enlazadas a los requisitos que fundamentan | **27 tipos de acta**, con editor en línea y exportación a Word y Markdown |
| Mapeo artículo por artículo a la **Res. SBS 00053-2023** y alineado con **SR 26-2**, **PRA SS1/23**, IFRS 9 y el **EU AI Act** | **Estándar operativo para agentes de IA** con verificador automático de evidencias |

## Contenido

| Estándar | Prefijo | Qué cubre |
|---|---|---|
| Gobierno del riesgo de modelo | `GOB` | Comité, inventario, categorización, aprobación previa, terceros, IA, informe anual |
| Desarrollo | `DES` | Definición, datos, segmentación, modelamiento, integración a la gestión, gobierno |
| Calibración | `CAL` | Entendimiento, datos, segmentación, calibrado e implementación del calibrado |
| Implementación | `IMP` | Documentación, lineamientos, controles, entorno tecnológico, certificación |
| Seguimiento | `SEG` | Indicadores y umbrales, forzajes, acciones ante alertas, informe periódico |
| Validación | `VAL` | Metodológica, de implementación, de parámetros y de pricing |
| Parámetros de riesgo | `PAR` | PD, LGD, EAD/CCF, escenarios, staging, ECL, overlays, backtesting y CLV |
| Pricing analítico | `PRC` | Precio técnico, respuesta al precio, optimización, experimentos, motor de precios, conducta |
| Agentes de IA | `AGT` | Contratos de tarea, puntos de control humanos, evidencias, evaluación de agentes |

Cada estándar distingue lo **vigente** (obligatorio), lo que está en **borrador** y las **propuestas de frontera**
(prácticas emergentes que no son obligatorias hasta aprobarse).

## Cómo usarlo

**Para leer.** Entra al [sitio publicado](https://yuriplasencia.github.io/estandares-modelos/) o abre `site/index.html` con doble clic (funciona sin servidor). Incluye buscador, panel de detalle por
requisito con sus lecturas, planificador por estándar, Tier, tipo de modelo y enfoque, y el editor de actas.
También puedes leer directamente `docs/` (Markdown con fórmulas en LaTeX).
En el sitio publicado, las actas se guardan en el navegador de cada persona; para editarlas en equipo, usa el
repositorio con `tools/acta.py` o una instancia con almacenamiento compartido.

**Para trabajar un modelo.**

```bash
pip install pyyaml
python tools/verificar.py --init ../MOD-ORI-001 --estandar Desarrollo --tier 2 --modelo ml --enfoque agil
python tools/verificar.py --plan ../MOD-ORI-001 --fase DES-D4
python tools/acta.py nueva --tipo R5 --codigo MOD-ORI-001 --nombre "Score de originación" -o ../MOD-ORI-001/actas/acta-05.json
python tools/acta.py exportar ../MOD-ORI-001/actas/acta-05.json --docx --md
python tools/documento.py nuevo ../MOD-ORI-001
python tools/documento.py render ../MOD-ORI-001/docs/documento.yaml   # .md, .html, .docx y .pdf
```

El documento metodológico se genera desde datos (`docs/documento.yaml`) con la plantilla dinámica; requiere
`pip install jinja2 pypandoc_binary typst`. Ver `docs/plantillas/documento-metodologico.md`.

Parte de la plantilla `plantillas/repo-modelo/`.

**Para agentes de IA.** Lee `AGENTS.md`. Los datos están en `dist/catalogo.json`, `dist/umbrales.json`,
`dist/literatura.json`, `dist/acta.schema.json` y `llms.txt`.

## Estructura

```text
catalogo/            Fuente de verdad: requisitos, umbrales, actas, literatura y modelo de esfuerzo (YAML)
docs/                Documentación por estándar (Markdown); los bloques de catálogo se generan
dist/                Generado: JSON para agentes y llms-full.txt
site/                Generado: sitio autocontenido (index.html)
plantillas/          Plantilla de repositorio de un modelo y plantilla dinámica del documento metodológico
ejemplos/            Acta y documento metodológico de ejemplo con datos ficticios
tools/               build.py · verificar.py · acta.py · documento.py · esfuerzo.py · generadores de catálogo
```

## Contribuir

`python tools/build.py` valida todo y regenera `docs/`, `dist/` y `site/`. **Falla** si un documento cita un ID que no
existe, si hay IDs duplicados, si un umbral o una obra referencia un requisito inexistente o si falta el sello de
custodio. Ver [`CONTRIBUTING.md`](CONTRIBUTING.md) y [`CHANGELOG.md`](CHANGELOG.md).

## Aviso

Este estándar recoge buenas prácticas y referencias públicas. No es asesoría regulatoria ni reemplaza las políticas
aprobadas de ninguna entidad. Los umbrales marcados como *valor de referencia* deben calibrarse con datos propios, y
las normas citadas deben verificarse en su versión vigente. Los nombres de entidades se citan solo a partir de
información pública.

## Licencia

- **Documentación, catálogo y datos** (`catalogo/`, `docs/`, `dist/`, `site/`, plantillas y ejemplos):
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Puedes usarlos y adaptarlos, incluso con fines
  comerciales, citando al autor.
- **Código** (`tools/`): [MIT](tools/LICENSE).

Detalle en [`LICENSE`](LICENSE).

## Cómo citar

Ver [`CITATION.cff`](CITATION.cff).
