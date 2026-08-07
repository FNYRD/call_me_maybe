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

- [ ] Ningún archivo dentro de `workflow/` se añade al `.gitignore` — todos se mantienen versionados, incluido `PSYCHOLOGY.md`.
  *(call me maybe, 2026-08-04)*
- [ ] Después de la fase de estudio de conceptos, dedicar foco extra a la planeación: reforzar tanto los conceptos estudiados como la estructura del propio sistema, para optimizar el conocimiento aplicado del tema y del proyecto antes de pasar a diseño.
  *(call me maybe, 2026-08-04)*
- [ ] Al volver de estudiar los temas del mapa (NotebookLM u otra fuente), el agente no da el estado por "dominado" solo porque el estudiante lo diga: hace un cuestionario/discusión donde el estudiante explica con sus palabras cada concepto (general y aplicado al proyecto). Solo pasa a `dominado` en `PROJECT.md` lo que resiste esa explicación.
  *(call me maybe, 2026-08-04)*
- [ ] Antes de entrar en Fase 1 (diseño), el agente hace obligatoriamente un **cuestionario de internalización** con este formato: un tema por vez, dos preguntas por tema (el concepto en general + cómo se aplica a este proyecto), el estudiante responde con sus palabras. Si la respuesta tiene un fallo, el agente **no da la respuesta**: aísla el fallo y va con preguntas cada vez más concretas, apoyadas en una escena del propio proyecto, hasta que el estudiante llega solo. Un tema solo pasa a `dominado` cuando resiste esa explicación; si el estudiante pide profundizar en la mecánica, el tema se queda abierto aunque las respuestas hayan sido correctas. El objetivo no es validar que estudió, es que internalice **funcionamiento, mecánica y lógica** del proyecto y de cada una de sus partes antes de diseñar nada. Los temas se recorren en **orden de ejecución del programa** — desde el punto 0, lo primero que ocurre al lanzarlo, hasta la salida final — no en orden temático ni por importancia. Nunca se empieza por un tema del medio: *"primero tengo que entender cómo funciona la puerta y cómo se abre, antes de entrar a entender la sala"*. Esto reordena el mapa de temas: lo que parece accesorio (gestión de entorno, arranque del paquete, parseo de argumentos) va primero si es lo primero que ejecuta el programa. Solapa con la propuesta anterior — al adoptarlas, fusionar en una sola regla de `[[SYSTEM#FASE 0 — COMPRENSIÓN]]`.
  *(call me maybe, 2026-08-05)*
- [ ] Cuando se hace un cuestionario, la **interacción se registra en `PROJECT.md`**, en la fase correspondiente: la pregunta tal cual se hizo, la respuesta del estudiante y la corrección si la hubo — no solo el resultado resumido. Motivo: al retomar el Tema 1 tras cortar la sesión, en `PROJECT.md` solo estaban los dos fallos corregidos y la conclusión; las preguntas exactas no estaban en ningún archivo, y sin ellas el estudiante no pudo reconstruir dónde se había quedado ni continuar la explicación que estaba a medias.
  *(call me maybe, 2026-08-06)*
- [ ] **Recorrido teórico del flujo completo, justo después de listar los temas.** Una vez cerrado el mapa de temas de Fase 0, y antes de empezar el cuestionario tema por tema, el agente explica el **flujo completo del proyecto de principio a fin en términos teóricos**, con el mínimo tecnicismo posible: qué entra, qué ocurre en cada etapa y qué sale, sin nombres de librería ni firmas de método salvo cuando sean imprescindibles. El recorrido se diseña para **tocar todos los temas del mapa en su sitio natural dentro del flujo**, de modo que cada tema aparezca ya con su papel en el proyecto antes de estudiarse por separado. Motivo: estudiar los temas sueltos y solo después descubrir dónde encajan obliga a reconstruir el modelo mental dos veces; con el flujo delante, cada tema entra sabiendo qué problema resuelve.
  *(call me maybe, 2026-08-07)*
- [ ] **Arranque de sesión fijo, en tres pasos.** (a) Al terminar de contextualizarse, el agente responde **solo con un mensaje corto de confirmación** — nada de resumen de lo que leyó, ni estado, ni lista de pendientes: el estudiante ya los conoce. (b) `FIRST.md` lleva escrita de forma explícita la regla de **poca verborrea**: respuestas cortas, una idea y una pregunta por mensaje. (c) Antes de abrir tema nuevo, el agente **pide al estudiante que repase en voz alta lo del día anterior** — qué hizo, qué aprendió y en qué punto quedaron. Hasta que ese repaso no salga, no se avanza.
  *(call me maybe, 2026-08-06)*
