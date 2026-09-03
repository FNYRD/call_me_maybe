---
tipo: contrato
bloque: 5
clase: Interface
proyecto: call me maybe
fecha: 2026-09-03
destinatario: agente de tests de caja negra
tags: [42, contrato, tests, caja-negra, bloque-5]
---

# Contrato del Bloque 5 — `Interface`

> [!important] Fecha: 2026-09-03
> Escrito con la clase **terminada y corriendo**. Todo lo que afirma este documento se ha comprobado ejecutando, salvo lo marcado con otro grado de certeza (ver `F5`).

---

# PARTE FIJA

## F1 · Tu encargo

Eres el **agente de tests** de este bloque. Trabajas **a caja negra**.

> [!warning] Prohibición absoluta — es el núcleo del encargo
> **No abres, no lees y no grepeas el archivo de implementación**, ni ningún otro de `src/`, bajo ninguna circunstancia — tampoco para entender un fallo.
> **Importar sí.** Importar no es leer: ejecutar la clase es tu trabajo, abrir su archivo no.
> No modificas nada fuera de la carpeta de tests. No corriges la implementación. Si crees que está mal, **lo dices y paras**.

**Tu única fuente de verdad es este documento.** Léelo entero antes de escribir una línea. Es autocontenido: si algo no está aquí, se pregunta — no se busca en el repositorio.

**Por qué:** un test escrito leyendo el cuerpo comprueba que el código hace lo que hace, y sale verde también cuando el código está mal.

**Lo que cuesta:** cuando un test salga rojo, tú no puedes decir por qué. Solo que la salida no cumple el contrato. **El diagnóstico es del estudiante.**

---

## F2 · Cómo trabaja el estudiante

> [!important] No es preferencia de estilo: son reglas suyas, con fecha
> Romperlas no hace la sesión más lenta — la hace inútil, porque deja de entender lo que lee.

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
> Una **invariante** —lo que debe ser verdad siempre— se verifica contra el **universo completo** de entradas posibles, nunca contra ejemplos escogidos a mano.

**Elemento objetivo:** el artefacto contra el que se contrasta. No lo escribe quien testea al vuelo: existe antes que el test y **se declara en la sección R9**.

| Nivel | Qué es | Cuándo se usa |
|---|---|---|
| **1 · Artefacto real** | Existe fuera del test: un vocabulario, un catálogo, una tabla de reglas | Siempre que exista |
| **2 · Estructura simulada** | Fabricada, pero reproduce el mundo real | Cuando el real no existe, no cabe o no se puede versionar |
| **3 · Ejemplo escogido** | Dos o tres valores puestos a mano | ==**Nunca** para una invariante.== Solo para forzar un borde declarado que ni el real ni el simulado contienen |

> [!warning] Lo que se le exige al nivel 2 — aquí se cuela el autoengaño
> ==**La estructura simulada contiene todas las características que podamos suponer del real.**== No una muestra representativa: todas las que se nos ocurran.
> La lista se **enumera antes** de fabricarla y se escribe. Es una lista **viva**: cuando aparezca una característica nueva se añade y **los tests ya escritos se vuelven a correr**.
> **Por qué:** una simulación con solo los casos fáciles vuelve verdes los tests sin cambiar nada del código — cobertura aparente y cero garantía.

> [!important] Los niveles se combinan
> Lo normal es **el real como base y la simulada encima**. Se declara qué parte es real y qué parte es añadida.

> [!warning] Si la lista no cabe, se dice — no se muestrea en silencio
> Si el universo es demasiado grande para recorrerlo en cada paso, ==**no se recorta por cuenta propia**==: se reporta el coste y **decide el estudiante**.
> Y hay una salida barata que casi siempre sirve: en vez de recorrer muchos caminos mirando pocos candidatos, **congelar un estado y recorrer su lista entera**. Un punto, pero completo.

---

## F4 · Los rojos se leen y se discuten, no se reciben resueltos

