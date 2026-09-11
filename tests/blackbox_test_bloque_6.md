---
tipo: contrato
bloque: 6
unidad: src/__main__.py (el comando) — Chat es mecanismo interno, no se prueba directo
creado: 2026-09-10
actualizado: 2026-09-10 — restructurado: el sujeto de prueba pasó de ser `Chat` a ser el comando completo
---

# Contrato del Bloque 6 — el comando `python -m src`

> [!warning] Cambio de fondo, no de detalle — 2026-09-10
> La primera versión de este contrato probaba `Chat` construida directo, con las rutas ya parseadas a mano. **Eso nunca ejercita `src/__main__.py`** — que es lo único que corre el evaluador (`uv run python -m src`, primera línea de la hoja de evaluación). Reescrito para que el sujeto de prueba sea **el comando**, y `Chat`/`Interface`/`Guardian`/`FileManager` queden como mecanismo interno: el agente ciego no necesita saber que existen.

| Campo | Valor |
|---|---|
| Quién lo escribió | El agente que acompañó la construcción |
| Quién lo aprobó | El estudiante |
| Quién lo lee | Solo el agente de tests |
| Escrito | 2026-09-10, con el programa escrito y corriendo |
| Dónde vive | `tests/blackbox_test_bloque_6.md` |

---

# PARTE FIJA — copiada literal

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
| **Nombre de cada test** | `test_` + lo que garantiza, en palabras: `test_start_acepta_el_prompt_vacio` |
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

> [!tip] Por qué el entorno del proyecto
> Es el mismo que ejecuta el evaluador. Un verde ahí vale; un verde en un entorno fabricado solo dice que allí funcionaba.

---

# PARTE RELLENABLE

## R1 · Qué hace el programa

`python -m src` es la herramienta de línea de comandos completa: recibe las rutas de un catálogo de funciones, una lista de prompts y una ruta de salida; por cada prompt, usa el LLM con decodificación restringida para producir una llamada de función estructurada; escribe el resultado en un JSON y, si algo falla, un log aparte.

## R2 · Interfaz pública

No es una clase — es un comando.

```bash
./callme/bin/python -m src [--functions_definition <ruta>] [--input <ruta>] [--output <ruta>]
```

| Flag | Default |
|---|---|
| `--functions_definition` | `data/input/functions_definition.json` |
| `--input` | `data/input/function_calling_tests.json` |
| `--output` | `data/output/function_calling_results.json` |

**Devuelve (observable desde afuera del proceso):**
- Código de salida: `0` si el programa completó su ciclo, `1` si no pudo — *(verificado ejecutando, ver R5)*.
- Efecto en disco: `--output` se escribe **siempre**; `logs/logs.json` se escribe **solo si hubo un fallo**.

## R3 · Cómo se conduce una sesión

Se corre el comando una vez. No hay sesión interactiva ni estado que inspeccionar entre medio — todo lo que importa queda en disco cuando el proceso termina.

```bash
./callme/bin/python -m src \
  --functions_definition <ruta> --input <ruta> --output <ruta>
echo $?                    # 0 o 1
cat <output>                # el resultado, o [] si no había prompts
cat logs/logs.json          # existe solo si algo fallo
```

## R4 · Qué debe aceptar

- Correrse **sin ningún flag** — usa los tres defaults de `R2`.
- Cualquier combinación de flags con rutas que existen.
- `--functions_definition` apuntando a 1 o más funciones válidas — tipos `number`, `integer`, `float`, `string`, `boolean`, o anidado con `properties`.
- `--input` apuntando a una lista de prompts, **incluida una lista vacía** — *(verificado ejecutando: 0 prompts → código de salida `0`, `--output` queda en `[]`, `logs/logs.json` no se crea)*.
- **`--output` apuntando a una ruta que no existe todavía, con carpetas intermedias tampoco creadas** — se crea todo automáticamente. *(Verificado ejecutando: `--output .../carpeta_nueva/salida.json` con `carpeta_nueva/` inexistente → se crea la carpeta y el archivo, código de salida `0`.)* A diferencia de las otras dos rutas, `--output` **no** es `FilePath` — es `Path`, nunca se exige que exista de antemano.

## R5 · Qué debe rechazar

