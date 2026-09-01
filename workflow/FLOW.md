---
tipo: mapa
proyecto: call me maybe
version: 1.0
tags: [42, flujo, bloques, diseño]
---

# FLOW.md — El proyecto de un vistazo

> [!important] Para qué es este archivo
> Ver **qué bloques hay, qué le entrega cada uno al siguiente y en qué orden se construyen**, sin leer el diseño entero.
> El detalle vive en `[[PROJECT]]`. Aquí solo está la forma.

---

## Orden de construcción

> [!info] Se implementa de arriba abajo
> Cada bloque solo depende de los que están **encima**. Ninguno necesita algo de más abajo.

```mermaid
graph TD
    B1["<b>1 · Tokenizer</b><br/>texto ↔ token ids"]
    B2["<b>2 · I/O de archivos</b><br/>leer, validar, escribir"]
    B3["<b>3 · Construcción del prompt</b><br/>plantilla del modelo"]
    B4["<b>4 · Validez de tokens</b><br/>esqueleto + huecos · lista blanca"]
    B5["<b>5 · Bucle de generación</b><br/>logits · máscara · argmax"]
    B6["<b>6 · Chat — orquestador</b><br/>recorre los N prompts"]

    B1 --> B5
    B2 --> B3
    B3 --> B5
    B4 --> B5
    B5 --> B6
    B1 --> B4
    B2 --> B6

    style B1 fill:#1f6f8b,stroke:#0d3d4d,color:#fff
    style B2 fill:#1f6f8b,stroke:#0d3d4d,color:#fff
    style B3 fill:#2e7d5b,stroke:#14442f,color:#fff
    style B4 fill:#8b5a1f,stroke:#4d310d,color:#fff
    style B5 fill:#8b2f2f,stroke:#4d1414,color:#fff
    style B6 fill:#5a3d8b,stroke:#2f1f4d,color:#fff
```

---

## Qué le entrega cada bloque a cuál

| De | A | Qué le pasa |
|---|---|---|
| 1 · Tokenizer | 5 · Generación | Texto → ids, ids → texto |
| 1 · Tokenizer | 4 · Validez | El `dict` del vocabulario, string → id |
| 2 · I/O | 3 · Prompt | Catálogo de funciones y prompts, ya validados |
| 2 · I/O | 6 · Chat | Las rutas y los datos de entrada |
| 3 · Prompt | 5 · Generación | Un string listo para tokenizar |
| 4 · Validez | 5 · Generación | Los ids permitidos en el estado actual del JSON |
| 5 · Generación | 6 · Chat | Un resultado validado, por prompt |
| 6 · Chat | 2 · I/O | Los N resultados y el registro de fallos, para escribir |

---

## El mismo mapa, pero en orden de ejecución

> [!info] Lo que pasa cuando corre el programa
> El de arriba es el orden en que se **construye**. Este es el orden en que las cosas **ocurren**.

```mermaid
graph LR
    CLI["<b>__main__</b><br/>argparse"] --> IO["<b>2</b><br/>leer y validar<br/>los dos JSON"]
    IO --> CHAT["<b>6 · Chat</b><br/>por cada prompt"]
    CHAT --> PR["<b>3</b><br/>construir<br/>el texto"]
    PR --> TOK["<b>1</b><br/>texto → ids"]
    TOK --> GEN

    subgraph GEN["<b>5 · bucle token a token</b>"]
        direction LR
        L["pedir<br/>logits"] --> M["aplicar<br/>máscara"]
        M --> A["argmax"]
        A --> C{"profundidad<br/>= 0?"}
        C -->|"no"| L
    end

    VAL["<b>4</b><br/>qué ids<br/>son válidos"] -.->|"consulta"| M
    C -->|"sí"| DEC["<b>1</b><br/>ids → texto"]
    DEC --> PY["json.loads<br/>+ pydantic"]
    PY --> CHAT
    CHAT --> OUT["<b>2</b><br/>escribir los N<br/>resultados"]

    style GEN fill:#2a1a1a,stroke:#8b2f2f
    style VAL fill:#8b5a1f,stroke:#4d310d,color:#fff
    style CHAT fill:#5a3d8b,stroke:#2f1f4d,color:#fff
```

---

## Estado

| # | Bloque | Diseño | Implementación | Tests |
|---|---|---|---|---|
| 1 | Tokenizer | ✅ | ✅ | ✅ |
| 2 | I/O de archivos | ✅ | ✅ | ✅ |
| 3 | Construcción del prompt | ✅ | ✅ | ✅ |
| 4 | Validez de tokens | ✅ | ✅ | ✅ |
| 5 | Bucle de generación | ⚪ | ⚪ | ⚪ |
| 6 | `Chat` orquestador | ⚪ | ⚪ | ⚪ |

**Estados:** ✅ cerrado · 🔵 en curso · ⚪ pendiente · 🔴 bloqueado

> [!note] Se actualiza al cerrar cada bloque
> Este archivo es la vista rápida. La fuente de verdad sigue siendo `[[PROJECT]]`.

> [!success] Bloques 2 y 3 — cerrados (2026-08-25)
> `src/filemanager.py` con los seis métodos y los tres getters (**46 tests**), y `src/promptbuilder.py` con la plantilla de chat de Qwen y el catálogo en JSON (**20 tests**). `flake8` y `mypy --strict` limpios en los dos.

> [!success] Bloque 4 — cerrado (2026-08-31)
> **`src/guardian.py` completo y verificado:** once métodos, **64 tests verdes**, `flake8` y `mypy --strict` limpios.
> Los tests los escribió un **agente ciego** que nunca abrió `src/`. De sus 5 rojos salieron **dos errores reales del código** —el cero a la izquierda y el cierre tras un punto—, los dos en la rama `number` de `_char_ok` y corregidos por él.
> **Diseño:** esqueleto + huecos, sin pila de estructura JSON. El modelo solo escribe **hojas** —nombre de función y valores—; el resto lo inyecta `Guardian`.
> ==El contrato en PDF se borró al cerrar el bloque, por decisión suya.==

> [!important] Método refundado (2026-08-31)
> El ciclo de un bloque: **lista de requisitos cerrada** → **él teclea y el agente verifica ejecutando** → **contrato escrito después** → **agente de tests ciego** → **él diagnostica los rojos** → **correcciones entre los dos** → **tres pasadas y cierre**.
> ==Los nombres, atributos y firmas ya no se cierran en el diseño: salen mientras se escribe.== Detalle en `[[SYSTEM]]`, plantilla del PDF en `[[contract]]`.

> [!success] Bloque 1 — dónde va (2026-08-17)
> **Construcción cerrada** en `src/tokenizer.py`: `encode` y `decode` completos, con el bucle de fusiones de BPE y los 26 tokens especiales cargados de `added_tokens`.
> ==El test que zanja el bloque pasa== — `assert mi_ids == sdk_ids` con los archivos reales de Qwen, en 43 textos. **129 tests verdes** en `tests/test_bloque_1.py`.
> Consecuencia: el **bonus 2 sigue vivo**, no hay que caer al plan B de usar el `encode` del SDK.
> Queda solo la pasada de **guards** y la de **`flake8`/`mypy`** — ver `[[PROJECT#Abierto en este bloque]]`.