> [!important] Regla
> El estudiante **ve el rojo** y lo discute. La discusión analiza dos cosas, en este orden:
> 1. **Qué produjo el fallo** — qué entrada, qué estado, qué línea del contrato se incumplió.
> 2. ==**Si el test representa un caso real**== — si ese estado puede darse de verdad en ejecución.

| Salida | Cuándo | Qué se corrige |
|---|---|---|
| **El código está mal** | El caso es real y el contrato lo cubre | La implementación |
| **El test está mal** | El caso no puede darse, o el `assert` espera algo que el contrato no promete | El test |
| **El contrato está mal** | El caso es real y el contrato no dice nada de él | El diseño — y se anota dónde |

> [!warning] El agente no entrega el diagnóstico hecho
> Da la salida real —lo que imprime— y espera. Si el estudiante pide la causa directamente, se le da.
> **Excepción:** los fallos de fontanería (import equivocado, ruta mal, entorno) se resuelven en el momento y sin ceremonia.

---

## F5 · Cada afirmación lleva su grado de certeza

| Grado | Qué significa |
|---|---|
| **Dato del contrato** | Está escrito en este documento |
| **Verificado ejecutando** | Se corrió y esta es la salida |
| **Convención** | Así se hace en el ecosistema, pero nadie lo obliga aquí |
| **Suposición del agente** | Le parece razonable y no lo ha comprobado |

> [!warning] Un `assert` escrito sobre una suposición no es cobertura: es una opinión con sintaxis de test
> Sale verde, cuenta como cubierto, y lo que garantiza no lo pidió nadie.

**Qué se hace con una suposición:** se marca como tal y **se convierte en pregunta al estudiante** antes de escribir el test. Si la confirma, pasa a dato del contrato y se anota. Si no, no se testea.

---

## F6 · Cómo se escriben y se corren los tests

**Framework: `pytest`, siempre.** Un test es una función que empieza por `test_` y afirma con `assert`; si el `assert` falla, el test sale rojo y pytest imprime los valores. No hace falta nada más de la herramienta.

| Asunto | Regla |
|---|---|
| **Un archivo por bloque** | `tests/test_bloque_N.py` — el número va en la sección R10 |
| **Nombre de cada test** | `test_` + lo que garantiza, en palabras: `test_reply_devuelve_vacio_con_prompt_vacio` |
| **Docstring de cada test** | Una o dos líneas: **qué garantiza**, no cómo funciona |
| **Carga cara** | Lo que tarde (modelos, vocabularios) va en una fixture de **sesión**, no por test |
| **Entorno** | El del proyecto, nunca uno propio. Comando en la sección R11 |
| **Cobertura por método** | Los cinco de abajo, y la lista se mantiene visible |
| **Linting** | ==**No aplica a los tests.**== Ver el callout de abajo |

> [!important] Los tests no pasan por `flake8` ni por `mypy` — decisión del estudiante, 2026-09-01
> ==**A un archivo de tests no se le exige `flake8`, ni `mypy --strict`, ni ninguna otra herramienta de estilo.**== Líneas largas, nombres, orden, imports sin usar: nada de eso es un pendiente.
> **Lo único que se le exige son dos cosas:**
> 1. ==**Que el test pruebe de verdad su objetivo**== — que el `assert` compruebe lo que la frase dice que compra.
> 2. ==**Que el tipado sea correcto**== — los tipos que se le pasan a la clase y los que se esperan de vuelta son los del contrato. Correcto de verdad, no *"limpio para la herramienta"*.
>
> **Alcance:** solo `tests/`. `src/` sigue con `flake8` y `mypy --strict` limpios como bloqueo de bloque — eso no cambia.

**Los cinco casos obligatorios por método:**

- [ ] Creación correcta
- [ ] Flujo normal
- [ ] Valor límite válido
- [ ] Stress sobre el límite
- [ ] Entradas inválidas

