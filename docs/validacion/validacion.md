---
id: VAL
titulo: "Validación"
estandar: Validación
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 40
---

# Validación

La validación es la **revisión independiente** (segunda línea) de que el modelo es conceptualmente sólido,
está bien construido y opera en producción tal como se aprobó. Tiene dos ámbitos:

| Ámbito | Cuándo | Qué dictamina |
|---|---|---|
| **VAL-M · Metodológica** | Tras el cierre de D4/D5 o C4, antes de producción | Que el modelo/calibración es adecuado para su uso |
| **VAL-I · Implementación** | Tras la certificación de IMP | Que producción replica el modelo y está controlada |
| **VAL-R · Parámetros** | Antes del comité de provisiones y tras cada recalibrado | Que PD, LGD, EAD, escenarios, staging, overlays y motor de ECL son sólidos y están conciliados |
| **VAL-P · Pricing** | Antes del Comité de Precios y tras certificar el motor | Que el precio técnico, la respuesta al precio y el optimizador son sólidos y que el motor cumple topes y conducta |

## Cómo usar este checklist

- Para la **primera línea**: es la lista de lo que el validador pedirá. Si todo está listo antes de la solicitud,
  la validación es un trámite.
- Para el **validador**: cada requisito tiene ID, de modo que el informe de validación pueda citar
  `VAL-I-01.09 — no cumple` en vez de describirlo.
- Los requisitos **KILLER** bloquean la conformidad: sin ellos no hay dictamen favorable.

## Observaciones frecuentes

Las observaciones más frecuentes en validación de implementación suelen ser:

1. Manual de implementación que **no llega hasta la tabla final** o no incluye la fórmula del modelo.
2. Falta de **certificación integral** cuando hay datos de un proveedor externo (mínimo 3 meses, U-16).
3. Ausencia de **control de calidad de datos** sobre las variables del modelo (missings, duplicados).
4. Rutas de documentación y backup **sin evidencia** (capturas) ni responsable identificado.
5. Tabla productiva **sin código de modelo**.

<!-- CATALOGO:INICIO VAL -->
## Catálogo de requisitos · Validación

> Bloque generado desde `catalogo/val.yaml` (95 requisitos).

### Validación metodológica

#### Documentación y gobierno

- [ ] **`VAL-M-01.01`** Documento de extracción de datos.
- [ ] **`VAL-M-01.02`** Documento metodológico de construcción / calibración.
- [ ] **`VAL-M-01.03`** Actas de coordinación con los equipos de negocio sobre el inicio, coordinación y aprobación del modelo.
- [ ] **`VAL-M-01.04`** Actas de coordinación y aprobación de definición de población, filtros y target.
- [ ] **`VAL-M-01.05`** Actas de criterios, supuestos específicos y segmentación/perfilamiento.
- [ ] **`VAL-M-01.06`** Documento de extracción y selección de variables/drivers.
- [ ] **`VAL-M-01.07`** Documento de extracción y selección de variables de segmentación/perfilamiento.
- [ ] **`VAL-M-01.08`** Actas de coordinación con los equipos de negocio sobre la elección de variables/drivers seleccionados.
- [ ] **`VAL-M-01.09`** Actas de coordinación con los equipos de negocio sobre la elección de segmentos/perfiles.
- [ ] **`VAL-M-01.10`** Actas de coordinación con los equipos de negocio sobre la aprobación de variables/drivers finalistas.
- [ ] **`VAL-M-01.11`** Acta de conformidad de las BBDD extraídas para la construcción de los modelos.
- [ ] **`VAL-M-01.12`** Verificar que el modelo se encuentre registrado en el inventario de modelos.
- [ ] **`VAL-M-01.13`** Análisis y actas de aprobación del Tier del modelo.

#### Calidad de datos

