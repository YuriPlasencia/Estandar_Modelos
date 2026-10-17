---
id: PAR-R2
titulo: "Parámetros · R2 Datos y reconstrucción histórica"
estandar: Parámetros
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 32
---

# Parámetros · R2 Datos y reconstrucción histórica

Los parámetros se estiman sobre **cuatro bases**, todas conciliadas con contabilidad:

| Base | Unidad | Uso | Error típico que se debe evitar |
|---|---|---|---|
| Cohortes de default | Operación × mes | PD 12m y lifetime, matrices, curas | Cohortes que no incluyen un período de estrés (U-27) |
| Recuperaciones (workout) | Default | LGD, LGD en default | Excluir procesos abiertos y sesgar la LGD a la baja (U-34) |
| Exposición | Operación × mes | EAD, CCF, prepago, vida conductual | Medir el uso de línea en el default y no 12 meses antes |
| Macro | Mes o trimestre | Modelos satélite | Usar series con frecuencias o rezagos distintos a los de Estudios Económicos |

**Profundidad.** Al menos cinco años con un período de estrés (U-27). Si la cartera es nueva, se combinan
datos internos de carteras similares, datos de buró o externos y un margen de conservadurismo documentado.

<!-- CATALOGO:INICIO PAR-R2 -->
## Catálogo de requisitos · Datos y reconstrucción histórica

> Bloque generado desde `catalogo/par-r2.yaml` (7 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17).

### 1 · Bases de estimación

#### 1.1 Series de default

- **`PAR-R2-01.01.01`** Construir las cohortes de default por cartera con al menos cinco años de historia que incluyan un período de estrés (U-27): saldos, estados de atraso mensuales, defaults, curas y salidas (prepago, castigo, venta).

  Aplica: Tier I–III · Esfuerzo: 4 d · Automatización: 2 · Crítico · Entregable: Tabla R1: Cohortes de default · Hito: Sprint 1 · Umbrales: U-27

- **`PAR-R2-01.01.02`** Reconstruir la historia de calificaciones o scores en una escala estable para estimar matrices de migración, corrigiendo cambios de modelo con un mapeo documentado.

  Aplica: Tier I–II · Esfuerzo: 3 d · Automatización: 2 · Entregable: Tabla R1: Cohortes de default

#### 1.2 Base de recuperaciones

- **`PAR-R2-01.02.01`** Construir la base de recuperaciones por default: flujos de cobranza, ejecución de garantías, costos directos e indirectos y fecha de cierre del proceso. Identificar los procesos incompletos y su tratamiento.

  Aplica: Tier I–III · Esfuerzo: 4 d · Automatización: 2 · Crítico · Entregable: Tabla R2: Base de recuperaciones (workout)

#### 1.3 Base de exposición

- **`PAR-R2-01.03.01`** Construir la base de exposición: cronogramas de amortización, prepagos, líneas y uso de línea 12 meses antes del default para estimar CCF.

  Aplica: Tier I–III · Esfuerzo: 2.5 d · Automatización: 2 · Crítico · Entregable: Tabla R3: Base de exposición y uso de línea

#### 1.4 Series macroeconómicas

- **`PAR-R2-01.04.01`** Recopilar las series macroeconómicas candidatas (PBI, desempleo, inflación, tasas, tipo de cambio, precios de inmuebles, términos de intercambio) con la misma frecuencia y rezagos que usará Estudios Económicos en sus escenarios.

  Aplica: Tier I–III · Esfuerzo: 1.5 d · Automatización: 2 · Crítico · Entregable: Tabla R4: Series macroeconómicas

### 2 · Calidad de datos

#### 2.1 Certificación

- **`PAR-R2-02.01.01`** Aplicar los controles de calidad de DES-D2 y los específicos de parámetros: continuidad de cohortes, defaults sin recuperación registrada, recuperaciones mayores al saldo, y conciliación de saldos y castigos con contabilidad.

  Aplica: Tier I–III · Esfuerzo: 2.5 d · Automatización: 3 · Crítico · Entregable: Documento R3: Certificación de datos de parámetros

- **`PAR-R2-02.01.02`** Certificar las bases con acta de conformidad de las fuentes (Riesgos, Cobranzas, Contabilidad, Estudios Económicos).

  Aplica: Tier I–III · Esfuerzo: 0.5 d · Automatización: 1 · Entregable: Documento R3: Certificación de datos de parámetros

<!-- CATALOGO:FIN -->
