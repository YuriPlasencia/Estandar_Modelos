"""
Genera el catálogo del estándar de Parámetros de riesgo (catalogo/par-r*.yaml) desde una definición estructurada.
Los IDs se asignan automáticamente (fase-tarea.subtarea.actividad), así nunca se repite numeración.
Una vez generado, el YAML es la fuente de verdad: este script solo se vuelve a ejecutar si se reestructura el estándar.

Formato de cada actividad: (texto, tiers, días, automatización, naturaleza, crítico, entregable, hito)
"""
import json
from pathlib import Path

ORIGEN = "Estándar de Parámetros de riesgo v1.0 (nuevo, 2026-10-17)"
CAB = ("# Fuente de verdad del catálogo normativo. Editar vía control de cambios (ver CONTRIBUTING.md).\n"
       "# Yuri Plasencia — Analytics Pricing & Revenue Management\n")
T = [1, 2, 3, 4]
T12 = [1, 2]
T123 = [1, 2, 3]

FASES = [
("PAR-R1", "Marco, alcance y gobierno de parámetros", [
  ("Alcance y usos", [
    ("Inventario de parámetros", [
      ("Inventariar los parámetros de riesgo por cartera y uso (PD 12 meses y lifetime, LGD, LGD en default, EAD/CCF, escenarios, criterios de staging, CLV) y registrar cada modelo en el inventario con su Tier.", T, 1, 1, "gobierno", True, ("Documento", "R1", "Mapa de parámetros y usos"), "Sprint 0"),
      ("Declarar los usos de cada parámetro (provisiones IFRS 9, provisiones regulatorias locales, capital, pricing, stress testing, CLV) y las diferencias de calibración que cada uso exige: point-in-time con forward-looking para IFRS 9, through-the-cycle o downturn para capital.", T, 1.5, 1, "analisis", True, ("Documento", "R1", "Mapa de parámetros y usos"), None),
    ]),
    ("Segmentación de carteras", [
      ("Definir las carteras con riesgo homogéneo (producto, segmento, garantía, canal, moneda) sobre las que se estiman los parámetros, con evidencia de homogeneidad y materialidad suficiente de defaults por segmento.", T, 2, 2, "datos", True, ("Excel", "R1", "Segmentación de carteras"), None),
    ]),
  ]),
  ("Definiciones comunes", [
    ("Default y unidad de análisis", [
      ("Alinear la definición de default de parámetros con la gestión del riesgo y con la contabilidad: en IFRS 9 el default no puede ocurrir después de los 90 días de atraso salvo evidencia que refute la presunción (U-28). Documentar el puente con la definición de default de los scores de originación (U-17: más de 60 días) y su efecto en la calibración.", T, 1.5, 1, "analisis", True, ("Documento", "R2", "Definiciones de default, cura y unidad"), None),
      ("Definir los criterios de salida de default y cura: período mínimo de observación y tratamiento de reestructurados (U-33), e impacto en LGD y en staging.", T, 1, 1, "analisis", True, ("Documento", "R2", "Definiciones de default, cura y unidad"), None),
    ]),
  ]),
  ("Gobierno inicial", [
    ("Kick off", [
      ("Kick off del proyecto de parámetros con Riesgos, Finanzas/Contabilidad, Estudios Económicos y Validación.", T, 0.5, 1, "reunion", False, ("Acta", "PAR-KO", "Kick off de parámetros"), "Kick Off"),
    ]),
  ]),
]),
("PAR-R2", "Datos y reconstrucción histórica", [
  ("Bases de estimación", [
    ("Series de default", [
      ("Construir las cohortes de default por cartera con al menos cinco años de historia que incluyan un período de estrés (U-27): saldos, estados de atraso mensuales, defaults, curas y salidas (prepago, castigo, venta).", T, 4, 2, "datos", True, ("Tabla", "R1", "Cohortes de default"), "Sprint 1"),
      ("Reconstruir la historia de calificaciones o scores en una escala estable para estimar matrices de migración, corrigiendo cambios de modelo con un mapeo documentado.", T12, 3, 2, "datos", False, ("Tabla", "R1", "Cohortes de default"), None),
    ]),
    ("Base de recuperaciones", [
      ("Construir la base de recuperaciones por default: flujos de cobranza, ejecución de garantías, costos directos e indirectos y fecha de cierre del proceso. Identificar los procesos incompletos y su tratamiento.", T, 4, 2, "datos", True, ("Tabla", "R2", "Base de recuperaciones (workout)"), None),
    ]),
    ("Base de exposición", [
      ("Construir la base de exposición: cronogramas de amortización, prepagos, líneas y uso de línea 12 meses antes del default para estimar CCF.", T, 2.5, 2, "datos", True, ("Tabla", "R3", "Base de exposición y uso de línea"), None),
    ]),
    ("Series macroeconómicas", [
      ("Recopilar las series macroeconómicas candidatas (PBI, desempleo, inflación, tasas, tipo de cambio, precios de inmuebles, términos de intercambio) con la misma frecuencia y rezagos que usará Estudios Económicos en sus escenarios.", T, 1.5, 2, "datos", True, ("Tabla", "R4", "Series macroeconómicas"), None),
    ]),
  ]),
  ("Calidad de datos", [
    ("Certificación", [
      ("Aplicar los controles de calidad de DES-D2 y los específicos de parámetros: continuidad de cohortes, defaults sin recuperación registrada, recuperaciones mayores al saldo, y conciliación de saldos y castigos con contabilidad.", T, 2.5, 3, "datos", True, ("Documento", "R3", "Certificación de datos de parámetros"), None),
      ("Certificar las bases con acta de conformidad de las fuentes (Riesgos, Cobranzas, Contabilidad, Estudios Económicos).", T, 0.5, 1, "gobierno", False, ("Documento", "R3", "Certificación de datos de parámetros"), None),
    ]),
  ]),
]),
("PAR-R3", "Probabilidad de default (PD)", [
  ("PD a 12 meses", [
    ("Estimación y calibración", [
      ("Estimar la PD a 12 meses por grado o segmento, o calibrar el score aprobado a tasas de default observadas siguiendo DES-D4-08, con la definición de default de R1.", T, 3, 2, "datos", True, ("Script", "R1", "Modelos de PD"), "Sprint 2"),
      ("Separar el componente through-the-cycle (tendencia de largo plazo) del point-in-time (ciclo), y documentar cómo se ancla la PD al promedio de largo plazo.", T12, 2, 2, "analisis", True, ("Documento", "R4", "Metodología de PD"), None),
    ]),
  ]),
  ("PD lifetime", [
    ("Estructura temporal", [
      ("Estimar la curva de PD lifetime (marginal y acumulada por período) con un método documentado: supervivencia en tiempo discreto, matrices de migración (Markov) o curvas vintage, según la cartera y los datos disponibles.", T, 4, 2, "datos", True, ("Script", "R1", "Modelos de PD"), None),
      ("Tratar los riesgos competitivos (prepago, cancelación, castigo) para no sobreestimar la PD acumulada de operaciones que salen del portafolio antes de su vencimiento.", T12, 2, 2, "datos", False, ("Script", "R1", "Modelos de PD"), None),
      ("Para matrices de migración: verificar monotonicidad (mayor PD en peores grados), estado absorbente de default y estabilidad de la matriz; si se condiciona al ciclo (factor Z de Vasicek u otro), documentar la estimación del factor.", T12, 1.5, 2, "datos", False, ("Script", "R1", "Modelos de PD"), None),
    ]),
  ]),
  ("Desempeño de la PD", [
    ("Validación de la PD", [
      ("Evaluar discriminación por horizonte y, sobre todo, calibración: tasa observada vs. PD por grado con el test de Jeffreys (U-30), en construcción y en los períodos más recientes.", T, 2, 3, "datos", True, ("Excel", "R2", "Desempeño y calibración de PD"), None),
      ("Documentar la metodología de PD, sus supuestos y limitaciones con la estructura de DES-D4-11.", T, 1.5, 1, "documentacion", False, ("Documento", "R4", "Metodología de PD"), None),
    ]),
  ]),
]),
("PAR-R4", "Severidad (LGD)", [
  ("LGD de operaciones vigentes", [
    ("LGD workout", [
      ("Calcular la LGD realizada por default como 1 menos el valor presente de las recuperaciones netas de costos sobre la EAD, descontadas a la tasa de interés efectiva (U-34).", T, 3, 2, "datos", True, ("Excel", "R3", "LGD realizada"), "Sprint 3"),
      ("Tratar los procesos de recuperación incompletos con un método documentado (proyección de recuperaciones remanentes, curvas de recuperación) en lugar de excluirlos, para no sesgar la LGD hacia los casos que se cierran rápido.", T, 2, 2, "datos", True, ("Excel", "R3", "LGD realizada"), None),
      ("Separar la LGD en sus componentes cuando aporte precisión: probabilidad de cura y severidad dado que no hay cura (modelo de dos etapas).", T12, 2, 2, "datos", False, ("Script", "R2", "Modelos de LGD"), None),
    ]),
    ("Modelo de LGD", [
      ("Estimar el modelo de LGD respetando su soporte acotado y su distribución bimodal (regresión fraccional, beta, dos etapas o métodos de ML con calibración), con drivers de garantía (LTV actual), producto y antigüedad del default.", T, 3, 2, "datos", True, ("Script", "R2", "Modelos de LGD"), None),
      ("Incorporar el forward-looking en la LGD cuando la recuperación dependa del ciclo (por ejemplo, precios de inmuebles para hipotecarios), con el mismo marco de escenarios de R6.", T12, 1.5, 2, "datos", False, ("Script", "R2", "Modelos de LGD"), None),
    ]),
  ]),
  ("LGD en default", [
    ("Exposiciones en default", [
      ("Estimar la LGD para exposiciones ya en default (mejor estimación de la pérdida, ELBE) en función del tiempo en default y del estado de la cobranza, para el cálculo de Stage 3.", T, 2, 2, "datos", True, ("Script", "R2", "Modelos de LGD"), None),
    ]),
  ]),
  ("Validación y documentación", [
    ("Desempeño de la LGD", [
      ("Comparar LGD estimada vs. realizada por segmento y por año de default, incluido el período de estrés, y evaluar el poder de ordenamiento.", T, 1.5, 3, "datos", True, ("Excel", "R4", "Desempeño de LGD"), None),
      ("Documentar la metodología de LGD (descuento, costos, incompletos, garantías, LGD en default).", T, 1.5, 1, "documentacion", False, ("Documento", "R5", "Metodología de LGD"), None),
    ]),
  ]),
]),
("PAR-R5", "Exposición (EAD y CCF)", [
  ("Exposición de productos amortizables", [
    ("Perfil de exposición", [
      ("Proyectar la exposición de cada período con el cronograma contractual ajustado por prepagos y cancelaciones esperadas, consistente con la tasa de interés efectiva.", T, 2, 2, "datos", True, ("Script", "R3", "Modelos de EAD y CCF"), "Sprint 3"),
    ]),
  ]),
  ("Exposición de productos revolventes", [
    ("CCF y vida conductual", [
      ("Estimar el factor de conversión (CCF) del monto no utilizado a 12 meses antes del default, con el uso de línea, la antigüedad y el estado de atraso como drivers.", T, 2.5, 2, "datos", True, ("Script", "R3", "Modelos de EAD y CCF"), None),
      ("Para revolventes (tarjetas, líneas), estimar el período de exposición conductual más allá del plazo contractual, durante el que el banco está expuesto porque no gestiona la línea en la práctica; documentar el horizonte usado para la ECL lifetime.", T, 1.5, 2, "analisis", True, ("Documento", "R6", "Metodología de EAD y vida conductual"), None),
    ]),
  ]),
]),
("PAR-R6", "Escenarios macroeconómicos y forward-looking", [
  ("Escenarios", [
    ("Diseño y probabilidades", [
      ("Recibir de Estudios Económicos al menos tres escenarios (base, optimista y pesimista) con sus probabilidades y su sustento, revisados como mínimo cada trimestre (U-32).", T, 1, 1, "gobierno", True, ("Documento", "R7", "Escenarios y probabilidades"), "Sprint 4"),
      ("Definir el horizonte de proyección explícito y la regla de reversión a la media de largo plazo de las variables macro y de los parámetros.", T, 1, 1, "analisis", True, ("Documento", "R7", "Escenarios y probabilidades"), None),
    ]),
  ]),
  ("Modelos satélite", [
    ("Vínculo macro–parámetros", [
      ("Estimar los modelos satélite que vinculan las variables macro con la tasa de default (y con la LGD cuando aplique): selección de variables con sentido económico y signo esperado, rezagos, y estabilidad fuera de muestra.", T, 3, 2, "datos", True, ("Script", "R4", "Modelos satélite"), None),
      ("Probar la no linealidad: la ECL ponderada se calcula como el promedio de las ECL de cada escenario, nunca como la ECL de un escenario promedio (U-32).", T, 1, 3, "datos", True, ("Excel", "R5", "ECL por escenario"), None),
      ("Evaluar riesgos que la macro no captura (clima, energía, cadenas de suministro, geopolítica, sectores concentrados) y decidir si requieren un ajuste del modelo o un overlay gobernado (R8).", T12, 1.5, 1, "analisis", False, ("Documento", "R7", "Escenarios y probabilidades"), None),
    ]),
  ]),
  ("Gobierno de escenarios", [
    ("Revisión trimestral", [
      ("Reunión trimestral de revisión de escenarios y probabilidades con Estudios Económicos, Riesgos y Contabilidad.", T, 0.25, 1, "reunion", False, ("Acta", "PAR-ESC", "Revisión de escenarios"), None),
    ]),
  ]),
]),
("PAR-R7", "Staging y aumento significativo del riesgo (SICR)", [
  ("Criterios de staging", [
    ("Criterios cuantitativos", [
      ("Comparar la PD lifetime actual con la PD lifetime en el reconocimiento inicial, por operación, con umbrales relativos y absolutos calibrados por cartera (U-29).", T, 2.5, 2, "datos", True, ("Documento", "R8", "Criterios de staging"), "Sprint 5"),
      ("Calibrar los umbrales SICR para que Stage 2 anticipe el default: proporción de defaults que pasaron antes por Stage 2, tiempo de permanencia y estabilidad de las transiciones.", T12, 2, 2, "datos", True, ("Excel", "R6", "Calibración de umbrales SICR"), None),
    ]),
    ("Criterios cualitativos y backstops", [
      ("Aplicar el backstop de 30 días de atraso para Stage 2 y el de default para Stage 3 (U-28), además de criterios cualitativos: refinanciados, lista de vigilancia y alertas tempranas.", T, 1, 2, "datos", True, ("Documento", "R8", "Criterios de staging"), None),
      ("Definir el retorno de Stage 2 a Stage 1 y de Stage 3 a Stage 2 con períodos de prueba (U-33), y documentar el tratamiento de activos adquiridos u originados con deterioro (POCI).", T, 1, 1, "analisis", False, ("Documento", "R8", "Criterios de staging"), None),
    ]),
  ]),
]),
("PAR-R8", "Pérdida crediticia esperada (ECL) y overlays", [
  ("Cálculo de la ECL", [
    ("Motor de cálculo", [
      ("Calcular la ECL por operación como la suma, período a período, de PD marginal × LGD × EAD descontada a la tasa de interés efectiva: 12 meses para Stage 1, lifetime para Stage 2 y LGD en default para Stage 3; ponderar por escenario (U-32).", T, 3, 2, "datos", True, ("Script", "R5", "Motor de ECL"), "Sprint 6"),
      ("Certificar el motor de ECL con el estándar IMP (coincidencia ≥ 95 % con el cálculo de modelamiento, U-15) y conciliar la ECL con contabilidad.", T, 2, 2, "datos", True, ("Documento", "14", "Certificación del modelo"), None),
    ]),
    ("Análisis de resultados", [
      ("Explicar los movimientos de la ECL entre períodos (originaciones, bajas, cambios de stage, cambios de parámetros, escenarios, castigos) para Contabilidad y para las revelaciones de IFRS 7.", T, 2, 3, "datos", True, ("Excel", "R7", "Movimiento de la ECL"), None),
      ("Calcular sensibilidades de la ECL: 100 % en cada escenario, cambios en ponderaciones y en umbrales SICR.", T, 1, 3, "datos", False, ("Excel", "R7", "Movimiento de la ECL"), None),
    ]),
  ]),
  ("Overlays y ajustes post-modelo", [
    ("Gobierno de overlays", [
      ("Todo overlay o ajuste post-modelo debe tener causa identificada (riesgo no capturado por el modelo), cuantificación reproducible, cartera afectada, fecha de revisión o expiración y aprobación en comité (U-31).", T, 1.5, 1, "gobierno", True, ("Documento", "R9", "Registro de overlays"), None),
      ("Reunión de aprobación de overlays y de los resultados de la ECL del período.", T, 0.25, 1, "reunion", False, ("Acta", "PAR-OVL", "Aprobación de overlays"), None),
      ("Planificar la absorción de cada overlay recurrente dentro del modelo en el siguiente ciclo de recalibrado, para que no se vuelva permanente.", T12, 1, 1, "analisis", False, ("Documento", "R9", "Registro de overlays"), None),
    ]),
  ]),
]),
("PAR-R9", "Backtesting, seguimiento y gobierno", [
  ("Backtesting", [
    ("Backtesting de parámetros", [
      ("Backtesting anual de PD (Jeffreys por grado, U-30), LGD (estimada vs. realizada), CCF y staging (proporción de defaults que estaban en Stage 2; transiciones entre stages).", T, 3, 3, "datos", True, ("Excel", "R8", "Backtesting de parámetros"), "Sprint 7"),
      ("Backtesting de la ECL: comparar pérdidas realizadas con la ECL constituida por cohorte, y explicar las diferencias (escenario materializado vs. probabilidades asignadas).", T12, 2, 3, "datos", False, ("Excel", "R8", "Backtesting de parámetros"), None),
      ("Reunión de resultados del backtesting y decisión de recalibrar o redesarrollar.", T, 0.25, 1, "reunion", False, ("Acta", "PAR-BT", "Resultados del backtesting"), None),
    ]),
  ]),
  ("Gobierno de provisiones", [
    ("Comité de provisiones", [
      ("Presentar al comité de provisiones los parámetros, escenarios, staging, overlays y la ECL resultante, con el puente frente a las provisiones regulatorias locales cuando ambas coexistan.", T, 0.5, 1, "reunion", True, ("Acta", "PAR-CP", "Comité de provisiones"), "Comité de provisiones"),
      ("Mantener la documentación del ciclo de cálculo (insumos, versiones, controles, aprobaciones) para auditoría externa y supervisión, con cuadro de control de cambios.", T, 1, 2, "documentacion", True, ("Documento", "R10", "Manual del ciclo de provisiones"), None),
    ]),
  ]),
]),
("PAR-R10", "Valor de vida del cliente (CLV) y usos de gestión", [
  ("CLV", [
    ("Modelo de valor", [
      ("Construir el valor de vida del cliente con los mismos parámetros lifetime (supervivencia por default, prepago y fuga, margen esperado, costo de riesgo y costo de capital) para que gestión, pricing y provisiones usen una sola visión del riesgo.", T12, 3, 2, "datos", False, ("Script", "R6", "Modelo de CLV"), "Sprint 8"),
      ("Documentar las diferencias entre los parámetros contables (PIT con forward-looking) y los de gestión (por ejemplo, TTC para pricing de largo plazo) y en qué uso aplica cada uno.", T123, 1, 1, "documentacion", False, ("Documento", "R1", "Mapa de parámetros y usos"), None),
    ]),
  ]),
  ("Entrega a usuarios", [
    ("Consumo de parámetros", [
      ("Publicar los parámetros vigentes en una tabla versionada con fecha de vigencia para sus consumidores (motor de ECL, pricing PRC-P3, capital, stress testing), con el registro de qué versión usó cada proceso.", T, 1.5, 2, "datos", True, ("Tabla", "R5", "Parámetros vigentes versionados"), None),
    ]),
  ]),
]),
]


