---
tipo: backlog
uso: propuestas de mejora al sistema de trabajo
ultima_actualizacion: 2026-08-31
tags: [42, sistema, mejoras]
---

# Posible mejoras al sistema

Backlog de propuestas de mejora al sistema de trabajo (`[[FIRST]]`, `[[SYSTEM]]`, `[[PROJECT]]`, `[[HANDOFF]]`, `[[PSYCHOLOGY]]`, `[[contract]]`).

## Propósito

Aquí se anota cualquier idea de mejora al método de trabajo que surja mientras se trabaja, sin interrumpir el proyecto en curso.

## Reglas de uso

- **Analizar primero, decidir después.** Ninguna propuesta se aplica en caliente: se evalúa al terminar el proyecto — salvo que esté **bloqueando el trabajo ahora mismo**, que entonces no es mejora, es error.
- Una propuesta por ítem, en checklist (`- [ ]`), redactada como regla y no como tarea.
- Al anotarla, indicar de qué proyecto vino y la fecha.
- Cuando una propuesta se adopta, su contenido **pasa al archivo de destino y deja de vivir aquí**. Este archivo no es registro histórico de lo ya implementado.
- Una propuesta que queda sin sentido se marca obsoleta con su razón, o se elimina.

---

## Propuestas

*(vacío — barrido completo el 2026-08-31)*

---

## Barrido del 2026-08-31

> [!success] Adoptadas — su contenido vive ya en su archivo de destino
> · **Tres pasadas de revisión** (lógica → guards → estilo) → `[[SYSTEM#Las tres pasadas de revisión — adoptada el 2026-08-31]]`
> · **Sistema de refuerzo en tres piezas** (`[[REVIEWS]]` + `Lista de refuerzo` + cuestionario escrito al cerrar) → `[[SYSTEM#Sistema de refuerzo — adoptada el 2026-08-31]]`. Absorbe la propuesta de *registrar la interacción de los cuestionarios*
> · **`[[FIRST]]` termina con la instrucción al próximo agente** → paso 6 del protocolo de cierre de `[[SYSTEM]]`
> · **El agente habla en el vocabulario del archivo** (sus identificadores · solo lo que ya existe · nada que pertenezca a otro método) → `[[SYSTEM#El agente habla en el vocabulario del archivo — adoptada el 2026-08-31]]`
> · **Se abole ignorar `[[PSYCHOLOGY]]`**: ningún archivo de `workflow/` va al `.gitignore` → `[[SYSTEM#Archivos del sistema]]`
> · **Cuestionario de internalización antes de Fase 1**, en orden de ejecución del programa, sin cerrar un tema por cuenta propia → `[[SYSTEM#Cuestionario de internalización — adoptada el 2026-08-31]]`. Absorbe la de *no dar `dominado` sin cuestionario*
> · **Recorrido teórico del flujo completo** tras cerrar el mapa de temas → `[[SYSTEM#Recorrido teórico del flujo completo — adoptada el 2026-08-31]]`
> · **Arranque de sesión fijo en tres pasos** → `[[SYSTEM#Arranque de sesión — fijo, en tres pasos]]`
> · **Todo lo que el agente escriba en un `.md` va fechado** → `[[SYSTEM#Archivos del sistema]]`
> · **Cada archivo ordena su skill** → `[[SYSTEM#Skills]]`
> · **Las firmas viven en el `.py`, no en `[[PROJECT]]`**, con el campo *Dónde vive* obligatorio → `[[SYSTEM#Dónde viven las firmas — adoptada el 2026-08-31]]`
> · **Orden de funciones dentro de una clase**: la más específica arriba, la que orquesta abajo → `[[SYSTEM#Cómo se ordena una clase — adoptada el 2026-08-31]]`. Aplicada ya a `src/guardian.py`
> · El **foco extra a la planeación** tras la fase de estudio queda cubierto por el recorrido teórico y el cuestionario de internalización, que es lo que aquella propuesta pedía sin nombrarlo

> [!bug] Descartadas — con su razón en `[[SYSTEM#Lo que se descartó y por qué]]`
> · **`code mockup`, la fase en tres tiempos** — la guía sin huecos convierte implementar en transcribir: *"es casi copiar código"*. Sobrevive el acompañamiento paso a paso con verificación ejecutando
> · **El contrato como origen de dos trabajos ciegos** — ya no hay agente que implemente, y el contrato escrito antes mentía. Sobreviven el contrato, ahora escrito **después** de la clase, y el agente de tests ciego
> · **Cerrar nombres, atributos y firmas antes de teclear** — *"no puedo diseñar toda la clase y 3 días después comenzar a codear porque me pierdo"*. Sobreviven el mapa de bloques y la **lista de requisitos** por bloque
