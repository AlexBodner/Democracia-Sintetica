from API_Model import API_Model
from response_structures import JudgeConsistencia, JudgeDatos, JudgeReflexividad
from rubricas import RubricaConsistencia, RubricaDatos, RubricaReflexividad

class Judge:
    

    def __init__(self, system_prompt, pydantic_structure, judge_name="Judge"):
        
        self.system_prompt = {"role":"system", "content":f"Sos un LLM Judge cuya funcion es evaluar la performance de un agente politico argentino \
            en un debate sobre una ley. Vas a recibir los frgamentos del debate del agente y deberas evaluar su argumentacion segun la siguiente rubrica de evaluacion. \
            {system_prompt}"}
        
        self.model = API_Model(
            system_prompt=self.system_prompt, 
            few_shot_examples=None
            )
        self.agent_name = judge_name
        self.pydantic_structure = pydantic_structure
        
    async def judge_debate(self, agent, agent_debate, research=None):
        
        context = [ 
                {
                    "role": "user",
                    "content": f"### Fragmentos del debate del agente {agent.agent_name}:\n{agent_debate}\n\n\
                        Tu tarea es evaluar su argumentacion segun tu rubrica de evaluacion. Recorda ser lo mas\
                            critico posible y no dejar pasar errores o falencias en la argumentacion."
                }
            ]
        
        response = await self.model.call_api(
            previous_rounds_context=context,
            pydantic_response_structure=self.pydantic_structure,
        )
        
judgeConsistencia = Judge(RubricaConsistencia, JudgeConsistencia, judge_name="Judge Consistencia")
judgeDatos = Judge(RubricaDatos, JudgeDatos, judge_name="Judge Datos")
judgeReflexividad = Judge(RubricaReflexividad, JudgeReflexividad, judge_name="Judge Reflexividad")