> [!important] ==El stress llega al límite real de uso, y ahí para== — regla del estudiante, 2026-09-02
> El caso *"stress sobre el límite"* se construye contra **el uso verdadero de la clase**, no contra un escenario inventado. Con sus palabras: *"no nos preparamos para hipótesis que no se corresponden con el verdadero uso de la clase"*.
> ==**Y la otra mitad, que es la que obliga:** todo lo que la clase declara —cada guard, cada tope, cada alarma— tiene que **dispararse al menos una vez** dentro de ese límite real.== Un tope que ninguna corrida activa no está probado, aunque esté escrito.
> **Motivo:** un test que fabrica un escenario imposible sale verde sin comprar nada, y esconde que el caso posible nunca se probó.

> [!important] Cómo se saca el límite real **de esta clase** — se responde por bloque, no se hereda
> El límite no es un número universal: sale de las secciones rellenables de **este** contrato. Antes de escribir el primer test de stress, responde estas cuatro, **con datos, no con adjetivos**:
>
> | # | Pregunta | De dónde sale la respuesta |
> |---|---|---|
> | 1 | ¿Qué recibe esta clase **en ejecución real**, y quién se lo pasa? | `R4 · Qué debe aceptar` y `R7 · Fronteras` |
> | 2 | ¿Cuál es el **dato real más grande y más raro** que puede llegarle? | `R9 · Elementos objetivos` — los archivos reales del proyecto, no muestras inventadas |
> | 3 | ¿Qué **declara** esta clase que la protege? Enuméralos uno a uno | `R5 · Qué debe rechazar` y `R6 · Invariantes` |
> | 4 | ¿Qué le pasaría a la clase **más allá** de ese límite? | `R8 · Descartado a propósito` — si está ahí, **no se testea** |
>
> **Lo que sale de las cuatro es una tabla, y esa tabla es el plan de stress:** una fila por cosa declarada en (3), y en cada fila **el dato real de (2) que la hace saltar**.
> ==**Si una fila se queda sin dato que la dispare, no se inventa uno: se dice.**== Puede significar dos cosas y las dos importan — que el guard sobra, o que el elemento objetivo elegido es demasiado pequeño. Las dos son hallazgos, y se reportan sin resolverlos.

> [!note] Un crash es una salida como cualquier otra
> Si el contrato dice *"no debe crashear nunca"*, una excepción es un rojo. Si dice *"lanza `ValueError` con el archivo ausente"*, la excepción **es** la salida correcta y no lanzarla es el rojo.

---

# PARTE RELLENABLE — Bloque 5, clase `Interface`

> [!important] La regla de corte
> ==**Entra lo público y lo comprobable desde fuera. No entra nada sobre cómo está construida por dentro.**==

---

## R1 · Qué hace la clase

`Interface` recibe **un** prompt del usuario en lenguaje natural y devuelve la llamada de función que le corresponde, escrita como JSON, generada token a token con el vocabulario del modelo restringido en cada paso.

**Lo que hace, en una frase:** convierte `"Greet shrek"` en `{"prompt":"Greet shrek", "name": "fn_greet", "parameters": {"name": "shrek"}}`.

**Es un prompt por llamada.** Recorrer los N prompts del archivo de entrada no es suyo (ver `R7`).

---

## R2 · Interfaz pública

### La clase

| Método | Firma completa | Qué recibe | Qué devuelve |
|---|---|---|---|
| `__init__` | `(functions: List[Function], vocab_path: FilePath, merges_path: FilePath, tokenizer_path: FilePath, logits_method: Callable[[List[int]], List[float]]) -> None` | El catálogo de funciones ya validado, las tres rutas de los archivos del modelo, y la función que produce los logits | — |
| `reply` | `(user_prompt: str) -> Output` | Un prompt crudo del usuario | Un `Output` |

> [!important] Los dos métodos llevan `@validate_call` de `pydantic`
> **Dato del contrato, verificado ejecutando el 2026-09-03.** Los tipos de las dos firmas se comprueban **antes** de entrar al cuerpo: una entrada de tipo equivocado sale por `pydantic.ValidationError`, no por un `TypeError` de dentro.

### El modelo que devuelve

