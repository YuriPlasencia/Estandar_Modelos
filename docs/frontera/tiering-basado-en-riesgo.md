---
id: FR-02
titulo: "FR-02 · Tiering basado en riesgo"
estandar: Frontera
estado: Propuesta
version: 0.1.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 52
---

# FR-02 · Tiering basado en riesgo

> **Línea base 2.0:** la Res. SBS 00053-2023 (art. 6) exige categorizar por materialidad, uso y complejidad con
> criterios aprobados por el comité (GOB-G2-02.01.01). Esta propuesta es un punto de partida para esos criterios.

**Problema:** el estándar usa Tier I–III para activar requisitos, pero no define cómo se asigna el Tier.
Eso produce asignaciones inconsistentes entre equipos.

**Propuesta:** un puntaje transparente de 0 a 100 con cuatro dimensiones.

| Dimensión | Peso | 1 punto (bajo) | 3 puntos (medio) | 5 puntos (alto) |
|---|---|---|---|---|
| **Materialidad** (saldo / ingreso / provisiones afectadas) | 35 % | < 1 % del portafolio | 1–10 % | > 10 % |
| **Uso** | 25 % | Informativo / interno | Decisión con revisión humana | Decisión automática, regulatoria o contable |
| **Complejidad** | 20 % | Regla o lineal simple | Lineal con segmentos / calibraciones | ML, ensambles, IA generativa |
| **Incertidumbre e impacto en clientes** | 20 % | Datos maduros y estables | Datos nuevos o proveedor externo | Población nueva, sin historia, o impacto directo en clientes |

$$\text{Puntaje}=20\sum_{d}w_d\cdot s_d,\qquad s_d\in\{1,\dots,5\}$$

| Puntaje | Tier |
|---|---|
| ≥ 75 | I |
| 55 – 74 | II |
| < 55 | III |

**Regla de piso:** todo modelo regulatorio o contable (capital, IFRS 9) es **mínimo Tier II**; todo modelo
de decisión automática sobre personas naturales con ML es **mínimo Tier II**.

Los cortes son ilustrativos y deben calibrarse reclasificando el inventario actual: la propuesta se aprueba
si reproduce ≥ 80 % de los Tiers vigentes y las discrepancias tienen justificación.
