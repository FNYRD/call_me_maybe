---
tipo: historico
proyecto: call me maybe
tags: [42, repasos, cuestionarios, historico]
---

# REVIEWS.md — Histórico de cuestionarios de repaso

> [!warning] No se lee al contextualizarse
> Este archivo **no entra en la ruta de lectura**. Es histórico: guarda cómo fue cada repaso, no qué hay que hacer hoy.
> Lo vivo — qué falta reforzar y qué se pregunta en la próxima sesión — vive en `[[PROJECT#🎯 Lista de refuerzo]]` y `[[PROJECT#📋 Cuestionario de la próxima sesión]]`.

> [!info] Cuándo sí se abre
> · Un tema falla por tercera vez y hace falta ver **cómo** se explicó las veces anteriores, para no repetir la explicación que no funcionó
> · El estudiante pregunta qué se contestó un día concreto
> · Se reconstruye la evolución de un concepto a lo largo del proyecto
>
> Fuera de esos casos, no se abre: son miles de palabras de contexto que no cambian lo que toca hacer hoy.

> [!note] Cómo crece
> Una entrada por sesión, **la más reciente arriba**. Nunca se sobrescribe una anterior.
> Cada entrada lleva: los fallos con su corrección, lo que salió correcto sin ayuda, y lo que se decidió diferir.

---

## Repaso 2026-09-03 (2ª sesión del día) — ==una sola pregunta, elegida por él==

> [!info] Dio el cuestionario por innecesario y luego pidió ver las preguntas
> Abrió con *"no hay cuestionario porque no hay ningún tema a reforzar"*. Se le respondió con el dato —quedaban filas 🔴— sin insistir, y pidió las cuatro preguntas para elegir: *"dime cuáles son las preguntas del cuestionario y las elijo"*. Escogió **solo la 2**, la de la invariante.
> ==**Elegir de una lista le funcionó mejor que aceptar o rechazar el cuestionario entero.**== Es el mismo patrón ya registrado: convertir la pregunta en una elección entre artefactos.

| # | Tema | Resultado |
|---|---|---|
| 2 | **Invariante vs caso** — `A: name ∈ catálogo` frente a `B: reply('Greet shrek') -> fn_greet` | ==**Cerrado, en cuatro turnos.**== Arrancó con *"no sé qué es una invariante"* → respuesta directa. Corrigió solo dos veces sobre su propia formulación |

**Cómo fue, turno a turno:**

1. *"No sé qué es una invariante"* → directo, con sus dos frases al lado: **caso = un punto** · **invariante = cierto siempre, para todo el universo**.
2. Devolvió *"¿entonces invariante es un test que se debe hacer de una manera específica y ya?"* → ==confundía la promesa con su comprobación==. Lo cerró separarlo en dos líneas: la invariante es **propiedad del código y existe aunque nadie escriba el test**; recorrer el universo es **consecuencia**, no definición.
3. Reformuló bien: *"una promesa que el artefacto dice cumplir sí o sí y se debe testar en todos los casos"*. Se aceptó con el matiz de qué se hace cuando el universo no cabe.
4. **Preguntó por el matiz** —*"estado de qué, qué lista"*—, y con razón: se le había dicho *"congelar un estado y recorrer su lista"* **en abstracto**. Lo cerró el artefacto suyo: `_slot='number'`, `_written='40'` → los **12 ids** de `get_valid_ids()`, los 12 y no tres a mano.

> [!success] Cierre con sus palabras
> *"Una invariante es una promesa del código de devolver o hacer algo, y en su test se debe hacer con todo el universo que representa un caso real; si no, no se estaría testando que cumpla en todos los casos."*

> [!warning] El fallo del agente, otra vez el mismo
> ==**"Se congela un estado y se recorre su lista" no es un artefacto: es prosa.**== Tuvo que pedir *"estado de qué, qué lista"*. Enésima confirmación de la regla del 08-29 — la explicación empieza por el artefacto, y aquí el artefacto estaba a mano: su `Guardian` congelado y los ids reales.

> [!note] Sin lanzar
> Las preguntas **1** (por qué en `name` no cabe flag), **3** (la regla de cifras) y **4** (por qué el agente de tests tampoco ejecuta) quedan en el banco, sin preguntar.

---

## Sesión 2026-09-02 — ==sin repaso, por decisión suya==

> [!info] No hubo cuestionario, y puede que no vuelva a haberlo
> Abrió la sesión con: *"estoy pensando en quitar los cuestionarios posterior a la fase de internalización de conceptos, así que hoy no haremos esa fase"*. ==**No lo cerró como decisión**==, así que el cuestionario de la siguiente quedó escrito igual, con la advertencia delante.
> **Es la segunda sesión seguida sin repaso completo:** la del 09-01 la anuló él a la tercera pregunta, por preguntas mal redactadas.
> **Lo que conviene preguntarle antes de borrar la regla:** si lo que sobra es el cuestionario o las preguntas malas. La regla del repaso la creó él (08-10) y la fijó como lo primero de la sesión (08-17).
>
> **Lo que sí se verificó, sin cuestionario:** la sesión fue de teclear, y los huecos salieron solos —`np.full` con la string, la línea con los logits dentro de los corchetes, el id como índice—. Los tres están en `[[PROJECT#🎯 Lista de refuerzo]]` con **cómo se cerró cada uno**, que es lo que se preguntaría.

---

## Repaso 2026-09-01 — ==anulado por él a la tercera pregunta==

> [!warning] Sesión cancelada: dos preguntas de tres estaban mal redactadas
> No es un resultado de repaso, es un fallo del cuestionario. Se registra entero porque el patrón ya va por su tercera aparición (08-29, 08-31, hoy) y las tres veces lo detectó él.

