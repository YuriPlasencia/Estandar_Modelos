---
id: PLT-FICHA
titulo: "Plantilla · Ficha de nacimiento del modelo (Model Card)"
estandar: Plantillas
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 60
---

# Plantilla · Ficha de nacimiento del modelo (Model Card)

> Copiar este bloque al repositorio del modelo como `MODEL_CARD.md`. Los campos en YAML permiten que el
> inventario y los agentes lean la ficha sin intervención manual. Cumple DES-D1-01.04.08 y DES-D7-01.01.04.

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
  oot: ""                      # >= 6 meses (U-01)
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

## Narrativa (1 página)

1. **Propósito y uso permitido.** Para qué sirve y para qué *no* debe usarse.
2. **Datos.** Fuentes, periodo, exclusiones principales.
3. **Desempeño.** Global, por segmento y en meses recientes.
4. **Limitaciones conocidas.** Discriminación, calibración, estabilidad, subpoblaciones.
5. **Plan de seguimiento.** Indicadores, periodicidad y responsable.
