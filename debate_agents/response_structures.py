from pydantic import BaseModel, Field

# --- Definición del Modelo Pydantic para la Respuesta Estructurada ---
class StructuredAgentResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un agente.
    Esta clase sirve como esquema para el parseo de la respuesta de texto del modelo.
    """
    razonamiento: str = Field(description="El razonamiento detallado detrás de la respuesta del agente, explicando los argumentos o pasos seguidos.")
    consigna_de_busqueda:str
    queres_buscar: bool

class SearchAgentResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un agente.
    Esta clase sirve como esquema para el parseo de la respuesta de texto del modelo.
    """
    razonamiento: str = Field(description="El razonamiento detallado detrás de la respuesta del agente, explicando los argumentos o pasos seguidos. No completar si va a querer hacer un google search (queres_buscar = True)")
    consigna_de_busqueda:str = Field(description="Las query de busqueda para el Google Search. No completar si va a querer hacer un google search (queres_buscar = True)")
    queres_buscar: bool
# --- Definición del Modelo Pydantic para la Respuesta Estructurada ---
class StructuredReviewerResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un reviewer.
    """
    resumen: str = Field(description="El resumen solicitado.")
    #resumen_principal: str = Field(description="Un resumen conciso de la idea principal o conclusión de la respuesta del agente.")
class InvestigadorResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un agente.
    Esta clase sirve como esquema para el parseo de la respuesta de texto del modelo.
    """
    razonamiento: str = Field(description="La informacion explicada de las distintas paginas que sean relevantes hacia la busqueda.")

class EvaluadorResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada del Evaluador de resultados del debate.
    """
    razonamiento: str = Field(description="La explicacion de porque considera que los argumentos son similares y porque asigna ese puntaje.")
    puntaje: float = Field(description="El puntaje de similaridad entre 0 y 1 entre los argumentos del debate sintético y el debate original.")
    
    
    """
        contexto = [{
        "role": "user",
        "content":
            f"
                Sos un evaluador experto en política argentina. Tu tarea es comparar dos debates políticos sobre una misma ley: uno generado por\
                    agentes de IA ideológicos, y otro basado en argumentos reales utilizados por representantes de partidos políticos argentinos.

                Debés analizar qué tan similares son ambos debates en cuanto a:
                - Posturas generales adoptadas por cada ideología (izquierda, centro-izquierda, centro-derecha, derecha).
                - Argumentos esgrimidos (legales, éticos, económicos, etc.).
                - Nivel de polarización y alineamiento político.
                - Tono y fundamentos de cada postura.

                ### Debate generado por agentes (sintético):
                {debate_sintetico}

                ### Debate real:
                {debate_real}

                Respondé con:
                1. Una explicación clara del razonamiento comparativo (qué coincidencias encontraste, qué diferencias, si alguna ideología cambió de\
                    posición, etc.).
                2. Un puntaje de similitud entre 0 y 1, donde:
                - 1.0 = coincidencia total (los agentes simulan perfectamente el debate real, con los mismos argumentos y posturas).
                - 0.5 = similitud parcial (algunos bloques alineados, otros no)
                - 0.0 = no hay coincidencia relevante, las posturas no corresponden a la ideologia del agente.

                Formato de salida esperado (en JSON):
                {{
                "razonamiento": "...",
                "puntaje": ...
                }}
                        ".strip()
                }]

    """