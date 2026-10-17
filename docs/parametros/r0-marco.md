---
id: PAR
titulo: "Parámetros de riesgo · Marco"
estandar: Parámetros
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 31
---

# Parámetros de riesgo · Marco

Los scores ordenan clientes; los **parámetros** ponen cifras en soles. PD, LGD y EAD, más los escenarios
macroeconómicos y los criterios de staging, determinan la **pérdida crediticia esperada (ECL)** que se registra
en los estados financieros bajo IFRS 9. También alimentan el capital, el stress testing, el precio técnico
(PRC-P3) y el valor de vida del cliente. Un punto básico mal estimado en la PD de una cartera grande es
un error contable, no solo estadístico. Por eso este estándar es el más exigente en conciliación, gobierno
y backtesting.

## Arquitectura de parámetros

```text
                 Escenarios macro (Estudios Económicos) ── probabilidades
                                │
                    modelos satélite (macro → tasas de default, LGD)
                                │
  Scores aprobados ──▶ PD 12m ─▶ PD lifetime ─┐
  (Desarrollo/CAL)                            │
  Recuperaciones ────▶ LGD / LGD en default ──┼──▶ ECL = Σ escenarios Σ períodos PD·LGD·EAD·descuento
  Cronogramas/líneas ▶ EAD / CCF / vida ──────┘          │
                                │                        ├── Stage 1: 12 meses
                    Staging (SICR: PD lifetime vs. origen,├── Stage 2: lifetime
                    backstops 30/90 días)                └── Stage 3: LGD en default
                                │
                         Overlays gobernados ──▶ ECL final ──▶ Contabilidad · IFRS 7 · Comité de provisiones
```

## Un parámetro, varios usos

| Uso | Horizonte | Calibración | Particularidad |
|---|---|---|---|
| **IFRS 9 (ECL)** | 12 meses o vida | Point-in-time con forward-looking | Ponderación de escenarios, staging, descuento a la EIR |
| **Provisiones regulatorias locales** | Según norma | Reglas del supervisor | En Perú conviven con IFRS 9 (Res. SBS 11356-2008); se documenta el puente |
| **Capital (IRB, económico)** | 12 meses | Through-the-cycle; LGD downturn | Margen de conservadurismo |
| **Pricing** | Vida de la operación | TTC o lifetime anualizada | Precio técnico (PRC-P3-01.02.01) |
| **CLV** | Vida del cliente | Lifetime con fuga y prepago | Visión única de riesgo y valor (PAR-R10) |

**Regla de oro:** un mismo dato, una misma definición de default (con sus puentes documentados) y una tabla de
parámetros versionada que todos los consumidores leen (PAR-R10-02.01.01).

## Fases del estándar

| Fase | Contenido | Página |
|---|---|---|
| R1 | Marco, alcance, usos, segmentación, definiciones de default y cura | esta página |
| R2 | Datos: cohortes, recuperaciones, exposición, macro, calidad | [R2](r2-datos.md) |
| R3 | PD 12 meses y lifetime | [R3](r3-pd.md) |
| R4–R5 | LGD, LGD en default, EAD, CCF y vida conductual | [R4–R5](r4-lgd-ead.md) |
| R6–R7 | Escenarios, modelos satélite y staging (SICR) | [R6–R7](r6-escenarios-staging.md) |
| R8 | Cálculo de la ECL, movimientos y overlays | [R8](r8-ecl.md) |
| R9–R10 | Backtesting, gobierno, CLV y publicación de parámetros | [R9–R10](r9-backtesting-clv.md) |

## Definición de default: el puente que siempre se debe documentar

El estándar de scores define el default como **más de 60 días de atraso en 12 meses** (U-17), porque busca
anticipar el deterioro al originar. IFRS 9, en cambio, presume que el default **no ocurre después de los 90 días**
(U-28), y la regulación prudencial suele usar 90 días. El área de Parámetros debe:

1. Usar para la ECL una definición coherente con la gestión del riesgo y con la contabilidad (PAR-R1-02.01.01).
2. Documentar el puente: si la PD se calibra desde un score entrenado con 60 días, mostrar la tasa de default a
   90 días por grado y recalibrar la PD a la definición contable.
3. Aplicar los mismos criterios de salida de default y cura en LGD y en staging (U-33).

<!-- CATALOGO:INICIO PAR-R1 -->
## Catálogo de requisitos · Marco, alcance y gobierno de parámetros

> Bloque generado desde `catalogo/par-r1.yaml` (6 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17).

