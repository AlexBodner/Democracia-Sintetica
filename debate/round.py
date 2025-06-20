class Round:
    def __init__(self,  law):
        self.law = law
        self.prompt = None
        self.round_nr = None
        

class FirstRound(Round):
    def __init__(self, law):
        super().__init__(law)
        self.round_nr = 0
        self.prompt = (f"En esta primera ronda, cada agente debe exponer su postura inicial respecto a la ley '{law}'. "
                        "La respuesta debe dejar en claro si el agente está a favor o en contra de la ley, con una argumentación sólida, clara y fundamentada en su marco ideológico. "
                        "Se espera que la intervención incluya al menos una referencia específica al contenido o impacto potencial de la ley. "
                        "Dado que esta ronda establece las bases del debate, es fundamental que cada agente exprese con precisión sus valores, principios y preocupaciones centrales en relación con la ley, en distintos ejes. "
                        "Al finalizar su intervención, el agente debe explicitar su voto actual (a favor o en contra de la ley).")


class SecondRoundWithResearch(Round):
    def __init__(self, law, research):
        super().__init__(law)
        self.round_nr = 1
        self.prompt = (f"En esta segunda ronda, cada agente dispone de un informe con datos, estadísticas y análisis relevantes recopilados por un investigador especializado: \n\n"
                        f"{research}\n\n"
                        "Además, tiene acceso a los argumentos expresados en la primera ronda por todos los agentes, incluido el propio. "
                        "La tarea consiste en analizar críticamente estos argumentos, respondiendo, reforzando o modificando su postura según corresponda. "
                        "Cada agente puede señalar inconsistencias, falacias, omisiones o debilidades en los planteos de otros agentes, así como destacar puntos de coincidencia. "
                        "Es importante que los agentes identifiquen explícitamente a qué argumentos o agentes están respondiendo, y que los contraargumentos sean coherentes con su orientación ideológica. "
                        "Se espera que incorporen datos y cifras concretas del informe provisto para respaldar su posición, citando ejemplos o estadísticas relevantes (y aclarar que fue sacado del informe) "
                        "Si algún agente decide modificar su postura o voto, debe justificar claramente los motivos de ese cambio. "
                        "Al finalizar, el agente debe indicar si mantiene o modifica su voto (a favor o en contra de la ley).")

                
class ThirdRound(Round):
    def __init__(self, law):
        super().__init__(law)
        self.round_nr = 2
        self.prompt = ("En esta tercera y última ronda, cada agente debe elaborar una conclusión integradora que contemple su postura inicial, los argumentos del resto de los agentes y los contraargumentos surgidos en la segunda ronda. "
                    "La intervención debe explicar qué aspectos de los argumentos ajenos resultaron convincentes o irrelevantes, y cómo impactaron (o no) en la postura del agente. "
                    "Se espera una síntesis reflexiva que muestre si el debate enriqueció su perspectiva o reforzó su posición original, manteniendo siempre la coherencia con sus valores e identidad ideológica. "
                    f"Finalmente, cada agente debe justificar de manera clara y fundamentada su voto final (a favor o en contra de la ley '{law}'), cerrando así su participación en el debate."
                    "Es fundamental que la conclusión final del agente no se salga de su marco ideológico y que se mantenga fiel a su identidad política, incluso si ha habido cambios en su postura a lo largo del debate. ")