| # | Qué pasó |
|---|---|
| 1 | **A medias.** Con las dos ramas delante acertó que la primera da `False`; dijo que la vieja (`candidate2add == "0" and text`) aprobaba el `7`, y **no la aprueba** — el `7` lo aprobaba la rama `in DIGITS` que había quedado **intacta encima**. Lo cerró sustituir los literales (`elif "7" == "0" and "0":`) y preguntar cuántas veces se ejecuta esa segunda rama: *"ninguna"*. ==La lección quedó: la corrección buena **restringe la rama que ya da el paso**, no añade otra debajo== |
| 2 | ==**Retirada.**== Venía redactada con `Reply.model_validate(d)`, clase del Bloque 5 **que no existe en `src/`**. Cortó: *"no sé qué es esto"*. Reformulada, el agente **volvió a apoyarse en la misma pieza** y la cortó otra vez: *"tu pregunta está muy fuera de contexto"*. Pidió que quedara registro → entrada nueva en *Evitar* de `[[PSYCHOLOGY]]`. Lo único que quedó en pie fue la ejecución: `json.loads('{"a": 40²}')` → `JSONDecodeError` |
| 3 | ==**Anulada, y con ella la sesión.**== *"¿Qué tiene que pasar para que un rojo sea del test y no del código?"* → *"pregunta estúpida y mal hecha. vaga, podría responder que el test esté mal hecho y ya tendría razón. se anula la sesión de repaso"*. **Tenía razón: la pregunta admite una respuesta tautológica**, así que no discrimina entre saber el criterio y repetir el enunciado |

> [!important] Las dos reglas que salen de aquí
> · ==**Cada identificador de una pregunta tiene que existir hoy en `src/`.**== Si el concepto necesita una pieza futura, va como dato suelto y sin nombre — o no se pregunta. (Regla del 08-29 aplicada al cuestionario, saltada dos veces seguidas hoy.)
> · ==**Una pregunta que se puede contestar repitiendo su enunciado no mide nada.**== Hermana de la del 08-31 (la respuesta estaba en el artefacto que la acompañaba): allí la respuesta la daba el artefacto, aquí la da la propia pregunta.

> [!note] Estado tras la anulación
> Las preguntas **4, 5 y 6** no llegaron a lanzarse. La lista de refuerzo queda con la fila del `40²` en 🔴 y *pregunta retirada*.

---

## Repaso 2026-08-31 — entrada de sesión, `Guardian` implementada y sin tests

> [!info] 4 limpias de 5 · una pregunta retirada por mal redactada
> El cuestionario traía **seis**. La **2** —qué comparten catálogo y prompts en `_load_json`— la retiró el agente tras cortarla él (*"esa pregunta es muy estúpida, paso"*): se contestaba leyendo el `if`/`elif` que se le había puesto delante en el mismo mensaje. ==Tenía razón: una pregunta cuya respuesta está en el artefacto que la acompaña no mide nada.==

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 3 | **`str.isdigit()` y los superíndices.** Los tokens los identificó (*"los tokens de números minúsculos"*), pero dijo que fallaría **`pydantic`** | Se le puso el `raw` congelado con `40²` dentro y las dos líneas separadas —`json.loads(raw)` y `Reply.model_validate(d)`— preguntando en cuál revienta. Contestó `json.loads` a la primera. **Revienta antes de llegar a `pydantic`** | Bloque 4 |
| 5 | **Contrato sin pasos numerados: el lado del implementador.** Dio entera la razón del que testea (*"que ninguno tuviera manera de hacer trampa… ni testar basado en lo que existe"*), pero del implementador no dijo nada | Se le puso el mismo requisito en dos formas —paso numerado `4.b` vs invariante— y se preguntó qué trabajo le queda con el paso delante. Dijo *"no sé, tu pregunta es confusa"* → directo: **ninguno, transcribir**; y si el paso está mal, el código sale mal sin que nadie lo note. Es lo que él mismo nombró el 08-29 escribiendo `_char_ok`: *"es casi copiar código"* | Sistema |

> [!success] Correcto sin ayuda
> **`copia` vs `self._written` en la simulación** — con la traza de `_token_ok` delante contestó *"`self._written = "40"` y copia `"40."`, aún no aprobamos el 5"*. ==Cae por fin: llevaba dos fallos, 08-27 y 08-29.== · **El atajo del nombre único** — *"debe elegir por lo menos la mínima cantidad de caracteres para que la única opción que quede sea 1, de esa manera él la eligió, nosotros autocompletamos"* · **Por qué el agente de tests no abre `src/`** — *"testaría basado en código, no sería una caja negra de test"*.

> [!note] Lo que confirmó el formato
> Las tres limpias tenían **un artefacto congelado delante** —la traza de `_token_ok`, el `raw` con `40²`, el enunciado de la regla—. La única que hubo que dar directa (la 5) estaba planteada como comparación abstracta entre dos formas de escribir un contrato. Mismo patrón que el 08-29, ya en `[[PSYCHOLOGY]]`.

---

## Repaso 2026-08-29 — entrada de sesión, `Guardian` a medias

