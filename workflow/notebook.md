---
tipo: bitacora
proyecto: call me maybe
tags: [42, notebook, bitacora]
---

# notebook.md — Bitácora del estudiante

> [!important] Es del estudiante
> Lo escribe él, con sus palabras. El agente no añade entradas por su cuenta: solo las que le pidan, y las deja tal cual salvo corrección ortográfica.

---

## 06/08

Nos enfocamos en repetir varias veces el flujo de entrada de datos y generación de salida del proyecto, lo que me ayudó a internalizar bien el proceso. Ahora estamos haciendo lo mismo un poco más en profundidad con el enmascarado usando `numpy`.

### El flujo, tal como lo describí

```
prompt + funciones (texto)
    ↓ encode
[~200 token ids]
    ↓ get_logits_from_input_ids
150.000 logits (uno por token del vocabulario)
    ↓ máscara: lo inválido a -inf, usando el dict de vocabulario
    ↓ np.argmax → id del token ganador
se añade al tensor → 201 ids → y vuelta a empezar
    ↓ hasta que el JSON cierra
input_ids[200:] → decode → string → json.loads → dict → validar con pydantic
```

> [!note] Nota para el agente de mañana
> **1.** Antes de cualquier otra cosa, pídeme que **repita lo que aprendí en la sesión anterior** — en este caso, el flujo de arriba. No lo leas tú: que lo diga yo.
> **2.** Después de contextualizarte, di solo **"estoy listo"**. Nada de sermón sobre lo que leíste, ni resumen del estado, ni lista de pendientes.
> **3.** Explícame qué es **lista blanca** y **lista negra**.
> **4.** Tu primera lectura es siempre `[[FIRST]]`.
