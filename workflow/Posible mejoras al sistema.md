# Posible mejoras al sistema

Backlog de propuestas de mejora al sistema de trabajo (`SYSTEM.md`, `PROJECT.md`, `HANDOFF.md`, `PSYCHOLOGY.md`).

## Propósito

Aquí se anota cualquier idea de mejora al método de trabajo que surja mientras se trabaja en un proyecto, sin interrumpir el proyecto en curso.

## Reglas de uso

- **Analizar primero, decidir después.** Ninguna propuesta se aplica en caliente: se evalúa al finalizar el proyecto actual.
- Una propuesta por ítem, en checklist (`- [ ]`), redactada como regla y no como tarea.
- Al anotarla, indicar de qué proyecto vino y la fecha.
- Cuando una propuesta se adopta, su contenido pasa al archivo de destino (`SYSTEM.md`, `PROJECT.md`, etc.) y deja de vivir aquí: este archivo no es registro histórico de lo ya implementado.
- Una propuesta que queda sin sentido se marca obsoleta con la razón, o se elimina.

## Propuestas

- [ ] **`[[FIRST]]` termina siempre con una `Instrucción para el próximo agente`: dónde quedamos y por dónde empezar.** La escribe el agente saliente en el protocolo de cierre, **fechada**, y sustituye a la de la sesión anterior — no se acumula.
  **Tres callouts fijos, siempre los mismos:**
    1. ==**Dónde quedamos**== — el punto **exacto** donde se cortó: archivo, clase, método, y qué falta dentro de él. No *"se avanzó en el Bloque 4"*, sino *"`_char_ok`, con solo la rama `"name"` y sin la regla de la comilla"*. Aquí entra también lo **decidido y no escrito**, que es lo que más fácil se pierde.
    2. ==**Por dónde empezar**== — los pasos numerados de la sesión siguiente, en orden, con el primero siendo casi siempre el cuestionario.
    3. ==**Cómo se trabaja ahora mismo**== — el modo en curso, si no es el de siempre: si se está en el tiempo (3) de un `code mockup`, ahí va escrito que se conduce un paso por mensaje y se verifica ejecutando. Un agente nuevo no puede deducir el modo del estado del proyecto.
  Y un cuarto opcional, **con lo que se va a tropezar**: herramientas rotas, comandos que hay que llamar de una forma concreta, cosas que no se re-ofrecen.

  **Por qué en `[[FIRST]]` y no en `[[HANDOFF]]`.** No sustituye al briefing: lo **destila**. `[[HANDOFF]]` guarda el *por qué* —qué se probó, qué se descartó, qué falló— y crece sin parar; esto son las tres cosas que el agente necesita para dar el primer paso, en el primer archivo que abre y sin haber leído nada más. Cuando el briefing y esta instrucción se contradigan, manda el briefing, que es más detallado.

  **Motivo:** el bloque `Dónde estamos ahora` de `[[FIRST]]` describe un **estado**, no una **orden**. Un agente que lo lee sabe en qué punto está el proyecto pero no qué hacer con eso, y arranca improvisando o preguntando algo que ya estaba escrito. La diferencia se ve en el modo de trabajo: nada en el estado del repositorio dice que el Bloque 4 se está escribiendo con acompañamiento paso a paso — si no está ordenado explícitamente, el agente entrante vuelve al modo por defecto y rompe la mecánica a mitad de bloque.
  **A resolver al evaluarla:** (a) si el bloque `Dónde estamos ahora` se mantiene aparte o se fusiona dentro de esta instrucción, que solapan; (b) que no se convierta en un segundo briefing — el límite son las tres cosas que hacen falta para el **primer** paso.
  *(call me maybe, 2026-08-27 — petición explícita del estudiante · aplicada ya en este proyecto: `FIRST.md`, cierre del 2026-08-27)*