| Caso | Código de salida | `logs/logs.json` | Certeza |
|---|---|---|---|
| `--functions_definition` o `--input` no apuntan a un archivo existente | `1` | Sí — texto del `ValidationError` de pydantic (`"...Path does not point to a file..."`) | Verificado ejecutando |
| `--functions_definition` apunta a una lista vacía `[]` | `1` | Sí — `"Function's file is empty"` | Verificado ejecutando |
| JSON corrupto en `--functions_definition`/`--input` | `1` | Sí — `"Corrupt JSON in ..."` | Dato del contrato |
| Un módulo requerido no se puede importar (ej. `llm_sdk` roto o ausente) | `1` | Sí — `"An error occurred while importing a required module: ..."` | Verificado ejecutando |
| `Ctrl+C` durante la carga de módulos, **antes** de empezar a generar | `1` | Sí — `"The keyboard has interrupted the program during startup"` | Verificado ejecutando con señal real (`SIGINT` a los 0.1s) |
| `Ctrl+C` durante la generación, ya con el modelo cargado | `1` | Sí — `"The keyboard has interrupted the generation process"` | Verificado ejecutando con señal real (`SIGINT` a los 6s) |

> [!important] Nunca un traceback crudo
> Ninguno de los seis casos de arriba debe imprimir una excepción de Python sin atrapar hacia `stderr` de forma descontrolada. Un traceback ahí es rojo — la hoja de evaluación lo califica como *"unexpected, uncontrolled termination"*, nota final 0.

> [!warning] Timing del `Ctrl+C` — no es instantáneo, hay que apuntar la señal
> La ventana de "durante el import" dura ~1-2 segundos (carga de `torch`/`transformers`) y varía con caché del sistema. Un test que mande la señal a un tiempo fijo puede caer en cualquiera de las dos ramas según cuánto tarde esa vez — si el objetivo es probar una rama específica, conviene forzar el punto (ej. con un `time.sleep` generoso antes de la señal, o repetir con varios tiempos) en vez de confiar en un número mágico.

## R6 · Invariantes

1. La salida siempre trae **exactamente N objetos para N prompts**, en el mismo orden que `--input` — el prompt fallido incluido. *(Verificado ejecutando con un fallo forzado entre dos prompts exitosos: 3 prompts → 3 objetos.)*
2. Cada objeto **exitoso** trae exactamente 3 claves: `prompt`, `name`, `parameters` — sin anidar, sin claves de más.
3. Cada objeto **fallido** trae exactamente 2 claves: `prompt`, `ERROR` — el texto de `ERROR` es una copia literal del **log** de esa generación (ej. `"Model entered an loop"`, `"Model failed while replying"`, `"Empty prompt"`), **nunca el texto del prompt**. *(Verificado ejecutando el 2026-09-10 — antes de hoy había un bug real: `ERROR` repetía el `prompt`, no el log. Corregido en `chat.py`.)*
4. `name` es siempre uno de los nombres del catálogo de `--functions_definition` — nunca un nombre fuera de esa lista. El catálogo real recibe internamente una función de escape adicional no declarada en el archivo (usada cuando ningún prompt calza) — su nombre también es válido, ver `R9`.
5. `logs/logs.json` se escribe **si y solo si** hubo al menos un fallo. Si todo sale bien, el archivo no se crea.
6. **Solo un tipo de fallo se reintenta:** cuando el SDK lanza una excepción pidiendo logits (`log == "Model failed while replying"`), hasta 3 veces, antes de darlo por definitivo. **Ningún otro fallo se reintenta nunca** — ni un prompt vacío (`"Empty prompt"`), ni uno que no cierra el JSON a tiempo (`"Model entered an loop"`), ni un fallo de contenido/tipo (`"ERROR"` de `_valid_parameters`). *(Verificado ejecutando con un fallo de loop forzado: un solo intento, va directo al objeto `{"prompt", "ERROR"}`.)*
7. **Un prompt individual que falla no hace fallar al programa** — el código de salida sigue siendo `0` si el ciclo completo terminó, aunque algún objeto de la salida sea `{"prompt", "ERROR"}`. Solo un fallo de *arranque* (construcción, import, interrupción — `R5`) da código `1`. *(Dato del contrato, coherente con el mecanismo que se debe verificar directamente esta sesión: el fallo de un prompt se registra y el recorrido sigue, sin lanzar nada hacia afuera.)*

## R7 · Fronteras

| Fuera de este programa | Por qué |
|---|---|
| Ejecutar de verdad la función elegida (calcular la suma, invertir el string, etc.) | El subject no lo exige — el programa se detiene en producir `name` + `parameters` |
| Elegir la función con una heurística (`if`/`else` sobre palabras clave) | Prohibido por el subject — la elección la hace el LLM |
| Soportar más de un modelo LLM además de Qwen3-0.6B | Bonus 1, no implementado |

