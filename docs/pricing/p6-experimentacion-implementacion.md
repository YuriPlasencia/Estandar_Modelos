---
id: PRC-P6
titulo: "Pricing · P6–P7 Experimentación e implementación"
estandar: Pricing
estado: Vigente
version: 1.0.0
custodio: Yuri Plasencia — Analytics Pricing & Revenue Management
actualizado: 2026-10-17
orden: 28
---

# Pricing · P6–P7 Experimentación e implementación

## P6 · Experimentar antes de escalar

Un experimento de precio bien diseñado es la única forma de medir la elasticidad sin sesgo, y además es la
mejor defensa ante el comité: muestra el efecto real en lugar de una proyección.

**Tamaño muestral** por brazo, para detectar una diferencia $\delta$ en la tasa de aceptación $p$:

$$n=\frac{\left(z_{1-\alpha/2}+z_{1-\beta}\right)^2\,2\,p\,(1-p)}{\delta^2}$$

Ejemplo: con $p=0.30$, $\delta=0.02$, $\alpha=5\,\%$ y potencia 80 % (U-22), $n\approx 8\,240$ ofertas por brazo.

**Reglas de oro**

- Pre-registrar hipótesis, métrica primaria, MDE, duración y regla de parada **antes** de lanzar (PRC-P6-01.01.01).
- No mirar los resultados para decidir antes de tiempo: inflar el error tipo I es la causa número uno de
  "pilotos exitosos" que luego no se replican.
- Aleatorizar por la unidad que decide (cliente, no oferta, si el cliente puede re-cotizar).
- Métricas de resguardo: riesgo de la cosecha, quejas, conversión por canal.
- Ética y conducta: los precios de prueba respetan topes y transparencia y se asignan por regla objetiva (PRC-P6-01.01.02).

<!-- CATALOGO:INICIO PRC-P6 -->
## Catálogo de requisitos · Experimentación y piloto