- [ ] **`VAL-M-02.01`** Programas usados para la extracción de datos, ordenados y comentados según la documentación de extracción de datos.
- [ ] **`VAL-M-02.02`** Reportes con los controles e incidencias de calidad de datos en la extracción de datos.
- [ ] **`VAL-M-02.03`** Programas usados para la extracción de variables/drivers, ordenados según su documentación.
- [ ] **`VAL-M-02.04`** Reportes con los controles e incidencias de calidad de datos en la extracción de variables/drivers.
- [ ] **`VAL-M-02.05`** Programas usados para la construcción de perfiles/segmentos, ordenados según su documentación.
- [ ] **`VAL-M-02.06`** Reportes con los controles e incidencias de calidad de datos en la construcción de perfiles/segmentos.

#### Metodología

- [ ] **`VAL-M-03.01`** Programas usados para la construcción/calibración del modelo, ordenados y comentados según la documentación metodológica.
- [ ] **`VAL-M-03.02`** Reportes utilizados para la construcción/calibración del modelo, ordenados según la documentación metodológica.
- [ ] **`VAL-M-03.03`** Estándar metodológico aplicado en la construcción/calibración, con los entregables según el estándar.
- [ ] **`VAL-M-03.04`** Archivos de trabajo de los controles, análisis y conclusiones de primera línea.
- [ ] **`VAL-M-03.05`** Definición y estabilidad de la población.
- [ ] **`VAL-M-03.06`** Definición y estabilidad del target.
- [ ] **`VAL-M-03.07`** Bondad de ajuste del modelo.
- [ ] **`VAL-M-03.08`** Análisis por subpoblaciones (precisión / discriminación).
- [ ] **`VAL-M-03.09`** Mix de riesgos, granularidad y monotonicidad del score.
- [ ] **`VAL-M-03.10`** Archivos de trabajo de las pruebas de selección de variables/drivers que justifiquen su elección.
- [ ] **`VAL-M-03.11`** Archivos de trabajo de las pruebas de selección de segmentos/perfiles que justifiquen su elección.
- [ ] **`VAL-M-03.12`** Análisis del performance del modelo a nivel global, mensual (hasta periodos recientes) y por drivers principales de negocio.

#### Integración a la gestión

- [ ] **`VAL-M-04.01`** Definición de los usos que tiene/tendrá el modelo y análisis de desempeño en la población de uso.
- [ ] **`VAL-M-04.02`** Análisis de impacto en la gestión por los usos del modelo.
- [ ] **`VAL-M-04.03`** Evidencias del seguimiento del modelo o de su planificación.

### Validación de implementación

#### Documentación

- [ ] **`VAL-I-01.01`** El documento de implementación cubre el proceso completo hasta la generación de la tabla final productiva.
- [ ] **`VAL-I-01.02`** El manual de implementación detalla la fórmula o ecuación del modelo.
- [ ] **`VAL-I-01.03`** El manual de implementación detalla la definición funcional de las variables utilizadas en el cálculo.
- [ ] **`VAL-I-01.04`** El documento de lineamientos identifica al responsable del proceso de backup.
- [ ] **`VAL-I-01.05`** El documento de lineamientos describe la tabla final del modelo y adjunta el flujo de ejecución.
- [ ] **`VAL-I-01.06`** La tabla productiva incluye un campo con el código de inventario del modelo (con evidencia).
- [ ] **`VAL-I-01.07`** La ruta de documentación (manuales, scripts, certificación, control de calidad) es correcta y se evidencia su contenido.
- [ ] **`VAL-I-01.08`** Se evidencia el proceso de log de la implementación y su ubicación.
- [ ] **`VAL-I-01.09`** **KILLER** Documento de certificación de la tabla final, con aprobación de la jefatura evidenciada por correo de conformidad. Si el modelo consume datos de un proveedor externo (p.ej. buró), la certificación debe ser integral y cubrir un mínimo de 3 meses. · Umbrales: U-16
- [ ] **`VAL-I-01.10`** **KILLER** Control de calidad de datos (missings, duplicados) sobre las variables del modelo.
- [ ] **`VAL-I-01.11`** Evidencia (correo o acta) de coordinación con los equipos consumidores de la tabla productiva, incluyendo fecha de inicio de consumo.

#### Entorno tecnológico - Accesos a documentación

