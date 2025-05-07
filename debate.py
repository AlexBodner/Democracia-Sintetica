from agents.reviewer import Reviewer
class Debate:
    def __init__(self, agents, law, reviewer, n_rounds = 3):
        self.agents = agents
        self.law = law
        self.reviewer = reviewer 
        self.n_rounds = n_rounds

        self.round_info = []
    def run_debate(self,):
        #TODO
        for round in range(self.n_rounds):
            #turn = self.reviewer.give_turn() #Esto no va si lo queremos hacer en paralelo como deciamos.
            self.round_info.append(self.debate_round())
        
        self.conclusiones()

    def debate_round(self,):
        #TODO
        output = ""
        for agent in self.agents():
            output += agent.speak()

        return output
    def conclusiones(self,):
        return self.reviewer.make_final_summary()