### 1 · Alcance y usos

#### 1.1 Inventario de parámetros

- **`PAR-R1-01.01.01`** Inventariar los parámetros de riesgo por cartera y uso (PD 12 meses y lifetime, LGD, LGD en default, EAD/CCF, escenarios, criterios de staging, CLV) y registrar cada modelo en el inventario con su Tier.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 1 · Crítico · Entregable: Documento R1: Mapa de parámetros y usos · Hito: Sprint 0

- **`PAR-R1-01.01.02`** Declarar los usos de cada parámetro (provisiones IFRS 9, provisiones regulatorias locales, capital, pricing, stress testing, CLV) y las diferencias de calibración que cada uso exige: point-in-time con forward-looking para IFRS 9, through-the-cycle o downturn para capital.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 1 · Crítico · Entregable: Documento R1: Mapa de parámetros y usos

#### 1.2 Segmentación de carteras

- **`PAR-R1-01.02.01`** Definir las carteras con riesgo homogéneo (producto, segmento, garantía, canal, moneda) sobre las que se estiman los parámetros, con evidencia de homogeneidad y materialidad suficiente de defaults por segmento.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Excel R1: Segmentación de carteras

### 2 · Definiciones comunes

#### 2.1 Default y unidad de análisis

- **`PAR-R1-02.01.01`** Alinear la definición de default de parámetros con la gestión del riesgo y con la contabilidad: en IFRS 9 el default no puede ocurrir después de los 90 días de atraso salvo evidencia que refute la presunción (U-28). Documentar el puente con la definición de default de los scores de originación (U-17: más de 60 días) y su efecto en la calibración.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 1 · Crítico · Entregable: Documento R2: Definiciones de default, cura y unidad · Umbrales: U-28

- **`PAR-R1-02.01.02`** Definir los criterios de salida de default y cura: período mínimo de observación y tratamiento de reestructurados (U-33), e impacto en LGD y en staging.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 1 · Crítico · Entregable: Documento R2: Definiciones de default, cura y unidad · Umbrales: U-33

### 3 · Gobierno inicial

#### 3.1 Kick off

- **`PAR-R1-03.01.01`** Kick off del proyecto de parámetros con Riesgos, Finanzas/Contabilidad, Estudios Económicos y Validación.

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 1 · Entregable: Acta PAR-KO: Kick off de parámetros · Hito: Kick Off

<!-- CATALOGO:FIN -->

## Fuentes públicas usadas para construir este estándar

El estándar se contrastó con guías libres y con la práctica pública de bancos de referencia:

- **GPPC (2016)**, [*The implementation of IFRS 9 impairment requirements by banks*](https://www.iasplus.com/en/publications/global/other/ifrs-9-impairment-banks): la guía libre más completa (LIT-110).
- **BCBS (2015)**, [*Guidance on credit risk and accounting for expected credit losses* (d350)](https://www.bis.org/bcbs/publ/d350.htm) (LIT-111).
- **EBA (2017)**, [*Guidelines on accounting for expected credit losses* (EBA/GL/2017/06)](https://eba.europa.eu/sites/default/documents/files/documents/10180/1842525/d769d006-d992-4202-8838-711a034e80a2/Final%20Guidelines%20on%20Accounting%20for%20Expected%20Credit%20Losses%20%28EBA-GL-2017-06%29.pdf) (LIT-112).
- **EBA (2023)**, [*IFRS 9 implementation by EU institutions*](https://www.eba.europa.eu/sites/default/files/2023-11/25b12d35-9c28-4335-a589-166c77198920/Final%20Report%20on%20IFRS9%20implementation%20by%20EU%20institutions.pdf): overlays estructurales, backtesting insuficiente (LIT-113).
- **BCE (2024)**, [*IFRS 9 overlays and model improvements for novel risks*](https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.IFRS9novelrisks_202407~5e0eb30b5c.ro.pdf) (LIT-114).
- **Credicorp, Form 20-F** ([ejercicio 2025](https://www.sec.gov/Archives/edgar/data/0001001290/000100129026000008/bap-20251231.htm)): PD × LGD × EAD descontada a la EIR, tres escenarios ponderados revisados trimestralmente, SICR mensual frente al origen y LGD ELBE para Stage 3 (LIT-122).

> Estas fuentes son públicas y se citan como referencia de buenas prácticas. Las cifras y los criterios
> de cualquier banco concreto se obtienen de sus documentos internos aprobados, no de este estándar.
