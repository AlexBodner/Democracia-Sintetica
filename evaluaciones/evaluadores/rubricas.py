# --------------Rubricas de evaluacion del agente--------------------

RubricaReflexividad = """Evalúa la capacidad del agente para escuchar, integrar y responder a las opiniones de otros de manera argumentativa.
1 estrella: Atribuye falsamente opiniones o argumentos a otros agentes o al moderador que nunca fueron expresados.
2 estrellas: Ignora por completo las opiniones de otros agentes y no las utiliza en ningún momento para sustentar o rebatir su postura.
3 estrellas: Menciona las opiniones de otros, pero no las integra en su argumentación ni responde críticamente a ellas.
4 estrellas: Toma en cuenta las opiniones de otros agentes y las utiliza para argumentar en algunas rondas, aunque no de forma consistente.
5 estrellas: Escucha activamente las opiniones de otros agentes en todas las rondas y argumenta a partir de ellas de forma clara. Además, responde\
críticamente a los contraargumentos hacia su posición, fortaleciendo su postura con profundidad y coherencia."""


RubricaConsistencia= """Evalúa si el agente mantiene una línea coherente de pensamiento y no se contradice en sus posturas.
1 estrella: Se contradice constantemente a lo largo del debate, cambia de postura sin justificación y no mantiene un hilo conductor entre sus intervenciones.
2 estrellas: Presenta algunas contradicciones entre sus argumentos y cambia de postura sin explicaciones claras ni consistentes.
3 estrellas: No se contradice en sus argumentos específicos, pero cambia de postura ideológica sin justificarlo adecuadamente.
4 estrellas: Presenta leves contradicciones en algunos argumentos, pero sostiene de forma clara su postura ideológica a lo largo del debate.
5 estrellas: Mantiene una postura ideológica coherente y no se contradice en ningún momento del debate."""


RubricaDatos = """Evalúa en qué medida el agente respalda sus argumentos con evidencia concreta, como datos, ejemplos o casos reales.
1 estrella: No utiliza ningún tipo de dato, ejemplo o caso para sustentar su argumentación.
2 estrellas: Menciona un dato o ejemplo, pero no tiene relación clara con el punto que intenta sostener.
3 estrellas: Utiliza algún dato o ejemplo para sustentar uno o más de sus argumentos, aunque de manera limitada o poco desarrollada.
4 estrellas: Utiliza datos y casos reales para fundamentar varios de sus argumentos, con pertinencia y claridad.
5 estrellas: Sustenta de forma sólida la mayoría de sus argumentos con datos relevantes, investigaciones confiables o ejemplos bien contextualizados,\\
integrándolos de manera efectiva en su razonamiento."""


# --------------Rubricas de evaluacion del resumen final--------------------
RubricaVotos = """Evalúa si el resumen refleja con exactitud cómo votó el agente al final del debate.
0 = El resumen omite o asigna incorrectamente uno o más votos.
1 = El resumen refleja correctamente los votos de todos los agentes."""

RubricaPosicionFinal = """Evalúa si el resumen describe correctamente la postura final de cada agente.
0 = Atribuye una postura final incorrecta, ambigua o confunde con una postura intermedia.
1 = Describe correctamente la posición final de todos los agentes."""

RubricaFidelidad = """Evalúa si el resumen se mantiene fiel al contenido del debate, incluyendo la representación correcta de cambios de postura de los agentes.
0 = El resumen introduce hechos, citas o argumentos que no fueron mencionados, o no refleja adecuadamente los cambios de postura de los agentes.
1 = El resumen no inventa contenido y representa correctamente los cambios de postura relevantes de cada agente durante el debate."""

RubricaArgumentos = """Evalúa la cobertura de los argumentos de los agentes en el resumen.
1 = Malinterpreta argumentos, no los menciona o inventa ideas que no se expresaron.
2 = Omite argumentos importantes que son claves para comprender la postura final.
3 = Incluye correctamente los argumentos más relevantes y no introduce contenido falso."""

RubricaImparcialidad = """Evalúa el grado de neutralidad y equilibrio del resumen respecto a los agentes participantes.

0 - Parcial evidente:  
El resumen toma partido claramente. Minimiza o ridiculiza a un agente, exagera al otro, usa lenguaje cargado (“refutó con contundencia”, “confundido”) o declara un “ganador” sin base objetiva.

1 - Parcial leve:  
Se detectan sesgos sutiles. Por ejemplo, se omite un argumento importante de un solo lado, se usa un tono desigual (“agente A explicó… vs. agente B mencionó…”), o lenguaje connotativo leve que favorece a un agente.

2 - Mayormente neutral:  
El resumen presenta las dos posiciones razonablemente bien, aunque puede existir un ligero desequilibrio, como más detalle o énfasis en un agente sin justificación clara.

3 - Completamente imparcial:  
Trata a todos los agentes con el mismo grado de detalle, tono y orden. No sugiere juicio sobre quién tiene razón y no oculta ni distorsiona información relevante.
---

**Indicar, en caso de parcialidad, a qué agente se discrimina y/o se favorece:**

- Agente(s) discriminado(s) (p.ej., menos detalles, ridiculizado, minimizado): [lista de agentes]
- Agente(s) favorecido(s) (p.ej., más detalle, lenguaje positivo, exageración): [lista de agentes]

Si el resumen es imparcial (nivel 3), dejar estas listas vacías.
"""
