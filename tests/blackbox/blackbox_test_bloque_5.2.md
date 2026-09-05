---
tipo: contrato
bloque: 5.2
clase: Interface
proyecto: call me maybe
fecha: 2026-09-05
destinatario: agente de tests de caja negra
tags: [42, contrato, tests, caja-negra, bloque-5]
---

# Contrato del Bloque 5.2 — `Interface` reabierta, adenda

> [!important] Qué es este documento
> `Interface` cambió después de `tests/blackbox_test_bloque_5.md` (2026-09-03): `Output.output` dejó de ser un `str` a medias y pasó a ser un `dict` ya traducido y validado. Este documento **no sustituye** al contrato anterior — lo actualiza en los puntos exactos que cambiaron, y añade dos encargos nuevos sobre el mismo archivo `tests/test_bloque_5.py`.
> **Léelo entero antes de tocar el archivo.** Donde este documento no diga nada, sigue valiendo el contrato anterior. Donde diga algo distinto, **este documento manda**.

---

# PARTE FIJA — igual que en el contrato anterior, se copia literal

## F1 · Tu encargo

Eres el **agente de tests** de este bloque. Trabajas **a caja negra**.

> [!warning] Prohibición absoluta — es el núcleo del encargo
> **No abres, no lees y no grepeas el archivo de implementación**, ni ningún otro de `src/`, bajo ninguna circunstancia — tampoco para entender un fallo.
> **Importar sí.** Importar no es leer: ejecutar la clase es tu trabajo, abrir su archivo no.
> No modificas nada fuera de la carpeta de tests. No corriges la implementación. Si crees que está mal, **lo dices y paras**.

**Tu única fuente de verdad es este documento y el contrato anterior (`tests/blackbox_test_bloque_5.md`), en lo que no haya cambiado.** Si algo no está en ninguno de los dos, se pregunta — no se busca en el repositorio.

**Por qué:** un test escrito leyendo el cuerpo comprueba que el código hace lo que hace, y sale verde también cuando el código está mal.

**Lo que cuesta:** cuando un test salga rojo, tú no puedes decir por qué. Solo que la salida no cumple el contrato. **El diagnóstico es del estudiante.**

---

## F2 · Cómo trabaja el estudiante

| Regla | Qué significa en una sesión de tests | Origen |
|---|---|---|
| **Responde lo que se te pregunta y para ahí** | Nada de adelantar el test siguiente ni de añadir el contexto de alrededor | 08-14 |
| **Una idea y una pregunta por mensaje** | Nunca una corrección y dos preguntas juntas | 08-04 · 08-05 · 08-06 |
| **La frase de qué garantiza va al chat; el código, solo al archivo** | Una línea por test — *qué compra este test*. ==Nunca volcar tests al chat== | 08-25 |
| **Explica qué prueba el test, no cómo funciona `pytest`** | La herramienta le da igual; quiere saber qué garantía compra cada test | 08-18 |
| **Sus identificadores, y nada que no exista** | Se habla con los nombres del archivo, y no se nombra una pieza sin escribir | 08-29 |
| **Marca si el código es suyo o es una propuesta** | Al poner un trozo delante, decir si ya está o si lo propones | 08-14 |
| **Si dice que está bloqueado, se para en el acto** | No se insiste ni se reformula: se corta y se cambia de tema | 08-18 |
| **Sin tablas resumen antes del bloque** | La frase y su test, pegados | 08-25 |

---

## F3 · Toda invariante se contrasta contra elementos objetivos

> [!important] Regla
> Una **invariante** se verifica contra el **universo completo** de entradas posibles, nunca contra ejemplos escogidos a mano.

| Nivel | Qué es | Cuándo se usa |
|---|---|---|
| **1 · Artefacto real** | Existe fuera del test | Siempre que exista |
| **2 · Estructura simulada** | Fabricada, pero reproduce el mundo real | Cuando el real no existe, no cabe o no se puede versionar |
| **3 · Ejemplo escogido** | Dos o tres valores puestos a mano | ==**Nunca** para una invariante.== Solo para forzar un borde declarado |

> [!important] Por qué esta adenda usa nivel 2 para casi todo — ver `A5`
> El catálogo real (`E1`) **no tiene ningún parámetro anidado**. Sin eso, la recursión de `_valid_parameters` no se puede estresar con nada real. Los elementos nuevos de esta adenda (`E6`, `E7`) son **fabricados a propósito**, y se declaran como nivel 2 — no nivel 3 — porque cubren **todas** las combinaciones de profundidad y tipo que la clase declara aceptar, no un par de valores sueltos.

---

