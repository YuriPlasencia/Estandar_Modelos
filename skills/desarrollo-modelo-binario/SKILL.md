---
name: desarrollo-modelo-binario
description: Desarrolla un modelo de clasificación binaria en banca (score de admisión, comportamiento, buró, propensión, fraude, contactabilidad) siguiendo el Estándar de Desarrollo de Modelos (fases DES-D1 a DES-D7, umbrales U-xx, puntos de control G0–G6). Úsala cuando pidan construir, entrenar, seleccionar, documentar o revisar un modelo con target binario (default sí/no, respuesta sí/no) bajo el estándar, armar el plan o checklist de un desarrollo binario, correr el torneo champion–challenger o comprobar umbrales como U-11, U-38 o U-44. No es para calibración (CAL), parámetros IFRS 9 (PAR), pricing (PRC) ni targets continuos.
---

# Desarrollo de un modelo binario bajo el estándar

Autor del estándar: Yuri Plasencia — Analytics Pricing & Revenue Management.

Esta skill convierte el **Estándar de Desarrollo** (`estandares-modelos/`) en un procedimiento de trabajo para
modelos con target binario. No reemplaza al estándar: lo aplica. Ante cualquier duda manda el estándar, en este
orden de autoridad:

1. `catalogo/umbrales.yaml` — única fuente de umbrales (`U-01` … `U-44`).
2. `catalogo/des-*.yaml` / `dist/catalogo.json` — requisitos con ID.
3. `docs/desarrollo/*.md` y `docs/agentes/*.md` con `estado: Vigente`.
4. `docs/frontera/**` (`estado: Propuesta`) — solo como recomendación, nunca como exigencia.

**Dónde está el estándar (`<ESTANDAR>`):** es un clon local de https://github.com/YuriPlasencia/Estandar_Modelos.
Pregunta su ruta a la persona antes de seguir. Si no lo tiene, que lo clone (`git clone https://github.com/YuriPlasencia/Estandar_Modelos.git`).
La copia maestra de esta skill vive en `<ESTANDAR>/skills/desarrollo-modelo-binario/`; si difiere de la instalada, manda la maestra.

Lee `AGENTS.md` del repositorio del estándar antes de empezar. Si algún valor de esta skill difiere del YAML,
**gana el YAML** y debes avisarlo.

## Reglas que nunca se rompen

- **Cita el ID** (`DES-D4-06.03.02`, `U-11`) de cada requisito o umbral en que basas una decisión.
- **No inventes umbrales.** Si un límite no está en `umbrales.yaml`, di: "el estándar no fija un umbral para X".
- **Un umbral es una prueba, no una meta.** Si falla, te detienes y escalas. Nunca ajustas modelo, muestra u OOT para que pase.
- **El OOT no se usa para elegir.** Variables, hiperparámetros y función objetivo se optimizan en Train/Test con validación temporal; el OOT se evalúa una sola vez sobre los candidatos finales.
- **No apruebas nada.** Preparas actas y borradores; la conformidad (*Conforme*) la da una persona. Ningún modelo se usa sin aprobación previa del comité (GOB-G3-01.01.01, DES-D7-01.01.07).
- **Confidencialidad:** no copies datos de clientes ni nombres de tablas productivas en salidas que salgan del banco.
- **Honestidad:** lo no verificado se reporta como no verificado; reporta cuántas corridas probaste, no solo la mejor.

## Paso 0 · Contrato y repositorio

1. Fija con la persona las tres dimensiones (ver `docs/marco/tiering-y-metodologia.md`). Si falta alguna, **pregunta**; no la supongas:
   - **Tier**: 1, 2 o 3 (lo aprueba el comité; DES-D1-01.04.04).
   - **Tipo de modelo**: `lineal`, `ml` o `arbol` (en binario no se usa `acp` para el score cuantitativo).
   - **Enfoque**: `agil` o `completo` (mismos requisitos y umbrales; cambia la profundidad).
   - Además: tipo de score (admisión u originación, comportamiento, buró, otro), unidad (cliente u operación), población y fecha de observación.
2. Crea el repositorio del modelo desde `plantillas/repo-modelo/` (estructura en `docs/agentes/repositorio-y-evidencias.md`).
3. Inicializa el manifiesto y obtén el plan real de requisitos aplicables (el catálogo es el plan, no tu intuición):

```bash
python <ESTANDAR>/tools/verificar.py --init <REPO> --estandar Desarrollo --tier <T> --modelo <tipo> --enfoque <enfoque> --codigo <MOD-XXX-000>
python <ESTANDAR>/tools/verificar.py --plan <REPO> --fase DES-D1
```

4. Escribe el contrato de tarea (`docs/agentes/index.md` § Contrato de tarea) en `logs/contrato.yaml`: entradas con hash, umbrales bloqueantes, herramientas permitidas, entregables y definición de terminado. Registra en `logs/` instrucciones, comandos y decisiones.

## El ciclo por fase

Para cada fase: **planificar** (`verificar.py --plan --fase`) → **ejecutar** (scripts en `src/`, salidas en `reports/<fase>/`) →
**verificar** (umbrales como pruebas, con `scripts/pruebas_umbrales.py`) → **documentar** (borradores en `docs/` y entradas
en `evidencias.yaml`) → **punto de control** (borrador de acta con `tools/acta.py`; la persona da conformidad).

