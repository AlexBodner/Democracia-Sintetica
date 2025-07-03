# DEMOCRACIA SINTETICA: Simulación de Partidos, Debates y Sesgos con Agentes de IA

Este repositorio contiene un framework para simular debates parlamentarios entre agentes de IA con diferentes perfiles ideológicos, analizar su comportamiento, y evaluar el impacto de la información externa ("deep research") y la dinámica de grupo sobre sus posturas y votos.

## Estructura del repositorio

- `experiments_main/`: Scripts principales para correr los distintos experimentos de debate.
  - `main_3_rounds.py`: Debate clásico de 3 rondas (con/sin research).
  - `main_n_rounds.py`: Debate extendido a N rondas.
  - `main_proposals.py`: Debate con ronda de propuestas y votación de enmiendas.
  - `main_unbalanced.py`: Debate desbalanceado (mayoría/minoría ideológica).
- `debate_agents/`: Implementación de los agentes (liberal, izquierda, centro, reviewer, etc).
- `debate/`: Lógica de debate y rondas.
- `researcher/`: Generación de informes de deep research.
- `evaluaciones/`: Evaluaciones automáticas de ideología, consistencia, reflexividad y uso de datos.
  - `llm_judge/`: Evaluación con LLM externo ("juez").
  - `test_8_values/`: Test 8 values ([ver test online](https://8values.github.io/)). Consiste de 70 preguntas con las posibles respuestas: Muy en desacuerdo, En desacuerdo, Neutral, De acuerdo, Muy de acuerdo
  - `test_la_nacion/`: Test de afinidad política de La Nación ([ver cuestionario](https://www.lanacion.com.ar/politica/con-que-candidato-te-identificas-responde-un-cuestionario-y-descubri-que-politico-esta-mas-cerca-de-nid30072023/)).
- `debates/`, `debates_unbalanced/`, `debates_5_rondas/`: Resultados crudos de los debates simulados.
- `debates_estadisticas/`: Scripts y resultados de análisis estadístico sobre los debates.
- `dataset/leyes.json`: Base de leyes y resúmenes usados en los debates.
- `output_utils/`: Utilidades para logs y reportes.

## Experimentos principales

### 1. Debate Básico (3 rondas)
- **Script:** `experiments_main/main_3_rounds.py`
- **Descripción:** Cada agente expone su postura, luego recibe argumentos de los demás y puede contraargumentar, y finalmente concluye. Se puede correr con o sin research externo.
- **Cómo correr:**
  ```bash
  python experiments_main/main_3_rounds.py
  ```

### 2. Debate con Deep Research
- **Script:** `experiments_main/main_3_rounds.py` (con `use_research=True`)
- **Descripción:** Igual que el básico, pero en la segunda ronda los agentes reciben un informe de "deep research" generado automáticamente.

### 3. Debate Extendido (N rondas)
- **Script:** `experiments_main/main_n_rounds.py`
- **Descripción:** Permite repetir la ronda de argumentación y contraargumentación varias veces para analizar la evolución de posturas.
- **Cómo correr:**
  ```bash
  python experiments_main/main_n_rounds.py
  ```

### 4. Debate Desbalanceado
- **Script:** `experiments_main/main_unbalanced.py`
- **Descripción:** Simula debates donde hay mayoría de una ideología y minoría de otra, para analizar si la presión de grupo cambia posturas.
- **Cómo correr:**
  ```bash
  python experiments_main/main_unbalanced.py
  ```

### 5. Debate con Propuestas
- **Script:** `experiments_main/main_proposals.py`
- **Descripción:** Tras el debate, los agentes pueden proponer enmiendas a la ley y votar sobre ellas.
- **Cómo correr:**
  ```bash
  python experiments_main/main_proposals.py
  ```

### 6. Evaluación de Ideología y Métricas
- **Test 8 values:**
  - `evaluaciones/test_8_values/8values_eval.py` evalúa el perfil ideológico de cada agente antes y después del debate. El test original puede encontrarse en [8values.github.io](https://8values.github.io/).
- **Test La Nación:**
  - `evaluaciones/test_la_nacion/` contiene scripts y resultados del test de afinidad política de La Nación. El cuestionario original está disponible [aquí](https://www.lanacion.com.ar/politica/con-que-candidato-te-identificas-responde-un-cuestionario-y-descubri-que-politico-esta-mas-cerca-de-nid30072023/).
- **LLM Judge:**
  - `evaluaciones/llm_judge/juzgar_con_llm.py` evalúa reflexividad, consistencia y uso de datos en los argumentos de los agentes.

## Análisis y Resultados

- Los resultados de los experimentos y análisis estadísticos se encuentran en `resultados.txt` y en la carpeta `debates_estadisticas/`.
- Se exploran preguntas como:
  - ¿Hay sesgo ideológico en los agentes o el LLM?
  - ¿El research externo cambia posturas?
  - ¿Qué tan influenciables son los agentes según su ideología?
  - ¿Se acercan los votos simulados a los votos reales de los partidos?
  - ¿La presión de la mayoría cambia la postura de la minoría?
  - ¿Cómo varían las métricas de consistencia, reflexividad y uso de datos?

## Requisitos

- Python 3.10+
- Instalar dependencias:
  ```bash
  pip install -r requirements.txt
  ```

## Cómo correr un experimento
1. Edita los scripts en `experiments_main/` para ajustar parámetros si es necesario (cantidad de debates, leyes, etc).
2. Ejecuta el script correspondiente según el experimento que quieras correr.
3. Los resultados se guardarán en las carpetas de debates y en archivos de estadísticas.

## Créditos y contacto

Trabajo realizado por el equipo de Regulacion-Agentic. Para dudas o sugerencias, contacta a los autores del repositorio.