> [!info] 3 limpias de 6
> Sesión corta, con la meta puesta en terminar la clase. Las tres limpias son sobre **lo que él escribió ayer**; los tres fallos, sobre **lo que aún no ha tecleado** — mismo patrón ya registrado: lo que está en código sobrevive, lo que solo se habló, no.

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 1 | **Qué recibe `start`.** El tipo lo acertó (`str`), pero dijo que el contenido era `{"prompt": "Greet shrek"}` entero | Se **ejecutó su propio `start`** con esa entrada: salió `{"prompt":"{\"prompt\": \"Greet shrek\"}", "name": "`. Comparado con el `_json_str` de la pregunta 1, lo corrigió solo: entra `"Greet shrek"` | Bloque 4 |
| 2 | **Quién deshace el dict.** Contestó *"el bloque siguiente, que lo va a llamar por prompt"* (quién lo pasa, no quién lo deshizo), y después señaló `json.dumps` dentro de `start` | Se ejecutó `src/filemanager.py:48` por partes: `json.load` → `dict`, `validate_python` → `Prompt`, `.prompt` → `str`. **Lo deshizo `pydantic` en el Bloque 2**; `json.dumps` corre después y solo escapa | Bloque 2 |
| 3 | **`written` vs `self._written`.** Con `self._written = "40"` y el token `".5"`, dijo que en la segunda llamada `written` valía `"40"` | Dijo *"no entiendo"* dos veces → directo: `written = "40."` (la copia ya creció con el punto) y `self._written = "40"`, que no se mueve hasta `add_token` | Bloque 4 |
| 4 | **Por qué `_closing_char` no hace `pop`.** El "no" lo tenía, pero la razón fue *"decidimos dejar esa responsabilidad a otra función"* — la regla, no la causa | Dijo *"no entendí la pregunta"* → directo: `get_valid_ids` prueba ~151.000 tokens por paso y consulta el cierre en cada uno; **solo uno se escribe**. Un `pop` ahí desmontaría la pila 151.000 veces por paso | Bloque 4 |

> [!success] Correcto sin ayuda
> **Modelo vs `Guardian` en un `_json_str` congelado** — señaló `fn_greet`, la **comilla de cierre** y el `4`, todo lo demás inyectado. Es la pregunta que el 08-27 no supo ni formular (*"¿a qué te refieres con huecos?"*) · **El `+=` en `start`** — *"el prompt anterior"* quedaría pegado delante, sin lanzar error · **La regla que falta en `_char_ok`** — con `written = "fn_greet"` y catálogo `fn_greet`/`fn_greeting`, su código **no** aprueba la comilla.

> [!warning] Se quejó de la redacción de las preguntas
> *"estas preguntas están saliendo mal porque no sabes redactarlas. las redactas como una máquina y yo no lo soy… realmente me confundo mucho con tus preguntas"*.
> Lo que sí funcionó fue **poner la traza delante** (la copia creciendo línea a línea) y **ejecutar su propio código** en vez de describir el escenario en prosa. Anotado en `[[PSYCHOLOGY]]`.

---

## Repaso 2026-08-27 — NO HUBO

> [!info] Sin cuestionario, por decisión suya del 2026-08-26
> *"Para la próxima sesión sin cuestionario, arrancamos repasando lo decidido y lo que falta por decidir"* — el diseño de `Guardian` había quedado a mitad y quiso seguir ahí en vez de interrumpir con verificación.
> **Excepción puntual.** La regla general (*"cuestionarios siempre primero"*) sigue en pie: el de la sesión siguiente ya está escrito en `[[PROJECT#📋 Cuestionario de la próxima sesión]]`.

**Lo que ocupó la sesión en su lugar:** cerrar el diseño del Bloque 4, escribir la guía `block_mockup/bloque_4_guardian.pdf` y arrancar la construcción de `Guardian`.

**Huecos detectados mientras escribía** — todos anotados en `[[PROJECT#🎯 Lista de refuerzo]]`, ninguno preguntado en frío:

| Salió al | Hueco | Cómo se cerró |
|---|---|---|
| Explicar `_written` | Qué es un **hueco** (`_slot`) — preguntó *"¿a qué te refieres con huecos?"* con el diseño ya cerrado | Los tres congelados puestos delante (`"name": "` · `{"a": ` · `{"s": "`) y que todo lo demás lo inyecta `Guardian` |
| Escribir `start` | Creía que entraba el **dict** del archivo | La cadena en cuatro líneas: JSON → `FileManager` → `List[Prompt]` → `Chat` coge uno → `"Greet shrek"` |
| Escribir `_char_ok` | De dónde sale `written` — dos preguntas seguidas | La traza de `_token_ok(".5")` con la copia creciendo `"40"` → `"40."` mientras `self._written` no se mueve |
| Escribir `_closing_char` | Propuso hacer el `pop` dentro | Que se llama **antes** de que el modelo elija, y miles de veces por paso: haría `pop` probando tokens que no se usan |
| Escribir `_char_ok` | Preguntó cuándo avanzan los índices de `_stack` | Los dos únicos momentos, con el JSON congelado en cada uno |

**Salió limpio sin ayuda:** la regla de `_closing_char` completa (`,` si quedan claves, `}` si es la última), escrita y verificada a la primera con su catálogo real.

---

## Repaso 2026-08-26 — entrada de sesión, Bloques 1-3 cerrados

> [!info] 5 limpias de 6 — solo el mecanismo del `\n` en la plantilla necesitó ayuda
> Los tres 🔴 heredados (`@validate_call` antes del cuerpo, caché de Hugging Face, asimetría `write_logs`/`write_replies`) y los dos de hoy sobre `PromptBuilder`/imports salieron limpios. El único hueco fue la mecánica de por qué el `\n` importa al modelo.

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 1 | **Por qué el `\n` en la plantilla le importa al modelo, mecánicamente.** Dio la razón general (*"así es como el modelo aprendió a usar las plantillas"*), correcta pero sin el mecanismo — no recordó qué hace distinto el `findall` con `"system You"` frente a `"system\nYou"` | Se dio directo: con espacio, `"You"` sale con `Ġ` pegado (palabra normal); con `\n`, el patrón corta ahí y `"You"` sale sin `Ġ`, otro id. Ids que el modelo no vio en su plantilla de entrenamiento | Bloque 3 · pre-tokenización |

