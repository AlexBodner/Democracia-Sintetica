class Round:
    def __init__(self,  law):
        self.law = law
        self.prompt = None
        self.round_nr = None
        

class FirstRound(Round):
    def __init__(self, law):
        super().__init__(law)
        self.prompt = f"En esta ronda cada agente puede dar argumentos a favor o en contra de la ley {law}. " \
                      "La argumentación no debe ser muy extensa pero debe estar bien fundamentada, con ejemplos y referencias a la ley concisos y reales."
        self.round_nr = 0


class SecondRound(Round):
    def __init__(self, law):
        super().__init__(law)
        self.prompt = f"En esta ronda cada agente recibe como contexto previo los argumentos de todos los agentes de la primera ronda (inlcuso lo que dijo el mismo) " \
                      "y van a poder contraargumentar o reafirmar su postura. Deben aclarar a qué agente le están respondiendo. " \
                      "Los agentes pueden intentar convencer al otro o cambiar su postura. Es importante que los agentes no se repitan y que\
                      cada uno aporte algo nuevo y sean fieles a su postura política. Tiene que seguir el planteo que hizo en la ronda\
                      anterior, pero puede cambiar de opinión si lo considera necesario, siempre aclarando por que cambia de opinion y argumentando su decision. " 
        self.round_nr = 1
                      
class ThirdRound(Round):
    def __init__(self, law):
        super().__init__(law)
        self.prompt = f"En esta ronda cada agente recibe como contexto previo los argumentos y contraargumentos de todos los " \
                      "agentes de la segunda ronda y van a poder hacer una argumentación final. Pueden mantener la misma postura o cambiar de opinión " \
                      "dado los contraargumentos. Deben hacer un resumen final de su postura y una conclusión sobre el tema, siempre fiel a su postura política."
        self.round_nr = 2