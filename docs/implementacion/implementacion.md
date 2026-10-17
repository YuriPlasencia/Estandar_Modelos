---
id: IMP
titulo: "Implementación"
estandar: Implementación
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 30
---

# Implementación

## Objetivo

Llevar el modelo aprobado a producción de forma **fiel, controlada, recuperable y auditable**. Aplica igual a
desarrollos nuevos (fase D6) y calibraciones (C5). Duración de referencia: ≈ 2 semanas dentro de un desarrollo
y ≈ 5–6 semanas como proyecto independiente.

## Los dos documentos obligatorios

### Documento 13 · Guía de implementación

Con cuadro de control de cambios. Debe contener:

- Versiones del modelo y **código de inventario**.
- Descripción funcional de variables **input** y **output**.
- Generación del universo, **llaves y desfases**.
- Proceso de implementación paso a paso y aplicativos necesarios.
- Control de calidad de datos (estabilidad poblacional con umbrales corporativos) y **plan de acción ante alertas**.

### Documento 14 · Lineamientos de ejecución

- Responsables de la ejecución periódica (y de los backups).
- Ubicación de la documentación y archivos de ejecución.
- **Planes de contingencia**: ausencia del responsable, caída de servidores o aplicativos (datalake, SAS…),
  indisponibilidad de información, alertas de calidad de datos.
- Evidencia de usuarios con acceso a ambientes productivos y de **backups** de documentos, scripts y datos.
- Medios y normativa para compartir información con Validación de forma segura.

## Requisitos técnicos

- Script productivo con **logs de ejecución y errores**.
- **Tabla productiva** con código de inventario del modelo y fecha de ejecución.
- Controles de calidad sobre input y output: evolutivos y **PSI** contra un periodo de referencia, unicidad, missing;
  umbrales de PSI definidos; si hay proveedor externo, exigir sus logs, estabilidad, unicidad y fechas de actualización.
- Ruta productiva definida y respaldada, **código único** del modelo, listado de usuarios con acceso.

## Certificación

1. Definir las pruebas (Correo 3).
2. Comparar modelamiento vs. implementación: **≥ 95 % de coincidencia** (U-15).
3. Constancia de pruebas (Documento 14: Certificación).
4. Conformidad del líder de implementación (o del Sub Gerente de Modelos de Riesgo si implementa el equipo modelador).
5. Presentación al equipo usuario y acta de cierre (Acta 10).

<!-- CATALOGO:INICIO IMP -->
## Catálogo de requisitos · Implementación