- [ ] **`code mockup` — la fase que va del bloque diseñado al código escrito, en tres tiempos: desmenuzar, documentar, acompañar.** No es un documento: es una **fase de trabajo con nombre**, y el PDF es solo la bisagra entre el segundo tiempo y el tercero.
  **Cuándo entra:** cuando el proyecto ya está partido en bloques y toca abordar **uno**. Va entre tener el bloque definido y tener el bloque escrito.
  **Cómo se dispara:** lo dice el estudiante — *"code mockup del Bloque N"*.

  ### (1) Desmenuzar — la conversación de diseño

  Agente y estudiante recorren la solución del bloque hasta el fondo, con el método que ya funciona: **una idea y una pregunta por mensaje** · escenas **congeladas del propio proyecto** · un fallo **no se corrige dando la respuesta**, se pone el caso límite que lo tumba · lo que el estudiante propone se discute, nunca se sustituye.
  **Termina cuando no queda ningún hueco.** Un hueco es cualquier punto donde, puesto a teclear, el estudiante tendría que parar a preguntar *"¿y aquí qué va?"*. Lo que quede abierto a propósito —diferido, o que solo se resuelve midiendo— se **nombra como tal**.

  ### (2) Documentar — el PDF, generado automáticamente al cerrar (1)

  El agente vuelca lo decidido a `[[PROJECT]]` **y genera el PDF**.

  > [!important] Dónde vive y cómo se llama
  > Carpeta ==**`block_mockup/`**== en la raíz del proyecto, junto a `src/` — **no** en `workflow/`: es herramienta de construcción, no archivo del sistema.
  > Un PDF por bloque, **nombrado con el bloque al que sirve**: `block_mockup/bloque_4_guardian.pdf`. Así se acumulan en orden y se ve de un vistazo qué bloques tienen mockup y cuáles no.
  > `[[PROJECT]]` enlaza al suyo en el campo *Dónde vive* de cada bloque.

  > [!important] ==Cero pendientes antes de entrar al tiempo (3)==
  > **No se empieza a escribir código con nada abierto.** Esa es la puerta: el tiempo (3) no arranca —ni un solo paso— mientras quede una decisión sin tomar. Pensar, quitar, poner, suponer y resolver era el tiempo (1); a partir de la puerta solo se teclea, se verifica y se corrige lo que uno mismo escribió mal.
  > **Si el agente encuentra un hueco al redactar la guía, vuelve con el estudiante y se cierra entre los dos**, antes de cruzar la puerta. ==No lo decide el agente por su cuenta, y tampoco lo deja anotado como pendiente.== Un hueco encontrado al documentar significa que el tiempo (1) no había terminado: **se vuelve al (1)** el rato que haga falta, se cierra, y entonces sí se sigue.
  > **Motivo:** el diseño es del estudiante, y una decisión tomada por el agente para no interrumpir es una decisión que él no sostiene — la descubre tecleando y tiene que pararse a entenderla, que es justo lo que la guía viene a evitar.

  **Estructura:** ==**una sección por método**==, en el orden en que conviene escribirlos, y en cada una: **firma** completa · **qué recibe** · **qué devuelve** · **pasos** numerados. Al final, un **recorrido completo** paso a paso con un caso real, marcando en cada línea quién escribe —el código o el modelo— y una tabla de **lo que es de otro bloque**, para que no se busque ahí.

  **Reglas de escritura:**
    - ==**Sin código de implementación.**== El código lo escribe el estudiante: los pasos se redactan en lenguaje natural preciso. Sí entran **firmas**, **datos** y **estados congelados**, que no son escribir su código sino ponerle el caso delante.
    - ==**Identificadores en inglés, descripciones en español.**== Nombres de métodos, atributos, parámetros y tipos, tal como van a quedar en el `.py`.
    - **Sin verborrea.** Nada de alegorías, motivaciones ni secciones de *por qué importa*: eso era del tiempo (1). Tablas y pasos.
    - **Cada afirmación lleva su grado de certeza** — dato del subject, verificado en ejecución, convención, o suposición del agente.

  ### (3) Acompañar — el agente guía la escritura, método a método

  Con el PDF hecho, **el agente conduce**, y así es como se trabaja de aquí en adelante:

  1. **El agente dice el siguiente paso, uno solo**, con el contexto que hace falta para ejecutarlo. Nunca dos pasos, nunca el método entero de golpe.
  2. **El estudiante lo escribe** y avisa (*"ya"*, *"done"*).
  3. ==**El agente lo verifica ejecutándolo, no leyéndolo.**== Abre el archivo, corre el trozo con datos reales del proyecto y enseña **la salida**. Un fallo se demuestra con lo que imprime, no se argumenta.
  4. **Si falla, se señala un solo fallo**, el que bloquea — y por orden: lógica primero; estilo y guards se anotan y esperan su pasada.
  5. **Si el estudiante pregunta por una variable o un mecanismo, se le contesta ahí mismo**, sin remitirlo al PDF: en el tiempo (3) no está leyendo el documento, está tecleando.

  > [!warning] El agente sigue sin escribir el código
  > Ni siquiera cuando el paso es de una línea y va lento. Lo que aporta el acompañamiento es **el orden y la verificación inmediata**, no la escritura.

  > [!tip] Lo que hace que funcione
  > El estudiante no sostiene el plan en la cabeza —está en el PDF— ni tiene que parar a preguntar qué venía después —lo dice el agente—, así que todo su esfuerzo va a **traducir un paso concreto a código**, que es exactamente donde está su hueco registrado en `[[PSYCHOLOGY]]` (2026-08-17): *el diseño lo tiene antes de escribir; lo que se le va es la traducción a código*.

  **Motivo:** un bloque se desmenuza en decenas de mensajes y al día siguiente hay que reconstruir el orden preguntando *"¿qué venía después?"*. `[[PROJECT]]` guarda el **qué** y el **porqué**; el code mockup guarda el **en qué orden**, y el tiempo (3) convierte ese orden en código sin que el estudiante tenga que sostenerlo. Y quien escribe la guía es quien acaba de tener la conversación entera en la cabeza — el mismo argumento que sostiene el cuestionario escrito al cerrar.
  **A resolver al evaluarla:** (a) el límite de "sin código" — la prueba es que los pasos no deben poder teclearse tal cual; (b) qué se hace si el diseño cambia durante el tiempo (3): regenerar el PDF o corregir `[[PROJECT]]` y marcarlo desactualizado; (c) dónde vive la regla — final de `[[SYSTEM#FASE 1 — DISEÑO]]` o principio de `[[SYSTEM#FASE 2 — IMPLEMENTACIÓN]]`; (d) si el tiempo (3) sustituye o convive con la regla de las tres pasadas de revisión, que mira el código ya terminado.
  > [!warning] Excepción registrada — 2026-08-27
  > En el Bloque 4 las ocho decisiones que faltaban **las cerró el agente**, a petición expresa del estudiante en ese momento (*"debe faltar 0 por decidir"*), y quedaron marcadas como revocables en `[[PROJECT]]`. La regla que se adopta es la de arriba: **a partir de aquí se vuelve con él**. Lo de aquel día fue una excepción puntual, no el precedente.

  *(call me maybe, 2026-08-27 — petición explícita del estudiante · aplicada ya en este proyecto: Bloque 4, `block_mockup/bloque_4_guardian.pdf`, y los cuatro primeros métodos de `Guardian` escritos así)*