> [!success] Correcto sin ayuda
> `@validate_call` no deja entrar al cuerpo con ruta inexistente · origen de `vocab.json`/`merges.txt` (Hugging Face) y que sin red no arranca · con `[]` solo existe `function_calling_results.json` con `[]`, sin `logs/logs.json` · la plantilla de `PromptBuilder` se construye una sola vez en `__init__`, no en cada `get_prompt` · `__package__` es lo que falta al correr el archivo suelto en vez de `-m src`.

---

## Repaso 2026-08-25 — entrada de sesión, Bloque 2 en construcción

> [!info] 3 limpias de 6 — ==lo que se escribió ayer en `src/` resistió; lo que solo se habló, no del todo==
> Las tres preguntas de lo trabajado el 08-24 (`TypeSpec`, `validate_python([])`, `FilePath` en la salida) salieron mucho mejor que los tres 🔴 heredados, que necesitaron el caso concreto otra vez.

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 1 | **Por qué el fallo de fichero no puede ir en `prompts`.** Acertó la clave (`files`) y el porqué fue circular: *"sencillamente porque no es un error de los prompts"*. **Segunda vez** (falló el 08-24) | Se le puso una entrada real delante —`"prompts": {"3": "..."}`— y se le preguntó qué número le pondría al fichero que falta: *"ninguno porque no tiene"*. Al preguntar **en qué momento revienta**, lo cerró él y mejor de lo esperado: *"lanza error en `FileManager` al instanciar el objeto, con `validate_call` y `FilePath`"* — es decir, **antes de que exista el array de prompts** | Bloque 2 |
| 2 | **Quién abre `logs/logs.json`.** La apertura única salió limpia y con su razón (*"primero se registra todo en el atributo y solo al final, caso existan logs, se abre"*), pero adjudicó el `open` a `Chat`. **Segunda vez** el mismo desliz | Se le pusieron sus **dos métodos** con la clase delante (`class FileManager: charge_logs / write_logs`) y se preguntó quién ejecuta el `open` → *"FileManager"*. El número de aperturas ya lo tiene; lo que se le va es **de qué clase es el método** | Bloque 2 |
| 3 | **Cuándo valida `@validate_call`.** Ante *"¿qué pasa si `output_path` fuera `FilePath`?"* dijo *"revienta error"* — correcto pero sin momento. Preguntado si revienta antes o después de entrar al cuerpo, contestó **"después"** | Se **ejecutó** delante de él con su venv `callme/`: una función decorada con un `print("ENTRE AL CUERPO")` dentro y una ruta inexistente → `ValidationError: path_not_file` y **el `print` no se imprimió**. El `mkdir` que crearía `data/output/` nunca llegaría a correr. Enésima confirmación de que ejecutar zanja lo que argumentar no | Bloque 2 · pydantic |

> [!success] Correcto sin ayuda
> **De dónde sale el resultado esperado del `assert` con el `merges.txt` real** — *"del encode de qwen"*, a la primera. ==Tercera vez preguntado, primera limpia== (falló el 08-18 y el 08-24); lo que cambió fue preguntar por el **resultado esperado** y no por el test · **`TypeSpec` recursivo** — *"se llama recursivamente… si anidan más, la estructura deja de ser `None` y crea `TypeSpec` on demand dependiendo de la cantidad de anidaciones"*, con el bonus 7 implícito · **`validate_python([])`** — pasa, devuelve `[]`, y sin guard salen 0 resultados, coherente con su regla de que la salida lleve siempre N objetos.

> [!note] Matiz corregido durante el repaso
> Al explicar `TypeSpec` dijo *"siguiendo el estándar de JSON"*. Se le recordó que **`properties` es convención de JSON Schema, no un dato del subject** — la línea del bonus dice solo *"Support for complex nested function arguments"*. Sigue anotado como suposición a verificar al montar los tests del bloque.

---

## Repaso 2026-08-24 — entrada de sesión, tras 6 días sin tocar el proyecto

> [!bug] 1 limpia de 5 — ==el diseño del Bloque 2 no sobrevivió a la pausa==
> Las tres preguntas del Bloque 2 (acordado el 08-18, **sin una línea escrita en `src/`**) fallaron las tres. Lo del Bloque 1, que sí está en código, salió limpio.

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 1 | **Con qué `merges.txt` se prueba la prioridad.** Contestó *"nada me impide nada, la idea del test es verificar que el código se adapta al formato"*. **Segunda vez** (falló el 08-18) | Objetó con razón que la pregunta pedía escribir un test, que no es suyo — se reformuló. Lo que lo desbloqueó fue apuntar al **`assert`**: *"con el de juguete sabes qué poner porque escribiste las dos líneas; con el real, ¿de dónde sacas el resultado esperado sin ejecutar tu propio `encode`?"* → *"del encode del modelo"*. Ahí está el coste: ese test dice **coincido con Qwen**, no **aplico la regla de línea más baja**, y si falla no sabes cuál de las dos se rompió | Testing |
| 2 | **Por qué el fallo de fichero no puede ir en `prompts`.** Acertó la clave (*"debe ser en FILES o algo así"*) y en el porqué dijo *"no sé"* | Directo: **no hay índice que poner**. El fichero revienta antes de que exista el array de prompts; los fallos de `prompts` ocurren dentro del bucle, cuando ya sabes en cuál vas. Ese nivel de fuera lo añadió él justo por eso | Bloque 2 |
| 3 | **Quién escribe el log.** El camino lo dio bien hasta el final —*"salta un raise, lo atrapa `Chat`"*— pero remató con *"y `Chat` lo escribe en el archivo"* | Se le puso el caso de dos fallos (prompt 3 y 7): dijo *"dos veces, y lo abre `Chat`"*. Lo cerró ponerle sus **propios dos métodos** delante (`charge_logs` carga en el dict · `write_logs` escribe al final si hay datos) y preguntar *"si `Chat` abre el archivo dos veces, ¿para qué sirve `charge_logs`?"* → *"tienes razón, no recordaba eso"* | Bloque 2 |
| 4 | **Qué comparten `validate_functions` y `validate_prompts`.** *"no recuerdo"* | Directo: se comparte **leer** (`_load_json` privado: `open` + `json.load` + los dos guards); no se comparten **las reglas de validación**, porque el catálogo mira `name`/`description`/`parameters`/`returns` y los prompts miran `{"prompt": str}` | Bloque 2 |

