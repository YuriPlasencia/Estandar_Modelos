---
id: PRC-P3
titulo: "Pricing · P3 Precio técnico y RAROC"
estandar: Pricing
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 26
---

# Pricing · P3 Precio técnico y RAROC

El precio técnico es la **tasa mínima a la que una operación crea valor**: la que deja un RAROC igual a la
tasa de retorno mínima exigida al capital (*hurdle*). Por debajo de ese piso, cada operación destruye valor
aunque contablemente parezca rentable.

## Cascada del precio

```text
  Tasa de lista ───────────────────────────────────────────────┐
     − descuento comercial (dentro de facultades, U-23)        │  margen comercial
  = Tasa ofrecida ─────────────────────────────────────────────┤
     − prima de opcionalidad (prepago, cancelación)            │
     − costo de capital   K·(h/(1−t) − r_FTP)                  │  precio técnico
     − costo operativo     c_op                                │  (piso, U-18)
     − pérdida esperada    PD_anual · LGD                      │
     − costo de fondos     r_FTP (+ prima de liquidez)         │
  = Margen económico  ≥ 0  ────────────────────────────────────┘
```

## Fórmulas

**Precio técnico mínimo** de una operación (tasa anual sobre el saldo), con $K$ el capital por unidad de
saldo, $h$ el hurdle después de impuestos y $t$ la tasa impositiva:

$$r_{\min}= r_{\text{FTP}} + \mathrm{PD}_{\text{anual}}\cdot \mathrm{LGD} + c_{\text{op}} + K\left(\frac{h}{1-t}-r_{\text{FTP}}\right) + \pi_{\text{opc}}$$

**RAROC** de la operación al precio $r$:

$$\mathrm{RAROC}(r)=\frac{\left(r - r_{\text{FTP}} - \mathrm{PD}_{\text{anual}}\cdot\mathrm{LGD} - c_{\text{op}} - \pi_{\text{opc}}\right)(1-t) + K\,r_{\text{FTP}}\,(1-t)}{K}$$

Se cumple $\mathrm{RAROC}(r_{\min}) = h$.

## Decisiones metodológicas que debes documentar

- **Horizonte de la PD.** Los scores del estándar estiman default a 12 meses (U-17). Para una operación a
  36 meses, la pérdida relevante es la de toda su vida esperada. Usa la PD *lifetime* anualizada sobre el
  perfil de amortización y prepago: $\mathrm{PD}_{\text{anual}} = 1-(1-\mathrm{PD}_{\text{vida}})^{1/T_{\text{esperado}}}$.
  Usar la PD a 12 meses en plazos largos **subestima** el piso de los créditos malos de maduración tardía.
- **Duración, no plazo.** El FTP se toma en la duración del flujo (amortización y prepago), no en el plazo contractual.
- **Capital económico o regulatorio.** Usa el que la entidad gestiona como restricción vinculante y declara cuál.
- **Costo marginal o completo.** Para decidir precio se usa el costo **marginal** de originar y mantener;
  el costo completo se reporta aparte. Declara cuál y por qué.
- **Depósitos.** El "piso" es inverso: la tasa máxima a pagar es la que deja el valor FTP del fondeo, menos
  los costos de captación y el costo de liquidez del comportamiento esperado del saldo.

<!-- CATALOGO:INICIO PRC-P3 -->
## Catálogo de requisitos · Precio técnico y rentabilidad ajustada por riesgo

> Bloque generado desde `catalogo/prc-p3.yaml` (9 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Pricing Analítico v1.0 (nuevo, 2026-10-17).

### 1 · Componentes del precio técnico

#### 1.1 Costo de fondos

- **`PRC-P3-01.01.01`** Asignar el costo de fondos con la curva de precios de transferencia (FTP) de Finanzas/ALM según plazo y perfil de amortización (duración equivalente), incluyendo la prima de liquidez. Para depósitos, el FTP es el valor del fondeo que aporta el producto.

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Excel P2: Calculadora de precio técnico · Hito: Sprint 2

#### 1.2 Pérdida esperada

- **`PRC-P3-01.02.01`** Calcular la pérdida esperada anualizada con los modelos de riesgo aprobados: PD ajustada al horizonte de la operación (lifetime o promedio anual sobre la vida esperada, no solo la PD a 12 meses de U-17), LGD y EAD con su perfil de amortización y uso de línea.

  Aplica: Tier I–IV · Esfuerzo: 3 d · Automatización: 2 · Crítico · Entregable: Excel P2: Calculadora de precio técnico

#### 1.3 Costos operativos y de adquisición

- **`PRC-P3-01.03.01`** Asignar costos operativos (originación, mantenimiento, cobranza) y de adquisición por canal, con su driver (por operación o por saldo), conciliados con Finanzas.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 2 · Entregable: Excel P2: Calculadora de precio técnico

#### 1.4 Costo de capital

- **`PRC-P3-01.04.01`** Calcular el cargo por capital: capital económico o regulatorio consumido por la operación por la tasa de retorno mínima (hurdle) antes de impuestos, neto del beneficio de fondear con capital.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 2 · Entregable: Excel P2: Calculadora de precio técnico

#### 1.5 Opcionalidad

- **`PRC-P3-01.05.01`** Valorar la opcionalidad del cliente (prepago sin penalidad, cancelación anticipada de depósitos, uso de línea) e incorporarla como prima o como ajuste del valor esperado.

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 1 · Entregable: Excel P2: Calculadora de precio técnico

### 2 · Precio técnico y RAROC

#### 2.1 Cálculo y grilla

- **`PRC-P3-02.01.01`** Calcular el precio técnico mínimo (tasa piso con RAROC igual al hurdle) por celda de producto × plazo × canal × tramo de riesgo, y el RAROC de cada operación al precio vigente. Ninguna oferta por debajo del piso salvo excepción dentro de facultades (U-18).

  Aplica: Tier I–IV · Esfuerzo: 2 d · Automatización: 3 · Crítico · Entregable: Excel P2: Calculadora de precio técnico · Umbrales: U-18

- **`PRC-P3-02.01.02`** Verificar la monotonicidad del precio técnico respecto del riesgo dentro de cada celda (U-19) y la coherencia de la estructura por plazo.

  Aplica: Tier I–IV · Esfuerzo: 0.5 d · Automatización: 3 · Entregable: Excel P2: Calculadora de precio técnico · Umbrales: U-19

- **`PRC-P3-02.01.03`** Conciliar el precio técnico con Finanzas (FTP, costos, capital) y con Riesgos (PD, LGD); diferencias mayores a 5 pb por celda se explican por escrito.

  Aplica: Tier I–IV · Esfuerzo: 1 d · Automatización: 1 · Entregable: Documento P3: Metodología de precio técnico

#### 2.2 Documentación

- **`PRC-P3-02.02.01`** Documentar la metodología de precio técnico, sus supuestos, fuentes y fecha de vigencia de cada insumo, con cuadro de control de cambios.

  Aplica: Tier I–IV · Esfuerzo: 1.5 d · Automatización: 1 · Entregable: Documento P3: Metodología de precio técnico

<!-- CATALOGO:FIN -->