- [ ] **Todo lo que el agente escriba en un `.md` va fechado con el día de hoy.** Al contextualizarse, el agente **fija la fecha del día** y la usa en **cada** actualización que haga a cualquier archivo del sistema: entradas de `[[PROJECT]]`, filas de la `Lista de refuerzo`, callouts de estado, observaciones de `[[PSYCHOLOGY]]`, briefings de `[[HANDOFF]]`, entradas de `[[REVIEWS]]` y propuestas de este archivo. Nada se escribe sin fecha, aunque parezca obvio en el momento.
  **Cómo se hace:** la fecha va en formato `AAAA-MM-DD`, dentro del propio texto que se añade — en el callout `> [!info] Estado — 2026-08-27`, en la columna de estado (`✅ 08-27`), o entre paréntesis al final de la línea. No vale una nota general al principio del archivo: fecha la **entrada**, no el archivo.
  **Motivo:** los archivos se leen meses después y por agentes que no estuvieron. Sin fecha no se distingue lo decidido ayer de lo decidido hace tres semanas, ni se ve qué quedó desactualizado — pasó con `[[FLOW]]`, que seguía marcando los Bloques 2 y 3 como pendientes días después de cerrarlos. Es además lo que ya exige `[[PSYCHOLOGY]]` para sus observaciones (*"cada entrada lleva la observación que la originó, con fecha"*) y lo que hace funcionar la regla de `[[FIRST]]` de citar el contenido con la fecha al final: sin fechas no hay contenido que citar.
  **A resolver al evaluarla:** dónde se escribe la orden — al ser un paso de contextualización, su sitio natural es `[[FIRST#Al arrancar, comprueba]]`, y el detalle del formato en `[[SYSTEM#Formato Obsidian]]`.
  *(call me maybe, 2026-08-27 — petición explícita del estudiante)*
