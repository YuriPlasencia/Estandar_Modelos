"""
Generador genérico de catálogos desde definiciones estructuradas (IDs automáticos fase-tarea.subtarea.actividad).
Lo usan generar_par.py y las definiciones de Gobierno (GOB) y Seguimiento (SEG) de este archivo.
Una vez generado, el YAML es la fuente de verdad: solo se regenera si se reestructura el estándar.

Formato de cada actividad: (texto, tiers, días, automatización, naturaleza, crítico, entregable, hito)
"""
import json
from pathlib import Path

CAB = ("# Fuente de verdad del catálogo normativo. Editar vía control de cambios (ver CONTRIBUTING.md).\n"
       "# Yuri Plasencia — Analytics Pricing & Revenue Management\n")
T, T12 = [1, 2, 3, 4], [1, 2]


def escribir(fases, estandar, origen):
    out = Path(__file__).resolve().parent.parent / "catalogo"
    total = 0
    for code, nombre, tareas in fases:
        L = [CAB.rstrip("\n"), f"fase: {code}", f"nombre: {json.dumps(nombre, ensure_ascii=False)}",
             f"estandar: {estandar}", f"origen: {json.dumps(origen, ensure_ascii=False)}", "actividades:"]
        for ti, (tarea, subs) in enumerate(tareas, 1):
            for si, (sub, acts) in enumerate(subs, 1):
                for ai, (txt, tiers, dias, aut, nat, crit, ent, hito) in enumerate(acts, 1):
                    L += [f"- id: {code}-{ti:02d}.{si:02d}.{ai:02d}", f"  tarea: {json.dumps(tarea, ensure_ascii=False)}",
                          f"  subtarea: {json.dumps(sub, ensure_ascii=False)}", f"  actividad: {json.dumps(txt, ensure_ascii=False)}",
                          f"  aplica_tier: {json.dumps(tiers)}", f"  dias_esfuerzo: {dias}", f"  nivel_automatizacion: {aut}",
                          f"  naturaleza: {nat}"]
                    if crit:
                        L.append("  critico: true")
                    if ent:
                        tipo, num, desc = ent
                        L += ["  entregables:", f"  - {{tipo: {tipo}, numero: {json.dumps(num)}, descripcion: {json.dumps(desc, ensure_ascii=False)}}}"]
                    if hito:
                        L.append(f"  hito: {json.dumps(hito, ensure_ascii=False)}")
                    total += 1
        (out / f"{code.lower()}.yaml").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{estandar}: {len(fases)} fases · {total} actividades")