> Bloque generado desde `catalogo/imp.yaml` (28 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Implementación v1.0.

### 1 · Implementación tecnológica

#### 1.1 Documento de implementación

- **`IMP-01.01.01`** Preparación del documento de implementación (Agregar un registo al cuadro de control de cambios con cada modificación ), este documento debe contener:
  - Proceso de Implementación. El cual debe detallar:  
   - Cuadro resumen de las versiones del modelo y código del modelo.  
   - Descripción funcional de las variables input  
   - Descripción a detalle de la generación del universo.  
   - Descripción de las llaves y desfases a usar.  
   - Descripción a detalle de todo el proceso de implementación.  
   - Descripción funcional de las variables del output.  
   - Descripción de los aplicativos necesarios para la ejecución del proceso..
  - Proceso de control de Calidad de Datos. El cual consta del análisis de estabilidad poblacional de las variables cuyas umbrales son definidos corportaivamente.
  - Detalle del plan de Acción cuando existan alertas en el control de Calidad de Datos

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1.75 d ágil / 2.75 d trad. · Automatización: 1 · Entregable: Documento 13: Guia de implementación · Hito: Sprint 20

- **`IMP-01.01.02`** Documentación y reglamentación de variables críticas del modelo. Luego de la implementación, realizar controles para alarmas sobre cambios relevantes en variables originales y transformadas.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1

- **`IMP-01.01.03`** Documentar variables que deben ser modificadas en el tiempo, por nuevas versiones u otros

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1

- **`IMP-01.01.04`** Documentar la existencia de dependencia de variables inputs y/o otros modelos

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1

- **`IMP-01.01.05`** Envío de manual de implementación al equipo implementador

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0 d ágil / 0 d trad. · Automatización: 1 · Entregable: Acta 9: Reunión con el equipo implementador.

- **`IMP-01.01.06`** Bitácora de cambios para variables, tablas empleada en modelo a implementar, tanto la versión del modelador como la versión final de data (ya que ellos cambian algunas fuentes)

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1

- **`IMP-01.01.07`** En caso la implementación no la realice el modelador se realizará una revisión con área de implementación y acta de entrega

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1

- **`IMP-01.01.08`** Registrar modelo en el inventario de modelos e incluir el código de modelo en el documento de implementación.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0 d ágil · Automatización: 1

- **`IMP-01.01.09`** Documentar un plan de contingencia, para variables erradas y/o caidas de herramientas como datalake/ sas

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1

#### 1.2 Documento de Lineamientos

- **`IMP-01.02.01`** Preparación del documento de Lineamientos del proceso de Implementación. (Agregar un registo al cuadro de control de cambios con cada modificación ), este documento debe precisar:
  - Responsables de la Ejecución Periódica.
  - Ubicación del documento de implementación y archivos de ejecución
  - Planes de Contingencia:  
   - En caso el responsable de la ejecución no se encuentre disponible..  
   - En caso los servidores y/o aplicaciones donde se ejecute el modelo no se encuentren disponibles.  
   - En caso la información no se encuentre disponible.  
   - En caso se tengan alertas de calidad de datos.
  - Evidencias de disponibilidad de los usaurios que tienen accesos a los ambientes productivos del modelo.
  - Evidencia de los backups de los docuemnto, archivos de ejecución e información procesada.
  - Detalles de las herramientas o medios de comunicación por la cual se comparte información del modelo a validación y la normativa en el cual se rigen para que la transferencia sea bajo los lineamientos indicados por seguridad

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1.75 d ágil / 2.75 d trad. · Automatización: 1 · Entregable: Documento 14: Documento de Lineamientos

#### 1.3 Desarrollo de implementación

- **`IMP-01.03.01`** Desarrollo de script de implementación, el cual debe contar con un proceso de almacenamiento de Logs de ejecución y errores durante el proceso

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.8333 d ágil / 0.8333 d trad. · Automatización: 1 · Entregable: Proceso Productivo

- **`IMP-01.03.02`** Construir la tabla productiva del modelo, la cual debe de contar con el código de inventario del modelo y fecha de ejecución

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.8333 d ágil / 0.8333 d trad. · Automatización: 1

- **`IMP-01.03.03`** Garantizar que la información final se encuentre resguardada y en caso contrario generar un archivo plano y almacenar en la ruta productiva del modelo

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.8333 d ágil / 0.8333 d trad. · Automatización: 1

#### 1.4 Calidad de datos

- **`IMP-01.04.01`** Desarrollo de controles de calidad de datos para variables input y output:
  - Evolutivos de distribución y calculo de PSI en función de un periodo de referencia.
  - Control de unicidad de registros.
  - Control de valores missing.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.5 d ágil / 0.5 d trad. · Automatización: 1 · Entregable: Excel: de Control de Calidad de Datos

- **`IMP-01.04.02`** Definición de umbrales de PSI con los cuales se evaluará el control de calidad

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.5 d ágil / 0.5 d trad. · Automatización: 1

- **`IMP-01.04.03`** Solicitud de controles de calidad en caso la información provenga de un proveedor externo.
  - Reportes de ejecución correcta (Logs)
  - Estabilidad Poblacional
  - Unicidad de Resgistros.
  - Fechas de Actualización de la información.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.5 d ágil / 0.5 d trad. · Automatización: 1

#### 1.5 Entorno Tecnológico

- **`IMP-01.05.01`** Definición de la ruta productiva en la cual se almacenará el proceso de implementació.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.3 d ágil / 0.3 d trad. · Automatización: 1

- **`IMP-01.05.02`** Solicitar al equipo de servidores la evidencia del resguardo de la ruta productiva del modelo

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.3 d ágil / 0.3 d trad. · Automatización: 1

- **`IMP-01.05.03`** Solicitud de un código único del modelo

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.3 d ágil / 0.3 d trad. · Automatización: 1

- **`IMP-01.05.04`** Solicitud del listado de usuarios que tienen acceso a la ruta productiva del modelo y a la ubicación del resultado final

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.3 d ágil / 0.3 d trad. · Automatización: 1

- **`IMP-01.05.05`** Solicitud de evidencia del resguardo de información en caso la información provenga de un proveedor externo.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.3 d ágil / 0.3 d trad. · Automatización: 1

#### 1.6 Pruebas de certificación

- **`IMP-01.06.01`** Definición de pruebas sobre el modelo a implementar

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1 d ágil / 1 d trad. · Automatización: 1 · Entregable: Correo 3: Pruebas a realizar.

- **`IMP-01.06.02`** Revisión de diferencias entre proceso de modelamiento vs proceso de implementación (95% de coincidencia mínima para obtener conformidad)

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1.0625 d ágil / 1.25 d trad. · Automatización: 1 · Umbrales: U-15

- **`IMP-01.06.03`** Constancia de pruebas de control sobre el modelo

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1 · Entregable: Documento 14: Certificación del modelo. · Hito: SME 13

- **`IMP-01.06.04`** Solicitar conformidad de los resultados al líder del proyecto de implementación (en caso la implementación sea realizada por el equipo modelador, la aprobación será brindada por el Sub Gerente de Modelos de Riesgos)

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1

- **`IMP-01.06.05`** Probar escenarios de error (datos faltantes, valores fuera de rango, caída de fuentes) y verificar el manejo de excepciones y el control de accesos del proceso productivo.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 1 d ágil / 1 d trad. · Automatización: 2 · Crítico · Nota: Línea base 2.0 (2026-10-17). Res. SBS 00053-2023 art. 18.

- **`IMP-01.06.06`** Registrar en cada resultado productivo la versión del modelo y del código que lo generó, para trazabilidad y seguimiento.

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 2 · Nota: Línea base 2.0 (2026-10-17). Práctica de bancos de referencia; FR-07.

#### 1.7 Presentación del proceso de implementación al equipo usuario

- **`IMP-01.07.01`** Reunión y elaboración de acta

  Aplica: Todos los tipos, Tier I–IV · Esfuerzo: 0.25 d ágil / 0.25 d trad. · Automatización: 1 · Entregable: Acta 10: Reunión de cierre · Hito: SME 13

<!-- CATALOGO:FIN -->
