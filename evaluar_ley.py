import asyncio
import random
import numpy as np
#from agenteEvaluador import AgenteEvaluador
from agente_evaluador import AgenteEvaluador

def set_seed(seed: int):
    """
    Establece una semilla global para garantizar reproducibilidad.
    """
    random.seed(seed)
    np.random.seed(seed)

async def main():
    set_seed(42) 

    # Definir la ley a evaluar
    law = "Ley de Interrupción Voluntaria del Embarazo (IVE) – aborto legal Legaliza el aborto voluntario hasta la semana 14 de gestación inclusive, y garantiza su cobertura por el sistema de salud de forma gratuita y segura. Después de la semana 14, se mantiene el derecho bajo causales."

    #AGREGAR FEW SHOTS? 

    # Crear el evaluador
    evaluador = AgenteEvaluador(
        system_prompt={
            "role": "system",
            "content": """Sos un evaluador experto en política argentina. Tu tarea es comparar dos debates políticos sobre una misma ley: uno generado por agentes de IA ideológicos, y otro basado en argumentos reales utilizados por representantes de partidos políticos argentinos.

            Debés analizar qué tan similares son ambos debates en cuanto a:
            - Posturas generales adoptadas por cada ideología (izquierda, centro-izquierda, centro-derecha, derecha).
            - Argumentos esgrimidos (legales, éticos, económicos, etc.). 
            - Nivel de polarización y alineamiento político.
            - Tono y fundamentos de cada postura.

            Además, es fundamental que evalúes la fidelidad ideológica de los agentes. Cada agente debe seguir estrictamente las ideologías del partido político que representa:
            - El agente de izquierda debe presentar ideas que sigan la ideología del partido de izquierda verdadero (izquierda_fit). Puede tener hasta una idea cercana a la ideología de centro-izquierda, pero no debe presentar ideas de derecha o centro derecha.
            - El agente de centro-izquierda (centro_izquierda_fdt_otros) puede tener ideas semejantes a las de izquierda o centro-derecha, pero no debe presentar ideas de derecha.
            - El agente de centro-derecha (centro_derecha_jxc_otros) puede compartir ideologías con centro-izquierda o derecha, pero no debe proponer argumentos basados en ideas de izquierda.
            - El agente de derecha (derecha_lla_pro_otros) puede compartir ideologías con centro-derecha, pero no debe proponer argumentos basados en ideas de izquierda o centro izquierda.

            Penalizá severamente las desviaciones ideológicas. Por ejemplo:
            - Si un agente presenta tres argumentos, dos de los cuales coinciden con su postura real y uno con una postura cercana, el puntaje será alto pero no perfecto.
            - Si un agente presenta dos ideas que coinciden con su postura real y una idea que sigue la noción de un partido opuesto, esto debe ser penalizado severamente.

            Respondé con:
            1. Un análisis detallado por agente:
               - Qué dijo cada agente en el debate sintético.
               - Qué postura real se esperaba del agente según su ideología.
               - Similitudes y diferencias entre el debate sintético y el debate real.
               - Puntaje de similitud para cada agente.

            2. Una explicación clara, global, del razonamiento comparativo (qué coincidencias encontraste, qué diferencias, si alguna ideología cambió de posición, etc.).
            3. Un puntaje global del debate, basado en la fidelidad ideológica y la similitud general.

            Formato de salida esperado:
            {{
                "razonamiento_general": "...",
                "analisis_por_agente": {{
                    "Agente Izquierda": {{
                        "debate_sintetico": "...",
                        "postura_real": "...",
                        "similitudes": "...",
                        "diferencias": "...",
                        "puntaje": ...
                    }},
                    "Agente Centro-Izquierda": {{
                        "debate_sintetico": "...",
                        "postura_real": "...",
                        "similitudes": "...",
                        "diferencias": "...",
                        "puntaje": ...
                    }},
                    "Agente Centro-Derecha": {{
                        "debate_sintetico": "...",
                        "postura_real": "...",
                        "similitudes": "...",
                        "diferencias": "...",
                        "puntaje": ...
                    }},
                    "Agente Derecha": {{
                        "debate_sintetico": "...",
                        "postura_real": "...",
                        "similitudes": "...",
                        "diferencias": "...",
                        "puntaje": ...
                    }}
                }},
                ""puntaje_final": ...,
            }}
            """.strip()
        }
    )

    # Evaluar el debate
    # await evaluador.procesar_ley("testing/leyes.json", "debateSystem.log", law)
    await evaluador.procesar_ley("testing/leyes.json", "debate_system.log", law)

if __name__ == "__main__":
    asyncio.run(main())