> [!success] Correcto sin ayuda
> **Qué valida `pydantic` y qué no** — con un `vocab.json` que existe y contiene `{}` fue directo a su propio `except ValueError: raise ValueError("Vocabulary's file empty")`. `FilePath` solo mira que la ruta exista; el resto sigue siendo de sus guards.

> [!note] Objeción suya, aceptada
> *"Los tests los escribió un agente, esta pregunta está mal planteada."* Tenía razón: la pregunta le pedía escribir un test. Reformulada apuntando al `assert` en vez de al test, contestó.

> [!warning] Lección de método
> **El Bloque 2 se diseñó entero y no se escribió nada.** Seis días después, las tres preguntas sobre él se fallaron, mientras que el Bloque 1 —que vive en `src/tokenizer.py`— salió limpio. El diseño que solo está en `PROJECT.md` se evapora; el que está en código, no.

---

## Repaso 2026-08-18 — entrada de sesión, antes del Bloque 2

> [!success] 4 limpias de 5 — ==los cuatro 🔴 pendientes cayeron sin ayuda==
> Tres de ellos llevaban tres sesiones fallando (mypy/`Optional`, bytes de `Ã`, `split(" ")`).

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 1 | **Por qué un vocabulario de juguete y no el real.** Contestó *"validar sobre los 256 bytes que igual usa el vocabulario"* — el suelo de bytes lo tienen los dos, así que no distingue nada | Se le puso el caso que discrimina: *"quiero un test que compruebe que se fusiona la regla de línea más baja. Con el de juguete escribo `merges.txt` con `a b` en la línea 1 y `b c` en la 2. ¿Podrías montar ese mismo test con el `merges.txt` real?"* → *"podría, pero tendría que adaptarse a la tabla del modelo real"*. Ahí está: con el real **no eliges las reglas**, buscas un caso que ya exista y montas el test alrededor | Testing |

> [!success] Correcto sin ayuda
> **`raise` como salida válida para mypy** — *"se ejecuta el raise y no se devuelve nada"*, limpio a la cuarta (falló 08-12, 08-14, 08-17) · **Bytes de `Ã` sola** — *"2"*, a la primera; la pregunta acotada funciona donde la del total escondía el fallo · **`split(" ")` sobre `"Greet shrek!\n\n"`** — *"el espacio desaparece, el `!` queda pegado a `k!\n`"*, las dos mitades · **Los 40 tests de juguete no prueban corrección** — *"no estábamos probando directamente contra el modelo, así que no era verídico"*.

> [!bug] El repaso guiado de los tests, cortado por él
> Lo había pedido él el 08-17. A los dos minutos: *"no me expliques pytest, brevemente dime qué se testea y ya; el objetivo no es aprender pytest sino entender por qué el test valida mi trabajo"*. Se le dio la tabla de las 8 secciones con qué prueba cada una, y respondió *"no tengo ahorita la capacidad para entender, pasemos al siguiente bloque, estoy un poco bloqueado"*.
> **Lección de método:** pidió *por qué el test valida su trabajo* y recibió *cómo funciona pytest*. Otra vez alcance equivocado, y esta vez la señal fue el bloqueo, no la corrección.

---

## Repaso 2026-08-17 — entrada de sesión, antes del bucle de merges

