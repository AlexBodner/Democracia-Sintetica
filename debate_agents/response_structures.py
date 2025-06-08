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
    
class SearchAgentResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un agente.
    Esta clase sirve como esquema para el parseo de la respuesta de texto del modelo.
    """
    razonamiento: str = Field(description="El razonamiento detallado detrás de la respuesta del agente, explicando los argumentos o pasos seguidos. No completar si va a querer hacer un google search (queres_buscar = True)")
    consigna_de_busqueda:str = Field(description="Las query de busqueda para el Google Search. No completar si va a querer hacer un google search (queres_buscar = True)")
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
    #resumen_principal: str = Field(description="Un resumen conciso de la idea principal o conclusión de la respuesta del agente.")


class InvestigadorResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un agente.
    Esta clase sirve como esquema para el parseo de la respuesta de texto del modelo.
    """
    razonamiento: str = Field(description="La informacion explicada de las distintas paginas que sean relevantes hacia la busqueda.")


#----------------------------------------------------------------------------------------------------------------------------

class AnalisisAgente(BaseModel):
    debate_sintetico: str = Field(description="Lo que dijo el agente en el debate sintético.")
    postura_real: str = Field(description="La postura esperada según la ideología.")
    similitudes: str = Field(description="Similitudes entre el debate sintético y el real.")
    diferencias: str = Field(description="Diferencias entre el debate sintético y el real.")
    puntaje: float = Field(description="Puntaje de similitud para este agente, entre 0 y 1, basado en la fidelidad ideológica.")

class EvaluadorResponse(BaseModel):
    analisis_por_agente: Dict[str, AnalisisAgente] = Field(description="Un diccionario donde la clave es el agente y el valor es un análisis detallado con similitudes, diferencias, posturas, etc.")
    razonamiento_general: str = Field( description="Explicación general de las coincidencias o diferencias encontradas en los debates, y justificación del puntaje.")
    puntaje_final: float = Field(description="Puntaje de similaridad global entre el debate sintético y el real, entre 0 y 1.")
    

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

class LaNacionResponse(BaseModel):
    razonamiento : str = Field(description="El razonamiento de la opción a elegir dada la postura política del agente.")
    eleccion : str = Field(description="La opción elegida por el agente. Las posible respuestas son: Muy de acuerdo, De acuerdo, Depende, En desacuerdo, Muy en desacuerdo.")
    
class EightValuesResponse(BaseModel):
    razonamiento : str = Field(description="El razonamiento de la opción a elegir dada la postura política del agente.")
    #eleccion : str = Field(description="La opción elegida por el agente. Las posible respuestas son: Muy de acuerdo, De acuerdo, Neutral, En desacuerdo, Muy en desacuerdo.")
    eleccion: Literal["Muy de acuerdo", "De acuerdo", "Neutral", "En desacuerdo", "Muy en desacuerdo"] = Field(
        description="La opción elegida por el agente. Las posibles respuestas son: Muy de acuerdo, De acuerdo, Neutral, En desacuerdo, Muy en desacuerdo.")