```python
class Output(BaseModel):
    log: str
    output: str
```

`Output` se importa del mismo módulo que `Interface` (ver `R11`).

| Campo | Qué contiene |
|---|---|
| `log` | Cómo salió el bucle. **Una de cuatro cadenas exactas**, ver `R6` |
| `output` | El JSON escrito hasta el momento de salir. Cadena vacía solo en el caso del prompt vacío |

### Los tipos de la firma, de dónde salen

| Tipo | Origen | Cómo se consigue en un test |
|---|---|---|
| `Function` | `src.filemanager` | `FileManager(...).get_functions()` — nunca a mano |
| `FilePath` | `pydantic` | Acepta un `str` o un `Path`; **exige que el archivo exista** |
| `Callable[[List[int]], List[float]]` | — | El método del SDK, o una función escrita por el test (ver `R9`, E5) |

---

## R3 · Cómo se conduce una sesión

Se construye una vez y se llama a `reply` tantas veces como prompts haya.

```python
model = Small_LLM_Model()

face = Interface(
    functions,                              # List[Function]
    model.get_path_to_vocab_file(),
    model.get_path_to_merges_file(),
    model.get_path_to_tokenizer_file(),
    model.get_logits_from_input_ids,        # el Callable
)

resultado = face.reply("Greet shrek")
resultado.log      # 'The prompt was replied correctly'
resultado.output   # '{"prompt":"Greet shrek", "name": "fn_greet", "parameters": {"name": "shrek"}}'
```

> [!important] La misma instancia atiende varios prompts seguidos
> **Verificado ejecutando el 2026-09-03:** cuatro llamadas seguidas sobre la misma instancia —tres prompts reales y uno vacío— y las cuatro salieron correctas. Cada `reply` arranca de cero: **el resultado de un prompt no depende de los anteriores ni de su orden.** Es una invariante, ver `R6.7`.

> [!warning] No hay más métodos públicos que estos dos
> No existe un método para "seguir generando", ni para leer el estado a medias, ni para reiniciar. Todo lo que se observa de esta clase sale del `Output` que devuelve `reply`.

---

## R4 · Qué debe aceptar

### `__init__`

| Entrada | Comportamiento |
|---|---|
| `functions` = el catálogo real completo, `List[Function]` de 5 funciones | Se construye sin error |
| `functions` = una lista de una sola `Function` | Se construye sin error |
| Las tres rutas como `str` **o** como `Path` | Las dos formas valen: `FilePath` acepta ambas |
| `logits_method` = cualquier invocable con esa firma | Se construye sin error. **No se llama durante la construcción** |

### `reply`

| Entrada | Comportamiento |
|---|---|
| Un prompt del archivo real (`R9`, E2) | Genera y devuelve el JSON completo |
| `""` — cadena vacía | ==No entra al bucle.== Devuelve `Output(log='The prompt was empty', output='')` |
| Un prompt corto y legítimo del dominio (`"Sum 2 3"`, `"Greet a"`) | Genera. Puede terminar correcto o cortar por tope — las dos salidas son válidas y **cuál sale depende del modelo**, no del contrato |
| Un prompt largo del real: `"Substitute the word 'cat' with 'dog' in 'The cat sat on the mat with another cat'"` (**81** caracteres) | Genera. Es el prompt más largo del archivo de entrada |
| Un prompt que no corresponde a ninguna función del catálogo | **Genera igual**, eligiendo una de las funciones disponibles. Ver `R8` |

---

## R5 · Qué debe rechazar

| Método | Entrada | Qué hace | Certeza |
|---|---|---|---|
| `__init__` | Una ruta que no existe | Lanza `pydantic.ValidationError` (`path_not_file`) | Verificado |
| `__init__` | `functions` que no es `List[Function]` — un `dict`, un `str`, un `int` | Lanza `pydantic.ValidationError` | Verificado |
| `__init__` | `logits_method` que no es invocable | Lanza `pydantic.ValidationError` | Suposición del agente — **pregúntalo antes de testearlo** |
| `reply` | `user_prompt` que no es `str` — `5`, `None`, una lista | Lanza `pydantic.ValidationError` | Verificado ejecutando el 2026-09-03 |

