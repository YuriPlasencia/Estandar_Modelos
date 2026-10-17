---
id: FR-07
titulo: "FR-07 · Reproducibilidad y MLOps"
estandar: Frontera
estado: Propuesta
version: 0.1.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 57
---

# FR-07 · Reproducibilidad y MLOps

**Hoy:** se exige guardar Train/Test/OOT, fijar semilla, documentar versiones y rutas, y certificar ≥ 95 % de
coincidencia en implementación. La validación de implementación pide capturas de pantalla de rutas.

**Propuesta: reemplazar evidencia manual por evidencia automática.**

| Práctica | Sustituye o mejora | Beneficio |
|---|---|---|
| Código en **Git** con revisión por pares (PR) | Scripts en carpetas compartidas | Trazabilidad línea a línea; el "cuadro de control de cambios" sale del historial |
| **Entorno fijado** (`requirements.txt`/`environment.yml`, contenedor) | "Versiones de herramientas" en Word | Reproducir el modelo en otra máquina |
| **Versionado de datos** (hash de Train/Test/OOT, snapshot o DVC) | Copias de tablas | Probar que el modelo validado usa exactamente esos datos |
| **Registro de modelos** (artefacto + métricas + código de inventario) | Ficha de nacimiento manual | Alta/baja automática en inventario |
| **Pruebas automáticas** en CI: unicidad, missing, PSI, coincidencia vs. modelo de referencia | Certificación manual | La certificación del 95 % (U-15) se ejecuta en cada cambio |
| **Champion / challenger** en producción | Comparación puntual con modelo vigente | Evidencia continua para recalibrar o redesarrollar |

**Requisito candidato:** `IMP-01.06.05 — La certificación se ejecuta como prueba automatizada versionada y
su log se adjunta como evidencia.` Reduce capturas de pantalla y acelera VAL-I.