- [ ] **`VAL-I-02.01`** Rutas donde se almacena la documentación del modelo.
- [ ] **`VAL-I-02.02`** Rutas donde se almacenan los scripts del modelo.
- [ ] **`VAL-I-02.03`** Capturas de pantalla de cada ruta mostrando su contenido.
- [ ] **`VAL-I-02.04`** Propietario de la ruta principal de documentación.
- [ ] **`VAL-I-02.05`** Personas con acceso a la ruta principal de documentación.
- [ ] **`VAL-I-02.06`** Flujo para solicitar acceso a la información y conformidades necesarias.

#### Entorno tecnológico - Accesos a datos

- [ ] **`VAL-I-03.01`** Acceso del validador a todas las tablas input del modelo y a la tabla final productiva.
- [ ] **`VAL-I-03.02`** Listado de equipos y owners de cada tabla input.
- [ ] **`VAL-I-03.03`** Rutas donde se almacenan las bases input y output del proceso.
- [ ] **`VAL-I-03.04`** Propietario del sandbox o de la tabla productiva.
- [ ] **`VAL-I-03.05`** Personas con acceso al sandbox o tabla productiva (el acceso debe estar restringido a ellas).
- [ ] **`VAL-I-03.06`** Flujo para solicitar acceso a los datos y conformidades necesarias.

#### Backup de documentación

- [ ] **`VAL-I-04.01`** Rutas de respaldo de la documentación.
- [ ] **`VAL-I-04.02`** Rutas de respaldo de los scripts.
- [ ] **`VAL-I-04.03`** Capturas de pantalla de cada ruta de respaldo mostrando su contenido.
- [ ] **`VAL-I-04.04`** Responsable de administrar los respaldos de la documentación.
- [ ] **`VAL-I-04.05`** Responsable de administrar los respaldos de los scripts.
- [ ] **`VAL-I-04.06`** Flujo para solicitar la restauración de la información y conformidades necesarias.

#### Backup de datos

- [ ] **`VAL-I-05.01`** **KILLER** Ruta de backup de las bases input y output del proceso, o evidencia de los respaldos.
- [ ] **`VAL-I-05.02`** **KILLER** Nombre del servidor, base de datos, sandbox y tabla de respaldo.
- [ ] **`VAL-I-05.03`** **KILLER** Responsable de administrar la ruta de respaldo y periodicidad del proceso.
- [ ] **`VAL-I-05.04`** **KILLER** Flujo para restaurar la información y conformidades necesarias.

### Validación de modelos de pricing

#### Precio técnico

- [ ] **`VAL-P-01.01`** Conciliación del precio técnico con Finanzas (FTP, costos, capital) y Riesgos (PD, LGD), con fecha de vigencia de cada insumo y diferencias por celda explicadas.
- [ ] **`VAL-P-01.02`** Uso de una PD coherente con el horizonte de la operación (lifetime o anualizada sobre la vida esperada) y sustento de la elección.
- [ ] **`VAL-P-01.03`** **KILLER** Ninguna celda del tarifario aprobado por debajo del piso técnico sin acta del Comité de Precios (U-18) y monotonicidad del precio en el riesgo (U-19).

#### Modelo de respuesta

- [ ] **`VAL-P-02.01`** **KILLER** Estrategia de identificación causal documentada y pruebas de robustez; un modelo de respuesta estimado solo sobre operaciones desembolsadas no es válido.
- [ ] **`VAL-P-02.02`** Elasticidad negativa y aceptación monótona en todos los segmentos (U-20), con el rango de precios en que la curva es válida.
- [ ] **`VAL-P-02.03`** Calibración de la aceptación por decil y por tramo de precio en OOT y meses recientes (U-21).

#### Optimizador

- [ ] **`VAL-P-03.01`** Reproducción independiente de la propuesta con el mismo código, semilla y datos, y verificación de que respeta todas las restricciones.
- [ ] **`VAL-P-03.02`** Sensibilidad de la propuesta a la incertidumbre de la elasticidad y a los supuestos de valor (prepago, fuga, venta cruzada).

