---
tipo: perfil
estudiante: 
skill: psychologist-analyst
creado: 2026-08-04
ultima_actualizacion: 2026-08-07
tags: [42, psicologia, desempeno, motivacion]
---

# PSYCHOLOGY.md

> [!important] Viaja con el proyecto, vuelve a la base
> Este archivo **no pertenece a ningún proyecto**: pertenece al estudiante y sobrevive a todos ellos. Pero se trabaja dentro del proyecto activo.
>
> | Momento | Dónde se trabaja |
> |---|---|
> | Al abrir un proyecto | Se copia de la base a `workflow/PSYCHOLOGY.md` |
> | Durante el proyecto | **Solo se toca la copia de `workflow/`** |
> | Al cerrar el proyecto | La copia **sustituye** a la de la carpeta base |
>
> **Carpeta base:** `~/Documents/system_development/` — en Finder, iCloud Drive → Documentos → system_development

> [!warning] Nunca dos versiones vivas
> Durante un proyecto, la de la base espera sin tocarse. Si un agente encuentra las dos, la buena es **la de `workflow/`** del proyecto activo.
> Si dos proyectos corrieran a la vez, el segundo cierre pisaría al primero: ver `[[SYSTEM#La carpeta workflow]]`.

> [!warning] No se sube al repositorio
> `workflow/PSYCHOLOGY.md` va al `.gitignore` del proyecto desde el primer commit. Es personal.

> [!important] Para qué existe este archivo
> **Mejorar el desempeño y la motivación del estudiante.**
> No es un diario ni un diagnóstico clínico. Es un perfil operativo: le dice al agente cómo enseñarle mejor a *esta* persona concreta, para que cada relevo no empiece de cero.

> [!warning] Es del estudiante
> Puede leerlo, corregirlo o borrar lo que no comparta, cuando quiera. Nada se registra a sus espaldas.

---

## Cómo se rellena

> [!tip] Herramienta
> Se usa la skill **`psychologist-analyst`** (instalada en `~/.claude/skills/psychologist-analyst`).
> Aporta marcos reales de psicología cognitiva, motivacional y del aprendizaje. Las anotaciones se apoyan en esos marcos, no en impresiones sueltas.

> [!important] Se actualiza conforme sea necesario
> **No espera a hitos.** En cuanto se observa algo que cambia cómo hay que enseñar, se escribe. Una observación no anotada se pierde con el agente: ante la duda, se anota.
> La actualización es silenciosa — no se anuncia ni corta el trabajo.

**Anotar es continuo; concluir no.**

| Acción | Cuándo |
|---|---|
| Apuntar en la **bitácora** ↓ | En cuanto ocurre |
| Subir a **fortaleza / debilidad / patrón** | Tras verlo **tres veces** |

Una vez es azar, dos es coincidencia, tres es patrón.

Cada entrada lleva la **observación real** que la originó, con fecha. Sin la escena concreta, la afirmación no se puede verificar ni corregir.

Si un patrón deja de cumplirse → se corrige o se borra. Un perfil desactualizado hace más daño que ninguno.

---

## 💪 Fortalezas

> [!success] Formato
> **Fortaleza** — cómo aprovecharla
> *Observado: [fecha] — [qué pasó exactamente]*

**Corrige su propio diseño cuando ve el caso límite** — no hace falta explicarle por qué algo está mal; basta con ponerle delante el peor caso concreto y llega solo a la alternativa buena. Aprovecharla: nunca dar la corrección, dar el caso.
*Observado: 2026-08-06 — partiendo de un `for` sobre 150.000 logits con lista negra, llegó a la lista blanca en 3 turnos con solo el caso `{"name": ` admite únicamente `"`.*
*Observado: 2026-08-07 — con `{"name": "fn_a` congelado, dedujo que el token `dd_numbers` también entra en la lista blanca.*
*Observado: 2026-08-07 — con `{"a": 40` delante, vio solo que faltaba la `,` al preguntarle si `40` ya era un número completo.*

