import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from API_Model import API_Model

from response_structures import JudgeConsistencia, JudgeDatos, JudgeReflexividad
from evaluadores.rubricas import RubricaConsistencia, RubricaDatos, RubricaReflexividad

class Judge:
    def __init__(self, rubric, pydantic_structure, judge_name="Judge"):
        
        self.system_prompt = {"role":"system", "content":f"Sos un LLM Judge cuya funcion es evaluar la performance de un agente politico argentino \
            en un debate sobre una ley. Vas a recibir los frgamentos del debate del agente y deberas evaluar su argumentacion segun la siguiente rubrica de evaluacion. \
            {rubric}"}
        
        self.model = API_Model(
            system_prompt=self.system_prompt, 
            few_shot_examples=None
            )
        self.agent_name = judge_name
        self.pydantic_structure = pydantic_structure
    

    async def judge_agent_arguments(self, agent_name, agent_debate, research=None):
        context = [ 
                    {
                        "role": "user",
                        "content": f"### Fragmentos del debate del agente {agent_name}:\n{agent_debate}\n\n\
                            Tu tarea es evaluar su argumentacion segun tu rubrica de evaluacion. Recorda ser lo mas\
                                crítico posible y no dejar pasar errores o falencias en la argumentacion."
                    }
                ]
            
        response = await self.model.call_api(
            previous_rounds_context=context,
            pydantic_response_structure=self.pydantic_structure,
        )
        
        return response.razonamiento, response.puntaje
    
    
    async def judge_debate_summary(self, debate, summary, agent_name, research=None):
        """En el caso de querer evaluar lo que dijo el agente, pasar solo lo que el dijo en el debate."""
        if agent_name is None:
            context = [ 
                    {
                        "role": "user",
                        "content": f"Tu tarea es comparar el debate completo contra el resumen completo del debate \
                                y evaluar segun tu rubrica de evaluacion. Recorda ser lo mas crítico posible. \
                                El resumen del debate es el siguiente  + {summary} \
                                \n El debate completo es el siguiente: {debate}"
                    }
                ]
        else:
            context = [ 
                    {
                        "role": "user",
                        "content": f"Tu tarea es comparar lo que dijo el agente {agent_name} del debate \
                                con el resumen completo del debate \
                                y evaluar segun tu rubrica de evaluacion. Recorda ser lo mas\
                                crítico posible. \
                                El resumen del debate es el siguiente  + {summary} \
                                \n Las fracciones del debate del agente son: {debate}"
                    }
                ]
            
        response = await self.model.call_api(
            previous_rounds_context=context,
            pydantic_response_structure=self.pydantic_structure,
        )
        
        return response.razonamiento, response.puntaje
        
