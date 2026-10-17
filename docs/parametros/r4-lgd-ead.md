---
id: PAR-R4
titulo: "Parámetros · R4–R5 Severidad y exposición"
estandar: Parámetros
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 34
---

# Parámetros · R4–R5 Severidad y exposición

## R4 · LGD

**LGD workout** de un default con exposición $\mathrm{EAD}$, recuperaciones $R_k$ y costos $C_k$ en los momentos
$t_k$, descontados a la tasa de interés efectiva (U-34):

$$\mathrm{LGD}=1-\frac{1}{\mathrm{EAD}}\sum_{k}\frac{R_k-C_k}{(1+\mathrm{EIR})^{t_k}}$$

**Modelo de dos etapas.** Muchos defaults minoristas se curan (vuelven al día) con pérdida casi nula. Separar ese
componente mejora la precisión:

$$\mathrm{LGD}=p_{\text{cura}}\cdot \mathrm{LGD}_{\text{cura}}+(1-p_{\text{cura}})\cdot \mathrm{LGD}_{\text{no cura}}$$

**Buenas prácticas**

- La LGD vive en $[0,1]$ y suele ser bimodal: usar regresión fraccional, beta, dos etapas o ML con calibración, nunca una regresión lineal sin restricciones.
- **Procesos incompletos:** se incluyen proyectando las recuperaciones remanentes. Excluirlos sesga la LGD hacia los casos que se resuelven rápido, que son los de menor pérdida.
- **Garantías:** el driver es el LTV *actual* (con el valor de la garantía actualizado), no el de originación.
- **LGD en default (ELBE):** para Stage 3 la severidad depende del tiempo en default; una operación con 24 meses en cobranza tiene menos probabilidad de recuperarse que una recién caída.

<!-- CATALOGO:INICIO PAR-R4 -->
## Catálogo de requisitos · Severidad (LGD)

> Bloque generado desde `catalogo/par-r4.yaml` (8 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17).

### 1 · LGD de operaciones vigentes

#### 1.1 LGD workout

- **`PAR-R4-01.01.01`** Calcular la LGD realizada por default como 1 menos el valor presente de las recuperaciones netas de costos sobre la EAD, descontadas a la tasa de interés efectiva (U-34).

  Aplica: Tier I–IV · Esfuerzo: 3 d · Automatización: 2 · Crítico · Entregable: Excel R3: LGD realizada · Hito: Sprint 3 · Umbrales: U-34

- **`PAR-R4-01.01.02`** Tratar los procesos de recuperación incompletos con un método documentado (proyección de recuperaciones remanentes, curvas de recuperación) en lugar de excluirlos, para no sesgar la LGD hacia los casos que se cierran rápido.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Excel R3: LGD realizada · Umbrales: U-34

- **`PAR-R4-01.01.03`** Separar la LGD en sus componentes cuando aporte precisión: probabilidad de cura y severidad dado que no hay cura (modelo de dos etapas).

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 2 · Entregable: Script R2: Modelos de LGD

#### 1.2 Modelo de LGD

- **`PAR-R4-01.02.01`** Estimar el modelo de LGD respetando su soporte acotado y su distribución bimodal (regresión fraccional, beta, dos etapas o métodos de ML con calibración), con drivers de garantía (LTV actual), producto y antigüedad del default.

  Aplica: Tier I–IV · Esfuerzo: 3 d · Automatización: 2 · Crítico · Entregable: Script R2: Modelos de LGD

- **`PAR-R4-01.02.02`** Incorporar el forward-looking en la LGD cuando la recuperación dependa del ciclo (por ejemplo, precios de inmuebles para hipotecarios), con el mismo marco de escenarios de R6.

  Aplica: Tier I–II · Esfuerzo: 1.5 d · Automatización: 2 · Entregable: Script R2: Modelos de LGD

### 2 · LGD en default

#### 2.1 Exposiciones en default

- **`PAR-R4-02.01.01`** Estimar la LGD para exposiciones ya en default (mejor estimación de la pérdida, ELBE) en función del tiempo en default y del estado de la cobranza, para el cálculo de Stage 3.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Script R2: Modelos de LGD

### 3 · Validación y documentación

#### 3.1 Desempeño de la LGD

- **`PAR-R4-03.01.01`** Comparar LGD estimada vs. realizada por segmento y por año de default, incluido el período de estrés, y evaluar el poder de ordenamiento.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 3 · Crítico · Entregable: Excel R4: Desempeño de LGD

- **`PAR-R4-03.01.02`** Documentar la metodología de LGD (descuento, costos, incompletos, garantías, LGD en default).

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 1 · Entregable: Documento R5: Metodología de LGD

<!-- CATALOGO:FIN -->

## R5 · EAD y CCF

Para productos **revolventes**, la exposición al default incluye la parte de la línea que el cliente usará antes de caer:

$$\mathrm{EAD}=\text{Saldo}+\mathrm{CCF}\cdot(\text{Línea}-\text{Saldo}),\qquad
\mathrm{CCF}_{\text{realizado}}=\frac{\mathrm{EAD}_{\text{default}}-\text{Saldo}_{t-12}}{\text{Línea}_{t-12}-\text{Saldo}_{t-12}}$$

Se mide con la foto **12 meses antes del default**. Medirla al momento del default subestima el CCF.

**Vida conductual.** Una tarjeta no tiene vencimiento contractual efectivo: el banco queda expuesto mientras no
gestione la línea. Para la ECL lifetime se usa el período de exposición observado (tiempo hasta la cancelación,
el default o la reducción efectiva de la línea), documentado por cartera (PAR-R5-02.01.02).

Para **amortizables**, la exposición sigue el cronograma ajustado por prepagos esperados, coherente con la EIR
(PAR-R5-01.01.01).

<!-- CATALOGO:INICIO PAR-R5 -->
## Catálogo de requisitos · Exposición (EAD y CCF)

> Bloque generado desde `catalogo/par-r5.yaml` (3 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17).

### 1 · Exposición de productos amortizables

#### 1.1 Perfil de exposición

- **`PAR-R5-01.01.01`** Proyectar la exposición de cada período con el cronograma contractual ajustado por prepagos y cancelaciones esperadas, consistente con la tasa de interés efectiva.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Script R3: Modelos de EAD y CCF · Hito: Sprint 3

### 2 · Exposición de productos revolventes

#### 2.1 CCF y vida conductual

- **`PAR-R5-02.01.01`** Estimar el factor de conversión (CCF) del monto no utilizado a 12 meses antes del default, con el uso de línea, la antigüedad y el estado de atraso como drivers.

  Aplica: Tier I–IV · Esfuerzo: 2.5 d · Automatización: 2 · Crítico · Entregable: Script R3: Modelos de EAD y CCF

- **`PAR-R5-02.01.02`** Para revolventes (tarjetas, líneas), estimar el período de exposición conductual más allá del plazo contractual, durante el que el banco está expuesto porque no gestiona la línea en la práctica; documentar el horizonte usado para la ECL lifetime.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 2 · Crítico · Entregable: Documento R6: Metodología de EAD y vida conductual

<!-- CATALOGO:FIN -->