## F4 · Los rojos se leen y se discuten, no se reciben resueltos

| Salida | Cuándo | Qué se corrige |
|---|---|---|
| **El código está mal** | El caso es real y el contrato lo cubre | La implementación |
| **El test está mal** | El caso no puede darse, o el `assert` espera algo que el contrato no promete | El test |
| **El contrato está mal** | El caso es real y el contrato no dice nada de él | El diseño — y se anota dónde |

---

## F5 · Cada afirmación lleva su grado de certeza

| Grado | Qué significa |
|---|---|
| **Dato del contrato** | Está escrito en este documento |
| **Verificado ejecutando** | Se corrió y esta es la salida |
| **Convención** | Así se hace en el ecosistema, pero nadie lo obliga aquí |
| **Suposición del agente** | Le parece razonable y no lo ha comprobado |

---

## F6 · Cómo se escriben y se corren los tests

Igual que el contrato anterior: `pytest`, un archivo por bloque, sin `flake8` ni `mypy` sobre `tests/`, cinco casos obligatorios por método, y el stress limitado al uso real de la clase.

> [!important] El límite real, para los métodos de esta adenda
> `_valid_parameters` y `_costume_translater` no tienen un "tamaño real de anidamiento" que sacar de datos de producción, porque el catálogo real no anida nada. El límite realista lo fija `E7` (`A5`): **dos niveles de objeto anidado** (`user` → `address` → hojas), que es la profundidad que declara el bonus 7 y la que ya se verificó ejecutando. ==No inventes una profundidad mayor: no correspondería a ningún uso real declarado.==

---

# PARTE RELLENABLE — ADENDA, Bloque 5.2

> [!important] La regla de corte, y su única excepción en este documento
> ==Entra lo público y lo comprobable desde fuera. No entra nada sobre cómo está construida por dentro.== **Excepción autorizada explícitamente por el estudiante, ver `A4`:** dos métodos privados, `_valid_parameters` y `_costume_translater`, se testean de forma directa en el Encargo 2. En todo lo demás, la regla de corte sigue intacta.

---

## A0 · Qué cambió desde `blackbox_test_bloque_5.md`

| Punto del contrato anterior | Antes | Ahora |
|---|---|---|
| `R2` — `Output.output` | `str` — el JSON crudo, con `Ġ` y disfraz en las hojas `string` | `dict` — ya parseado, con las hojas traducidas a texto real y sus tipos validados contra el catálogo |
| `R6.2` — cadenas de `log` | Cuatro exactas | ==**Seis** exactas==, ver `A2` |
| `R6.6` — JSON parseable | Se verificaba con `json.loads(resultado.output)` | `resultado.output` **ya es** el `dict`: no hace falta `json.loads` |
| `R7`/`R8` — el disfraz del vocabulario (`Ġ`, `Äł`) | Correcto que apareciera en `output`; el decode era del Bloque 6 | ==**Revertido.**== El decode y la validación de tipos viven ahora en `Interface`. `output` en el estado correcto **nunca** lleva texto disfrazado — ver `A3` |
| Los 3 estados de fallo (`vacío`, `fallo del modelo`, `bucle`) | `output` era el JSON incompleto tal cual iba, como `str` | `output` es siempre `{"prompt": user_prompt}`, un `dict` de una sola llave |

> [!warning] Lo más importante de esta tabla, para que no se te pase
> **Todo lo que el contrato anterior decía sobre `Ġ` en `output` (`R8`, punto 1) queda revertido.** Si un test de esta adenda o uno migrado encuentra un `Ġ` dentro de `output` en el estado correcto, **es un rojo real**, no un caso descartado.

---

## A1 · `R2` actualizado — Interfaz pública

### El modelo que devuelve `reply`, ahora

```python
type ParamValue = Union[str, float, Dict[str, "ParamValue"]]

class Output(BaseModel):
    log: str
    output: ParamValue
```

| Campo | Qué contiene ahora |
|---|---|
| `log` | Una de **seis** cadenas exactas, ver `A2` |
| `output` | En el estado correcto: `Dict` con `prompt`, `name` y `parameters` — `parameters` con las hojas **ya traducidas**, sin disfraz. En cualquier otro estado: `{"prompt": user_prompt}` |

> [!important] `output` nunca vuelve a ser `str` a secas en esta clase
> El tipo declarado es `ParamValue` (`Union[str, float, Dict]`) porque es recursivo por dentro, pero en la práctica, para todo lo que `reply` devuelve hoy, `output` **siempre es un `Dict`**. No hay ningún camino que lo deje como `str` suelto.

---