> [!important] El no-`str` es un **doble guard**, no un caso de uso real — decisión del estudiante, 2026-09-03
> `Chat` recibe `List[Prompt]` del `FileManager`, donde el campo ya está tipado `str` por `pydantic`: un `int` **no puede llegar** a `reply` en ejecución real. El `@validate_call` está ahí como segunda barrera.
> ==**Consecuencia para la suite:** un test por caso, y ya. No es zona de stress.==

> [!warning] Lo que `reply` NO hace nunca: caerse
> Cualquier excepción que salga de pedir los logits **se atrapa** y se devuelve como estado (`R6.3`). ==Una excepción que escape de `reply` con un `user_prompt` de tipo `str` es un rojo del código.==

---

## R6 · Invariantes

> [!important] Se contrastan contra el universo del proyecto, no contra ejemplos
> El universo de esta clase son los **11 prompts reales** con el **catálogo real** (`R9`). Una invariante que solo se compruebe con dos prompts escogidos no está comprobada.

**R6.1 · `reply` siempre devuelve un `Output`.** Con cualquier `str`, en cualquier estado, salga bien o mal. Nunca `None`, nunca otra cosa.

**R6.2 · `log` es siempre una de estas cuatro cadenas, exactas:**

```
'The prompt was empty'
'Model failed while replying'
'Model entered an loop'
'The prompt was replied correctly'
```

> [!note] La tercera está escrita así en el código, con la errata gramatical incluida
> Es el valor literal que devuelve la clase. **El `assert` compara contra esta cadena, no contra una corregida.**

**R6.3 · Si la función de logits lanza, el bucle no se propaga.** Devuelve `log='Model failed while replying'` y en `output` **lo que llevara escrito hasta ese momento** — que puede ser un JSON incompleto. *Verificado ejecutando el 2026-09-03:* con una función que lanza `RuntimeError` en la primera vuelta, `output='{"prompt":"Greet shrek", "name": "'`.

**R6.4 · El tope por hoja corta el bucle.** Si lo escrito **dentro de la hoja en curso** supera los caracteres del **prompt crudo**, el bucle para y devuelve `log='Model entered an loop'` con lo escrito hasta ahí. Es un guard contra el cuelgue, no un criterio de calidad.

**R6.5 · Con `user_prompt=''` no se pide ni un solo logit.** El `Callable` no se llama ninguna vez. Se devuelve `output=''`.

**R6.6 · En el estado correcto, `output` es un JSON parseable.** *Verificado ejecutando el 2026-09-03 sobre los prompts reales:* `json.loads(resultado.output)` no lanza. Y el objeto resultante tiene exactamente tres claves de primer nivel: `prompt`, `name`, `parameters`.

**R6.7 · Las llamadas son independientes.** Dos `reply` seguidos sobre la misma instancia dan el mismo resultado que dos instancias distintas, y el orden no cambia nada.

**R6.8 · En el estado correcto, `name` es uno de los nombres del catálogo que se le pasó al constructor.** Nunca un nombre inventado ni uno de otro catálogo. ==Esto se contrasta contra el catálogo entero, no contra una función escogida.==

**R6.9 · En el estado correcto, las claves de `parameters` son exactamente las del schema de esa función en el catálogo** — todas, sin sobrantes.

**R6.10 · El tipo de cada valor de `parameters` corresponde al `type` declarado en el catálogo:** un parámetro `number` sale como número JSON, un parámetro `string` sale entre comillas.

---

## R7 · Fronteras — lo que NO es de esta clase

