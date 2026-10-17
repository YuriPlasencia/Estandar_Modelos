---
id: AGT-REPO
titulo: "Agentes de IA · Repositorio del modelo y evidencias"
estandar: Agentes
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 46
---

# Agentes de IA · Repositorio del modelo y evidencias

Cada modelo vive en **su propio repositorio**, con una estructura fija. Así, un agente o un analista nuevo lo
entiende en minutos, y Validación encuentra cada evidencia sin pedirla. La plantilla está en `plantillas/repo-modelo/`.

```text
MOD-ORI-001/
├── MODEL_CARD.md        ficha de nacimiento (DES-D1-01.04.08)
├── evidencias.yaml      manifiesto: requisito → estado → archivos → acta
├── Makefile             `make datos`, `make modelo`, `make reportes`, `make verificar`
├── environment.yml      entorno fijado (versiones exactas)
├── data/                solo referencias y hashes; los datos reales quedan en el entorno gobernado
├── src/                 código: extracción, calidad, features, entrenamiento, calibración, implementación
├── reports/<fase>/      salidas que el estándar llama "Excel N", "Script N", "Tabla N"
├── docs/                documentos del estándar (Documento N), en Markdown
├── actas/               actas en JSON, exportables a Word con tools/acta.py
└── logs/                log de ejecución y del agente
```

## El manifiesto de evidencias

`evidencias.yaml` es la columna vertebral. Une cada requisito aplicable con lo que prueba que se cumplió:

```yaml
modelo:
  codigo: MOD-ORI-001
  estandar: Desarrollo        # Desarrollo | Calibración | Implementación | Parámetros | Pricing | Seguimiento
  tier: 2
  tipo_modelo: ml             # lineal | ml | arbol | acp (solo Desarrollo e Implementación)
  enfoque: agil
evidencias:
  - requisito: DES-D4-06.03.02
    estado: cumplido          # cumplido | pendiente | no_aplica | excepcion
    archivos: [reports/D4/indicadores.html]
    sha256: {reports/D4/indicadores.html: 3b1f…}   # opcional: lo registra `verificar.py --sellar`
    umbrales: {U-11: 1.9}     # valor obtenido
    acta: ACTA-MOD-ORI-001-05
  - requisito: DES-D4-07.01.01
    estado: excepcion
    justificacion: Modelo lineal; SHAP no aplica, se reportan coeficientes y WOE.
    acta: ACTA-MOD-ORI-001-05
```

## El verificador

`tools/verificar.py` compara el manifiesto contra el catálogo y responde lo mismo que preguntaría un validador:

```bash
python tools/verificar.py --init  ruta/al/repo --estandar Desarrollo --tier 2 --modelo ml --enfoque agil
python tools/verificar.py --plan  ruta/al/repo --fase DES-D4
python tools/verificar.py         ruta/al/repo --hash
python tools/verificar.py --sellar ruta/al/repo      # registra el sha256 de los archivos al cerrar una fase
```

| Comprobación | Resultado si falla |
|---|---|
| Todo requisito aplicable está en el manifiesto | Lista de requisitos faltantes |
| Los archivos citados existen (y su hash coincide, con `--hash`) | Lista de archivos faltantes o modificados |
| Las excepciones tienen justificación y acta | Excepciones incompletas |
| Los umbrales reportados cumplen su regla numérica | Umbrales en falla |
| Los IDs citados existen en el catálogo | IDs desconocidos (posible requisito inventado) |

El reporte sale en Markdown (`reports/verificacion.md`) y termina con código de salida 1 si hay brechas,
para usarlo en integración continua: un *pull request* no se fusiona con brechas abiertas.
