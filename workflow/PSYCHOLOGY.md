---
tipo: perfil
estudiante: 
skill: psychologist-analyst
creado: 2026-08-04
ultima_actualizacion: 2026-08-05
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

*(vacío — se rellena con la evidencia)*

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
| 2026-08-05 | Orden del cuestionario | Pidió recorrer los temas en **orden de ejecución del programa**, no por importancia: *"primero tengo que entender cómo funciona la puerta y cómo se abre antes de entrar a entender la sala"*. Necesita la secuencia real completa, sin saltos, para construir el modelo mental |