> [!note] Lanzado el primero, por regla suya
> Ante la duda de si arrancar por el bucle de merges o por el cuestionario, la zanjó él: *"cuestionarios siempre primero"*. Queda como regla de arranque de sesión.

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 1 | **Por qué mypy no exige `Optional`.** Contestó *"try except resuelve eso, queda como un tipo de retorno valido"* — atribuye el efecto al `try-except`, no al `raise`, y trata la excepción como si fuera un valor devuelto: *"seria como hacer un return ERROR"*. **Tercera vez que se pregunta** (08-12, 08-14, 08-17) | Dos bloques comparados: el mismo `except` con `raise` (A) y con `print` (B), y el dato de que mypy solo se queja en B. Ahí aisló el `raise`. Después se le puso el caso que discrimina *"return de error"* de *"salida sin valor"*: `t = Tokenizer("no_existe.json"); print(t)` dentro de un `except`. Dijo que `self._vocab` *"queda vacío"* y luego *"no sé"* → respuesta directa: **`NameError`, la asignación nunca ocurrió**. No hay un `Tokenizer` con vocabulario vacío: no hay `Tokenizer`. El tipo de retorno promete *"si devuelve algo, será un `Dict`"*; el `raise` es **otra puerta de salida** | Tipado |
| 2 | **Qué devuelve el patrón de pre-tokenización.** *"no sé en qué patrones los divide"* | Se **ejecutó** con su propio patrón: `findall("<\|im_start\|>user\nGreet<\|im_end\|>")` → `['<\|','im','_start','\|>','user','\n','Greet','<\|','im','_end','\|>']`. El especial despedazado en 4 trozos — que es justo por lo que el split de especiales va **antes**. Cuarta vez que ejecutar zanja lo que explicar no zanjaba | Pre-tokenización |
| 3 | **Bytes de `"JosÃ©".encode("utf-8")`.** Contestó **5**, y *"quiero 4"*. Son **7** y quiere **5**. **Segunda vez** (08-14 contestó 5 también) | Se le pidió **contar por carácter** (`J o s Ã ©`) y dijo *"1"* para todos. Se ejecutó carácter a carácter: `Ã` → `b'\xc3\x83'` y `©` → `b'\xc2\xa9'`, 2 bytes cada uno por estar fuera de ASCII; total 7, frente a los 5 de `"José"`. Corolario recordado: en `decode` cada carácter pasa por `_char_byte` y el byte va al `bytearray` | `str` / `bytes` |
| 4 | **Qué se rompe con `split(" ")` (parte a).** Saltó a la consecuencia (*"el acierto disminuye"*) en vez de a la mecánica, y añadió que *"los especiales no tienen id"* — que ya lo resuelve el otro patrón | Se le puso `"Greet shrek!\n\n"` con las dos salidas al lado (`['Greet','shrek!\n\n']` vs `['Greet',' shrek','!\n\n']`) y se preguntó qué le pasa al `!` y al espacio. Dijo *"no sé"* → respuesta directa: **el espacio se lo come el separador** (y `Ġshrek` es otra entrada del vocabulario, otro id), y **el `!` queda pegado**, así que el bucle puede fusionar `('k','!')` y producir símbolos que el modelo nunca vio | Pre-tokenización |

> [!success] Correcto sin ayuda
> **Los especiales no están en `vocab.json`** — *"solo se encuentran definidos en el archivo del tokenizer"*, a la primera. Era 🔴 y falló dos veces el 08-14 · **El split de especiales** — dio los 3 tramos exactos · **El bucle de merges corre por trozo** — *"corre 12 veces, una para cada trozo"*, y ante qué fusión sería posible con el texto pegado contestó **`40`**, el caso exacto. Era 🟡 y el 08-14 había dicho *"corre sobre todo"* · **Qué se cae con ids distintos: el acierto**, no el JSON válido · **Qué hace falta para testear la lista blanca: el vocabulario, y el modelo no** — *"lo que hace el modelo es predecir en base a vocabulario que yo le permito usar"*. Era 🔴 desde el 08-11.

> [!note] Fuera de guion
> Abolida la regla de meter `workflow/PSYCHOLOGY.md` en el `.gitignore` — decisión suya: *"ese archivo queda siempre dentro del proyecto"*. Borrada de `[[FIRST]]`, `[[PSYCHOLOGY]]` y los 4 sitios de `[[SYSTEM]]`, y anotada en `Posible mejoras al sistema.md` para aplicarla a la carpeta base al cerrar.

---

## Repaso 2026-08-14 — entrada de sesión, corrección de los 4 fallos del Bloque 1

> [!note] Lanzado en segundo lugar, no al abrir
> El orden lo había fijado él el 08-12: primero los 4 fallos, luego la hoja de evaluación, luego el repaso. Se arrancó por los fallos y **cortó él** para pedir el cuestionario primero.

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 1 | **Por qué no fiarse del mensaje de error del `except:` pelado.** Leyó el mensaje como verdadero y buscó razones por las que el archivo podría no existir: *"aún no tengo la ruta"*, *"que el archivo haya sido borrado post descarga"* | Se le congeló la escena: *"el archivo existe, se abre y se lee entero, y a mitad del `try` salta `raise ValueError("Merge board is empty")` — ¿qué mensaje sale por pantalla?"*. Contestó **"Merge board is empty"** — todavía mal. Lo que cerró: poner el `raise` y el `except` en el mismo bloque de código con una flecha, y preguntar **dónde cae** ese `ValueError`. Ahí lo vio: *"va a salir el raise, va a llevar al try y va a salir el filenotfounderror"* | Guards de lectura |
| 2 | **Por qué mypy no exige `Optional` si el método puede no devolver.** Dijo *"no sé"* directo | Se respondió directo, como manda la regla. **`raise` es una salida válida**: el tipo de retorno dice *"si esto devuelve algo, será `Dict[str, int]"*, no *"esto siempre devuelve"*. Por la rama del `except` no se sale de la función, así que mypy no tiene ahí ningún camino que revisar. **Segunda vez que se le enseña** — ya se le corrió `--strict` delante el 08-12 | Tipado |
| 3 | **La regla de pre-tokenización.** Ante `"<\|im_end\|>\n"` partido por Qwen en un solo trozo `'\|>\n'`, propuso un parche a posteriori: recorrer el resultado del split y pegar `[i] == "\|>"` con `[i+1] == "\n"` | Se le puso un caso que su parche no cubre: `"Greet shrek!\n\n"` → Qwen devuelve `'!\n\n'` de una pieza. Preguntado qué tienen en común los dos casos, dijo *"no tengo ni idea"* → se respondió directo con la rama del patrón, ` ?[^\s\p{L}\p{N}]+[\r\n]*`: **una tirada de símbolos que no son ni espacio ni letra ni dígito, y detrás todos los saltos de línea que vengan**. No es una excepción del `\|>`, es una regla general de puntuación | Pre-tokenización |