| Fuera | De quién |
|---|---|
| Recorrer los N prompts del archivo | `Chat` — Bloque 6 |
| `json.loads` sobre el resultado y validarlo con `pydantic` | `Chat` — Bloque 6 |
| ==Traducir el texto crudo del vocabulario a texto real== | `Chat` — Bloque 6. Ver `R8` |
| Leer y escribir archivos, y el log de fallos | `FileManager` — Bloque 2 |
| Las reglas de qué token es válido en cada punto del JSON | `Guardian` — Bloque 4 |
| La plantilla de chat y el catálogo dentro del texto del modelo | `PromptBuilder` — Bloque 3 |
| Construir el `Small_LLM_Model` y sacarle las rutas | `Chat` — Bloque 6 |

> [!important] `Interface` no conoce ningún SDK — decisión de diseño del estudiante, 2026-09-02
> Por eso recibe las **rutas ya resueltas** y la **función de logits ya extraída**. Es lo que sostiene el bonus de *soportar varios modelos*: quien conoce el SDK concreto es `Chat`, no esta clase.
> ==**Consecuencia directa para ti:** el `Callable` es un punto de entrada legítimo y público. Pasarle una función escrita por el test no es hacer trampa: es usar la clase como está diseñada.==

---

## R8 · Descartado a propósito

> [!warning] Todo lo de esta sección **no se testea**. Un test que lo exija es un rojo del test, no del código.

**1 · El texto crudo del vocabulario dentro de las hojas `string`.**

Los tres prompts de `fn_substitute_string_with_regex` salen así:

```
"source_string": "HelloĠ34ĠI'mÄł233ĠyearsĠold"
"source_string": "ProgrammingĠisĠfun"
"source_string": "TheĠcatĠsatĠonĠtheÄłmatÄłwithAnotherCat"
```

**Esto es correcto en este bloque.** `Ġ` es cómo se llama el espacio en la tabla byte↔carácter de Qwen, y `Äł` es otro invisible. El JSON que sale mezcla dos alfabetos a propósito: el **esqueleto** va en texto real y solo las **hojas** llevan el disfraz del vocabulario.

==El decode es del **Bloque 6**, donde ya vive el `json.loads`.== Decisión del estudiante del 2026-09-02, tomada después de descartar las tres vías alternativas ejecutándolas.

> [!warning] Lo que esto significa para tus `assert`
> ==**Ningún test puede exigir que `output` contenga texto legible con espacios.**== Un `assert '"name": "shrek"' in output` es válido —ahí no hay espacios—; un `assert "The cat sat" in output` es un rojo del test.
> Lo que **sí** puedes afirmar: que el JSON es parseable, que las claves son las del catálogo, y que el valor de una hoja `string` no está vacío.

**2 · El acierto del modelo.** Que el prompt `"Greet shrek"` elija `fn_greet` y no `fn_add_numbers` depende de Qwen, no de esta clase. La clase garantiza que **lo que salga sea estructuralmente correcto** (`R6.8`, `R6.9`, `R6.10`), no que sea la función acertada. ==Un test que afirme qué función concreta elige el modelo mide a Qwen, no al código.==

**3 · Un prompt fuera del dominio** (`"hola"`, `"aaaa"`, un texto en otro idioma). La clase generará una llamada válida en formato pero inventada. **No es un fallo declarado**: no hay nada que afirmar más allá de las invariantes generales.

**4 · Archivos del modelo existentes pero equivocados** (pasar el `merges.txt` donde va el `vocab.json`). El fallo viene de los bloques 1 y 3, que tienen sus propios tests. Fuera de este contrato.

**5 · El tiempo de ejecución.** Los prompts reales tardan entre 1,0 s y 7,0 s con el modelo real. **No hay límite declarado por prompt**, así que no se testea el tiempo.

---

## R9 · Elementos objetivos

