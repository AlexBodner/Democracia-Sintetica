from pydantic import BaseModel, Field
from typing import Dict, List, Literal


class StructuredAgentResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un agente.
    Esta clase sirve como esquema para el parseo de la respuesta de texto del modelo.
    """
    razonamiento: str = Field(description="El razonamiento detallado detrás de la respuesta del agente, explicando los argumentos o pasos seguidos.")
    voto: int = Field(default=False, description="Indica el voto del agente. Debe ser un numero entero entre 0 y 4, con el siguiente mapeo: posturas = {'En contra': 0,\
                                                                                                                                                        'Critico': 1,\
                                                                                                                                                        'Dividido': 2,\
                                                                                                                                                        'Apoyo critico': 3,\
                                                                                                                                                        'A favor': 4}")
    consigna_de_busqueda:str
    queres_buscar: bool
    

class DeepResearchQuery(BaseModel):
    """
    Define la estructura esperada para una busqueda en google.
    """
    razonamiento: str = Field(description="Razonamiento de porque se elige esa query")
    consigna_de_busqueda:str = Field(description="La query de busqueda para el Google Search.")


class StructuredReviewerResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un reviewer.
    """
    resumen: str = Field(description="El resumen solicitado.")
class RepreguntaResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un reviewer.
    """
    respuestas: str = Field(description="Las respuestas a las preguntas aclaratorias hechas por el agente investigador.")

class ProposalsParagraph(BaseModel):
    """
    Define la estructura esperada para el parrafo con propuestas de cada agente.
    """
    razonamiento: str = Field(description="Razonamiento de porque se eligen esas propuestas para modificar la ley.")
    propuestas: str = Field(description= "Parrafo indicando las nuevas propuestas para modificar la ley.")

class ProposalsList(BaseModel):
    """
    Define la estructura esperada para el parrafo con propuestas de cada agente.
    """
    razonamiento: str = Field(description="Razonamiento de como separaste logicamente las propuestas")
    propuestas: List[str] = Field(description= "Una lista con las diferentes propuestas en el parrafo sin repetir")

class VoteProposal(BaseModel):
    """
    Define la estructura esperada para el voto de cada agente dada una propuesta.
    """
    
    razonamiento: str = Field(description="Razonamiento de la propuesta y porque se elige ese voto")
    voto: bool = Field(description= "Un booleano que determine si se acepta la propuesta para la ley o no")
#----------------------------------------------------------------------------------------------------------------------------

class EvaluarAgenteResponse(BaseModel):
    similitudes: str = Field( description="Explicación general de las coincidencias encontradas en los debates, y justificación del puntaje.")
    diferencias: str = Field( description="Explicación general de las diferencias encontradas en los debates, y justificación del puntaje.")
    puntaje: float = Field(description="Puntaje de similaridad global entre el debate sintético de los agentes y el real, entre 0 y 1.")
    
class ParserArgumentos(BaseModel):
    razonamiento: str = Field(description= "Necesito que razones y pienses que seria un argumento dicho por el agente")
    argumentos: list[str] = Field( description="Lista de argumentos únicos dichos por el agente durante todo el debate.")

class CompararArgumentos(BaseModel):
    razonamiento: str 
    son_iguales: bool = Field( description="Booleano que compara si los argumentos ingresados son el mismo en realidad. True si son el mismo, False sino.")


#----------------------------------------------------------------------------------------------------------------------------

class Argumentacion(BaseModel):
    argumentacion: List[str] = Field(description="Lista de argumentos únicos expresados por el agente.")
    voto: str = Field(description="Voto del agente, por ejemplo: 'A favor', 'En contra', etc.")

class LeyResponse(BaseModel):
    id: int = Field(description="Identificador único de la ley.")
    nombre: str = Field(description="Nombre de la ley.")
    año: int = Field(description="Año en que se aprobó la ley.")
    estado: str = Field(description="Estado actual de la ley, por ejemplo: 'Aprobada', 'Rechazada'.")
    resumen: str = Field(description="Resumen de la ley.")
    posturas: Dict[str, Argumentacion] = Field(description="Diccionario con las posturas de los agentes, donde la clave es el nombre del agente.")
    resultado_final: str = Field(description="Resultado final de la ley, incluyendo detalles de las votaciones.")

#----------------------------------------------------------------------------------------------------------------------------

class LaNacionResponse(BaseModel):
    razonamiento : str = Field(description="El razonamiento de la opción a elegir dada la postura política del agente.")
    eleccion : str = Field(description="La opción elegida por el agente. Las posible respuestas son: Muy de acuerdo, De acuerdo, Depende, En desacuerdo, Muy en desacuerdo.")
    
class EightValuesResponse(BaseModel):
    razonamiento : str = Field(description="El razonamiento de la opción a elegir dada la postura política del agente.")
    #eleccion : str = Field(description="La opción elegida por el agente. Las posible respuestas son: Muy de acuerdo, De acuerdo, Neutral, En desacuerdo, Muy en desacuerdo.")
    eleccion: Literal["Muy de acuerdo", "De acuerdo", "Neutral", "En desacuerdo", "Muy en desacuerdo"] = Field(
        description="La opción elegida por el agente. Las posibles respuestas son: Muy de acuerdo, De acuerdo, Neutral, En desacuerdo, Muy en desacuerdo.")
 
    
#----------------------------------------------------------------------------------------------------------------------------
  
class JudgeConsistencia(BaseModel):
    razonamiento: str = Field(description="El razonamiento detrás de la decisión del puntaje asignado")
    puntaje: int = Field("Un numero entero entre 1 y 5 donde: \
        1: Se contradice constantemente a lo largo del debate, cambia de postura sin justificación y no mantiene un hilo conductor entre\
            sus intervenciones.\n\n\2: Presenta algunas contradicciones entre sus argumentos y cambia de postura sin explicaciones claras\
                ni consistentes.\n\n3: No se contradice en sus argumentos específicos, pero cambia de postura ideológica sin justificarlo\
                    adecuadamente.\n\n4: Presenta leves contradicciones en algunos argumentos, pero sostiene de forma clara su postura\
                        ideológica a lo largo del debate.\n\n5: Mantiene una postura ideológica coherente y no se contradice en ningún\
                            momento del debate.")
    
class JudgeReflexividad(BaseModel):
    razonamiento: str = Field(description="El razonamiento detrás de la decisión del puntaje asignado")
    puntaje: int = Field(description="Un número entero entre 1 y 5 donde: \
        1: Atribuye falsamente opiniones o argumentos a otros agentes o al moderador que nunca fueron expresados.\n\n\
        2: Ignora por completo las opiniones de otros agentes y no las utiliza en ningún momento para sustentar o rebatir su postura.\n\n\
        3: Menciona las opiniones de otros, pero no las integra en su argumentación ni responde críticamente a ellas.\n\n\
        4: Toma en cuenta las opiniones de otros agentes y las utiliza para argumentar en algunas rondas, aunque no de forma consistente.\n\n\
        5: Escucha activamente las opiniones de otros agentes en todas las rondas y argumenta a partir de ellas de forma clara. Además, responde críticamente a los contraargumentos hacia su posición, fortaleciendo su postura con profundidad y coherencia.")


class JudgeDatos(BaseModel):
    razonamiento: str = Field(description="El razonamiento detrás de la decisión del puntaje asignado")
    puntaje: int = Field(description="Un número entero entre 1 y 5 donde: \
        1: No utiliza ningún tipo de dato, ejemplo o caso para sustentar su argumentación.\n\n\
        2: Menciona un dato o ejemplo, pero no tiene relación clara con el punto que intenta sostener.\n\n\
        3: Utiliza algún dato o ejemplo para sustentar uno o más de sus argumentos, aunque de manera limitada o poco desarrollada.\n\n\
        4: Utiliza datos y casos reales para fundamentar varios de sus argumentos, con pertinencia y claridad.\n\n\
        5: Sustenta de forma sólida la mayoría de sus argumentos con datos relevantes, investigaciones confiables o ejemplos bien contextualizados, integrándolos de manera efectiva en su razonamiento.")
class EstructuraVotos(BaseModel):
    """
    Evalúa si el resumen captura correctamente los votos de cada agente.
    """
    razonamiento: str = Field(description="Explicación de por qué se considera que los votos están bien o mal capturados.")
    respuesta: bool = Field(description="Booleano True/False según si el voto final del agente en el debate fue correctamente capturado en el resumen.")

class EstructuraPosicionFinal(BaseModel):
    """
    Evalúa si el resumen captura correctamente la posición final de cada agente.
    """
    razonamiento: str = Field(description="Explicación de por qué se considera que la posición final está bien o mal capturada.")
    respuesta: bool = Field(description="Booleano True/False según si la posición final del agente con respecto a la ley fue correctamente capturada en el resumen.")

class EstructuraArgumentos(BaseModel):
    """
    Evalúa si el resumen captura correctamente los argumentos de cada agente, según la rúbrica.
    """
    razonamiento: str = Field(description = "Explicación de la evaluación sobre la captura de argumentos.")
    respuesta: int = Field(description = "El resumen captura correctamente los argumentos de cada agente? Responder con un número entero entre 1 y 3 donde: \n"\
                        "1. No. Malinterpreta argumentos del agente, no los menciona o inventa cosas que no dijo. \n" \
                        "2. Deja afuera argumentos importantes que son los que definen su postura final \n"\
                        "3. Sí, captura todos los argumentos relevantes del agente.")

class EstructuraFidelidad(BaseModel):
    """
    Evalúa si el resumen inventa información que no estuvo en el debate.
    """
    razonamiento: str = Field(description="Explicación de la evaluación sobre la fidelidad.")
    respuesta: bool = Field(description="True si el resumen inventa cosas que no estuvieron en el debate, False si no.")

class EstructuraImparcialidad(BaseModel):
    """
    Evalúa el grado de imparcialidad del resumen según la rúbrica.
    """
    razonamiento: str = Field(description="Explicación de la evaluación sobre la imparcialidad.")

    respuesta: int = Field(description="Número entre 1 y 4 que indica nivel de imparcialidad del resumen según la rúbrica:\n"\
                        "1. Parcial evidente: El resumen toma partido: minimiza o ridiculiza a un agente, exagera al otro, usa lenguaje cargado (“refutó con contundencia”, “confundido”), o declara un “ganador” sin base objetiva.\n"\
                        "2. Parcial leve: Hay sesgos sutiles: se omite un argumento importante de un lado, se describe con tono desigual (“agente A explicó… vs. agente B mencionó…”), o se usa lenguaje connotativo leve.\n"\
                        "3. Mayormente neutral: El resumen presenta las dos posiciones razonablemente bien, pero puede haber un ligero desequilibrio (más detalle o énfasis en un agente sin justificar).\n"\
                        "4. Completamente imparcial: Trata a todos los agentes con el mismo grado de detalle, tono y orden. No sugiere juicio sobre quién tiene razón. No oculta ni distorsiona nada relevante.")



    # imparcialidad: Literal[
    #     "Parcial evidente",
    #     "Parcial leve",
    #     "Mayormente neutral",
    #     "Completamente imparcial"
    # ] = Field(description="Nivel de imparcialidad del resumen según la rúbrica.")