> [!success] Correcto sin ayuda
> **`"José"` da 5 símbolos antes de fusionar** — *"porque la e con acento son 2 bytes, son 4 caracteres 5 bytes"* · **Un `str` no se decodifica** — *"porque decode solo actúa sobre un byte array"*, sin rodeos y sin repetir el `.unicode` inventado del 08-12 · **Los números se parten dígito a dígito** — 2 pasos del bucle para escribir `40`.

> [!bug] Corolario que sigue sin verse — el de `.encode("utf-8")` sobre la string disfrazada
> Preguntado cuántos bytes da `"JosÃ©".encode("utf-8")`, contestó **5**. Son **7**: la `Ã` es el disfraz del byte 195, pero como carácter ella misma ocupa 2 bytes en UTF-8 (`b'\xc3\x83'`), y lo mismo la `©`.
> Se cerró **ejecutándolo** — carácter a carácter con su `.encode` al lado. Tercera vez que un `python3 -c` zanja algo que la explicación no zanjaba.
> Es lo que obliga a que `decode` vaya carácter → byte por `_char_byte` y acumule en un `bytearray`, en vez de decodificar la string entera.

> [!note] Fuera de guion — salió del propio repaso
> · **Puede o no usarse la librería `regex`.** Preguntó si el subject lo prohíbe. Se leyó el texto exacto del PDF (IV.3.1) y se le presentaron los tres caminos con su coste. **Decidió `regex`** — ver `[[PROJECT#Restricciones generales]]`.
> · **Un `dict` no se accede por índice.** Preguntó si se podía; se le respondió directo con el `KeyError` y con `list(vocab)[0]` como lo que cuesta hacerlo por posición.
> · **El `{}` de la línea 30 no llega vivo al guard** — creía que `vocab: Dict[str, int] = {}` hacía saltar el `if not vocab`. Lo pisa `json.load` dos líneas después; esa asignación solo sirve para poner el tipo.

---

## Repaso 2026-08-12 — entrada de sesión, Bloque 1 en construcción

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 1 | **Por qué un prompt por llamada:** dio tres razones ciertas pero secundarias — que el contexto se expandiría, que los errores se localizan mejor y que el contador de profundidad se lleva más fácil. La razón de fondo no apareció | Se le pegaron los 5 prompts en un solo texto y se le preguntó de cuál de los 5 era el token que sale de `argmax`. Reaccionó con *"¿pueden mezclarse las respuestas del modelo?"* — ahí estaba el hueco. **No se mezclan: solo hay una continuación**, la del último token de la secuencia; los otros 4 prompts quedan como contexto sucio. Cerró él: *"el modelo responde basado en el contexto, según el próximo token, que es lo más probable que siga"* | 1, 7 |
| 2 | **Tensor:** dijo que cada fila del tensor era *"un token id"*, y después preguntó si las filas eran los turnos (pregunta, respuesta, pregunta…) | Se pusieron **dos textos con nombre** (`texto_A`, `texto_B`) al lado de un tensor de dos filas y se le preguntó *"¿en qué fila quedó `texto_B`?"*. Contestó "segunda" y lo vio: **una fila = un texto entero**. Corregido además que la conversación completa va en **una sola fila** — lo que separa turnos son los tokens especiales (`<\|im_start\|>`), no las filas | 6, 8 |
| 3 | **De qué depende la lista blanca:** contestó *"del catch y de la máscara"*. La máscara es el resultado, no la causa | Dos congelados con el mismo texto y schema distinto (`{"a":` number vs `{"s":` string) → sacó **el schema**. Con el segundo par (`{"a":` vs `{"a": 40`, mismo schema) dijo *"no sé"* y se le dio directo: **el texto ya escrito**. El schema dice qué forma puede tener el valor; el texto, en qué parte de esa forma vas | 10 |

> [!success] Correcto sin ayuda
> **BPE byte-level** — con el emoji `🜛` nunca visto: *"no es el carácter lo que pasa, se pasa todo a bytes"* · **Tabla byte↔carácter** — byte 127 → 289, *"porque es el carácter invisible número 33 y la fórmula es 256 + 33"*. ==Dijo el puesto, no el byte==: primera vez limpio tras cuatro explicaciones fallidas el 08-11 · **Prioridad de merges** — `l o w` con `o w` en la línea 5 y `l o` en la 900 → `ow`, *"porque se hace por orden de prioridad y no de izquierda a derecha"*.

> [!note] Explicaciones dadas durante el repaso
> · **Batching**, a petición suya: entrada de 2 filas → salida de 2 filas de logits, cada fila procesada aislada. Y por qué no aplica aquí — `get_logits_from_input_ids` recibe **lista plana**.
> · **Paralelizar llamadas no es batching.** Propuso una función que reciba un batch y llame N veces a `get_logits_from_input_ids` en paralelo. Se le puso el caso límite: sin GPU, una sola pasada ya reparte el trabajo entre todos los núcleos — *"¿de dónde saca núcleos la segunda llamada?"*. Lo cerró con *"entiendo"*. Ya estaba descartado el 08-10 en `[[PROJECT#Responsabilidades sueltas]]`.
>
> Pidió él que las tres (prompt por llamada, tensor, batching) se anotaran para reforzar.

---