> [!important] Internamente se apoya en `Chat`, `Interface`, `Guardian`, `FileManager`, `Tokenizer` — pero eso no hace falta saberlo
> Son mecanismo interno del programa, cada uno con su propio contrato de bloque (2, 4, 5, 6). **El agente ciego de este contrato no necesita conocerlos ni nombrarlos**: todo lo que hay que verificar es observable desde afuera — el archivo de salida, `logs/logs.json`, y el código de salida del proceso.

## R8 · Descartado a propósito

- **Ejecutar de verdad la función elegida** — el subject no lo pide.
- **Soporte para más de un modelo LLM** (bonus 1) — pendiente, no implementado esta ronda.
- **Forzar un espacio antes o después de una comilla embebida en un string** — se evaluó y se descartó el 2026-09-10: cruzaría la regla del subject de que la elección/contenido lo produce el LLM, nunca una heurística fija.
- **`"type": "float"` es un alias exacto de `"number"`**, sin comportamiento propio — se agregó sin que ningún catálogo real (subject, `new_data`, el del compañero) lo use todavía, por el mismo motivo que se agregó `"integer"` cuando apareció sin avisar.

## R9 · Elementos objetivos
Fueron definidos 3 catalogos diferentes de funciones para testear varios escenarios. El del proyecto real que viene junto con el proyecto desde la escuela y que explicitamente piden que no sea un limite de teste sino al contrarios, testear con mas funciones. El del companero extraido del proyecto de un companero de la escuela que supero con exito el proyecto y el de estres propio que fue disenado con el fin de estresar al proyecto lo maximo posible sin sobrepasar la linea del uso real del mismo.
| Identificador | Nivel | Ruta | Forma | Cómo se carga | Qué reproduce |
|---|---|---|---|---|---|
| Catálogo real del proyecto | 1 | `data/input/functions_definition.json` | Lista de 5 funciones (`fn_add_numbers`, `fn_greet`, `fn_reverse_string`, `fn_get_square_root`, `fn_substitute_string_with_regex`) | `TypeAdapter(List[Function]).validate_python(json.load(...))`, o pasando la ruta directo a `Chat`/`FileManager` | Tipos `number`/`string`, sin anidar, sin `integer`/`boolean`/`float` |
| Prompts reales del proyecto | 1 | `data/input/function_calling_tests.json` | Lista de prompts del subject | Igual que arriba | Prompts simples de una sola función |
| Catálogo del "examen" del compañero | 1 | `tests/new_data/input/functions_definition.json` | 6 funciones, incluye `integer`, `string`, `number` | Igual | Tipos ya vistos en producción real de otro proyecto |
| Prompts del "examen" | 1 | `tests/new_data/input/function_calling_tests.json` | 11 prompts, incluye rutas con backslash y strings con comillas embebidas | Igual | Casos reales de escapado, no inventados |
| Respuesta correcta del "examen" | 1 | `tests/new_data/correction/function_calling_corrections.json` | 11 objetos `{prompt, name, parameters, expected_output}` | Se lee y se compara `name`+`parameters` — `expected_output` **fuera de alcance**, no se usa | El resultado correcto de function calling para los 11 prompts de arriba |
| Catálogo de estrés propio | 2 | `tests/stress_data/input/functions_definition.json` | 9 funciones fabricadas: anidación de 1 y 2 niveles, dos nombres con prefijo largo compartido, `float`, `boolean`, dos parámetros del mismo tipo en una función | Igual que el real | Casos que ni el subject ni el compañero cubren, diseñados el 2026-09-10 |
| Prompts de estrés propio | 2 | `tests/stress_data/input/function_calling_tests.json` | 9 prompts, uno por función de arriba (uno usa comillas solas, otro combina comillas+backslash y está marcado de frontera) | Igual | — |
| Respuesta correcta del estrés propio | 1 | `tests/stress_data/correction/function_calling_corrections.json` | 9 objetos `{prompt, name, parameters}`, 1 con campo extra `boundary_case` | Se lee tal cual | Respuesta correcta diseñada a mano — la fila con `boundary_case` **no es exigible**: documenta un límite real del modelo (comillas+backslash combinados en el mismo valor) sin el enmascarado del eco del prompt, no un fallo de `Chat` |
| Modelo real | 1 | — (paquete `llm_sdk`) | `Small_LLM_Model()` | Se construye **una sola vez por sesión de tests** (fixture de sesión, `F6`) — cargar el modelo es caro | El modelo Qwen3-0.6B real, no un mock — usado toda esta sesión para verificar |
| Rutas del modelo | 1 | Salen de `model.get_path_to_vocab_file()` / `get_path_to_merges_file()` / `get_path_to_tokenizer_file()` | 3 `str`, se envuelven en `Path(...)` | Se llaman sobre la instancia de `Small_LLM_Model` de arriba | Vocabulario y reglas de fusión reales del modelo |
| Función de escape `fn_unknown` | 1 | No vive en ningún archivo — se inyecta en tiempo de ejecución antes de construir el mecanismo interno | `name="fn_unknown"`, `parameters={}`, `returns={"type": "string"}` | Se agrega siempre, encima de lo que traiga `--functions_definition` | Verificado ejecutando: con un prompt sin match real (`"What's the weather like today?"`), el programa eligió `fn_unknown` con `parameters: {}` |

