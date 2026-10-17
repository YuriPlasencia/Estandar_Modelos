---
id: PRC-IA
titulo: "Pricing · Agentes de IA en el ciclo de pricing"
estandar: Pricing
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 30
---

# Pricing · Agentes de IA en el ciclo de pricing

Pricing es una de las áreas donde los agentes de IA aportan más. El trabajo es repetitivo y muy cargado de
datos (recalcular pisos, refrescar curvas, preparar escenarios, redactar comités), y las decisiones están
muy reguladas. La regla que lo hace posible es simple: **el agente prepara, la persona decide**.
PRC-P9-03.01.01 lo hace obligatorio.

## Arquitectura de referencia

```text
                    ┌──────────────────────────────────────────────┐
                    │  Analista de pricing (orquesta, revisa, firma)│
                    └───────────────┬──────────────────────────────┘
                                    │ instrucciones + aprobación por paso
   ┌───────────────┬────────────────┼────────────────┬───────────────────┐
   ▼               ▼                ▼                ▼                   ▼
 Agente de      Agente de        Agente de        Agente de          Agente revisor
 datos          precio técnico   respuesta        escenarios         (2ª opinión)
 P2: arma la    P3: recalcula    P4: reentrena,   P5: corre el       contrasta contra
 base, corre    pisos y RAROC    calibra, reporta optimizador y      el catálogo y los
 controles      por celda        U-20/U-21        arma el comité     umbrales; lista
                                                                     faltantes
   │               │                │                │                   │
   └───────────────┴──── herramientas permitidas ────┴───────────────────┘
        consultas de solo lectura · scripts del toolkit · tools/acta.py · catálogo
   ─────────────────────────── límite duro ───────────────────────────────
        SIN acceso a: publicar tarifario · motor de precios · aprobar actas
```

## Qué hace cada agente y qué no

| Agente | Hace | Nunca |
|---|---|---|
| **Datos** | Construye la base de cotizaciones, corre los controles de PRC-P2-02.01.01, reporta variación exógena | Modificar fuentes, borrar registros |
| **Precio técnico** | Recalcula pisos y RAROC cuando cambian FTP, costos o PD/LGD; concilia diferencias > 5 pb | Cambiar supuestos de Finanzas o Riesgos |
| **Respuesta** | Reentrena con restricciones monotónicas, reporta calibración por decil y tramo de precio | Relajar U-20 o U-21 para "mejorar" resultados |
| **Escenarios** | Corre el optimizador con robustez, arma escenarios, redacta el borrador del acta PRC-CP | Elegir el escenario, enviar al comité |
| **Revisor** | Contrasta entregables con el catálogo (PRC, VAL-P) y los umbrales; lista faltantes | Dar conformidad |

## Controles obligatorios

1. **Registro del agente:** rol, modelo usado, versión, herramientas y datos a los que accede (PRC-P9-03.01.01).
2. **Log completo** de instrucciones, llamadas a herramientas y salidas, conservado con la evidencia del proyecto.
3. **Herramientas de solo lectura** sobre datos productivos. Los agentes escriben solo en el espacio del proyecto.
4. **Citas obligatorias:** toda afirmación normativa cita el ID (`PRC-P3-02.01.01`, `U-18`). Ver `AGENTS.md`.
5. **Evaluación del agente:** antes de usarlo en un proyecto Tier I–II se prueba con un caso cerrado de
   resultado conocido. Por ejemplo, recalcular el piso de un tarifario ya aprobado y obtener la misma cifra al punto básico.
6. **Sin datos de clientes en prompts a servicios externos** no aprobados por Seguridad de la Información.

## Impacto esperado en el esfuerzo

El modelo de esfuerzo v2 aplica a pricing la misma lógica que a desarrollo: el agente reduce el trabajo de
datos (≈ 75 %) y documentación (≈ 70 %), menos el de análisis (≈ 40 %), y nada en gobierno ni en reuniones.
Ver los resultados en [Estimación](../marco/estimacion.md) y en el Planificador (estándar *Pricing*).