- [ ] **Cada archivo del sistema termina con la orden de activar su skill.** Al final de cada `.md`, un callout fijo que le dice al agente qué skill invocar **antes de trabajar sobre lo que ese archivo gobierna**. Así la activación no depende de que el agente se acuerde: está escrita en el sitio por el que pasa obligatoriamente.
  **Mapa inicial:** `[[PSYCHOLOGY]]` → `psychologist-analyst`, antes de escribir cualquier observación de perfil · `[[SYSTEM]]` y `[[FIRST]]` → `caveman` en intensidad *ultra* al entrar en modo ejecución · `[[PROJECT]]` → `caveman ultra` al volcar progreso.
  **Motivo:** las skills se olvidan. Pasó con `psychologist-analyst`, que estuvo cuatro agentes sin instalar mientras `[[PSYCHOLOGY]]` decía que se usaba, y pasó con `caveman`, que el estudiante detectó sin usar pese a que `[[SYSTEM]]` lo pedía — y que hubo que respaldar con un hook. La orden escrita al pie del archivo es la versión sin infraestructura del mismo remedio: el recordatorio vive donde ya se está leyendo.
  **A resolver al evaluarla:** el texto de un `.md` no obliga a nada por sí solo —no es un hook— así que la orden funciona como recordatorio, no como garantía. Decidir si las que de verdad importan llevan además su hook en `.claude/settings.json`, y si el callout va al **final** (donde se lee al terminar) o al **principio** (donde se lee antes de actuar).
  *(call me maybe, 2026-08-17 — petición explícita del estudiante)*
- [ ] **Revisar código en tres pasadas separadas, en este orden: lógica → guards → estilo.** Cuando el estudiante pide *"evalúa esto"*, la primera pasada mira **solo si la lógica es correcta**: si el algoritmo hace lo que se diseñó, si el bucle termina, si las estructuras se reinician donde toca. Nada de excepciones, nada de `flake8`, nada de nombres. La segunda pasada mira **qué guards hacen falta** y dónde. La tercera, y solo al final, **`flake8` y `mypy`**.
  **La regla es que no se mezclan**: el agente no cuela un aviso de estilo ni un `try-except` que falta dentro de la revisión de lógica, aunque lo vea. Se anota y espera su turno.
  **Motivo:** una revisión que mezcla las tres llega como una lista larga donde un bucle que no termina pesa lo mismo que un nombre de variable, y obliga a arreglar tres cosas distintas a la vez sobre el mismo código. Es el mismo patrón que ya está registrado en `[[PSYCHOLOGY]]` para las preguntas —una cosa por mensaje— aplicado a la revisión de código. Encaja además con su decisión del 2026-08-14 de pasar `mypy` y `flake8` **al final**, no durante.
  *(call me maybe, 2026-08-17 — petición explícita del estudiante · aplicada ya en este proyecto)*
