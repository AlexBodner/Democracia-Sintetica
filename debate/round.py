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

class SecondRound(Round):
    def __init__(self, law, round_nr=1):
        super().__init__(law)
        self.round_nr = round_nr
        self.prompt = (
                        "En esta ronda, cada agente tiene acceso a los argumentos expresados por todos los agentes en todo el debate hasta el momento, incluido el propio. "
                        "La tarea consiste en analizar críticamente estos argumentos, respondiendo, reforzando o modificando su postura según corresponda. "
                        "Cada agente puede señalar inconsistencias, falacias, omisiones o debilidades en los planteos de otros agentes, así como destacar puntos de coincidencia. "
                        "Es importante que los agentes identifiquen explícitamente a qué argumentos o agentes están respondiendo, y que los contraargumentos sean coherentes con su orientación ideológica. "
                        "Si algún agente decide modificar su postura o voto, debe justificar claramente los motivos de ese cambio. "
                        "Al finalizar, el agente debe indicar si mantiene o modifica su voto (a favor o en contra de la ley).")
           
class SecondRoundWithResearch(SecondRound):
    def __init__(self, law, research):
        super().__init__(law)
        self.round_nr = 1
        self.prompt = f"En esta segunda ronda, cada agente dispone de un informe con datos, estadísticas y análisis relevantes recopilados por un investigador especializado: \n\n"\
                        "Se espera que incorporen datos y cifras concretas del informe provisto para respaldar su posición, citando ejemplos o estadísticas relevantes (y aclarar que fue sacado del informe) "\
                        f"{research}\n\n" + self.prompt
                        


class ThirdRound(Round):
    def __init__(self, law, round_nr = 2):
        super().__init__(law)
        self.round_nr = round_nr
        self.prompt = ("En esta última ronda, cada agente debe elaborar una conclusión integradora que contemple su postura inicial, los argumentos del resto de los agentes y los contraargumentos surgidos en la segunda ronda. "
                    "La intervención debe explicar qué aspectos de los argumentos ajenos resultaron convincentes o irrelevantes, y cómo impactaron (o no) en la postura del agente. "
                    "Se espera una síntesis reflexiva que muestre si el debate enriqueció su perspectiva o reforzó su posición original, manteniendo siempre la coherencia con sus valores e identidad ideológica. "
                    f"Finalmente, cada agente debe justificar de manera clara y fundamentada su voto final (a favor o en contra de la ley '{law}'), cerrando así su participación en el debate."
                    "Es fundamental que la conclusión final del agente no se salga de su marco ideológico y que se mantenga fiel a su identidad política, incluso si ha habido cambios en su postura a lo largo del debate. ")

class ProposalRound(Round):
    def __init__(self, law):
        super().__init__(law)
        self.round_nr = 3
        self.prompt = (f"En esta ronda, los agentes tienen la oportunidad de formular propuestas concretas de modificación, mejora o reglamentación adicional respecto a la ley '{law}'. "
                       "Estas propuestas deben surgir tanto de su análisis ideológico como de los argumentos debatidos en rondas anteriores y de los datos provistos por el informe. "
                       "Cada agente podrá sugerir artículos nuevos, cambios puntuales en el texto legal, mecanismos de implementación, o salvaguardas para atender preocupaciones propias o ajenas. "
                       "Es importante que las propuestas sean viables, estén bien fundamentadas y respondan a principios políticos coherentes con la identidad del agente. "
                       "Asimismo, pueden indicar si están dispuestos a votar afirmativamente la ley solo si se incorporan ciertas modificaciones clave. "
                       "Al finalizar, el agente debe indicar si condiciona su voto a la aceptación de alguna propuesta, o si su posición respecto a la ley permanece firme.")


class VoteProposals(Round):
    def __init__(self, law):
        super().__init__(law)
        self.round_nr = 4
        self.prompt = ("En esta ronda, cada agente debe evaluar las propuestas realizadas por los demás participantes. "
                       "Deben indicar con claridad cuáles propuestas apoyan, cuáles rechazan, y por qué. "
                       "Se espera que el análisis sea ideológicamente consistente, considerando tanto la viabilidad política como la coherencia con los principios del agente. "
                       "Los agentes pueden modificar su voto final sobre la ley si consideran que las propuestas aceptadas alteran sustancialmente su contenido original. "
                       f"Al cerrar su intervención, cada agente debe declarar su voto definitivo (a favor o en contra de la ley '{law}'), teniendo en cuenta tanto el texto original como las modificaciones aceptadas o descartadas. "
                       "Este voto final debe estar sólidamente justificado desde una perspectiva política, ética e institucional.")

class FinalProposalRound(Round):
        def __init__(self, law, voted_proposals):
            super().__init__(law)
            self.round_nr = 5
            if len(voted_proposals) > 0:
                proposals = ""
                for proposal in voted_proposals:
                    proposals += proposal + "\n"
                self.prompt = (f"En esta última ronda, tenes que votar a favor o en contra de la ley {law} con las siguientes modificaciones: \n{proposals}. Estas propuestas seran agregadas a la ley ya que la mayoria voto a  favor de incorporarlas a la ley original. Tu tarea ahora es votar a favor o en contra de esta nueva ley. Recorda mantenerte dentro de tu ideoloia politica y justificar tu veredicto final")
            else:
                self.prompt = (f"En esta última ronda, tenes que votar a favor o en contra de la ley {law}. Ninguna de las propuestas fue aprobada por la mayoria por lo que la ley queda como estaba originalmente. Recorda mantenerte dentro de tu ideoloia politica y justificar tu veredicto final")