| Id | Nivel | Qué es | Ruta exacta | Cómo se carga |
|---|---|---|---|---|
| **E1** | 1 · real | Catálogo de funciones — **5 funciones** | `data/input/functions_definition.json` | `FileManager(...).get_functions() -> List[Function]` |
| **E2** | 1 · real | Prompts de entrada — **11 prompts** | `data/input/function_calling_tests.json` | `FileManager(...).get_prompts() -> List[Prompt]`, y de cada uno `.prompt` |
| **E3** | 1 · real | Los tres archivos del modelo | Las da el SDK | `Small_LLM_Model().get_path_to_vocab_file()`, `...get_path_to_merges_file()`, `...get_path_to_tokenizer_file()` |
| **E4** | 1 · real | Los logits de Qwen | — | `Small_LLM_Model().get_logits_from_input_ids` |
| **E5** | 2 · simulado | Funciones de logits escritas por el test | — | Ver la lista de características de abajo |
| **E6** | 3 · escogido | Valores sueltos: `""`, `5`, `None` | — | Solo para los bordes declarados de `R5` |

### E1 — el catálogo real, entero

| Función | Parámetros y tipos |
|---|---|
| `fn_add_numbers` | `a`: number · `b`: number |
| `fn_greet` | `name`: string |
| `fn_reverse_string` | `s`: string |
| `fn_get_square_root` | `a`: number |
| `fn_substitute_string_with_regex` | `source_string`: string · `regex`: string · `replacement`: string |

### E2 — los 11 prompts reales, con su longitud en caracteres

```
27  What is the sum of 2 and 3?
31  What is the sum of 265 and 345?
11  Greet shrek
10  Greet john
26  Reverse the string 'hello'
26  Reverse the string 'world'
30  What is the square root of 16?
32  Calculate the square root of 144
64  Replace all numbers in "Hello 34 I'm 233 years old" with NUMBERS
57  Replace all vowels in 'Programming is fun' with asterisks
81  Substitute the word 'cat' with 'dog' in 'The cat sat on the mat with another cat'
```

**El más corto son 10 caracteres, el más largo 81.** Ese es el universo real de entradas de esta clase.

> [!warning] Corregido el 2026-09-03 — las longitudes anteriores estaban mal
> La tabla traía cinco cifras contadas a ojo por el agente que escribió el contrato, no medidas. ==Las de arriba salen de `len()` sobre el archivo real.== El prompt más largo son **81** caracteres, no 87.

### E5 — la lista de características que la función simulada debe reproducir

> [!important] Se enumera antes de fabricarla, y es una lista viva (`F3`)
> Si al escribir los tests aparece una característica más del real, **se añade aquí y se vuelven a correr los tests ya escritos**.

- [ ] Recibe **una lista de `int`** — los ids del texto ya tokenizado
- [ ] Devuelve una **lista de `float`**
- [ ] La lista tiene **exactamente 151.936 posiciones**. *Verificado ejecutando el 2026-09-03:* `len(model.get_logits_from_input_ids([9707])) == 151936`
- [ ] El valor de la posición `i` es la puntuación del token cuyo id es `i` — ==el id **es** el índice, no hay traducción de por medio==
- [ ] Es **determinista**: la misma entrada da la misma salida
- [ ] Se la llama **una vez por vuelta del bucle**, y la entrada crece a cada vuelta

**Las dos variantes que hacen falta, y qué compra cada una:**

| Variante | Qué hace | Qué estado dispara |
|---|---|---|
| **La que lanza** | `raise RuntimeError(...)` en la primera llamada, o en la enésima | `'Model failed while replying'` (`R6.3`) |
| **La plana** | Devuelve `[0.0] * 151936` | `'Model entered an loop'` (`R6.4`) — *verificado ejecutando el 2026-09-03 con el prompt `"Greet shrek"`* |

> [!warning] La función simulada NO sustituye al modelo real
> **Orden del estudiante, 2026-09-03:** *"quiero usar los dos, porque necesito saber que los dos funcionan. Haz las pruebas con A y con B; lo que no se pueda hacer con uno se fuerza con el otro"*.
> **Reparto:** el flujo real, el recorrido de los 11 prompts y las invariantes de estructura (`R6.6`, `R6.8`, `R6.9`, `R6.10`) van con **E4, el modelo real**. Los dos estados que Qwen no provoca nunca —el fallo y el tope— se fuerzan con **E5**.
> ==Un test que compruebe el flujo normal usando solo E5 no compra nada: mide la función del propio test.==

