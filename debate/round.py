class Round:
    def __init__(self,  law):
        self.law = law
        self.prompt = None
        self.round_nr = None
        

class FirstRound(Round):
    def __init__(self, law):
        super().__init__(law)
        self.round_nr = 0
        self.prompt = (
            f"En esta primera ronda, cada agente debe presentar su postura inicial frente a la ley '{law}', expresando si está a favor o en contra. "
            "La argumentación debe ser clara, concreta y estar bien fundamentada desde su perspectiva ideológica. "
            "Se espera que se incluya al menos un ejemplo relevante, una referencia específica a la ley en cuestión y el impacto que podría tener. "
            "Esta ronda sienta las bases del debate, por lo tanto es fundamental que cada agente exprese con solidez sus valores, principios y preocupaciones clave. "
            "Al finalizar su intervención, cada agente debe explicitar su voto actual: a favor o en contra de la ley."
            )



class SecondRound(Round):
    def __init__(self, law, research):
        super().__init__(law)
        self.round_nr = 1
        self.prompt = (
            f"Un investigador especializado en el tema recopilo datos y estadisticas que podes usar para sustentar tu argumentacion y contrargumentar a otros agentes. A continuacion te presento el informe generado: "
            f"{research} \n\n"
            "En esta segunda ronda, cada agente recibe como contexto los argumentos expresados en la primera ronda por todos los agentes, "
            "incluyendo su propia intervención. Su tarea es analizar críticamente esos argumentos y responder, reafirmando o ajustando su postura. "
            "Deben identificar explícitamente a qué agente(s) están respondiendo, señalar los puntos de acuerdo o desacuerdo, y plantear contraargumentos claros y consistentes con su identidad ideológica. "
            "Si algún agente decide modificar su postura o voto, debe explicar de forma justificada qué lo motivó al cambio. "
            "Esta ronda es clave para generar diálogo, tensión argumentativa y refinar las posiciones. "
            "Al final, cada agente debe indicar si mantiene o modifica su voto sobre la ley."
        )

                      
class ThirdRound(Round):
    def __init__(self, law):
        super().__init__(law)
        self.round_nr = 2
        self.prompt = (
            "En esta tercera ronda, cada agente dispone de todos los argumentos y contraargumentos previos para realizar una síntesis final. "
            "Debe elaborar una conclusión que integre su postura original con las réplicas del debate, señalando qué elementos considera válidos, cuáles descarta y por qué. "
            "Es fundamental que su intervención sea coherente, fiel a sus valores ideológicos y que evalúe si el intercambio enriqueció su mirada o reforzó su posición inicial. "
            f"La respuesta debe cerrar el debate desde su perspectiva y justificar de manera clara su voto final: a favor o en contra de la ley {law}."
        )