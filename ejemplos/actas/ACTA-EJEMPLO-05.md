# Acta de reunión · ACTA-MOD-EJEMPLO-001-05

**Reunión 5 · Selección del modelo final** · Estado: **Aprobada** · Versión 1 · Requisito del estándar: `DES-D4-06.03.01`

## 1. Datos generales

| | | | |
|---|---|---|---|
| **Código de modelo** | MOD-EJEMPLO-001 | **Nombre del modelo** | Score de originación — ejemplo |
| **Tier** | II | **Tipo de modelo** | ML |
| **Fecha** | 2026-10-20 | **Horario** | 10:00 – 11:15 |
| **Modalidad** | Virtual | **Lugar / enlace** | Sala virtual del equipo |
| **Secretario** | Analista de modelos (ejemplo) | **Hito** | Acta 5 |

## 2. Participantes

| Nombre | Área | Rol | Asistió |
|---|---|---|---|
| Gerente de producto (ejemplo) | Negocio / banca usuaria | Decide | Sí |
| Jefe de modelos (ejemplo) | Jefatura de modelos | Aprueba | Sí |
| Analista de modelos (ejemplo) | Equipo de modelos | Secretario | Sí |

## 3. Objetivo

Seleccionar el modelo final a partir de su desempeño, estabilidad y sentido económico.

## 4. Agenda

1. Indicadores del modelo final (global, por mes, por segmento, meses recientes)
2. Diferencia de desempeño Train vs. OOT
3. Comparación con el modelo vigente
4. Sentido económico de las variables finales

## 5. Desarrollo de la reunión

Se presentaron tres modelos candidatos (XGBoost, LightGBM y logística WOE como benchmark). El XGBoost obtuvo Gini OOT de 52.1 frente a 54.0 en Train (diferencia de 1.9 pts, dentro de U-11) y supera al modelo vigente en 6.4 pts en las cosechas aprobadas de los últimos seis meses.

Negocio revisó el sentido económico de las 24 variables finales; se pidió retirar una variable de canal por riesgo de sesgo operativo.

## 6. Decisiones

| # | Decisión | Requisito | Responsable | Estado |
|---|---|---|---|---|
| 1 | Modelo final seleccionado | DES-D4-06.03.01 | Gerente de producto (ejemplo) | Acordada |
| 2 | Diferencia de Gini Train–OOT ≤ 10 pts (o excepción sustentada) | U-11 | Jefe de modelos (ejemplo) | Acordada |
| 3 | Variables finales con sentido económico validado | DES-D4-05.02.02 | Jefe de modelos (ejemplo) | Acordada |

## 7. Excepciones a umbrales

No se registraron excepciones.

## 8. Acuerdos y pendientes

| # | Acción | Responsable | Fecha compromiso | Estado |
|---|---|---|---|---|
| 1 | Reentrenar sin la variable de canal y confirmar Gini OOT | Analista de modelos (ejemplo) | 2026-10-24 | Abierto |

## 9. Evidencias y entregables revisados

- PPT 9 · Indicadores del modelo final
- PPT 10 · Comparación con el modelo vigente

## 10. Conformidad

| Nombre | Área / cargo | Conformidad | Fecha | Medio |
|---|---|---|---|---|
| Gerente de producto (ejemplo) | Negocio / banca usuaria | Conforme | 2026-10-21 | Correo |
| Jefe de modelos (ejemplo) | Jefatura de modelos | Conforme | 2026-10-21 | Correo |

## 11. Control de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1 | 2026-10-20 | Creación del acta |
| 1 | 2026-10-21 | Aprobada |

---
*Estándares de Modelos en Banca v1.2.0 · Yuri Plasencia — Analytics Pricing & Revenue Management*
