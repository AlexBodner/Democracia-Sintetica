from API_Model import API_Model
class Agent:
    def __init__(self, sys_prompt, few_shot_ex, agent_name):
        self.sys_prompt = sys_prompt
        self.few_shot_ex = few_shot_ex
        self.api_model_agent = API_Model(
            system_prompt=sys_prompt, 
            few_shot_examples=few_shot_ex
            )
        self.agent_name = agent_name
    # def give_initialization(self):
    #     return [{"role":"system",
    #             "content": self.sys_prompt},
    #             "role": ]
    async def speak(self, prev_round_context, topic, law, round_nr):
        generated_response = await self.api_model_agent.call_api(
            topic=topic,
            ronda= round_nr,
            law=law,
            previous_rounds_context=prev_round_context
        )
        output = {
            "role": "assistant",
            "content": f"[{self.agent_name}]: " + generated_response.razonamiento,
        }
        return output

    def vote_topic(self, topic, summary):
        pass
    
