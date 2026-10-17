# MOD-XXX-000 · Nombre del modelo

Repositorio de un modelo bajo los **Estándares de Modelos en Banca** (Yuri Plasencia — Analytics Pricing & Revenue Management).

## Empezar

```bash
python ../estandares-modelos/tools/verificar.py --init . --estandar Desarrollo --tier 2 --modelo ml --enfoque agil --codigo MOD-XXX-000
make verificar
```

1. Completa `MODEL_CARD.md` (ficha técnica del modelo); sustenta su registro en el inventario.
2. Trabaja fase por fase; al cerrar cada requisito, actualiza su entrada en `evidencias.yaml`.
3. Crea las actas con `python ../estandares-modelos/tools/acta.py nueva --tipo R1 ... -o actas/acta-01.json`.
4. Crea el documento metodológico con `python ../estandares-modelos/tools/documento.py nuevo .`, completa
   `docs/documento.yaml` y genera Markdown, HTML, Word y PDF con `make documento`.
5. Antes de cada punto de control (G0–G6), `make verificar` debe quedar sin brechas para las fases cerradas.

## Estructura

| Carpeta | Contenido |
|---|---|
| `data/` | Referencias y hashes de las bases; los datos reales quedan en el entorno gobernado |
| `src/` | Código de extracción, calidad, features, entrenamiento, calibración e implementación |
| `reports/<fase>/` | Salidas que el estándar llama Excel N, Script N, Tabla N |
| `docs/` | Documentos del estándar (Documento N) en Markdown |
| `actas/` | Actas en JSON, exportables a Word |
| `logs/` | Logs de ejecución y del agente de IA |