> Bloque generado desde `catalogo/prc-p6.yaml` (6 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Pricing Analítico v1.0 (nuevo, 2026-10-17).

### 1 · Diseño del experimento

#### 1.1 Protocolo

- **`PRC-P6-01.01.01`** Pre-registrar el experimento antes de lanzarlo: hipótesis, métrica primaria (margen esperado por oferta o conversión), métricas de resguardo (riesgo de cosecha, quejas), unidad de aleatorización, tamaño muestral con potencia y MDE (U-22), duración y regla de parada.

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 1 · Crítico · Entregable: Documento P6: Diseño del experimento · Hito: Sprint 5 · Umbrales: U-22

- **`PRC-P6-01.01.02`** Revisar el experimento con Cumplimiento y Legal: los precios de prueba respetan topes y transparencia, no discriminan por atributos protegidos y se aplican por reglas objetivas comunicables.

  Aplica: Tier I–II · Esfuerzo: 0.5 d · Automatización: 1 · Crítico · Entregable: Documento P6: Diseño del experimento

#### 1.2 Aprobación

- **`PRC-P6-01.02.01`** Aprobación del piloto o experimento por el dueño del precio y Riesgos, con el grupo de control y los límites de exposición definidos.

  Aplica: Tier I–II · Esfuerzo: 0.25 d · Automatización: 1 · Entregable: Acta PRC-PIL: Aprobación del piloto

### 2 · Ejecución y lectura

#### 2.1 Lectura de resultados

- **`PRC-P6-02.01.01`** Ejecutar el piloto con control aleatorio y monitorear diariamente asignación, balance entre grupos y métricas de resguardo. Leer resultados solo al cumplir el tamaño muestral pre-registrado (sin "espiar" para decidir antes).

  Aplica: Tier I–II · Esfuerzo: 2 d · Automatización: 2 · Entregable: Excel P4: Resultados del piloto

- **`PRC-P6-02.01.02`** Estimar el efecto con intervalo de confianza, actualizar la elasticidad del modelo de respuesta con la evidencia experimental y documentar la decisión (escalar, ajustar o descartar).

  Aplica: Tier I–II · Esfuerzo: 1.5 d · Automatización: 2 · Entregable: Excel P4: Resultados del piloto

#### 2.2 Despliegue gradual

- **`PRC-P6-02.02.01`** Para Tier III sin experimento, desplegar de forma escalonada por región o canal (champion/challenger) y comparar contra el grupo que mantiene el precio anterior.

  Aplica: Tier III · Esfuerzo: 1.5 d · Automatización: 2 · Entregable: Excel P4: Resultados del piloto

<!-- CATALOGO:FIN -->

## P7 · El precio llega al cliente tal como se aprobó

La mayor fuga de valor no ocurre en el modelo, ocurre en la ejecución: excepciones sin control, tarifarios
desactualizados en un canal o descuentos acumulados. P7 cierra esa brecha con tres piezas:

1. **Tarifario versionado** con TCEA/TREA por celda (PRC-P7-01.01.01).
2. **Matriz de facultades:** cuántos pb puede ceder cada nivel, hasta qué piso y con qué evidencia (PRC-P7-01.02.01).

   | Nivel | Descuento máximo sobre tarifario | Piso | Evidencia |
   |---|---|---|---|
   | Ejecutivo | hasta 25 pb | ≥ piso técnico | Motivo registrado |
   | Jefe de agencia / banca | hasta 75 pb | ≥ piso técnico | Motivo + oferta de la competencia |
   | Gerencia de producto | hasta 150 pb | ≥ piso técnico | Caso de relación comercial |
   | Comité de Precios | sin límite | puede ir bajo el piso | Acta PRC-CP |

   *Valores ilustrativos: cada entidad los fija en su política (PRC-P9-01.02.01).*
3. **Motor de precios con controles preventivos** que bloquea ofertas sobre el tope o bajo el piso sin facultad,
   certificado con el estándar de [Implementación](../implementacion/implementacion.md) (U-15) y con registro de cada oferta (PRC-P7-02.03.01).

<!-- CATALOGO:INICIO PRC-P7 -->
## Catálogo de requisitos · Implementación en el motor de precios

> Bloque generado desde `catalogo/prc-p7.yaml` (6 requisitos). Para modificarlo, edita el YAML y ejecuta `python tools/build.py`. Fuente: Estándar de Pricing Analítico v1.0 (nuevo, 2026-10-17).

### 1 · Tarifario y facultades

#### 1.1 Tarifario

- **`PRC-P7-01.01.01`** Publicar el tarifario aprobado con fecha de vigencia, versión y la TCEA o TREA resultante para cada celda, según la normativa de transparencia aplicable.

  Aplica: Tier I–III · Esfuerzo: 1 d · Automatización: 2 · Crítico · Entregable: Documento P7: Tarifario y matriz de facultades · Hito: Sprint 6

#### 1.2 Matriz de facultades

- **`PRC-P7-01.02.01`** Definir la matriz de facultades de descuento: quién puede ceder cuántos puntos básicos sobre el tarifario, hasta qué piso y con qué evidencia. Ningún nivel puede ofrecer por debajo del piso técnico sin aprobación del Comité de Precios (U-18, U-23).

  Aplica: Tier I–III · Esfuerzo: 1 d · Automatización: 1 · Crítico · Entregable: Documento P7: Tarifario y matriz de facultades · Umbrales: U-18, U-23

### 2 · Motor de precios

#### 2.1 Reglas y controles preventivos

- **`PRC-P7-02.01.01`** Implementar en el motor de precios las reglas del tarifario, la matriz de facultades y los controles preventivos que bloquean ofertas por encima del tope regulatorio (U-24) o por debajo del piso sin facultad, registrando cada excepción con su motivo y aprobador.

  Aplica: Tier I–III · Esfuerzo: 3 d · Automatización: 2 · Crítico · Entregable: Script P3: Reglas del motor de precios · Umbrales: U-24

#### 2.2 Certificación

- **`PRC-P7-02.02.01`** Certificar la implementación con el estándar IMP: los precios que calcula el motor coinciden con los del modelo aprobado en ≥ 99.9 % de casos de prueba (U-15) y el 100 % de las restricciones regulatorias se cumplen.

  Aplica: Tier I–III · Esfuerzo: 2 d · Automatización: 2 · Crítico · Entregable: Documento 14: Certificación del modelo

#### 2.3 Registro de ofertas

- **`PRC-P7-02.03.01`** Registrar cada oferta emitida (precio, versión del tarifario, componentes del piso, excepción y aceptación) para cerrar el ciclo de datos que alimenta el siguiente recalibrado del modelo de respuesta.

  Aplica: Tier I–III · Esfuerzo: 1.5 d · Automatización: 2 · Crítico · Entregable: Tabla P1: Base de cotizaciones

#### 2.4 Habilitación comercial

- **`PRC-P7-02.04.01`** Capacitar a la fuerza de ventas en el nuevo tarifario, las facultades y la argumentación al cliente; dejar evidencia de la capacitación.

  Aplica: Tier I–III · Esfuerzo: 1 d · Automatización: 1 · Entregable: Documento P7: Tarifario y matriz de facultades

<!-- CATALOGO:FIN -->
