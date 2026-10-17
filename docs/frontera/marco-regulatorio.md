---
id: FR-01
titulo: "FR-01 · Marco regulatorio de referencia"
estandar: Frontera
estado: Propuesta
version: 0.1.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 51
---

# FR-01 · Marco regulatorio de referencia

**Propuesta:** mapear cada requisito del estándar contra los marcos de referencia internacionales para poder
demostrar cumplimiento ante supervisores, auditores y casas matrices, y detectar brechas.

| Marco | Alcance | Ideas clave para nuestro estándar |
|---|---|---|
| **SR 26-2** (Fed/OCC/FDIC, EE. UU., abril 2026; reemplaza a SR 11-7) | Gestión del riesgo de modelo basada en riesgo | Enfoque proporcional, sección de terceros; excluye IA generativa y agéntica |
| **Res. SBS 00053-2023** (Perú) | Gestión de riesgos de modelo | Ya incorporada a la línea base 2.0: ver [Gobierno del riesgo de modelo](../marco/gobierno-mrm.md) |
| *SR 11-7 (histórico, 2011)* | Gestión del riesgo de modelo | *Effective challenge*; validación de solidez conceptual, monitoreo continuo y *outcomes analysis*; inventario completo |
| **PRA SS1/23** (Reino Unido) | Principios de MRM para bancos | Cinco principios: identificación y clasificación, gobierno, desarrollo/implementación/uso, validación independiente, mitigantes; incluye explícitamente modelos de ML y de proveedores |
| **EU AI Act** (Reglamento UE 2024/1689) | IA de alto riesgo | La evaluación de solvencia y el *credit scoring* de personas naturales son de **alto riesgo**: gestión de riesgos, gobernanza de datos, documentación técnica, registro de eventos, transparencia, supervisión humana, exactitud y robustez |
| **IFRS 9** | Pérdida esperada | Coherencia entre scores, PD/LGD/EAD y provisiones (ya cubierto parcialmente en DES-D5-01.02) |
| **Basilea / EBA IRB** | Modelos regulatorios de capital | Definición de default, *margin of conservatism*, backtesting de PD |
| **Regulación local** | Gestión de riesgo de modelo del supervisor local | En Perú: Res. SBS 00053-2023, mapeada artículo por artículo en [Gobierno](../marco/gobierno-mrm.md) |

## Brechas detectadas frente al estándar actual

1. **Criterios de Tier** no definidos (ver FR-02). SS1/23 los exige explícitos.
2. **Seguimiento** sin estándar formal (ver [Seguimiento](../seguimiento/seguimiento.md)).
3. **Modelos de proveedores** y **modelos de IA generativa** fuera del alcance explícito (ver FR-08).
4. **Supervisión humana / overrides** no medidos: el AI Act y SS1/23 piden monitorear el uso real del modelo.
5. **Uso fuera de alcance**: falta un control de *post-model adjustments* y de usos no previstos.

## Entregable propuesto

Una columna `marcos` en el catálogo YAML, p.ej. `marcos: [SR11-7:validacion, SS1/23:P4, AIAct:art10]`,
que permita generar automáticamente una matriz de cumplimiento.
