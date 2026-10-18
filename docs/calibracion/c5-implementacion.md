---
id: CAL-C5
titulo: "Calibración · C5 Implementación del calibrado"
estandar: Calibración
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 22
---

# Calibración · C5 Implementación del calibrado

La implementación de un calibrado sigue el estándar transversal de [Implementación](../implementacion/implementacion.md)
(documento de implementación, lineamientos, calidad de datos, entorno tecnológico y certificación ≥ 99.9 %).
Las actividades específicas del calibrado son:

- **Manual metodológico del calibrado** y **manual de implementación**.
- Envío del manual al equipo implementador, revisión conjunta y **acta de entrega**.
- Certificación con **≥ 99.9 % de coincidencia** (U-15) y conformidad del líder de implementación
  (o del Sub Gerente de Modelos de Riesgo si implementa el equipo modelador).
- Presentación al equipo usuario con acta.

<!-- CATALOGO:INICIO CAL-C5 -->
## Catálogo de requisitos · Implementación del calibrado

> Bloque generado desde `catalogo/cal-c5.yaml` (12 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Calibración v1.0.

### 1 · Implementación

#### 1.1 Documento del calibrado

- **`CAL-C5-01.01.01`** Elaboración del manual metodológico de calibardo

  Aplica: Tier I–III · Esfuerzo: 2.75 d

- **`CAL-C5-01.01.02`** Elaboración del manual de implementación

  Aplica: Tier I–III · Esfuerzo: 2.75 d

- **`CAL-C5-01.01.03`** Envío de manual de implementación al equipo implementador

  Aplica: Tier I–III · Esfuerzo: 0.25 d

- **`CAL-C5-01.01.04`** Revisión con área de implementación y acta de entrega

  Aplica: Tier I–III · Esfuerzo: 0.25 d

- **`CAL-C5-01.01.05`** Una recalibración es una modificación del modelo: requiere validación y aprobación previa del comité de riesgos de modelo antes de su uso.

  Aplica: Tier I–III · Esfuerzo: 0.25 d · Automatización: 1 · Crítico · Nota: Línea base 2.0 (2026-10-17). Res. SBS 00053-2023 art. 17.

#### 1.2 Desarrollo de implementación

- **`CAL-C5-01.02.01`** Desarrollo de script de implementación

  Aplica: Tier I–III

#### 1.3 Calidad de datos

- **`CAL-C5-01.03.01`** Desarrollo de controles de calidad de datos para variables input

  Aplica: Tier I–III · Esfuerzo: 2.5 d

#### 1.4 Pruebas de certificación

- **`CAL-C5-01.04.01`** Definición de pruebas sobre el modelo a implementar

  Aplica: Tier I–III · Esfuerzo: 1 d

- **`CAL-C5-01.04.02`** Revisión de diferencias entre proceso de modelamiento vs proceso de implementación (99.9 % de coincidencia mínima para obtener conformidad, U-15)

  Aplica: Tier I–III · Esfuerzo: 1.25 d · Umbrales: U-15

- **`CAL-C5-01.04.03`** Constancia de pruebas de control sobre el modelo

  Aplica: Tier I–III · Esfuerzo: 0.25 d

- **`CAL-C5-01.04.04`** Solicitar conformidad de los resultados al líder del proyecto de implementación (en caso la implementación sea realizada por el equipo modelador, la aprobación será brindada por el Sub Gerente de Modelos de Riesgos)

  Aplica: Tier I–III · Esfuerzo: 0.25 d

#### 1.5 Presentación del proceso de implementación al equipo usuario

- **`CAL-C5-01.05.01`** Reunión y elaboración de acta

  Aplica: Tier I–III · Esfuerzo: 0.5 d

<!-- CATALOGO:FIN -->
