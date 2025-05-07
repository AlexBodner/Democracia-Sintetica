from agents.reviewer import Reviewer
class Debate:
    def __init__(self, agents, law, reviewer, n_rounds = 4):
        self.agents = agents
        self.law = law
        self.reviewer = reviewer 
        self.n_rounds = n_rounds

    def run_debate(self,):
        for round in range(self.n_rounds):
            #turn = self.reviewer.give_turn() #Esto no va si lo queremos hacer en paralelo como deciamos.
            debate_round(
            )

