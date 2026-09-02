---
tipo: plantilla
uso: plantilla del PDF de un bloque — el único documento que recibe el agente de tests
creado: 2026-08-29
ultima_actualizacion: 2026-08-31
tags: [42, sistema, diseno, contrato, tests, plantilla]
---

# contract.md — Plantilla del contrato de bloque

> [!important] Qué es esto — refundido el 2026-08-31
> La plantilla del **PDF de un bloque**: el ==**único**== documento que recibe el agente que va a testear la clase sin verla por dentro. Antes eran dos —el contrato y un briefing aparte que se pegaba a mano—; ahora el PDF es autocontenido y no hay nada que pegar.

> [!important] Dos clases de contenido, y no se mezclan
> · La **PARTE FIJA** se copia **literal** en cada bloque y en cada proyecto. No se adapta, no se resume, no se reescribe.
> · La **PARTE RELLENABLE** es lo que cambia de una clase a otra. Un hueco por sección, y ninguno se deja vacío.

> [!warning] Se escribe DESPUÉS de que la clase exista y corra
> Antes se generaba al cerrar el diseño, y mentía: el del Bloque 4 traía mal el número de funciones y de prompts, no declaraba las rutas del vocabulario, y ponía un ejemplo (`.5`) que no existe en el vocabulario real.
> Escrito después se redacta contra la clase terminada, y **lo que afirma se puede comprobar**.

> [!warning] El riesgo de escribirlo después, y cómo se paga
> Si se redacta mirando la implementación, la implementación se cuela dentro y el que testea deja de ser ciego. ==**Por eso la regla de corte es más estricta que antes, no menos.**==

| Campo | Valor |
|---|---|
| Quién lo escribe | El agente que implementó la clase |
| Quién lo aprueba | El estudiante |
| Quién lo lee | Solo el agente de tests |
| Cuándo | Con la clase escrita y corriendo, justo antes de abrir la sesión de tests |
| Dónde vive | Junto al código, no en `workflow/`: es herramienta de construcción |
| Fecha | ==Siempre==. Un contrato sin fecha no se distingue de uno desactualizado |

---

# PARTE FIJA — se copia literal en todos los bloques

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
> *(Salió el 2026-08-31: un test miraba 8 de 150.134 candidatos; congelando el estado se comprobaron los 150.134 en 7 segundos.)*

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

> [!example] La misma regla, aplicada a dos clases distintas
> **Una clase que valida un archivo de entrada:** el límite real es el archivo más grande y más malformado que el proyecto puede recibir de verdad. Un archivo de 2 GB no es stress, es ficción. Un JSON con una clave de más, sí.
> **Una clase con un bucle y un tope:** el límite real es la entrada legítima más larga que existe en los datos del proyecto — y el test **obligatorio** es el que hace **saltar el tope**, no el que se queda cómodo por debajo. Si ninguna entrada real lo dispara, se construye la entrada legítima más extrema que el dominio admita, y se dice que hizo falta fabricarla.

> [!note] Un crash es una salida como cualquier otra
> Si el contrato dice *"no debe crashear nunca"*, una excepción es un rojo. Si dice *"lanza `ValueError` con el archivo ausente"*, la excepción **es** la salida correcta y no lanzarla es el rojo.

> [!tip] Por qué el entorno del proyecto
> Es el mismo que ejecuta el evaluador. Un verde ahí vale; un verde en un entorno fabricado solo dice que allí funcionaba.

---

# PARTE RELLENABLE — un hueco por sección, ninguno vacío

> [!important] La regla de corte
> ==**Entra lo público y lo comprobable desde fuera. No entra nada sobre cómo está construida por dentro.**==

| Entra | No entra |
|---|---|
| Los **métodos públicos**: firma, qué acepta, qué devuelve | Los métodos privados |
| Qué debe **aceptar** y qué debe **rechazar** | Con qué estructura de datos se resuelve |
| **En qué orden se llaman** para conducir una sesión | En qué orden se escriben los `if` |
| **Invariantes** | Los pasos numerados del algoritmo |
| Estados congelados y datos reales | Código de implementación |
| Lo **descartado a propósito**, con su razón | Alegorías, motivación, *por qué importa* |

> [!warning] La frontera fina: conducir ≠ construir
> **Conducir** es *"llama a `start(prompt)`, pide `get_valid_ids()`, elige uno, pásalo a `add_token(id)`, repite mientras `is_open()`"*. Eso **va**: sin ello no se puede montar un solo test.
> **Construir** es *"`add_token` mira si el último carácter cierra el hueco y hace `pop` de la pila"*. Eso **no va** nunca.
> ==La prueba: si el dato solo se puede saber abriendo el archivo, sobra.==

## R1 · Qué hace la clase
Una frase: el problema que resuelve. No cómo.

## R2 · Interfaz pública
Tabla: método · firma completa · qué recibe · qué devuelve. **Solo lo público.**

## R3 · Cómo se conduce una sesión
El orden real de llamadas, con un ejemplo corto de principio a fin.

## R4 · Qué debe aceptar
Por método, con los bordes declarados (vacíos, límites, caracteres raros).

## R5 · Qué debe rechazar
Por método, y ==**con qué excepción**==. Es la mitad que más se olvida.

## R6 · Invariantes
Lo que debe ser verdad siempre, numeradas. Una invariante se contrasta contra el universo entero (F3), no contra ejemplos.

## R7 · Fronteras
Lo que **no** es de esta clase, y de quién es.

## R8 · Descartado a propósito
Con su razón. Sin esto se reporta como bug.

## R9 · Elementos objetivos
Tabla: identificador · nivel (1/2/3) · **ruta exacta** · forma · **cómo se carga** (con qué clase o función, nunca a mano) · qué características reproduce.

> [!important] Los recursos se declaran, no se buscan
> El agente de tests no explora el repositorio. Si no está declarado aquí, no existe para él.

## R10 · Archivo de tests
`tests/test_bloque_N.py`

## R11 · Comando de ejecución
El del entorno del proyecto, escrito entero.

## R12 · Recorrido completo
Un caso real de principio a fin, marcando en cada línea **quién produce qué**.

---

> [!warning] Cero huecos
> Un hueco encontrado al redactar significa que algo no estaba decidido. Se **vuelve con el estudiante** y se cierra entre los dos — no lo decide el agente por su cuenta ni lo deja como pendiente.
> **Hueco** es cualquier punto donde quien testea no sabría qué esperar. Lo que se deje abierto **a propósito** se nombra como tal, con su razón.

> [!warning] Si falta una sección, la sesión de tests no arranca
> Un contrato incompleto se paga en tests que prueban otra cosa.

## Cómo se escribe

| Regla | Detalle |
|---|---|
| **Sin código de implementación** | Sí entran firmas, datos y estados congelados: no son escribir el código, son poner el caso delante |
| **Identificadores en el idioma del código, descripciones en el del estudiante** | Los nombres, tal como están en el archivo |
| **Cada afirmación con su grado de certeza** | Ver F5 |
| **Tablas y estados congelados, no prosa** | Una tabla por conjunto de reglas; un estado real por cada caso límite |
| **Sin verborrea** | Nada de motivación ni de *por qué importa* |
