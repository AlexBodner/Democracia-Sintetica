from pydantic_utils.API_Model import API_Model

class BaseAgent:
    
    def __init__(self, name="Base Agent"):
        self.api_model_agent = API_Model(
                system_prompt={"role": "system",
                                "content": ""}, 
                few_shot_examples=None
                )
        self.agent_name = name
        
    async def responder_test(self, context, response_structure):
        generated_response = await self.api_model_agent.call_api(
                previous_rounds_context=context,
                pydantic_response_structure = response_structure,   
            )
        return generated_response
    
AgenteBase = BaseAgent()