- [ ] **Se abole la regla de ignorar `PSYCHOLOGY.md`.** Ningún archivo dentro de `workflow/` se añade al `.gitignore` — todos se mantienen versionados, incluido `PSYCHOLOGY.md`, que queda **siempre dentro del proyecto**.
  **Al adoptarla, borrar la regla de los tres sitios donde vive en la base:** el chequeo de arranque de `[[FIRST#Al arrancar, comprueba]]`, los avisos de `[[SYSTEM]]` (*La carpeta workflow*, *Cómo lo verifica el agente*, la plantilla de `.gitignore` y la sección *PSYCHOLOGY.md*), y el callout de cabecera de `[[PSYCHOLOGY]]`.
  **Motivo:** el archivo es parte del proyecto y se quiere versionado con él. Mientras la regla siguió escrita, cada agente nuevo la comprobaba al arrancar y abría la sesión con un aviso falso.
  *(call me maybe, 2026-08-04 · reafirmada y ampliada el 2026-08-17 — petición explícita del estudiante · aplicada ya en este proyecto: `FIRST.md` y `PSYCHOLOGY.md`)*
- [ ] Después de la fase de estudio de conceptos, dedicar foco extra a la planeación: reforzar tanto los conceptos estudiados como la estructura del propio sistema, para optimizar el conocimiento aplicado del tema y del proyecto antes de pasar a diseño.
  *(call me maybe, 2026-08-04)*
- [ ] Al volver de estudiar los temas del mapa (NotebookLM u otra fuente), el agente no da el estado por "dominado" solo porque el estudiante lo diga: hace un cuestionario/discusión donde el estudiante explica con sus palabras cada concepto (general y aplicado al proyecto). Solo pasa a `dominado` en `PROJECT.md` lo que resiste esa explicación.
  *(call me maybe, 2026-08-04)*
- [ ] Antes de entrar en Fase 1 (diseño), el agente hace obligatoriamente un **cuestionario de internalización** con este formato: un tema por vez, dos preguntas por tema (el concepto en general + cómo se aplica a este proyecto), el estudiante responde con sus palabras. Si la respuesta tiene un fallo, el agente **no da la respuesta**: aísla el fallo y va con preguntas cada vez más concretas, apoyadas en una escena del propio proyecto, hasta que el estudiante llega solo. Un tema solo pasa a `dominado` cuando resiste esa explicación; si el estudiante pide profundizar en la mecánica, el tema se queda abierto aunque las respuestas hayan sido correctas. El objetivo no es validar que estudió, es que internalice **funcionamiento, mecánica y lógica** del proyecto y de cada una de sus partes antes de diseñar nada. Los temas se recorren en **orden de ejecución del programa** — desde el punto 0, lo primero que ocurre al lanzarlo, hasta la salida final — no en orden temático ni por importancia. Nunca se empieza por un tema del medio: *"primero tengo que entender cómo funciona la puerta y cómo se abre, antes de entrar a entender la sala"*. Esto reordena el mapa de temas: lo que parece accesorio (gestión de entorno, arranque del paquete, parseo de argumentos) va primero si es lo primero que ejecuta el programa. Solapa con la propuesta anterior — al adoptarlas, fusionar en una sola regla de `[[SYSTEM#FASE 0 — COMPRENSIÓN]]`.
  *(call me maybe, 2026-08-05)*