def main():
    out = Path(__file__).resolve().parent.parent / "catalogo"
    total = 0
    for code, nombre, tareas in FASES:
        lines = [CAB.rstrip("\n"), f"fase: {code}", f"nombre: {json.dumps(nombre, ensure_ascii=False)}",
                 "estandar: Parámetros", f"origen: {json.dumps(ORIGEN, ensure_ascii=False)}", "actividades:"]
        for ti, (tarea, subs) in enumerate(tareas, 1):
            for si, (sub, acts) in enumerate(subs, 1):
                for ai, (txt, tiers, dias, aut, nat, crit, ent, hito) in enumerate(acts, 1):
                    lines += [f"- id: {code}-{ti:02d}.{si:02d}.{ai:02d}",
                              f"  tarea: {json.dumps(tarea, ensure_ascii=False)}",
                              f"  subtarea: {json.dumps(sub, ensure_ascii=False)}",
                              f"  actividad: {json.dumps(txt, ensure_ascii=False)}",
                              f"  aplica_tier: {json.dumps(tiers)}",
                              f"  dias_esfuerzo: {dias}",
                              f"  nivel_automatizacion: {aut}",
                              f"  naturaleza: {nat}"]
                    if crit:
                        lines.append("  critico: true")
                    tipo, num, desc = ent
                    lines += ["  entregables:", f"  - {{tipo: {tipo}, numero: {json.dumps(num)}, descripcion: {json.dumps(desc, ensure_ascii=False)}}}"]
                    if hito:
                        lines.append(f"  hito: {json.dumps(hito, ensure_ascii=False)}")
                    total += 1
        (out / f"{code.lower()}.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(FASES)} fases · {total} actividades")


if __name__ == "__main__":
    main()
