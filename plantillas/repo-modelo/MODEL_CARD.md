# Ficha de nacimiento del modelo

```yaml
codigo_inventario: ""          # IMP-01.05.03
nombre: ""
version: "1.0.0"
tipo_estandar: Desarrollo      # Desarrollo | Calibración
tier: ""                       # I | II | III | IV  (acta: VAL-M-01.13)
tipo_modelo: ""                # lineal | ml | arbol | acp
enfoque: ""                    # agil | completo
uso: ""                        # originación | comportamiento | cobranza | estimador | PD/LGD/EAD | otro
decision_automatica: false
poblacion_objetivo: ""
target:
  tipo: ""                     # binario | continuo
  definicion: "Atraso > 60 días al menos una vez en 12 meses desde la observación"   # U-17; desviaciones con acta
  fecha_observacion: ""        # admision: fecha de otorgamiento | buro: fecha de la foto (clientes activos)
  materialidad: ""             # monto mínimo vencido (Documento 4)
ventana:
  train_test: ""               # >= 12 meses (U-01)
  oot: ""                      # último mes con desempeño completo (U-01)
segmentos: []
metricas_construccion: {gini_train: null, gini_test: null, gini_oot: null}
modelo_reemplazado: ""
dueno_negocio: ""
lider_desarrollo: ""
validador: ""
fecha_aprobacion_cm: ""
fecha_produccion: ""
ruta_productiva: ""
dependencias: []               # otros modelos o fuentes externas (IMP-01.01.04)
limitaciones: []               # resumen de PPT 14
```

## Narrativa

1. **Propósito y uso permitido.**
2. **Datos.**
3. **Desempeño.**
4. **Limitaciones conocidas.**
5. **Plan de seguimiento.**
