from pydantic import BaseModel, Field

# --- Definición del Modelo Pydantic para la Respuesta Estructurada ---
class StructuredAgentResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un agente.
    Esta clase sirve como esquema para el parseo de la respuesta de texto del modelo.
    """
    razonamiento: str = Field(description="El razonamiento detallado detrás de la respuesta del agente, explicando los argumentos o pasos seguidos.")
    #consigna_de_busqueda:str
    #queres_buscar: bool

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