#### Implementación y conducta

- [ ] **`VAL-P-04.01`** **KILLER** Control preventivo de topes regulatorios en el motor de precios con 100 % de cumplimiento en las pruebas (U-24) y certificación ≥ 95 % (U-15).
- [ ] **`VAL-P-04.02`** Análisis de equidad del precio y de proxies de atributos protegidos (PRC-P9-02.02.01).
- [ ] **`VAL-P-04.03`** Registro y log de los agentes de IA usados en el ciclo de pricing, sin facultad para fijar ni aprobar precios (PRC-P9-03.01.01).

### Validación de parámetros de riesgo

#### Definiciones y datos

- [ ] **`VAL-R-01.01`** Definición de default consistente con la gestión del riesgo y la contabilidad, con la presunción de 90 días (U-28) y el puente documentado con la definición de los scores (U-17).
- [ ] **`VAL-R-01.02`** Profundidad y representatividad de los datos (U-27) y conciliación de saldos, defaults y castigos con contabilidad.

#### PD

- [ ] **`VAL-R-02.01`** Calibración de la PD por grado con el test de Jeffreys (U-30) y PD lifetime con tratamiento de riesgos competitivos (prepago, cancelación).

#### LGD

- [ ] **`VAL-R-02.02`** LGD workout descontada a la tasa de interés efectiva, con costos y procesos incompletos incluidos (U-34), y LGD en default para Stage 3.

#### EAD

- [ ] **`VAL-R-02.03`** Perfil de exposición consistente con prepagos, CCF de revolventes y sustento del período de exposición conductual.

#### Escenarios y staging

- [ ] **`VAL-R-03.01`** **KILLER** Al menos tres escenarios con probabilidades sustentadas y ECL ponderada como promedio de las ECL por escenario (U-32).
- [ ] **`VAL-R-03.02`** Umbrales SICR calibrados (U-29), backstops de 30 y 90 días (U-28) y evidencia de que Stage 2 anticipa el default.

#### ECL y gobierno

- [ ] **`VAL-R-04.01`** **KILLER** Overlays con causa, cuantificación, expiración y aprobación (U-31), y plan de absorción en el modelo.
- [ ] **`VAL-R-04.02`** **KILLER** Motor de ECL certificado con coincidencia ≥ 95 % (U-15) y conciliado con contabilidad.
- [ ] **`VAL-R-04.03`** Backtesting anual de PD, LGD, CCF, staging y ECL, con acciones documentadas.

### Validación metodológica

#### Alcance y profundidad de la validación

- [ ] **`VAL-M-05.01`** Réplica completa e independiente del modelo para los modelos de mayor categoría (Tier I), incluida la reconstrucción de la base y del entrenamiento. · Umbrales: U-35
- [ ] **`VAL-M-05.02`** Benchmarking con un modelo alternativo (challenger) construido o seleccionado por Validación.
- [ ] **`VAL-M-05.03`** Validación periódica según la categoría (U-35) que revise el uso real del modelo, la categoría asignada y los forzajes. · Umbrales: U-35
- [ ] **`VAL-M-05.04`** **KILLER** Hallazgos clasificados por severidad (alta, media, baja) con responsable, plazo y seguimiento hasta su cierre; los de severidad alta exigen mitigación temporal hasta corregirse.
- [ ] **`VAL-M-05.05`** Para modelos de IA: evaluación de interpretabilidad (incluida la estabilidad de las explicaciones), optimización de hiperparámetros, validación cruzada y nivel de sobreajuste.
- [ ] **`VAL-M-05.06`** Modelos de terceros: réplica o, si la propiedad intelectual lo impide, benchmarking u otra técnica alternativa documentada.
- [ ] **`VAL-M-05.07`** **KILLER** Verificación independiente de la no anticipación temporal de las variables (U-39) y de la ausencia de fuga de información: revisión de variables con IV mayor a 0.50 (U-38) y del embudo de filtros previo al entrenamiento.


<!-- CATALOGO:FIN -->
