class Reviewer:# o orquestador
    def __init__(self, prompt, agents):
        self.prompt = prompt
        self.agents = agents

    def give_turn(self,):
        pass

    def make_topic_summary(self,):
        pass

    def make_final_summary(self,):
        pass
    
    def search_similar_laws(self,):
        """RAG"""
        pass

    def turn_is_valid(self, turn):
        pass