---

## R10 · Archivo de tests

`tests/test_bloque_5.py`

---

## R11 · Comando de ejecución y arranque

```bash
make testN test=5
```

Que es, entero:

```bash
./callme/bin/python -m pytest tests/test_bloque_5.py -v
```

**Imports:**

```python
from llm_sdk import Small_LLM_Model
from src.filemanager import FileManager, Function, Prompt
from src.interface import Interface, Output
```

> [!warning] La carga del modelo va en una fixture de **sesión**
> `Small_LLM_Model()` descarga y carga pesos: **cárgalo una sola vez para toda la suite**, nunca por test. La suite del Bloque 4 tarda ~4 minutos por no tener esto medido; aquí sí lo está.

**Las rutas de los datos se construyen desde la raíz del repositorio, no relativas al `cwd`:**

```python
RAIZ = Path(__file__).resolve().parent.parent
FUNCIONES = RAIZ / "data" / "input" / "functions_definition.json"
PROMPTS = RAIZ / "data" / "input" / "function_calling_tests.json"
```

`FileManager` pide además una ruta de salida; usa `tmp_path` de pytest para eso. **No escribas nada dentro de `data/`.**

---

## R12 · Recorrido completo — un caso real de principio a fin

> [!info] Verificado ejecutando el 2026-09-03. Cada línea dice quién produce qué

```
1 · el test           Small_LLM_Model()                       -> el modelo, una vez por sesión
2 · el test           FileManager(...).get_functions()        -> List[Function], las 5 reales
3 · el test           Interface(functions, vocab, merges,
                                tokenizer, get_logits...)     -> la instancia
4 · el test           face.reply("What is the sum of 2 and 3?")
5 · Interface         ...genera token a token...              (1,9 s)
6 · Interface         devuelve Output(
                        log='The prompt was replied correctly',
                        output='{"prompt":"What is the sum of 2 and 3?",
                                 "name": "fn_add_numbers",
                                 "parameters": {"a": 2,"b": 3}}')
7 · el test           json.loads(out.output)                  -> dict con 3 claves
8 · el test           assert d["name"] in {f.name for f in functions}
9 · el test           assert set(d["parameters"]) == set(schema de fn_add_numbers)
```

**Los otros tres estados, tal como salieron el 2026-09-03:**

```
face.reply("")                 -> log='The prompt was empty'
                                  output=''

con E5 que lanza:              -> log='Model failed while replying'
face.reply("Greet shrek")         output='{"prompt":"Greet shrek", "name": "'

con E5 plana:                  -> log='Model entered an loop'
face.reply("Greet shrek")         output='{"prompt":"Greet shrek", "name": "fn_add_numbers",
                                           "parameters": {"a": 0,"b": 0.0000000000...'
```

---

## Antes de escribir el primer test — la checklist del encargo

- [ ] ¿Has leído las secciones `R1` a `R12` enteras, y entendido qué **no** es de esta clase (`R7`) y qué está descartado a propósito (`R8`)?
- [ ] ¿Tienes claro por qué un `output` con `Ġ` dentro **es correcto** en este bloque?
- [ ] ¿Has respondido las cuatro preguntas del límite real (`F6`) con los datos de `R9`, y escrito la tabla del plan de stress?
- [ ] ¿Cada estado de `R6.2` tiene **al menos un test que lo dispara**, incluidos los dos que solo salen con `E5`?
- [ ] ¿Cada invariante se contrasta contra el catálogo entero y los 11 prompts, no contra dos ejemplos?
- [ ] ¿El modelo real se carga **una vez** por sesión?
- [ ] Lo que no puedas decidir, ¿lo has marcado como suposición y preguntado, en vez de asumirlo (`F5`)?

> [!warning] Cero huecos
> Si al escribir un test no sabes qué esperar, **para y pregunta**. No lo decidas por tu cuenta y no lo dejes como pendiente silencioso.
