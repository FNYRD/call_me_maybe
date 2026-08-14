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
