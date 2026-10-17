---
id: PAR-R3
titulo: "Parámetros · R3 Probabilidad de default"
estandar: Parámetros
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 33
---

# Parámetros · R3 Probabilidad de default

## De la PD a 12 meses a la curva lifetime

La ECL de Stage 2 necesita la PD **de cada período futuro**, no solo la de los próximos 12 meses. Con un modelo
de supervivencia en tiempo discreto, la probabilidad de default en el período $t$ dado que la operación llegó
viva es la *hazard* $h(t)$, y:

$$S(t)=\prod_{u=1}^{t}\big(1-h(u)\big),\qquad \mathrm{PD}^{\text{marg}}(t)=S(t-1)\,h(t),\qquad \mathrm{PD}^{\text{acum}}(T)=1-S(T)$$

Con **riesgos competitivos** (prepago o cancelación con hazard $h^{p}$), la supervivencia relevante es
$S(t)=\prod_{u\le t}(1-h(u)-h^{p}(u))$. Ignorarlos **sobreestima** la PD acumulada de los créditos que se
prepagan (PAR-R3-02.01.02).

| Método | Cuándo usarlo | Cuidado |
|---|---|---|
| **Supervivencia discreta** (logit o cloglog por período, con variables de comportamiento y macro) | Carteras minoristas con historia mensual | Separar efectos de antigüedad, cohorte y calendario |
| **Matrices de migración (Markov)** | Carteras con escala de calificación estable (empresas) | Monotonicidad, estado absorbente, no estacionariedad |
| **Curvas vintage** | Productos homogéneos, buen volumen | Extrapolación de la cola de la curva |

## Point-in-time y through-the-cycle

Con el modelo de un factor de Vasicek, una PD de largo plazo $\mathrm{PD}_{\text{TTC}}$ se condiciona al estado del
ciclo $Z$ (negativo en recesión) con correlación de activos $\rho$:

$$\mathrm{PD}_{\text{PIT}}(Z)=\Phi\!\left(\frac{\Phi^{-1}(\mathrm{PD}_{\text{TTC}})-\sqrt{\rho}\,Z}{\sqrt{1-\rho}}\right)$$

Proyectando $Z$ con los escenarios macro se obtienen matrices PIT por período y, multiplicándolas, la PD lifetime
condicional a cada escenario. La literatura reciente propone filtros de estado para estabilizar estas
proyecciones a varios años (ver Frontera en [R9–R10](r9-backtesting-clv.md)).

## Calibración

La PD se calibra al nivel observado con la definición de default de parámetros, y se contrasta por grado con
el **test de Jeffreys** (U-30): con $d$ defaults en $n$ operaciones, el p-valor es la CDF de una
$\mathrm{Beta}(d+\tfrac12,\;n-d+\tfrac12)$ evaluada en la PD. Valores bajos indican que la PD subestima el riesgo.

<!-- CATALOGO:INICIO PAR-R3 -->
## Catálogo de requisitos · Probabilidad de default (PD)

> Bloque generado desde `catalogo/par-r3.yaml` (7 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17).

### 1 · PD a 12 meses

#### 1.1 Estimación y calibración

- **`PAR-R3-01.01.01`** Estimar la PD a 12 meses por grado o segmento, o calibrar el score aprobado a tasas de default observadas siguiendo DES-D4-08, con la definición de default de R1.

  Aplica: Tier I–III · Esfuerzo: 3 d · Automatización: 2 · Crítico · Entregable: Script R1: Modelos de PD · Hito: Sprint 2

- **`PAR-R3-01.01.02`** Separar el componente through-the-cycle (tendencia de largo plazo) del point-in-time (ciclo), y documentar cómo se ancla la PD al promedio de largo plazo.

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Documento R4: Metodología de PD

### 2 · PD lifetime

#### 2.1 Estructura temporal

- **`PAR-R3-02.01.01`** Estimar la curva de PD lifetime (marginal y acumulada por período) con un método documentado: supervivencia en tiempo discreto, matrices de migración (Markov) o curvas vintage, según la cartera y los datos disponibles.

  Aplica: Tier I–III · Esfuerzo: 4 d · Automatización: 2 · Crítico · Entregable: Script R1: Modelos de PD

- **`PAR-R3-02.01.02`** Tratar los riesgos competitivos (prepago, cancelación, castigo) para no sobreestimar la PD acumulada de operaciones que salen del portafolio antes de su vencimiento.

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 2 · Entregable: Script R1: Modelos de PD

- **`PAR-R3-02.01.03`** Para matrices de migración: verificar monotonicidad (mayor PD en peores grados), estado absorbente de default y estabilidad de la matriz; si se condiciona al ciclo (factor Z de Vasicek u otro), documentar la estimación del factor.

  Aplica: Tier I–II · Esfuerzo: 1.5 d · Automatización: 2 · Entregable: Script R1: Modelos de PD

### 3 · Desempeño de la PD

#### 3.1 Validación de la PD

- **`PAR-R3-03.01.01`** Evaluar discriminación por horizonte y, sobre todo, calibración: tasa observada vs. PD por grado con el test de Jeffreys (U-30), en construcción y en los períodos más recientes.

  Aplica: Tier I–III · Esfuerzo: 2 d · Automatización: 3 · Crítico · Entregable: Excel R2: Desempeño y calibración de PD · Umbrales: U-30

- **`PAR-R3-03.01.02`** Documentar la metodología de PD, sus supuestos y limitaciones con la estructura de DES-D4-11.

  Aplica: Tier I–III · Esfuerzo: 1.5 d · Automatización: 1 · Entregable: Documento R4: Metodología de PD

<!-- CATALOGO:FIN -->
