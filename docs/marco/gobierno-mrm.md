---
id: MARCO-GOB
titulo: Gobierno del riesgo de modelo
estandar: Marco
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 2
---

# Gobierno del riesgo de modelo

Los estándares de Desarrollo, Calibración, Parámetros o Pricing dicen **cómo se hace un modelo**. Este documento dice
**cómo la entidad gobierna todos sus modelos**: quién decide, con qué inventario y categorías, cuándo se valida, qué
pasa con los proveedores y cómo se reporta. Sus requisitos (GOB-G1 a GOB-G5) aplican a la entidad, no a un
proyecto, y por eso no aparecen en el Planificador.

## Marcos que lo sustentan

| Marco | Alcance | Estado |
|---|---|---|
| **Res. SBS 00053-2023**, Reglamento de Gestión de Riesgos de Modelo (Perú) | Bancos y entidades supervisadas; crédito, mercado, liquidez, operacional, LA/FT | **Obligatorio en Perú** (LIT-131) |
| **SR 26-2** (Fed, OCC, FDIC, 17-abr-2026) | Bancos de EE. UU., sobre todo los de más de 30 000 MM USD | Reemplaza a SR 11-7; excluye la IA generativa y agéntica (LIT-130) |
| **PRA SS1/23** (Reino Unido) | Cinco principios de MRM, incluidos ML y terceros | Referencia internacional (LIT-101) |
| **EU AI Act** | IA de alto riesgo, incluido el scoring de personas | Referencia para IA (LIT-102) |

## Correspondencia entre la norma peruana y este estándar

| Res. SBS 00053-2023 | Exigencia | Dónde se cumple |
|---|---|---|
| Art. 5 | Inventario actualizado y remitido anualmente (SUCAVE) | GOB-G2-01.01.01, GOB-G2-01.01.02 |
| Art. 6 | Categorización por materialidad, uso y complejidad, aprobada por comité | GOB-G2-02.01.01, Tier ([FR-02](../frontera/tiering-basado-en-riesgo.md)), U-35 |
| Art. 7 | Acciones correctivas y mitigación temporal | GOB-G5-01.01.01, VAL-M-05.04 |
| Art. 8 | Informe anual de la unidad de riesgos | GOB-G5-02.01.01 |
| Arts. 9–11 | Directorio y comité de riesgos de modelo trimestral | GOB-G1-01.02.01 a GOB-G1-01.02.03; acta CRM |
| Arts. 12–13 | Independencia y nivel organizacional de validación y seguimiento | GOB-G1-01.01.01, GOB-G1-01.01.02 |
| Art. 14 | Manuales de desarrollo, validación, uso, seguimiento, datos y proveedores | GOB-G3-01.02.01 (este estándar) |
| Art. 15 | Documentación con historial de versiones | GOB-G3-01.02.02, DES-D4-11.01.03 |
| Art. 16 | Desarrollo: propósito, calidad de datos, sensibilidad o benchmark; en IA, interpretabilidad, HPO y validación cruzada | DES-D2, DES-D4-10.01.06, DES-D4-05.03.02, DES-D4-05.03.03, DES-D4-07 |
| Art. 17 | Aprobación previa de todo modelo nuevo, modificado o con cambio de uso | GOB-G3-01.01.01, DES-D7-01.01.07, CAL-C5-01.01.05 |
| Art. 18 | Implementación: escenarios de error, automatización, accesos | IMP-01.06.05, IMP |
| Art. 19 | Uso consistente con el propósito; capacitación; forzajes | DES-D5-01.01.02, SEG-S2-01.03.02 |
| Art. 20 | Validación inicial y periódica; réplica en alta categoría | VAL-M-05.01, VAL-M-05.03, U-35, VAL-I |
| Arts. 21–22 | Seguimiento con indicadores y umbrales; informe anual (forzajes, sobreajuste en IA) | SEG-S1 a SEG-S4, U-36, U-37 |
| Arts. 23–25 | Terceros: responsabilidad, seguimiento interno, réplica o benchmarking | GOB-G4-01.01.01 a GOB-G4-01.01.03, VAL-M-05.06 |

> La correspondencia se basa en el texto publicado en El Peruano. Verifica la versión vigente y su cronograma de
> adecuación por tipo de riesgo antes de usarla como evidencia de cumplimiento.

## Lo que hacen los bancos de referencia (fuentes públicas)

