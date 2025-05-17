from pydantic import BaseModel, Field

# --- Definición del Modelo Pydantic para la Respuesta Estructurada ---
class StructuredAgentResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un agente.
    Esta clase sirve como esquema para el parseo de la respuesta de texto del modelo.
    """
    razonamiento: str = Field(description="El razonamiento detallado detrás de la respuesta del agente, explicando los argumentos o pasos seguidos.")

# --- Definición del Modelo Pydantic para la Respuesta Estructurada ---
class StructuredReviewerResponse(BaseModel):
    """
    Define la estructura esperada para una respuesta estructurada de un reviewer.
    """
    resumen: str = Field(description="El resumen solicitado.")
    #resumen_principal: str = Field(description="Un resumen conciso de la idea principal o conclusión de la respuesta del agente.")