GOB = [
("GOB-G1", "Organización y comité de riesgos de modelo", [
  ("Estructura", [
    ("Roles e independencia", [
      ("Mantener una función de riesgo de modelo independiente de las áreas que desarrollan, usan e implementan los modelos, con un responsable que reporta a la gerencia de riesgos (SBS 53-2023 arts. 12–13).", T, 0, 1, "gobierno", True, None, None),
      ("Los responsables de validación y seguimiento tienen al menos el mismo nivel organizacional que los de desarrollo; los desarrolladores están separados de las unidades de negocio.", T, 0, 1, "gobierno", True, None, None),
      ("Asignar al usuario del modelo la propiedad de su riesgo de uso y la obligación de usarlo solo para el propósito aprobado (SBS art. 19).", T, 0, 1, "gobierno", False, None, None),
    ]),
    ("Comité de riesgos de modelo", [
      ("Operar un comité de riesgos de modelo con al menos un director, el jefe de riesgos y los responsables de desarrollo, validación y seguimiento, que sesione como mínimo cada trimestre (SBS arts. 10–11).", T, 0, 1, "gobierno", True, ("Acta", "CRM", "Comité de riesgos de modelo"), None),
      ("El comité aprueba los criterios de categorización (Tier), los indicadores y umbrales de seguimiento, la periodicidad de las validaciones, los informes de validación y seguimiento y las acciones ante debilidades.", T, 0, 1, "gobierno", True, ("Acta", "CRM", "Comité de riesgos de modelo"), None),
      ("El directorio aprueba las políticas, asigna recursos y aprueba las excepciones de uso de modelos de mayor categoría con debilidades relevantes (SBS art. 9).", T, 0, 1, "gobierno", True, None, None),
    ]),
  ]),
]),
("GOB-G2", "Inventario y categorización", [
  ("Inventario", [
    ("Registro de modelos", [
      ("Mantener un inventario completo y actualizado de modelos con sus atributos mínimos (propósito, uso, dueño, categoría, estado, versión, validaciones, debilidades), incluidas herramientas informales influyentes como hojas de cálculo y los sistemas de IA.", T, 0, 2, "gobierno", True, ("Documento", "G1", "Inventario de modelos"), None),
      ("Remitir el inventario al supervisor con la periodicidad y el formato que exija la norma local (en Perú, anualmente vía SUCAVE según el Anexo A de la Res. SBS 53-2023).", T, 0, 2, "gobierno", True, ("Documento", "G1", "Inventario de modelos"), None),
    ]),
  ]),
  ("Categorización", [
    ("Criterios de categoría", [
      ("Categorizar cada modelo por materialidad, uso y complejidad con criterios aprobados por el comité (ver FR-02); la categoría determina la profundidad y frecuencia de validación y seguimiento y si se exige réplica completa (SBS art. 6; U-35).", T, 0, 1, "gobierno", True, ("Documento", "G2", "Criterios de categorización"), None),
      ("Revisar periódicamente el propio esquema de categorización (que sea objetivo y que discrimine), como exige SS1/23.", T12, 0, 1, "analisis", False, ("Documento", "G2", "Criterios de categorización"), None),
    ]),
  ]),
]),
("GOB-G3", "Políticas, aprobación y documentación", [
  ("Ciclo de aprobación", [
    ("Aprobación previa", [
      ("Todo modelo nuevo, modificado (cambio de variables, supuestos o parámetros, incluida una recalibración) o con cambio de uso requiere validación y aprobación previa del comité antes de usarse (SBS art. 17).", T, 0, 1, "gobierno", True, None, None),
    ]),
    ("Manuales", [
      ("Mantener manuales aprobados de desarrollo, validación, uso, seguimiento, categorización, calidad de datos y contratación de proveedores de modelos (SBS art. 14); este estándar cumple esa función para los modelos analíticos.", T, 0, 1, "documentacion", True, None, None),
      ("Conservar la documentación de cada modelo (desarrollo, validación, seguimiento, actas, bases, diccionarios y código) con historial de versiones y disponible para el supervisor (SBS art. 15).", T, 0, 2, "documentacion", True, None, None),
    ]),
  ]),
]),
("GOB-G4", "Modelos de terceros y sistemas de IA", [
  ("Terceros", [
    ("Proveedores", [
      ("La entidad es plenamente responsable de los modelos de terceros: puede tercerizar desarrollo, validación o implementación, pero el seguimiento lo hace la propia entidad (SBS arts. 23–24).", T, 0, 1, "gobierno", True, None, None),
      ("Para modelos de terceros de mayor categoría, exigir réplica; si la propiedad intelectual lo impide, aplicar benchmarking u otra técnica alternativa documentada (SBS art. 25).", T, 0, 1, "gobierno", True, None, None),
      ("Contar con una estrategia de continuidad para los modelos de proveedores que soportan servicios priorizados.", T12, 0, 1, "gobierno", False, None, None),
    ]),
  ]),
  ("Sistemas de IA", [
    ("IA responsable", [
      ("Inventariar los sistemas de IA (incluidos los de IA generativa y los agentes) y aplicarles controles proporcionales a su riesgo: los modelos de IA no generativa siguen este estándar; los generativos y agénticos, además, el estándar AGT.", T, 0, 2, "gobierno", True, ("Documento", "G1", "Inventario de modelos"), None),
      ("Adoptar principios de IA responsable (transparencia, equidad, privacidad, seguridad y supervisión humana) traducidos en métricas y controles verificables, no solo en declaraciones.", T12, 0, 1, "gobierno", False, None, None),
    ]),
  ]),
]),
("GOB-G5", "Reporte, debilidades y auditoría", [
  ("Debilidades", [
    ("Gestión de debilidades", [
      ("Registrar cada debilidad o hallazgo con severidad, responsable, plazo y estado; si no puede corregirse de inmediato, aplicar medidas temporales de mitigación (SBS art. 7).", T, 0, 2, "gobierno", True, ("Documento", "G3", "Registro de debilidades"), None),
    ]),
  ]),
  ("Reporte", [
    ("Informe anual", [
      ("La unidad de riesgos emite un informe anual con el estado de las debilidades, los modelos desarrollados o modificados en los últimos 12 meses y el cronograma de los próximos 12 meses (SBS art. 8).", T, 0, 2, "documentacion", True, ("Documento", "G4", "Informe anual de riesgo de modelo"), None),
      ("Auditoría interna incluye en su plan anual la evaluación del cumplimiento de la gestión de riesgo de modelo.", T, 0, 1, "gobierno", True, None, None),
    ]),
  ]),
]),
]

