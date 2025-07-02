from pydantic_utils.API_Model import API_Model
from pydantic_utils.response_structures import *

class Agent:
    def __init__(self, sys_prompt, few_shot_ex, agent_name):
        self.sys_prompt = sys_prompt
        self.few_shot_ex = few_shot_ex
        self.api_model_agent = API_Model(
            system_prompt=sys_prompt, 
            few_shot_examples=few_shot_ex
            )
        self.agent_name = agent_name
        
    async def responder_test(self, context, response_structure):
        generated_response = await self.api_model_agent.call_api(
                previous_rounds_context=context,
                pydantic_response_structure = response_structure
            )
        return generated_response
    
    async def speak(self, prev_round_context):
        generated_response = await self.api_model_agent.call_api(previous_rounds_context=prev_round_context)
        razonamiento = generated_response.razonamiento
        voto = generated_response.voto
        output = {
            "role": "assistant",
            "content": {"argumentacion": f"[{self.agent_name}]: " + f"{razonamiento}", "voto": voto},
        }
        return output
    
    async def propose(self, context, response_structure):
        generated_response = await self.api_model_agent.call_api(
                previous_rounds_context=context,
                pydantic_response_structure = response_structure
            )
        return generated_response
    

    async def vote_proposal(self, context, response_structure, proposal):
        
        context.append({"role": "user", "content": f"Todos los agentes han hecho propuestas de modificacioes a la ley. Ahora tenes que votar a favor o en contra de poner esta propuesta en particular {proposal}"})
        generated_response = await self.api_model_agent.call_api(
                previous_rounds_context=context,
                pydantic_response_structure = response_structure
            )
        return generated_response
    

    def get_system_prompt(self):
        return self.sys_prompt