## Repaso 2026-08-11 — entrada de sesión, Bloque 1 en diseño

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 1 | Nombró **5 de los 6 bloques**: metió un *"parser"* que no existe y omitió el **Bloque 4 — Validez de tokens**. Al señalárselo, situó la máscara y la validez *dentro* del bucle de generación | Con `{"name": "fn_a` congelado llegó solo a que la lista blanca se calcula **sin logits** — solo con el texto escrito y el catálogo. De ahí salió la razón de que sea bloque propio: su test no carga el modelo | Bloques |
| 2 | Creía que los tokens existentes **salen de los logits**: *"sin logits no voy a saber qué tokens hay"* | Los tokens existentes salen del **vocabulario** (`{string: id}`, cargado al arrancar). Los logits solo **puntúan** ids ya conocidos. Lo cerró él al preguntarle de dónde saca el id de `dd_numbers` | 8, 10 |
| 3 | Propuso enmascarar todo menos el id de `dd_numbers`, **dando por hecho que esa pieza existe** en el vocabulario | Con el caso de un vocabulario que solo tiene `dd`, `_num`, `bers`, llegó solo: se recorre el vocabulario marcando las continuaciones válidas, nunca se supone una pieza concreta | 10 |
| 4 | **Cache de la lista blanca (bonus 4):** no supo qué va de clave y qué de valor. Volvió **tres veces** al `dict` invertido del tokenizer (`{id: str}`), que es otra cosa. Tampoco recordaba de qué depende la lista blanca | Se le dio directo tras decir *"no recuerdo"*: **clave = el texto ya escrito + el schema del campo**, **valor = la lista de ids permitidos**. Explicado después con los dos bloques de código (sin cache / con cache). Quedó *"medio claro"* — se difiere a Fase 2 por decisión suya | 4 (bonus) |

> [!success] Correcto sin ayuda
> **Decodificar byte a byte** — ==cuarta vez preguntado, primera vez limpio==: acumular todos los bytes y una sola llamada a `.decode("utf-8")` al final, con el caso de `José` · **Token vs carácter** — `dd_numbers` es **una vuelta** del bucle y **10 caracteres**, respondido sin dudar · `loads` / `dump` y por qué cada uno · **determinismo de greedy** — *"idéntica, el proceso es determinista y no probabilístico"* · **bucle de fusiones BPE** — `l o` → `lo`, luego la regla `lo w` → `low` · **tensor** — array de arrays de ids, y vio solo que con el bonus 2 su `encode` ya devuelve `list[int]`, así que el `tensor[0]` no le hace falta.

> [!note] Explicaciones dadas al terminar el repaso
> · **Tabla byte↔carácter**, pendiente desde el 2026-08-10 y pedida por él para después del cuestionario. Se dio completa (para qué existe, `chr()`, el desplazamiento `256 + n`, y las dos direcciones en `encode` y `decode`). El **algoritmo** de construcción se difirió a Fase 2 por decisión suya.
> · **Cache de la lista blanca**, con dos bloques de código comparados. Quedó *"medio claro"* → sigue en la lista de refuerzo.

---

## Repaso 2026-08-10 — Fase 0 completa, entrada a Fase 1

**Fallos:**

| # | Fallo | Corrección | Tema |
|---|---|---|---|
| 1 | Sabía que se manda **un prompt por llamada**, pero no la razón: la atribuyó al procesamiento de la respuesta. Ante el caso de 5 objetos con uno repetido y otro sin responder, dijo *"no sé"* | La razón no es el formato — es la **correspondencia prompt↔resultado**. La máscara garantiza estructura (JSON válido, nombres y tipos del schema); que el objeto 3 responda al prompt 3 es **semántica** y no se puede enmascarar. Con un prompt por llamada la correspondencia la garantiza el bucle: un prompt, un resultado, mismo índice | 1, 10 |
| 2 | Dijo **"carácter"** en vez de **token**, dos veces seguidas | Un logit por **entrada del vocabulario**, no por letra. Hay entradas multicarácter (`name`, `{"`, `dd_numbers`): un solo token puede añadir 10 caracteres de golpe. Confundirlos rompe el diseño de la máscara, que compara **strings de token** | 6, 8 |
| 3 | Del bucle al archivo saltó de `decode` directo a `json.dump`. No recordaba qué hace `json.loads` | `decode` devuelve un **string**; pydantic valida un **dict**. Orden real: `decode` → `json.loads` → `dict` → pydantic → guardar en la lista de los N → **un solo** `json.dump` del array al final. Un `dump` sobre el string escribe el JSON escapado entre comillas | 5 |
| 4 | `while deep_counter > 0` con el contador a 0 antes de generar — el bucle no entra nunca | Lo resolvió él: primera llamada **fuera** del `while`, el resto dentro. Antes había propuesto inicializar el contador al número de llaves esperado por función; se descartó al ver que el nombre de la función aún no está escrito cuando toca inicializar | — |
| 5 | Creía que las rutas de los archivos de entrada eran fijas | Salen de `argparse`, con `data/input/` y `data/output/` como defaults. El corrector puede pasar cualquier ruta | 4 |
| 6 | No sabía quién convierte `functions_definition.json` (dict) en el texto que recibe `encode` | Lo hace **tu programa**: es una responsabilidad propia. El SDK solo tokeniza lo que le des. El formato exacto sigue abierto en `[[PROJECT#A analizar en esta fase]]` | 1 |

> [!success] Correcto sin ayuda
> El texto que entra a `encode` (prompt + funciones, después ids acumulados sin re-encodear) · los ~150.000 logits y qué puntúan · la lista blanca por **prefijo** en `{"name": "fn_a` · el contador de profundidad y su valor exacto (1) en `..."b": 2}` · el corte `input_ids[len(prompt_ids):]` antes de `decode` · el bonus 7 necesita **pila (PDA)**, no basta un FSM.