SEG = [
("SEG-S1", "Diseño del seguimiento", [
  ("Plan de seguimiento", [
    ("Indicadores y umbrales", [
      ("Definir para cada modelo los indicadores de seguimiento (estabilidad, discriminación, calibración, forzajes, calidad de datos y, para IA, sobreajuste) con umbrales y alertas aprobados por el comité de riesgos de modelo (SBS art. 21; U-37).", T, 1.5, 2, "analisis", True, ("Documento", "S1", "Plan de seguimiento"), "Sprint 0"),
      ("Fijar la periodicidad por categoría (Tier I mensual o trimestral; Tier III–IV al menos semestral) y la fecha en que cada cosecha madura lo suficiente para medir desempeño.", T, 0.5, 1, "analisis", False, ("Documento", "S1", "Plan de seguimiento"), None),
      ("Asegurar los datos de seguimiento: tabla productiva con versión del modelo, scores, decisiones, forzajes y desempeño posterior; para estimadores, la muestra mínima acordada en DES-D5-01.03.01.", T, 2, 2, "datos", True, ("Tabla", "S1", "Base de seguimiento"), None),
    ]),
  ]),
]),
("SEG-S2", "Ejecución del seguimiento", [
  ("Indicadores", [
    ("Estabilidad y datos", [
      ("Medir el PSI del score y de cada variable frente a la población de construcción, y los controles de calidad de los datos productivos (missings, duplicados, fuentes desactualizadas).", T, 1, 4, "datos", True, ("Dashboard", "S1", "Tablero de seguimiento"), None),
    ]),
    ("Desempeño", [
      ("Medir la discriminación (Gini, KS) por cosecha madura, global y por segmento, frente a la de construcción (U-37).", T, 1, 4, "datos", True, ("Dashboard", "S1", "Tablero de seguimiento"), None),
      ("Medir la calibración: tasa observada vs. PD por tramo con intervalos binomiales o de Jeffreys; para estimadores, el % de casos dentro de ±25 % y ±50 % (U-12).", T, 1, 4, "datos", True, ("Dashboard", "S1", "Tablero de seguimiento"), None),
      ("Para modelos de IA, medir el sobreajuste en producción: brecha de desempeño entre construcción y los meses recientes (SBS art. 22).", T, 0.5, 3, "datos", False, ("Dashboard", "S1", "Tablero de seguimiento"), None),
    ]),
    ("Uso y forzajes", [
      ("Medir el volumen de forzajes (overrides) y el desempeño de los casos forzados frente a los no forzados, por motivo y por nivel que forzó (U-36).", T, 1, 3, "datos", True, ("Dashboard", "S1", "Tablero de seguimiento"), None),
      ("Verificar que el modelo se usa solo para el propósito y la población aprobados; un uso nuevo es un cambio de uso que requiere aprobación (GOB-G3-01.01.01).", T, 0.5, 1, "gobierno", True, None, None),
    ]),
  ]),
]),
("SEG-S3", "Acciones ante alertas", [
  ("Respuesta", [
    ("Árbol de decisión", [
      ("Aplicar el árbol de decisión: verde, continuar; ámbar, análisis de causa raíz en un mes; rojo en calibración con discriminación aceptable, calibrar (CAL); rojo en discriminación, redesarrollar (DES); rojo en datos, plan de contingencia (IMP-01.02.01).", T, 1, 1, "analisis", True, ("Documento", "S2", "Informe de seguimiento"), None),
      ("Escalar al comité un rojo que persista tres períodos o un cambio material de política o de población, con medidas temporales de mitigación mientras se corrige (SBS art. 7).", T, 0.5, 1, "gobierno", True, ("Acta", "CRM", "Comité de riesgos de modelo"), None),
    ]),
  ]),
]),
("SEG-S4", "Reporte del seguimiento", [
  ("Informes", [
    ("Informe periódico", [
      ("Emitir el informe de seguimiento al menos una vez al año (más frecuente según categoría) con desviaciones de indicadores, backtesting, sensibilidad, forzajes, cumplimiento de acciones y, para IA, sobreajuste; aprobarlo en el comité (SBS art. 22).", T, 2, 2, "documentacion", True, ("Documento", "S2", "Informe de seguimiento"), None),
      ("Actualizar el inventario con el estado del modelo y sus debilidades abiertas después de cada informe (GOB-G2-01.01.01).", T, 0.25, 2, "gobierno", False, None, None),
    ]),
  ]),
]),
]

if __name__ == "__main__":
    escribir(GOB, "Gobierno", "Línea base 2.0 (2026-10-17): Res. SBS 00053-2023, SR 26-2, PRA SS1/23 y práctica pública de bancos de referencia")
    escribir(SEG, "Seguimiento", "Línea base 2.0 (2026-10-17): consolidación de requisitos vigentes, Res. SBS 00053-2023 y práctica de bancos de referencia")