**Dice cuándo llegó a su límite, en vez de improvisar** — responde *"no sé"*, *"no entendí la pregunta"* o *"no entendí nada"* sin rodeos. Aprovecharla: fiarse de que si no lo dice, lo entendió; y reformular de inmediato cuando lo dice, sin insistir con la misma forma.
*Observado: 2026-08-06 — "no sé nada más" al final del recorrido del flujo.*
*Observado: 2026-08-07 — "no entendí la pregunta" ante una pregunta abstracta sobre tokens y caracteres; con dos líneas comparadas contestó bien al primer intento.*
*Observado: 2026-08-07 — "no entendí nada" ante la contradicción del subject explicada con tres números de línea; al reducirlo a los dos nombres de archivo, lo pilló.*

---

## 🔧 Debilidades

> [!warning] Formato
> **Debilidad** — cómo compensarla
> *Observado: [fecha] — [qué pasó exactamente]*

*(vacío)*

---

## 🎓 Cómo aprende mejor

Qué formatos, ritmos y tipos de explicación le funcionan.

| Funciona | No funciona |
|---|---|
|  |  |

---

## 🧩 Cómo razona

Cómo aborda un problema nuevo. Dónde se atasca y con qué se desatasca.

*(vacío)*

---

## 🔥 Motivación

| Qué la levanta | Qué la hunde | Cómo se recupera tras un bloqueo |
|---|---|---|
|  |  |  |

---

## ⚠️ Dificultades de aprendizaje

Patrones concretos observados, con su ejemplo real.

*(vacío)*

---

## 📋 Instrucciones para el próximo agente

Lo más importante del archivo: qué hacer y qué evitar, en directo.

### Hacer

- **Respuestas cortas.** Pidió explícitamente menos verborrea (2026-08-06). Una idea y una pregunta por mensaje. Nada de repasos largos ni de recontextualizar lo que ya sabe. Anotado también en `[[FIRST]]`.
- **Dejarle explicar el flujo entero en voz alta, por pasos**, con la tabla de referencia delante y confirmación tras cada paso. Es su método y lo pide él: *"dame la tabla y voy a intentar explicarlo de nuevo"*, *"lo hacemos por pasos"*.
- **Cuando su diseño es ineficiente, darle el peor caso concreto** en vez de explicarle por qué está mal. Con el caso límite delante corrige solo.
- **Una pregunta a la vez.** Lo ha pedido dos veces (2026-08-04, 2026-08-05). Con una sola pregunta aislada responde bien.
- **Explicar y preguntar con escenas del propio proyecto**, congelando un momento concreto ("la generación está parada justo aquí, ¿qué puede venir ahora?"). Es lo único que lo desbloqueó cuando dijo estar perdido.
- **Recorrer las cosas en orden de ejecución**, desde el punto 0, sin saltarse pasos intermedios.
- **Preguntarle si da un tema por cerrado**, aunque las respuestas hayan sido correctas.
- **Cuando pregunte "¿te parece que ya lo domino?", responder con criterio honesto**, nombrando el hueco concreto si lo hay. Lo pregunta para decidir, no para que lo animen: con un hueco señalado sigue trabajando, y sin él cierra y avanza.
- **Antes de dar un tema por recorrido, comprobarlo con un caso límite**, no con un resumen. Congelar un momento de la generación y preguntar qué pasa ahí saca los huecos que una explicación correcta esconde.
- **Decir siempre qué escribe él y qué ya existe en el lenguaje.** Cuando aparezca una función, marcar explícitamente si es suya, de la librería estándar o del SDK. Lo pidió él (2026-08-10): al explicarle `decode`, confundió **su** `decode` (ids → texto) con `bytes.decode("utf-8")` de Python, y dijo *"si no me explicabas que era una función aparte, puede que no lo supiera nunca"*. Con los bonus 2 y 8 dentro, esa frontera se cruza todo el rato: reimplementa cosas que también existen ya, y sin la marca no sabe cuál toca escribir.
- **Refuerzo diferido:** si dice que entendió algo a medias y pide retomarlo más adelante, no insistir en el momento — anotarlo en `[[PROJECT#🎯 Lista de refuerzo]]` y **traerlo de vuelta cuando el concepto aparezca en el código**, sin esperar a que lo pida. Patrón confirmado tres veces (2026-08-07, 2026-08-11 ×2). Corolario: **si un tema ya está diferido, no lo re-expliques**. El 2026-08-11 se insistió con el algoritmo de la tabla de bytes, marcado ⏸️, y lo que desbloqueó fue parar y decirlo en voz alta.
- **Cuando una explicación falla dos veces, deja de explicar y hazle contar.** Con la tabla byte↔carácter fallaron cuatro intentos (tabla, traza, código) y funcionó a la primera preguntarle qué puesto ocupaba un elemento concreto en una fila escrita delante. Convertir la idea en una operación que él ejecuta, no en una descripción que él escucha.
- **Cuando el error es sobre qué hace una función, ejecútala en vez de argumentar.** Un `python3 -c` con la salida real cierra la discusión en un mensaje; explicárselo no. Confirmado dos veces el 2026-08-12: defendió `"JosÃ©".unicode("utf-8")` hasta ver `hasattr → False`, y sostuvo que mypy exigía `Optional` hasta ver `mypy --strict` pasando sin él. **No es terquedad: es que su modelo de la función compite con tu afirmación, y la ejecución no compite, zanja.**
- **Elegir el caso de prueba donde la regla equivocada falle.** Preguntando por la tabla de bytes con el espacio (byte 32), su regla errónea daba el resultado correcto por casualidad y el fallo quedaba invisible. Con el byte 127 saltaba. Vale como criterio general: el ejemplo tiene que **discriminar**, no solo ilustrar.

