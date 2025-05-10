class Round:
    def __init__(self, topic, law, previous_rounds_context, agents, round_nr):
        self.topic = topic
        self.law = law
        self.previous_rounds_context = previous_rounds_context
        self.agents = agents
        self.round_nr = round_nr
