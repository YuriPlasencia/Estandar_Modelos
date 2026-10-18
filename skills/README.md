# Skills para agentes de IA

Skills que aplican los **Estándares de Modelos en Banca** (Yuri Plasencia — Analytics Pricing & Revenue Management)
con agentes de IA como Claude Code. Cada skill es una carpeta con un `SKILL.md`.

| Skill | Qué hace |
|---|---|
| [`desarrollo-modelo-binario`](desarrollo-modelo-binario/SKILL.md) | Desarrolla un modelo de clasificación binaria (admisión, comportamiento, buró, propensión, fraude) por las fases DES-D1 a DES-D7, con los umbrales U-xx como pruebas y los puntos de control humanos G0–G5 |

## Instalar

```bash
npx skills add YuriPlasencia/Estandar_Modelos
```

O manualmente: copia la carpeta de la skill a `~/.claude/skills/` (todos tus proyectos) o a `.claude/skills/` del proyecto.

La skill necesita un clon local de este repositorio, porque usa `tools/verificar.py`, `tools/acta.py`,
`tools/documento.py` y el catálogo. Sus scripts requieren Python 3 con `numpy` y `pandas`; los del estándar, `pyyaml`.

```bash
git clone https://github.com/YuriPlasencia/Estandar_Modelos.git
python desarrollo-modelo-binario/scripts/pruebas_umbrales.py --autotest
```

## Alcance

La skill aplica el estándar; no lo reemplaza. Ante cualquier diferencia mandan `catalogo/umbrales.yaml` y el catálogo de
requisitos. El agente prepara análisis, evidencias y borradores de actas, pero **no aprueba nada**: la conformidad la da una
persona y el modelo no se usa sin aprobación previa del comité (GOB-G3-01.01.01). No es asesoría regulatoria.

## Licencia

Texto de las skills: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Scripts (`scripts/`): MIT, como `tools/`.
Ver [`LICENSE`](../LICENSE).
