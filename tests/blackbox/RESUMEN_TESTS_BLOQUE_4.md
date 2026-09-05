# Tests del Bloque 4 — `Guardian`

**Resultado de la corrida: 56 verdes / 5 rojos** (61 casos, 4 min 07 s). Los cinco rojos van marcados en la tabla.

Todos los tests están escritos a caja negra contra el contrato del bloque: ninguna afirmación sale de leer la implementación.

---

| Test | Qué garantiza | Contra qué se contrasta | Qué se rompe si se pone rojo |
|---|---|---|---|
| `construye_con_vocabulario_y_catalogo_reales` | Lo que salen del Bloque 1 y del Bloque 2 entra en el Guardian tal cual, y el objeto nace en reposo | E1 E2 E3 | Los bloques no encajan entre sí: haría falta un adaptador que el diseño no contempla |
| `construye_con_catalogo_de_varias_funciones` | El caso de todos los días: catálogo de cinco funciones y sesión que arranca | E3 E4 | El programa no funcionaría con su propio catálogo |
| `construye_con_catalogo_de_una_sola_funcion` | Un catálogo con una única función también vale | E3 | Fallaría el caso más simple, y con él el escenario del atajo del nombre único |
| `construye_con_el_catalogo_ampliado` | Aguanta el vocabulario entero y un catálogo con anidamiento, función sin parámetros y nombres parecidos | E1 E5 | El bloque solo serviría para el catálogo actual; añadir una función lo rompería |
| `init_rechaza_argumentos_de_tipo_equivocado` (×5) | Construirlo con basura falla en la puerta, no más tarde | E6 | Un error de cableado entre bloques aparecería mucho después, disfrazado de otra cosa |
| `start_abre_la_sesion_con_los_prompts_reales` | Los once prompts del proyecto encienden la sesión | E4 | El bucle de generación no arrancaría para algún prompt del banco de pruebas |
| `start_acepta_el_prompt_vacio` | El prompt vacío es un caso válido, no un fallo | E6 | Filtrarlo aquí duplicaría una decisión que es del orquestador |
| `start_acepta_prompts_dificiles` (×7) | Comillas, llaves, saltos de línea, acentos, emoji, barra invertida y textos muy largos abren sesión igual | E6 | Un usuario escribiendo comillas o una llave tumbaría el programa |
| `start_repetido_borra_la_sesion_anterior` | Empezar de nuevo borra lo anterior: nada del prompt viejo aparece en el resultado nuevo | E4 | Las respuestas se contaminarían entre prompts al reutilizar el objeto |
| `start_rechaza_lo_que_no_es_texto` (×5) | Solo acepta texto; un número o una lista se cortan de entrada | E6 | Un prompt mal pasado se colaría y ensuciaría el JSON |
| `is_open_es_falso_antes_del_primer_start` | Sin haber empezado, no hay sesión abierta | E1 E3 | El bucle arrancaría solo, sin prompt |
| `is_open_se_apaga_justo_en_el_token_que_cierra` | Sigue abierta en cada paso y se apaga exactamente con el último token | E4 | El bucle pararía antes de tiempo, dejando el JSON a medias, o no pararía nunca |
| `is_open_repetido_no_mueve_nada` | Preguntar cincuenta veces no avanza el estado ni cambia la respuesta | E4 | Consultar el estado tendría efectos secundarios: cualquier traza o comprobación cambiaría el resultado |
| `is_open_nunca_lanza_en_ningun_momento` | Se puede preguntar en cualquier punto del recorrido sin que reviente | E4 | El bucle no podría usarlo como condición sin envolverlo en un `try` |
| `get_valid_ids_devuelve_ids_mientras_haya_hueco` | Mientras quede algo por escribir, siempre hay al menos un token con el que seguir | E4 | El modelo se quedaría sin opciones a mitad de camino: JSON imposible de cerrar |
| `todos_los_ids_ofrecidos_existen_en_el_vocabulario` | Todo id ofrecido existe de verdad en el vocabulario de Qwen, recorriendo los once prompts | E1 E4 | Se ofrecerían ids fantasma: el enmascarado de logits fallaría o elegiría un token inexistente |
| `consultar_los_ids_no_altera_el_estado` | Preguntar dos veces seguidas da lo mismo y no abre ni cierra nada | E4 | La caché de la lista blanca (bonus 4) sería imposible: consultar cambiaría el resultado |
| `la_comilla_cierra_el_nombre_en_cuanto_esta_completo` | Escrito `fn_greet`, se puede cerrar ya, aunque exista `fn_greeting` | E5 | El modelo no podría elegir el nombre corto: quedaría obligado a escribir el largo |
| **`el_nombre_no_admite_prefijos_imposibles_ni_comilla_temprana` — ROJO** | En el hueco del nombre solo entra lo que sigue pudiendo completar algún nombre del catálogo, y la comilla no entra con el nombre a medias ni sin empezar | E3 | El modelo podría escribir un nombre que no existe: `name` inválido y la llamada a función no se puede ejecutar |
| `la_hoja_number_no_admite_cierre_ni_punto_sin_digito` | Un número recién empezado no se puede cerrar ni empezar por un punto | E3 | Saldría `{"a": }` o `{"a": .}`: JSON roto |
| `la_hoja_number_no_admite_falsos_digitos` | Los caracteres que parecen dígitos pero JSON no acepta (`²`, `³`, `¹`) quedan fuera, barriendo el vocabulario real entero | E1 | El modelo podría elegir un superíndice y producir un número que no parsea |
| `la_hoja_number_no_admite_un_segundo_punto` | Con `40.5` escrito, el punto ya está gastado | E3 | Saldría `40.5.`: JSON roto |
| `en_la_hoja_number_solo_hay_un_cierre_admisible` | Nunca son admisibles la coma y la llave a la vez: el schema decide cuál toca | E3 | Se cerraría un nivel equivocado y la estructura dejaría de cuadrar con el schema |
| `todo_lo_ofrecido_en_una_hoja_number_deja_un_numero_valido` | Recorriendo la lista entera de la hoja, cualquier id ofrecido lleva a un JSON que parsea | E1 E3 | Habría trampas: tokens ofrecidos que rompen el número más adelante |
| `la_hoja_string_no_admite_barra_invertida` | Ningún token con barra invertida entra en un texto, porque no hay escapado | E1 | Saldría `"a\b"` sin escapar: JSON roto |
| `la_hoja_string_no_cierra_con_coma_ni_llave` | Dentro de un texto, la coma y la llave son contenido legítimo, no cierre | E3 | El texto se cortaría en cuanto el modelo escribiera una coma |
| `tras_la_comilla_la_hoja_string_no_admite_mas_contenido` | Escrita la comilla, el texto terminó y solo cabe seguir con la estructura | E3 | Saldría `"hello"x`: JSON roto |
| **`ningun_id_ofrecido_rompe_el_json` — ROJO** | En cada paso, cualquiera de los ids ofrecidos deja un JSON que todavía se puede terminar | E1 E3 E4 | La promesa central del bloque: el modelo podría elegir una opción ofrecida y quedarse con un JSON imposible de cerrar |
| `add_token_avanza_el_estado` | Comunicar el token elegido mueve la sesión: el JSON crece y conserva lo anterior | E4 | El bucle se quedaría clavado repitiendo el mismo paso |
| `el_ultimo_token_cierra_la_sesion` | El token que cierra la raíz apaga la sesión y deja el JSON terminado y parseable | E4 | El bucle no sabría cuándo parar |
| **`add_token_rechaza_lo_que_no_es_un_entero` (×5) — 2 ROJOS** (`"40"` y `True`) | Solo acepta un entero de Python; texto, decimal, `None`, lista o booleano se cortan en la puerta | E6 | Un id mal convertido entraría sin avisar y corrompería el estado |
| `get_json_a_medias_no_lanza` | Con la sesión abierta devuelve el JSON incompleto, para poder inspeccionar | E4 | No se podría depurar ni registrar el estado a mitad de generación |
| `el_resultado_tiene_exactamente_las_tres_claves` | Cerrado, el JSON trae `prompt`, `name` y `parameters`, ni una más ni una menos, en los once prompts | E4 | La validación final del Bloque 5 fallaría y el resultado no se podría guardar |
| `el_nombre_del_resultado_es_uno_del_catalogo` | El nombre sale tal cual del catálogo, sin inventarse ni deformarse | E3 E4 | Se intentaría ejecutar una función que no existe |
| `el_prompt_del_resultado_es_identico_al_recibido` | El prompt vuelve intacto, también con comillas, llaves y saltos de línea | E4 E6 | El archivo de resultados no se podría casar con la pregunta que lo originó |
| `los_parametros_son_los_del_schema_en_su_orden` | A cualquier profundidad, las claves de `parameters` son las del schema, ni una de más ni una de menos y en su orden | E4 E5 | La función se llamaría con argumentos que le faltan o que le sobran |
| `el_anidamiento_de_dos_niveles_se_completa` | Un parámetro que es un objeto con campos dentro se escribe entero y cierra igual que uno plano | E5 | El bonus de anidamiento no funcionaría y el catálogo no podría crecer |
| `la_funcion_sin_parametros_deja_un_objeto_vacio` | Una función sin parámetros no le pide nada al modelo: `parameters` sale vacío y el JSON queda completo | E5 | Se pediría al modelo que escribiera argumentos inexistentes, o el JSON no cerraría |
| **`todos_los_prompts_reales_terminan_en_un_json_valido` — ROJO** | Los once prompts reales, con recorridos aleatorios pero legales, siempre acaban en un JSON parseable con las tres claves | E1 E3 E4 | El programa produciría resultados inservibles en cuanto el modelo eligiera algo distinto de lo más obvio |
| `el_nombre_no_se_completa_sin_un_caracter_del_modelo` | Con una sola función en el catálogo, el nombre sigue sin escribirse hasta que el modelo pone su primer carácter | E3 | Se incumpliría la exigencia del enunciado: la función la elige el modelo, no el código |
| `con_un_solo_candidato_el_nombre_se_completa_y_cierra` | Puesto el primer carácter, el nombre entero y su comilla aparecen sin gastar más tokens | E3 | Se desperdiciarían pasos de generación deletreando algo ya decidido |
| `el_atajo_tambien_salta_cuando_el_catalogo_se_reduce_a_uno` | Con dos nombres parecidos, en cuanto lo escrito deja un solo candidato el nombre se completa y cierra | E5 | El atajo solo valdría para el caso trivial de un catálogo de una función |
| `ninguna_llamada_lanza_con_entradas_validas` | Catálogo ampliado y prompts reales, ciclo entero, sin una sola excepción | E1 E4 E5 | El programa se caería a mitad de una generación válida |

