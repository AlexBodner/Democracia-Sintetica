import asyncio
from agente_evaluador import AgenteEvaluador

async def main():
    # Definir la ley a evaluar
    law = "Ley de Interrupción Voluntaria del Embarazo (IVE) – aborto legal Legaliza el aborto voluntario hasta la semana 14 de gestación inclusive, y garantiza su cobertura por el sistema de salud de forma gratuita y segura. Después de la semana 14, se mantiene el derecho bajo causales."

    # Crear el evaluador
    evaluador = AgenteEvaluador(
        system_prompt={
            "role": "system",
            "content": """Sos un evaluador experto en política argentina. Tu tarea es comparar dos debates políticos sobre una misma ley: uno generado por\
                        agentes de IA ideológicos, y otro basado en argumentos reales utilizados por representantes de partidos políticos argentinos.

                    Debés analizar qué tan similares son ambos debates en cuanto a:
                    - Posturas generales adoptadas por cada ideología (izquierda, centro-izquierda, centro-derecha, derecha).
                    - Argumentos esgrimidos (legales, éticos, económicos, etc.).
                    - Nivel de polarización y alineamiento político.
                    - Tono y fundamentos de cada postura.

                    ### Debate generado por agentes (sintético):
                    {debate_sintetico}

                    ### Posturas reales por partido:
                    {posturas_reales}

                    Respondé con:
                    1. Una explicación clara del razonamiento comparativo (qué coincidencias encontraste, qué diferencias, si alguna ideología cambió de\
                        posición, etc.).
                    2. Un puntaje de similitud entre 0 y 1, donde:
                    - 1.0 = coincidencia total (los agentes simulan perfectamente el debate real, con los mismos argumentos y posturas).
                    - 0.5 = similitud parcial (algunos bloques alineados, otros no)
                    - 0.0 = no hay coincidencia relevante, las posturas no corresponden a la ideología del agente.

                    Formato de salida esperado (en JSON):
                    {{
                    "razonamiento": "...",
                    "puntaje": ...
                    }}
                    """.strip()
        }
    )

    # Evaluar el debate
    await evaluador.procesar_ley("testing/leyes.json", "debate_system.log", law)

if __name__ == "__main__":
    asyncio.run(main())