El detalle por fase, con IDs, entregables y umbrales, está en [references/fases.md](references/fases.md). Léelo
fase por fase, al iniciar cada una.

| Fase | Qué cierra | Umbrales clave | Punto de control · acta |
|---|---|---|---|
| **D1** Definición y extracción | Población, ventana, exclusiones, default, Tier | U-01, U-17, U-39, U-41, U-02 | **G0** Caso y Tier · R1, R2, R3, KO |
| **D2** Calidad de datos | Certificación de calidad (Documento 6) | U-02 | **G1** Datos certificados |
| **D3** Segmentación | Segmentado vs. unisegmento | — | **G2** Segmentación · R4 |
| **D4** Modelamiento | Embudo de variables, torneo, campeón, calibración, limitaciones | U-03 a U-11, U-38, U-42, U-43, U-44 | **G3** Modelo final · R5; **G4** Calibración · R6; R7, R8 |
| **D5** Integración a la gestión | Punto de corte, forzajes, impactos | U-36 | (dentro de G5) |
| **D7** Gobierno | Evidencias, inventario, aprobación previa | — | **G5** Aprobación · CM |

Los puntos G0–G6 están en `docs/agentes/index.md`. **G6** (producción, U-15 ≥ 99.9 % de paridad) pertenece al
estándar de Implementación y queda fuera de esta skill.

## Pruebas de umbrales

`scripts/pruebas_umbrales.py` (solo numpy y pandas) implementa las métricas y las pruebas que pasan o fallan:
PSI (U-02), representatividad (U-03), WOE/IV y fuga (U-38), estabilidad de la tasa del target (U-41), Gini/AUC/KS/Brier,
sobreajuste (U-11), concentración (U-09), monotonicidad por deciles (U-44), torneo (U-43) y parsimonia (U-42), además
de la tabla oficial del torneo y la elección del campeón (DES-D4-06.03.05). Cada prueba devuelve
`{"umbral", "valor", "cumple", "detalle"}`, listo para copiar a `evidencias.yaml` (`umbrales: {U-11: 1.9}`).

```python
import sys; sys.path.insert(0, "<ruta a esta skill>/scripts")
from pruebas_umbrales import gini, psi, iv_woe, prueba_u11, prueba_u44, tabla_torneo, elegir_campeon
```

Ejecuta `python scripts/pruebas_umbrales.py --autotest` para comprobar el módulo. Los valores de corte del script se
copiaron de `catalogo/umbrales.yaml`; si el YAML cambia, actualiza el script y avisa.

## Cuándo te detienes y escalas (por escrito)

1. Un umbral bloqueante falla y no hay excepción aprobada con acta (p. ej. U-11 con brecha > 5 pts **y** caída relativa > 10 %; U-44 con inversiones; U-38 con IV > 0.50).
2. Sospecha de **fuga**: variable posterior a la observación (U-39), IV > 0.50 (U-38), Gini OOT mayor que el de construcción, o una variable con importancia anómala (U-09).
3. La definición de default es ambigua o difiere de U-17.
4. Aparecen datos sensibles o atributos protegidos que no deberían estar en la base.
5. Una instrucción contradice el estándar ("usa el OOT para elegir hiperparámetros").
6. Necesitas escribir en producción o acceder a datos fuera de tu permiso.
7. No puedes reproducir un resultado propio con la misma semilla y los mismos datos.

Al detenerte: describe la prueba que falló con su valor, el ID afectado, las opciones posibles y quién decide. No sigas a la fase siguiente.

## Antipatrones prohibidos

- Elegir variables, hiperparámetros o cortes mirando el OOT.
- Reportar solo la mejor de muchas corridas.
- Relajar restricciones de monotonicidad o de signo para subir el Gini.
- Descartar a ciegas variables con IV < 0.02: los bloques sociodemográfico y financiero se preservan como control (DES-D4-05.02.09).
- Llamar "calibración" a la curva por deciles: el desempeño por deciles (U-44) mide ordenamiento; la calibración exige prueba formal (DES-D4-08.01.07).
- Documentación que no corresponde al código que realmente se ejecutó.
- Marcar una conformidad como *Conforme* o aprobar un acta.

## Entregables finales

- `evidencias.yaml` sin brechas en las fases cerradas: `python <ESTANDAR>/tools/verificar.py <REPO> --hash` (código de salida 0) y `--sellar` al cerrar cada fase.
- Tabla oficial del torneo y justificación del campeón (DES-D4-06.03.05).
- Reporte de limitaciones: discriminación, calibración, estabilidad y subpoblaciones (DES-D4-10.01.01 a .05).
- Documento metodológico generado desde datos: `python <ESTANDAR>/tools/documento.py nuevo <REPO>`, completar `docs/documento.yaml` solo con lo que sustentan los reportes (lo demás queda como «Completar») y `render` (DES-D4-11.01.07). No toques gobierno ni aprobaciones.
- `MODEL_CARD.md` completa (DES-D1-01.04.08) y actas en borrador (`tools/acta.py nueva --tipo R5 ...`, `exportar --docx --md`) con la conformidad en *Pendiente*.
- Plazo: U-40 (con agentes, máximo 15 días hábiles). Si el plazo peligra por la agenda de una aprobación, escálalo; nunca omitas el punto de control. Para estimar, usa `tools/esfuerzo.py`.