| Banco | Práctica pública | Incorporado como |
|---|---|---|
| **JPMorgan Chase** | Función independiente de gobierno y revisión de modelos (MRGR); el usuario es dueño del riesgo de uso; el inventario incluye ML e IA | GOB-G1-01.01.01, GOB-G1-01.01.03, GOB-G4-02.01.01 |
| **HSBC** | Chief Model Risk Officer con reporte al CRO, independiente de quienes desarrollan y usan los modelos | GOB-G1-01.01.01 |
| **BBVA** | Inventario y monitoreo de sistemas de IA; ocho principios de IA responsable traducidos en controles | GOB-G4-02.01.01, GOB-G4-02.01.02 |
| **Santander** | Remediación ordenada de hallazgos y revisiones anuales | VAL-M-05.04, U-35 |
| **Credicorp** (Form 20-F) | Metodología pública de pérdida esperada: tres escenarios ponderados, staging mensual | PAR |

Detalle y fuentes en [Línea base 2.0](linea-base.md).

<!-- CATALOGO:INICIO GOB-G1 -->
## Catálogo de requisitos · Organización y comité de riesgos de modelo

> Bloque generado desde `catalogo/gob-g1.yaml` (6 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Línea base 2.0 (2026-10-17): Res. SBS 00053-2023, SR 26-2, PRA SS1/23 y práctica pública de bancos de referencia.

### 1 · Estructura

#### 1.1 Roles e independencia

- **`GOB-G1-01.01.01`** Mantener una función de riesgo de modelo independiente de las áreas que desarrollan, usan e implementan los modelos, con un responsable que reporta a la gerencia de riesgos (SBS 53-2023 arts. 12–13).

  Aplica: Tier I–III · Automatización: 1 · Crítico

- **`GOB-G1-01.01.02`** Los responsables de validación y seguimiento tienen al menos el mismo nivel organizacional que los de desarrollo; los desarrolladores están separados de las unidades de negocio.

  Aplica: Tier I–III · Automatización: 1 · Crítico

- **`GOB-G1-01.01.03`** Asignar al usuario del modelo la propiedad de su riesgo de uso y la obligación de usarlo solo para el propósito aprobado (SBS art. 19).

  Aplica: Tier I–III · Automatización: 1

#### 1.2 Comité de riesgos de modelo

- **`GOB-G1-01.02.01`** Operar un comité de riesgos de modelo con al menos un director, el jefe de riesgos y los responsables de desarrollo, validación y seguimiento, que sesione como mínimo cada trimestre (SBS arts. 10–11).

  Aplica: Tier I–III · Automatización: 1 · Crítico · Entregable: Acta CRM: Comité de riesgos de modelo

- **`GOB-G1-01.02.02`** El comité aprueba los criterios de categorización (Tier), los indicadores y umbrales de seguimiento, la periodicidad de las validaciones, los informes de validación y seguimiento y las acciones ante debilidades.

  Aplica: Tier I–III · Automatización: 1 · Crítico · Entregable: Acta CRM: Comité de riesgos de modelo

- **`GOB-G1-01.02.03`** El directorio aprueba las políticas, asigna recursos y aprueba las excepciones de uso de modelos de mayor categoría con debilidades relevantes (SBS art. 9).

  Aplica: Tier I–III · Automatización: 1 · Crítico

<!-- CATALOGO:FIN -->

<!-- CATALOGO:INICIO GOB-G2 -->
## Catálogo de requisitos · Inventario y categorización

> Bloque generado desde `catalogo/gob-g2.yaml` (4 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Línea base 2.0 (2026-10-17): Res. SBS 00053-2023, SR 26-2, PRA SS1/23 y práctica pública de bancos de referencia.

### 1 · Inventario

#### 1.1 Registro de modelos

- **`GOB-G2-01.01.01`** Mantener un inventario completo y actualizado de modelos con sus atributos mínimos (propósito, uso, dueño, categoría, estado, versión, validaciones, debilidades), incluidas herramientas informales influyentes como hojas de cálculo y los sistemas de IA.

  Aplica: Tier I–III · Automatización: 2 · Crítico · Entregable: Documento G1: Inventario de modelos

- **`GOB-G2-01.01.02`** Remitir el inventario al supervisor con la periodicidad y el formato que exija la norma local (en Perú, anualmente vía SUCAVE según el Anexo A de la Res. SBS 53-2023).

  Aplica: Tier I–III · Automatización: 2 · Crítico · Entregable: Documento G1: Inventario de modelos

### 2 · Categorización

#### 2.1 Criterios de categoría

- **`GOB-G2-02.01.01`** Categorizar cada modelo por materialidad, uso y complejidad con criterios aprobados por el comité (ver FR-02); la categoría determina la profundidad y frecuencia de validación y seguimiento y si se exige réplica completa (SBS art. 6; U-35).

  Aplica: Tier I–III · Automatización: 1 · Crítico · Entregable: Documento G2: Criterios de categorización · Umbrales: U-35

- **`GOB-G2-02.01.02`** Revisar periódicamente el propio esquema de categorización (que sea objetivo y que discrimine), como exige SS1/23.

  Aplica: Tier I–II · Automatización: 1 · Entregable: Documento G2: Criterios de categorización

<!-- CATALOGO:FIN -->

<!-- CATALOGO:INICIO GOB-G3 -->
## Catálogo de requisitos · Políticas, aprobación y documentación

> Bloque generado desde `catalogo/gob-g3.yaml` (3 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Línea base 2.0 (2026-10-17): Res. SBS 00053-2023, SR 26-2, PRA SS1/23 y práctica pública de bancos de referencia.

### 1 · Ciclo de aprobación

#### 1.1 Aprobación previa

- **`GOB-G3-01.01.01`** Todo modelo nuevo, modificado (cambio de variables, supuestos o parámetros, incluida una recalibración) o con cambio de uso requiere validación y aprobación previa del comité antes de usarse (SBS art. 17).

  Aplica: Tier I–III · Automatización: 1 · Crítico

#### 1.2 Manuales

- **`GOB-G3-01.02.01`** Mantener manuales aprobados de desarrollo, validación, uso, seguimiento, categorización, calidad de datos y contratación de proveedores de modelos (SBS art. 14); este estándar cumple esa función para los modelos analíticos.

  Aplica: Tier I–III · Automatización: 1 · Crítico

- **`GOB-G3-01.02.02`** Conservar la documentación de cada modelo (desarrollo, validación, seguimiento, actas, bases, diccionarios y código) con historial de versiones y disponible para el supervisor (SBS art. 15).

  Aplica: Tier I–III · Automatización: 2 · Crítico

<!-- CATALOGO:FIN -->

<!-- CATALOGO:INICIO GOB-G4 -->
## Catálogo de requisitos · Modelos de terceros y sistemas de IA

> Bloque generado desde `catalogo/gob-g4.yaml` (5 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Línea base 2.0 (2026-10-17): Res. SBS 00053-2023, SR 26-2, PRA SS1/23 y práctica pública de bancos de referencia.

### 1 · Terceros

#### 1.1 Proveedores

- **`GOB-G4-01.01.01`** La entidad es plenamente responsable de los modelos de terceros: puede tercerizar desarrollo, validación o implementación, pero el seguimiento lo hace la propia entidad (SBS arts. 23–24).

  Aplica: Tier I–III · Automatización: 1 · Crítico

- **`GOB-G4-01.01.02`** Para modelos de terceros de mayor categoría, exigir réplica; si la propiedad intelectual lo impide, aplicar benchmarking u otra técnica alternativa documentada (SBS art. 25).

  Aplica: Tier I–III · Automatización: 1 · Crítico

- **`GOB-G4-01.01.03`** Contar con una estrategia de continuidad para los modelos de proveedores que soportan servicios priorizados.

  Aplica: Tier I–II · Automatización: 1

### 2 · Sistemas de IA

#### 2.1 IA responsable

- **`GOB-G4-02.01.01`** Inventariar los sistemas de IA (incluidos los de IA generativa y los agentes) y aplicarles controles proporcionales a su riesgo: los modelos de IA no generativa siguen este estándar; los generativos y agénticos, además, el estándar AGT.

  Aplica: Tier I–III · Automatización: 2 · Crítico · Entregable: Documento G1: Inventario de modelos

- **`GOB-G4-02.01.02`** Adoptar principios de IA responsable (transparencia, equidad, privacidad, seguridad y supervisión humana) traducidos en métricas y controles verificables, no solo en declaraciones.

  Aplica: Tier I–II · Automatización: 1

<!-- CATALOGO:FIN -->

<!-- CATALOGO:INICIO GOB-G5 -->
## Catálogo de requisitos · Reporte, debilidades y auditoría

> Bloque generado desde `catalogo/gob-g5.yaml` (3 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Línea base 2.0 (2026-10-17): Res. SBS 00053-2023, SR 26-2, PRA SS1/23 y práctica pública de bancos de referencia.

### 1 · Debilidades

#### 1.1 Gestión de debilidades

- **`GOB-G5-01.01.01`** Registrar cada debilidad o hallazgo con severidad, responsable, plazo y estado; si no puede corregirse de inmediato, aplicar medidas temporales de mitigación (SBS art. 7).

  Aplica: Tier I–III · Automatización: 2 · Crítico · Entregable: Documento G3: Registro de debilidades

### 2 · Reporte

#### 2.1 Informe anual

- **`GOB-G5-02.01.01`** La unidad de riesgos emite un informe anual con el estado de las debilidades, los modelos desarrollados o modificados en los últimos 12 meses y el cronograma de los próximos 12 meses (SBS art. 8).

  Aplica: Tier I–III · Automatización: 2 · Crítico · Entregable: Documento G4: Informe anual de riesgo de modelo

- **`GOB-G5-02.01.02`** Auditoría interna incluye en su plan anual la evaluación del cumplimiento de la gestión de riesgo de modelo.

  Aplica: Tier I–III · Automatización: 1 · Crítico

<!-- CATALOGO:FIN -->