## A2 · `R6.2` actualizado — las seis cadenas exactas de `log`

```
'The prompt was empty'
'Model failed while replying'
'Model entered an loop'
'The prompt was replied correctly'
'Model produced malformed parameters'
"processed function doesn't match the function parameters"
```

| # | Cadena | Cuándo sale | ¿Se puede disparar con el catálogo real (`E1`–`E4`)? |
|---|---|---|---|
| 1–4 | Las cuatro del contrato anterior | Igual que antes | Sí — ya cubiertas por los tests existentes |
| 5 | `'Model produced malformed parameters'` | El JSON cerró bien pero `parameters` no es un objeto | **No.** Verificado: la construcción de `Guardian` siempre escribe `parameters` como objeto literal (`'"parameters": {'`), pase lo que pase. Con el catálogo real, este estado es inalcanzable — no lo fuerces con `E4` ni con `E5`, no hay manera |
| 6 | `"processed function doesn't match the function parameters"` | Un valor no coincide con el tipo declarado en el catálogo | **No**, por la misma razón que el 5: `Guardian` solo permite escribir el tipo que el schema declara para cada hueco. Se dispara únicamente con `_valid_parameters` llamado directo — ver Encargo 2 |

> [!important] No busques cómo forzar 5 y 6 con `reply` y el modelo real o con `E5`
> Es una pregunta ya cerrada: **no hay ninguna combinación de prompt o de logits fabricados que los dispare**, porque no dependen de lo que el modelo escribe — dependen de la estructura fija que `Guardian` construye. Si tu primer instinto es fabricar una función de logits rara para forzarlos, para: no va a funcionar, y se explica en `A0` por qué. Se prueban **solo** por la vía del Encargo 2.

> [!note] `LOGS_VALIDOS`, la constante que ya existe en el archivo
> Sigue valiendo tal cual — las cuatro cadenas de siempre — porque describe lo que puede salir de **`resultados_reales`** (el recorrido de los 11 prompts reales), y ahí las cadenas 5 y 6 nunca aparecen. No la amplíes ni la toques.

---

## A3 · `R7`/`R8` — lo que se revierte

> [!warning] El punto 1 de `R8` del contrato anterior queda anulado
> Decía: *"el texto crudo del vocabulario dentro de las hojas `string` es correcto en este bloque, y ningún test puede exigir texto legible con espacios"*. **Ya no es así.** Hoy `Interface` traduce cada hoja antes de devolverla. En el estado correcto, `output["parameters"]` tiene texto real, legible, con espacios normales.

**Verificado ejecutando el 2026-09-05:**
```python
resultado.output["parameters"]["source_string"] == "Programming is fun"
```
Sin `Ġ`, sin `Äł`. Si tu test encuentra uno de estos caracteres dentro de una hoja `string` en el estado correcto, es un rojo real del código, no un caso descartado.

---

## A4 · La excepción a la regla de corte — autorizada por el estudiante, 2026-09-05

> [!important] Por qué se rompe la regla, con su razón
> `_valid_parameters` y `_costume_translater` son dos métodos con una responsabilidad concreta cada uno, construidos y cerrados en esta sesión. El estudiante decidió testearlos **directamente**, como métodos privados, en vez de forzarlos a través de `reply` — porque a través de `reply` **es estructuralmente imposible** llegar a los casos que necesitan probarse (ver `A2`, fila 5 y 6). Es una decisión suya, consciente de que rompe la regla de corte del contrato general.

**Lo que esto significa para ti:**
- Puedes llamar `cara._valid_parameters(...)` y `cara._costume_translater(...)` directamente, usando la fixture `cara` que ya existe en `tests/test_bloque_5.py`.
- Esto **no** habilita nada más: sigue prohibido leer `src/interface.py`, y sigue prohibido testear cualquier otro método privado que no sea estos dos.

---

## A5 · Elementos objetivos nuevos

| Id | Nivel | Qué es | Cómo se carga |
|---|---|---|---|
| **E6** | 2 · simulado | Una `Function` de un solo parámetro `number`, sin anidar | Fabricada — ver tabla abajo |
| **E7** | 2 · simulado | Una `Function` con **dos niveles** de objeto anidado (bonus 7) | Fabricada — ver tabla abajo |

### E6 — `funcion_simple`

| Campo | Valor |
|---|---|
| `name` | `"fn_test_simple"` |
| `description` | cualquier texto |
| `parameters` | `{"a": TypeSpec(type="number")}` |
| `returns` | `TypeSpec(type="string")` |

### E7 — `funcion_anidada`

Estructura, de afuera hacia adentro:

```
parameters:
  user:    TypeSpec(type="object", properties={
             name:    TypeSpec(type="string"),
             address: TypeSpec(type="object", properties={
                        city: TypeSpec(type="string"),
                        zip:  TypeSpec(type="number"),
                      })
           })
  active:  TypeSpec(type="string")
```

`name` = `"fn_test_anidada"`, `returns` = `TypeSpec(type="string")`.

### Los seis casos, verificados ejecutando el 2026-09-05 contra la clase real

| # | Método | Entrada | Salida real |
|---|---|---|---|
| 1 | `_valid_parameters(funcion_simple, {"a": 3})` | `a` correcto | `{"a": 3}` — sin `"ERROR"` |
| 2 | `_valid_parameters(funcion_simple, {"a": "x"})` | `a` con tipo equivocado | `{"ERROR": "processed function doesn't match the function parameters"}` |
| 3 | `_valid_parameters(funcion_anidada, {"user": {"name": "shrek", "address": {"city": "Duloc", "zip": 12345}}, "active": "yes"})` | los dos niveles correctos | el mismo `dict`, sin tocar, sin `"ERROR"` |
| 4 | `_valid_parameters(funcion_anidada, {"user": {"name": "shrek", "address": {"city": "Duloc", "zip": "12345"}}, "active": "yes"})` | falla en el nivel **más profundo** (`zip` como `str`) | `{"ERROR": "processed function doesn't match the function parameters"}` — el error se propaga desde el fondo hasta arriba |
| 5 | `_valid_parameters(funcion_anidada, {"user": "no soy un dict", "active": "yes"})` | el nivel intermedio no es un objeto, siendo que el schema pide uno | `{"ERROR": "processed function doesn't match the function parameters"}` |
| 6 | `_costume_translater({"source_string": "ProgrammingĠisĠfun"})` | una hoja con disfraz real del vocabulario | `{"source_string": "Programming is fun"}` |

> [!important] El caso 4 es la invariante central de esta adenda
> Antes de esta sesión, un fallo en el nivel más profundo **no se propagaba**: la función devolvía `parameters` como si todo estuviera bien. El caso 4 es la prueba directa de que eso ya no pasa. ==Este es el test que más importa de todo el Encargo 2 — no se omite bajo ninguna circunstancia.==

---

## Encargo 1 — MIGRACIÓN: adaptar los 13 tests rotos por el cambio de tipo

> [!important] Regla de esta migración, sin excepción
> ==**Cambias únicamente cómo se lee `.output` — nunca qué hipótesis verifica el test, ni su docstring, ni su nombre.**== Si un test comprobaba que `name` está en el catálogo, sigue comprobando exactamente eso; solo deja de pasar por `json.loads`.
> Antes de tocar cada uno, corre la suite y confirma que el único motivo del rojo es `AttributeError: 'dict' object has no attribute 'startswith'` o un error de `json.loads` sobre algo que ya es `dict`. Si un rojo dice otra cosa, **para y pregunta** — no lo migres a ciegas.

**Los 13, uno por uno, con el cambio exacto:**

| # | Test | Antes | Ahora |
|---|---|---|---|
| 1 | `test_reply_devuelve_json_parseable_de_tres_claves` | `objeto = json.loads(resultado.output)` | `objeto = resultado.output` — ya es el `dict`, no hace falta parsear |
| 2 | `test_reply_conserva_el_prompt_crudo_en_la_clave_prompt` | `json.loads(resultado.output)["prompt"]` | `resultado.output["prompt"]` |
| 3 | `test_reply_elige_siempre_un_nombre_del_catalogo` | `json.loads(resultado.output)["name"]` | `resultado.output["name"]` |
| 4 | `test_reply_escribe_exactamente_los_parametros_del_schema` | `objeto = json.loads(resultado.output)` | `objeto = resultado.output` |
| 5 | `test_reply_respeta_el_tipo_declarado_de_cada_parametro` | `objeto = json.loads(resultado.output)` | `objeto = resultado.output` |
| 6 | `test_reply_no_deja_vacia_una_hoja_string` | `objeto = json.loads(resultado.output)` | `objeto = resultado.output` |
| 7 | `test_reply_recorre_el_catalogo_entero_sin_inventar_nombres` | `{json.loads(r.output)["name"] for r in correctos.values()}` | `{r.output["name"] for r in correctos.values()}` |
| 8 | `test_reply_con_prompt_vacio_devuelve_el_estado_vacio` | `assert resultado.output == ""` | `assert resultado.output == {"prompt": ""}` |
| 9 | `test_reply_con_prompt_vacio_no_pide_ni_un_logit` | `resultado.output == ""` | `resultado.output == {"prompt": ""}` |
| 10 | `test_reply_atrapa_el_fallo_de_los_logits_en_la_primera_vuelta` | `resultado.output.startswith('{"prompt":%s' % json.dumps(prompt_mas_corto))` | `resultado.output == {"prompt": prompt_mas_corto}` |
| 11 | `test_reply_atrapa_el_fallo_de_los_logits_en_una_vuelta_posterior` | `resultado.output.startswith('{"prompt":%s' % json.dumps(prompt_mas_corto))` | `resultado.output == {"prompt": prompt_mas_corto}` |
| 12 | `test_reply_atrapa_el_fallo_con_todos_los_prompts_reales` | `resultado.output.startswith('{"prompt":%s' % json.dumps(texto)), texto` | `resultado.output == {"prompt": texto}, texto` |
| 13 | `test_reply_corta_por_el_tope_de_hoja_con_logits_planos` | `resultado.output.startswith('{"prompt":%s' % json.dumps(prompt_mas_largo))` | `resultado.output == {"prompt": prompt_mas_largo}` |