- [ ] Cuando se hace un cuestionario, la **interacción se registra**: la pregunta tal cual se hizo, la respuesta del estudiante y la corrección si la hubo — no solo el resultado resumido. Motivo: al retomar el Tema 1 tras cortar la sesión, en `PROJECT.md` solo estaban los dos fallos corregidos y la conclusión; las preguntas exactas no estaban en ningún archivo, y sin ellas el estudiante no pudo reconstruir dónde se había quedado ni continuar la explicación que estaba a medias.
  **Corregida el 2026-08-11:** el destino ya no es `PROJECT.md` sino **`REVIEWS.md`**, y `PROJECT.md` se queda solo con lo vivo. Entraba en fricción directa con la propuesta del sistema de refuerzo en tres piezas: registrar cada interacción completa en `PROJECT.md` es justo lo que lo infla y lo vuelve ilegible para el agente entrante. Al adoptarlas, **esta se absorbe dentro de aquella** — no son dos reglas.
  *(call me maybe, 2026-08-06)*
- [ ] **Recorrido teórico del flujo completo, justo después de listar los temas.** Una vez cerrado el mapa de temas de Fase 0, y antes de empezar el cuestionario tema por tema, el agente explica el **flujo completo del proyecto de principio a fin en términos teóricos**, con el mínimo tecnicismo posible: qué entra, qué ocurre en cada etapa y qué sale, sin nombres de librería ni firmas de método salvo cuando sean imprescindibles. El recorrido se diseña para **tocar todos los temas del mapa en su sitio natural dentro del flujo**, de modo que cada tema aparezca ya con su papel en el proyecto antes de estudiarse por separado. Motivo: estudiar los temas sueltos y solo después descubrir dónde encajan obliga a reconstruir el modelo mental dos veces; con el flujo delante, cada tema entra sabiendo qué problema resuelve.
  *(call me maybe, 2026-08-07)*
- [ ] **Sistema de refuerzo en tres piezas, con el cuestionario escrito al cerrar la sesión.** Sustituye a la propuesta del *cuestionario breve de repaso al iniciar cada sesión* (2026-08-10), que se queda corta: aquella dejaba lo pendiente repartido por las entradas de cada repaso, y obligaba al agente entrante a deducir las preguntas leyendo el histórico entero.

  **(a) `REVIEWS.md` — el histórico.** Archivo nuevo en `workflow/`. Una entrada por sesión, la más reciente arriba, con los fallos y su corrección, lo que salió correcto sin ayuda y lo que se difirió. Se acumula, nunca se sobrescribe. **`FIRST.md` dice explícitamente que no se lee al contextualizarse:** es histórico, crece sin parar y no cambia lo que toca hacer hoy — leerlo por costumbre gasta el contexto que hace falta para trabajar. Se abre solo en tres casos: un tema falla por tercera vez y hay que ver **cómo** se explicó antes para no repetir la explicación que no funcionó; el estudiante pregunta qué se contestó un día concreto; o se reconstruye la evolución de un concepto.

  **(b) `PROJECT.md` → `Lista de refuerzo` — lo vivo.** Una **sola** tabla acumulada con todo lo que hay que reforzar, y ningún otro sitio donde buscarlo. Una fila por tema, con cuatro columnas: el tema · el **origen** de la solicitud · el estado · cómo preguntarlo. El origen distingue tres cosas, y esa distinción es el núcleo de la propuesta: **🙋 lo pidió el estudiante** (refuerzo voluntario, o un tema que él mismo difiere a cuando se toque en el código) · **❌ falló en un cuestionario** · **🔍 lo propone el agente** porque lo ve flojo aunque no se haya preguntado. Estados: 🔴 pendiente · 🟡 explicado sin verificar · ✅ resiste sin ayuda · ⏸️ diferido a una fase posterior por decisión suya. **Una fila resuelta no se borra:** el rastro de que costó es lo que evita darla por sabida demasiado pronto.

  **(c) `PROJECT.md` → `Cuestionario de la próxima sesión` — el puente.** Lo escribe el agente **saliente**, en el protocolo de cierre, con las preguntas ya redactadas. Se construye mezclando dos fuentes: lo que está en 🔴 en la lista de refuerzo, y lo trabajado en la sesión que se cierra. Así el estudiante, en una sola tanda, se pone al día con lo de ayer y machaca lo que le cuesta. Se lanza una pregunta por mensaje; un fallo no se corrige dando la respuesta, se pone el caso límite concreto — salvo que diga *"no sé"*.

  **Motivo:** con el sistema anterior lo pendiente vivía en cuatro sitios a la vez (dos entradas de repaso, la fila de un tema del cuestionario de verificación y la cabecera del mapa de flujo). Para saber qué faltaba había que leerlos todos y cruzarlos a mano, y un agente con el contexto justo se saltaba alguno. Y las preguntas las improvisaba quien **menos** contexto tenía —el agente entrante— cuando quien acaba de ver qué costó es el que cierra.

  **Al adoptarla:** el ciclo completo va a `[[SYSTEM]]`; el paso *"escribir el cuestionario de la próxima sesión"* se añade al **protocolo de cierre** de `[[SYSTEM#Relevo de agente]]` como paso obligatorio; `REVIEWS.md` entra en la carpeta base como plantilla vacía y en la tabla de archivos de `FIRST.md` con la marca de *no leer*; y la plantilla de `PROJECT.md` incorpora las dos secciones nuevas.
  *(call me maybe, 2026-08-11 — petición explícita del estudiante · aplicada ya en este proyecto)*