### Evitar

- **Amontonar corrección + varias preguntas en un mismo mensaje.** Corta y pide ir por partes.
- **Preguntas abstractas sin anclaje** ("¿de dónde sale esa información?" en el aire). Ahí se pierde.
- **Cerrar un tema por tu cuenta** porque las respuestas fueron correctas.

---

## 🗓️ Registro de observaciones

> [!note] Bitácora
> Observaciones sueltas todavía sin patrón. Cuando una se repite tres veces, sube a la sección que le corresponda.

| Fecha | Situación | Qué se observó |
|---|---|---|
| 2026-08-04 | Filtrado del mapa de temas de Fase 0 | Pidió dividir la revisión en secciones pequeñas (máx. 4 temas) con aprobación sí/no explícita por ítem, en vez de aprobar la lista completa de una vez |
| 2026-08-05 | Cuestionario, Tema 1 (function calling) | Al recibir corrección + 3 preguntas de golpe, cortó y dijo *"vamos por partes"*, aislando una sola pregunta. Segunda vez que pide trocear (ver 2026-08-04) — con una sola pregunta a la vez, responde bien |
| 2026-08-05 | Cuestionario, Tema 1 — pregunta sobre el constrained decoder | Dijo *"no sé, me estoy perdiendo un poco"* ante una pregunta abstracta. Con una escena concreta (la generación congelada en `{"name": "` y qué puede ir ahí) llegó solo a la respuesta en dos turnos. Las preguntas abstractas lo bloquean; las escenas del propio dominio lo desbloquean |
| 2026-08-05 | Cierre de Tema 1 | Con las respuestas ya correctas, **rechazó cerrar el tema**: pidió profundizar en flujo y mecánica antes de avanzar. No busca aprobar el check, busca internalizar. No dar un tema por cerrado solo porque las respuestas sean correctas — preguntarle a él |
| 2026-08-06 | Retomar el Tema 1 tras días sin sesión | No pudo reconstruir dónde se había quedado: pidió las preguntas exactas del agente anterior y no estaban registradas. Al retomar, **"punto 0"** significaba para él el flujo **teórico**, no el arranque técnico del programa (`uv run`) — *"los comandos aún ni los he visto"*. Los conceptos van antes que las herramientas |
| 2026-08-06 | Explicaciones largas del agente | Pidió explícitamente **menos verborrea**: respuestas cortas, una idea y una pregunta por mensaje. Se anotó en `[[FIRST]]`. Tercera señal de trocear (2026-08-04, 2026-08-05) — ya es patrón |
| 2026-08-06 | Tema 9 (`numpy`) | Partiendo de un `for` con `if in forbidden`, llegó **solo** a la lista blanca en 3 turnos, sin que se le diera la respuesta. Lo que funcionó: ponerle el **peor caso concreto** (en `{"name": ` solo vale `"` y el modelo quiere escribir `Sure`) en vez de explicarle el coste. Con un caso límite real, corrige su propio diseño |
| 2026-08-06 | Cuando el agente saca un tema que no toca | Preguntó *"no entiendo por qué lo traes"* ante el formato del prompt — que es decisión de Fase 1, no de comprensión. Detecta cuándo algo está fuera de fase; si el agente arrastra un pendiente heredado sin justificar por qué, lo corta |
| 2026-08-06 | Recorrido del flujo completo | Su método propio: *"dame la tabla y voy a intentar explicarlo de nuevo"* y *"lo hacemos por pasos"*. Reconstruye explicando en voz alta paso a paso, con la referencia delante y validación tras cada paso. Con ese formato encadenó el flujo entero y absorbió 7 correcciones sin bloquearse. Cuando llega al límite lo dice claro (*"no sé nada más"*) en vez de improvisar |
| 2026-08-07 | Ritmo de la sesión | Cerró **9 temas en una sola sesión**, cuando en las tres anteriores no había cerrado ninguno. Lo que cambió: el flujo completo ya estaba internalizado, así que cada tema nuevo tenía dónde engancharse. El cuello de botella no era la cantidad de temas, era tener el mapa del proyecto en la cabeza |
| 2026-08-07 | Uso del agente como calibrador | Preguntó siete veces alguna variante de *"¿te parece que ya lo domino o falta algo?"* antes de cerrar cada tema. No busca aprobación: usa la respuesta para decidir. Cuando se le dijo que faltaba algo, siguió; cuando se le dijo que era suficiente, cerró. Hay que responder con criterio honesto, no con ánimo |
| 2026-08-07 | Refuerzo diferido | Ante un mecanismo que entendió a medias (imports relativos) pidió explícitamente: *"quiero que se refuerce en el momento en el que se toque en una fase futura"*. No quiere repetirlo en frío ahora; quiere el recordatorio cuando el concepto aparezca de verdad en el código. Aprendizaje *just-in-time*, decidido por él |
| 2026-08-07 | Trae material propio | Descargó el `llm_sdk` por su cuenta y llegó con `get_path_to_merges_file()` justo cuando el agente había marcado esa duda como abierta. Lee el código fuente sin que se lo pidan |
| 2026-08-07 | Repaso del flujo + Tema 8 | Reconstruyó el flujo entero de memoria con solo 3 fallos. Ante la pregunta abstracta *"¿lo que cuentas son tokens o caracteres?"* respondió *"no entendí la pregunta"*; con las dos opciones puestas como dos líneas de texto comparadas, contestó bien al primer intento. Cuarta confirmación del patrón: pregunta abstracta bloquea, comparación concreta desbloquea |
| 2026-08-07 | Diccionario de vocabulario | Dijo *"no sé"* sin dar rodeos al preguntarle cómo cargar el diccionario. Se le dio la respuesta directa (era detalle, no concepto) y aun así respondió *"no entendí bien eso"*: le faltaba el **porqué** del coste. Con el bucle por valor escrito al lado del acceso por clave, cerró solo: *"pensé que la llave era id: carácter, es al contrario, de esa manera es O(1)"*. No le basta la regla — necesita ver el coste de la alternativa mala |
| 2026-08-07 | Tema 5 (JSON) | Ante una pregunta sobre manejo de excepciones cortó con *"pero eso es parte de otra fase, ¿no crees? el planear el código y poner los guards"*. Tenía razón: **dónde** van los guards es Fase 1, de Fase 0 solo hace falta saber qué excepciones existen. Segunda vez que detecta que el agente se sale de fase (ver 2026-08-06, formato del prompt). Vigilar si llega a tres — sería patrón, no anécdota |
| 2026-08-10 | Volcado de la lista de responsabilidades | El agente escribió el bonus 3 con un mecanismo concreto ("reformular el prompt o inyectar el error, con límite de reintentos") que había salido en la conversación pero **no se había decidido**. Lo cortó: *"no decidimos nada aún con respecto al sistema de recuperación"*. **Tercera vez** que detecta al agente saliéndose de su sitio (2026-08-06 formato del prompt, 2026-08-07 guards de Fase 1) — ya es patrón: distingue entre *lo que se habló* y *lo que se decidió*, y no acepta que el registro los confunda |
| 2026-08-10 | Repaso de inicio de sesión | Pidió que el cuestionario de repaso se institucionalice: al abrir cada sesión, con **histórico registrado en `PROJECT.md`** para que el agente vea sus fallos anteriores y enfoque en *"lo último y lo que he fallado y aún no logro controlar"*. No quiere solo repasar: quiere que el sistema recuerde por él qué no domina |
| 2026-08-10 | Diseño del Bloque 1 | Pidió parar la explicación y que se le describiera **qué es un tensor** antes de seguir con el algoritmo. Después preguntó *"¿por qué es que te pregunté qué era un tensor?"* — no había perdido el hilo, estaba comprobando que la pieza encajaba donde tocaba. Cuando pide una definición a mitad de un diseño, no es una digresión: está cerrando un hueco que le impide seguir |
| 2026-08-10 | Diseño del Bloque 1 — clase `Chat` | Ante la objeción de que una clase que lo construye todo dentro no se puede testear, dijo tres veces seguidas *"no entiendo"* / *"estás hablando muy enredado"*. Lo que lo desbloqueó **no fue una explicación mejor**: fue que él mismo reformulara con una analogía propia (piezas de un carro, probar el motor aparte). Cuando se atasca en una idea abstracta, dejarle construir su propia analogía en vez de dar otra vuelta a la explicación |
| 2026-08-11 | Cuestionario de repaso | Cortó para pedir contexto en las preguntas: *"me parece que tus preguntas no están muy bien formuladas… soy un humano que necesita contexto algunas veces. cuando dice probar no entiendo a qué quieres que pruebe"*. La pregunta usaba un verbo (*probar*) sin decir en qué escenario — test de `pytest`, Fase 2. Con el escenario nombrado, contestó bien. **No es falta de concepto: es falta de encuadre.** Toda pregunta tiene que decir en qué momento del proyecto ocurre |
| 2026-08-11 | Cuestionario de repaso | Dijo *"no entendí"* / *"sigo sin entender"* dos veces seguidas sobre lo mismo (por qué el Bloque 4 se testea aparte). Lo que lo desbloqueó fue **poner los dos casos como dos bloques de código comentados**, uno al lado del otro. Se repitió idéntico con el cache. Quinta confirmación del patrón: prosa explicativa bloquea, dos bloques de código comparados desbloquean |
| 2026-08-11 | Refuerzo diferido, segunda vez | Ante dos temas que quedaron a medias (tabla byte↔carácter y cache de la lista blanca) preguntó él mismo *"¿conviene dejarlo para reforzar al momento de la construcción?"*. Ya no hay que ofrecerle el aplazamiento: **lo pide él y distingue solo qué es concepto de diseño y qué es detalle de implementación**. Segunda vez (ver 2026-08-07) |
| 2026-08-11 | Tabla byte↔carácter | Cuatro explicaciones seguidas fallaron —tabla comparativa, traza byte a byte, código— con *"no entiendo"*, *"no entendí nada"*, *"no entendí ni papa"*. Lo que funcionó a la primera fue **pedirle que contara**: puestos los invisibles en fila (`0…32, 127…`), a la pregunta *"¿qué puesto ocupa el 127?"* respondió 33 sin dudar. No es que el concepto le supere: es que **explicar una posición no es lo mismo que hacerle contarla** |
| 2026-08-11 | Pide código y luego lo rechaza | Dijo *"no me des el maldito código, ya te lo he dicho"* y minutos después *"dame el código de los conjuntos, ya lo entendí, es más fácil para mí verificarlo viéndolo"*. No es contradicción: rechaza el código que le **quita el ejercicio**, y pide el que le sirve de **verificación de algo ya entendido**. Distinguir por ahí — si aún no lo entiende, no dárselo; si ya lo razonó y quiere confirmarlo, dárselo |
| 2026-08-11 | Gestión del contexto y del sistema | Preguntó si un subagente con caveman gasta más o menos tokens, y sin que se lo dijeran señaló que el agente no estaba usando caveman en ejecución pese a que `[[SYSTEM]]` lo pide. Al proponerle remedios eligió **los dos** (regla escrita + hook) y añadió por su cuenta que la regla debía obligar a **verificar y crear el hook si falta**. Piensa en que el sistema sobreviva a la máquina y al agente concretos |
| 2026-08-11 | Reconoce cuándo diferir | Ante dos temas a medias preguntó él mismo *"¿conviene dejarlo para reforzar al momento de la construcción?"*. **Tercera vez** que aparece el refuerzo diferido (2026-08-07, 2026-08-11 ×2) — ya es patrón: separa solo lo que es concepto de diseño de lo que es detalle de implementación, y aplaza lo segundo sin perderlo |
| 2026-08-12 | Pre-tokenización, negativa a postergar | Ante un tema que se podía aplazar (cómo parte Qwen el texto antes de BPE) dijo *"si postergamos este tema, nos lo vamos a encontrar más adelante y nos va a dejar un tema muy complicado a revisar"* y pidió que el agente lo investigara. **Contrasta con su patrón de refuerzo diferido**: no aplaza todo por igual — aplaza lo que es *detalle de implementación* y bloquea lo que es *decisión estructural*. Distingue bien las dos cosas |
| 2026-08-12 | Su idea de partir el texto, tres rondas | Propuso `split()` → se le puso la plantilla de chat y vio que los `\n` desaparecían. Propuso `split(" ")` + reañadir espacios → **tenía razón, era reversible**, y se le dijo. Propuso una cascada de cortes → se le puso el trozo `'\|>\n'` y vio que su primer corte lo rompía. **Tres iteraciones sin frustrarse**, cada una mejor que la anterior. El formato que funcionó las tres veces fue el mismo: un trozo de salida real puesto delante, y una pregunta de una línea |
| 2026-08-12 | Gestión del riesgo del bonus 2 | Propuso él solo el plan B: implementar `encode`/`decode` propios, medir, y si el acierto cae, usar los del SDK — *"son solo dos métodos y luego es solo cambiar la clase de la que vienen"*. **Está cobrando la costura que diseñó en Fase 1** sin que nadie se lo recuerde. Y acotó el esfuerzo por su cuenta: *"sin demasiado trabajo que nos comprometa a seguir y perder semanas ahí"* |
| 2026-08-12 | Pregunta el porqué de un número del subject | Ante el objetivo del 90% preguntó *"¿un porcentaje de cuántos? porque si es 1, falla y 0%"*. Detectó solo que el subject da un porcentaje sin fijar N. **No acepta una métrica sin saber sobre qué se calcula** — de ahí salió que traiga la hoja de evaluación antes de seguir |
| 2026-08-12 | Confusión `str` / `bytes` | Escribió `"JosÃ©".unicode("utf-8")` y lo defendió (*"¿no leíste que la paso por…?"*). No cedió ante la explicación; cedió ante la **ejecución**: `hasattr(s,'unicode') → False` y los 7 bytes frente a los 5 correctos. Con este tipo de error —creencia sobre qué hace una función— **correr el código es más rápido que argumentar**. Segunda vez en la sesión que un `python3 -c` cierra una discusión (la otra, mypy con `raise`) |
| 2026-08-05 | Orden del cuestionario | Pidió recorrer los temas en **orden de ejecución del programa**, no por importancia: *"primero tengo que entender cómo funciona la puerta y cómo se abre antes de entrar a entender la sala"*. Necesita la secuencia real completa, sin saltos, para construir el modelo mental |