> [!warning] Después de migrar los 13, corre la suite entera
> `make testN test=5`. Los 13 deben pasar a verde. Los que ya pasaban (19) tienen que seguir pasando — si alguno se rompe, es un rojo real y se reporta, no se ajusta el test para que calle.

---

## Encargo 2 — AMPLIACIÓN: nuevo bloque de tests en `tests/test_bloque_5.py`

> [!important] Va en el mismo archivo, al final
> No se crea un archivo nuevo. Se añade una sección nueva, con su propio separador de comentario, igual que las secciones ya numeradas (`0`, `1`, `2`...) que ya tiene el archivo.

### Qué fixtures hacen falta

1. `funcion_simple` — construye la `Function` de `E6`.
2. `funcion_anidada` — construye la `Function` de `E7`.

Ninguna de las dos necesita el modelo ni el tokenizer para construirse — son solo objetos `pydantic`. Pueden ser fixtures de módulo o de sesión, tu elección.

### Los casos obligatorios, contra los seis verificados en `A5`

- [ ] **Flujo normal, válido, sin anidar** — caso 1 de `A5`.
- [ ] **Flujo normal, válido, con los dos niveles de anidamiento** — caso 3 de `A5`.
- [ ] **Entrada inválida, tipo equivocado sin anidar** — caso 2 de `A5`.
- [ ] **Entrada inválida, tipo equivocado en el nivel más profundo** — caso 4 de `A5`. ==Obligatorio, ver la nota de `A5`.==
- [ ] **Entrada inválida, un nivel intermedio que debía ser objeto y no lo es** — caso 5 de `A5`.
- [ ] **Traducción de una hoja con disfraz real** — caso 6 de `A5`.

Cada test compara el resultado contra el valor **exacto** de la tabla de `A5` — no solo si trae o no `"ERROR"`, sino el `dict` completo cuando el caso es válido.

> [!warning] Esto no es zona de stress con niveles arbitrarios
> No escribas un test con 5, 10 o 50 niveles de anidamiento "para estar seguros". `F6` de esta adenda ya explica por qué: no corresponde a ningún uso real declarado del bonus 7. Los dos niveles de `E7` son el límite realista, y ya cubren la invariante que importa — que el error se propague desde cualquier profundidad, no que aguante una arbitraria.

---

## R10 · Archivo de tests

`tests/test_bloque_5.py` — el mismo de siempre, no uno nuevo.

## R11 · Comando de ejecución

```bash
make testN test=5
```

---

## Antes de escribir la primera línea — checklist de esta adenda

- [ ] ¿Entendiste por qué los estados 5 y 6 de `A2` **no se pueden forzar** con `reply` y el modelo real, ni con ninguna función de logits fabricada?
- [ ] ¿Migraste los 13 tests de `Encargo 1` cambiando solo la lectura de `.output`, sin tocar qué verifican?
- [ ] ¿Confirmaste que el `Ġ` ya no aparece en ningún `output` del estado correcto (`A3`)?
- [ ] ¿Escribiste el caso 4 de `A5` — el fallo en el nivel más profundo — sin omitirlo?
- [ ] ¿Usaste la fixture `cara` que ya existe, en vez de construir una `Interface` nueva para esto?
- [ ] ¿Corriste la suite entera al final y los 32 tests (19 + 13 migrados) más los nuevos de `Encargo 2` están en verde?

> [!warning] Cero huecos
> Si algo de esta adenda no te deja claro qué esperar, para y pregunta. No lo decidas por tu cuenta.