- [ ] **Las firmas de Fase 1 se escriben directamente en los archivos `.py`, no en `PROJECT.md`.** El estudiante escribe clase, atributos y firmas completas (con `self`, tipos y retorno) en su `src/*.py` como esqueleto sin cuerpo, y el agente discute sobre ese archivo. `PROJECT.md` deja de duplicar las tablas de atributos y métodos: guarda la descripción del bloque, las decisiones y las objeciones, y **enlaza al archivo** donde viven las firmas. Motivo: escribirlas dos veces (tabla en Markdown y luego código) cuesta tiempo y esfuerzo sin aportar nada, y la versión de `PROJECT.md` se queda desactualizada en cuanto el código cambia.
  **Condición obligatoria de la regla:** cada bloque de `PROJECT.md` lleva la **lista de los archivos donde vive su diseño**, con su ruta, en un campo fijo junto a *Qué recibe* y *Qué entrega*. Sin ese enlace el agente nuevo abre `PROJECT.md`, no encuentra clases ni firmas por ninguna parte y no tiene forma de saber dónde mirar — el relevo arranca ciego. El enlace se escribe **en el momento de crear el archivo**, no al cerrar el bloque.
  **A resolver al evaluarla:** que un esqueleto sin cuerpo no se confunda con empezar la Fase 2.
  *(call me maybe, 2026-08-11 — petición explícita del estudiante)*
- [ ] **Arranque de sesión fijo, en tres pasos.** (a) Al terminar de contextualizarse, el agente responde **solo con un mensaje corto de confirmación** — nada de resumen de lo que leyó, ni estado, ni lista de pendientes: el estudiante ya los conoce. (b) `FIRST.md` lleva escrita de forma explícita la regla de **poca verborrea**: respuestas cortas, una idea y una pregunta por mensaje. (c) Antes de abrir tema nuevo, el agente **pide al estudiante que repase en voz alta lo del día anterior** — qué hizo, qué aprendió y en qué punto quedaron. Hasta que ese repaso no salga, no se avanza.
  **Ajuste del 2026-08-11:** el punto (c) se cumple lanzando el **cuestionario ya redactado** por el agente saliente, no pidiendo un repaso libre. Al adoptar ambas, (c) desaparece de aquí y queda dentro del sistema de refuerzo en tres piezas. Los puntos (a) y (b) siguen siendo independientes y se mantienen.
  *(call me maybe, 2026-08-06)*