## R10 · Archivo de tests

`tests/test_bloque_6.py`

## R11 · Comando de ejecución

```bash
./callme/bin/python -m pytest tests/test_bloque_6.py -v
```
(equivalente a `make testN test=6` desde la raíz del proyecto)

> [!important] La mayoría de estos tests corren `python -m src` como subproceso, no importan `Chat`
> Lanzan el comando real (`subprocess.run`/`subprocess.Popen`), con archivos temporales de catálogo/prompts, y verifican el código de salida + el contenido de `--output`/`logs/logs.json` — exactamente como en `R3`. Es más lento que importar clases directo, pero es lo único que prueba de verdad lo que corre el evaluador. La carga del modelo sigue siendo cara: reusar el mismo proceso o los mismos archivos temporales entre tests cuando se pueda, en vez de relanzar el intérprete completo para cada `assert`.

## R12 · Recorrido completo

> [!important] Ejecutado de verdad, arrancando en `src/__main__.py` — no construyendo `Chat` a mano
> ```bash
> ./callme/bin/python -m src \
>   --functions_definition data/input/functions_definition.json \
>   --input <archivo con un solo prompt> \
>   --output <archivo de salida>
> ```
> Salida real, verificada ejecutando el 2026-09-10:
> ```json
> [{"prompt": "What is the sum of 2 and 3?", "name": "fn_add_numbers", "parameters": {"a": 2, "b": 3}}]
> ```
> `a`/`b` quedan `int`, no `2.0`/`3.0` — confirma el arreglo de `ParamValue` de hoy en el flujo real, no solo aislado. Previamente se encontro un bug con respecto al typing numerico.

Caso real: prompt `"What is the sum of 2 and 3?"` contra el catálogo real (`data/input/functions_definition.json`).

1. **`src/__main__.py`** parsea `--functions_definition`/`--input`/`--output` con `argparse` → 3 rutas.
2. **`src/__main__.py`** construye `Small_LLM_Model()`, le saca `get_path_to_vocab_file()`/`get_path_to_merges_file()`/`get_path_to_tokenizer_file()` y `get_logits_from_input_ids`.
3. **`Chat.__init__`** construye `FileManager` (lee y valida los 5 nombres del catálogo real + el prompt) y `Interface` — que a su vez construye `Tokenizer`, `PromptBuilder` y `Guardian` con el catálogo **más `fn_unknown` inyectado**.
4. **`Chat.chatting()`** entra al `for` de un solo prompt, llama `Interface.reply("What is the sum of 2 and 3?")`.
5. **`Interface.reply`**: `Guardian.start(...)` arma el esqueleto del JSON; en cada vuelta, `Tokenizer.encode` tokeniza lo escrito hasta ahora, `Guardian.get_valid_ids()` filtra qué tokens son válidos, el modelo real da los logits, se elige el `argmax` entre los válidos, `Guardian.add_token` lo agrega — hasta que `Guardian.is_open()` da `False`.
6. **`Interface`** valida los tipos de `parameters` (`_valid_parameters`) y traduce los bytes disfrazados (`_costume_translater`), devuelve un `Output(log="The prompt was replied correctly", output={"prompt": ..., "name": "fn_add_numbers", "parameters": {"a": 2, "b": 3}})`.
7. **`Chat`** ve que `output` tiene 3 claves, llama `FileManager.charge_replies(answer.output)`.
8. Fin del `for` (un solo prompt). **`Chat`** llama `FileManager.write_logs()` (no escribe nada, no hubo fallos) y `FileManager.write_replies()` — el archivo de salida queda con **un** objeto: `{"prompt": "What is the sum of 2 and 3?", "name": "fn_add_numbers", "parameters": {"a": 2, "b": 3}}`.
