from API_Model import API_Model

class Reviewer:# o orquestador
    def __init__(self, system_prompt, agents):
        self.system_prompt = system_prompt
        self.agents = agents
        self.api_model_agent = API_Model(
            system_prompt=self.system_prompt, 
            few_shot_examples=None
            )
    def give_turn(self,):
        pass

    async def make_topic_summary(self,full_topic_debate):
        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=full_topic_debate
        )
        output = {
            "role": "assistant",
            "content": f"[{self.agent_name}]: " + generated_response.razonamiento,
        }
        return output    
    async def make_final_summary(self):
        """Creates the final summary out of the topic summaries (o lo hacemos dado toda la conversacion?)

        Args:
        Returns:
            string: The final summary.
        """
        # TODO
        generated_response = await self.api_model_agent.call_api(
            previous_rounds_context=prev_round_context
        )
        output = {
            "role": "assistant",
            "content": f"[{self.agent_name}]: " + generated_response.razonamiento,
        }
        return output    
    def search_similar_laws(self,):
        """RAG"""
        pass

    def turn_is_valid(self, turn):
        pass