---

## Elementos objetivos

- **E1** — vocabulario real de Qwen (151.643 entradas), cargado con el Tokenizer del Bloque 1 sobre los archivos del modelo.
- **E2** — el mismo vocabulario en la otra dirección.
- **E3** — catálogo real de `data/input/`: 5 funciones.
- **E4** — los 11 prompts reales de `data/input/`.
- **E5** — catálogo ampliado: E3 más funciones fabricadas para lo que el real no tiene (nombre que es prefijo de otro, función sin parámetros, función de un solo parámetro, anidamiento a dos niveles, más de dos parámetros con tipos mezclados).
- **E6** — valores sueltos forzados a mano, solo para bordes declarados por el contrato que ningún artefacto real contiene.

## Dos límites declarados

En una hoja de texto la lista de tokens admisibles ronda los 150.000 candidatos, así que la comprobación de que *ninguna* opción ofrecida rompe el JSON se hace exhaustiva donde la lista cabe —huecos de nombre y hojas numéricas, de 1 a 19 candidatos— y con una muestra estable de 8 cuando pasa de 20. En esas hojas la pasada **no** es exhaustiva y no debe leerse como si lo fuera; pagarla entera o dejarla así es una decisión pendiente.

Aparte, el ejemplo del contrato con el token `.5` no es testeable con el vocabulario real: Qwen tokeniza los números dígito a dígito y `.5` no existe como token suelto. La regla general que lo engloba —que ningún token ofrecido en una hoja numérica deja un número que JSON rechace— sí queda cubierta.

## Pendiente por decisión

Tres casos siguen sin testear a la espera de que se decida si son uso incorrecto o comportamiento exigible: pedir los ids válidos sin un hueco abierto, comunicar un token antes de haber empezado, y pedir el JSON antes del primer arranque.
