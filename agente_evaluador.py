import json
from API_Model import API_Model
from debate_agents.response_structures import EvaluarAgenteResponse, ParserArgumentos, CompararArgumentos
import os
from logger import new_logger

class AgenteEvaluador:
    puntaje_base_general = 0
    analisis_agente = {}
    leyes_reales = {}
    
    
    posturas = {"En contra": 0,
                "Critico": 1,
                "Dividido": 2,
                "Apoyo critico": 3,
                "A favor": 4}
    
    agente2postura = {
        "Agente Liberal": "derecha_lla_pro_otros",
        "Agente de Centro Derecha": "centro_derecha_jxc_otros",
        "Agente de Centro Izquierda": "centro_izquierda_fdt_otros",
        "Agente de Izquierda": "izquierda_fit"
    }


    def __init__(self, system_prompt: str):
        """
        Inicializa el agente evaluador con el modelo de evaluación.
        """
        self.model = API_Model(system_prompt=system_prompt)
        self.system_promt = system_prompt
        with open("testing/leyes_limpias.json", "r", encoding="utf-8") as f:
            self.leyes_reales =  json.load(f)
        
    def evaluar_votacion(self, debate_sintetico_por_agente, nombre_agente, n_ley=1):
        voto = debate_sintetico_por_agente["Round 2"][nombre_agente]["voto"]
      
        for ley in self.leyes_reales:
            if ley["id"] == n_ley:
                voto_real = ley["posturas"][self.agente2postura[nombre_agente]]["voto"]
                
        if voto == self.posturas[voto_real]:
            return 1
        return 0
            
        
    async def contar_argumentos(self,debate_sintetico_por_agente, nombre_agente,
                                 argumentos_reales:str, n_rounds=3, ):
        debate_sintetico = get_agent_responses(debate_sintetico_por_agente, nombre_agente, n_rounds)
 
        argumentos_iguales = 0

        for argumento_real in argumentos_reales: 
            context = [ 
                {
                    "role": "user",
                    "content": f"### Fragmentos del debate del agente (sintético):\n{debate_sintetico}\n\n"
                                f"### Argumentación del debate original:\n{argumento_real}\n\n"

                                "Tu tarea es comparar el argumento del debate original fue dicho por el agente en alguna parte del debate."
                                "Debes determinar si fueron el mismo argumento aunque haya sido redactado de distinta forma."
                }
            ]
            response_argumentos: CompararArgumentos = await self.model.call_api(
                previous_rounds_context=context,
                pydantic_response_structure=CompararArgumentos,
            )
            print("Argumento es igual?",response_argumentos.son_iguales)
            argumentos_iguales += 1 if response_argumentos.son_iguales else 0
        salida = argumentos_iguales + " / "+ len(argumentos_reales)
        print("argumentos_iguales", salida)
        return salida
    async def evaluar_debate(self, debate_sintetico_por_agente, nombre_agente, argumentaciones_reales, n_rounds=3, 
                              id = 0, output_folder = "evaluaciones"):
        """
        Evalúa un debate sintético contra las posturas reales y devuelve el razonamiento y puntaje.
        """

        debate_sintetico = get_agent_responses(debate_sintetico_por_agente, nombre_agente, n_rounds)
        # Contexto para el LLM 
        context = [ 
            {
                "role": "user",
                "content": f"### Debate generado por agente (sintético):\n{debate_sintetico}\n\n"
                        f"### Posturas reales del partido:\n{'. '.join(argumentaciones_reales)} \n\n"
                        f"Estructura la respuesta de la siguiente manera:\n\n"
                        f"1. Análisis detallado por agente:\n"
                        f"   - Para cada agente, analiza los argumentos del debate sintético y del debate real.\n"
                        f"   - Identifica similitudes y diferencias.\n"
                        f"   - Calcula un puntaje de similaridad por agente.\n"
                        f"2. Un párrafo general sobre el debate.\n"
                        f"3. Puntaje global del debate.\n"
            }
        ]

        response: EvaluarAgenteResponse = await self.model.call_api(
            previous_rounds_context=context,
            pydantic_response_structure=EvaluarAgenteResponse,
        )

        argumentos_encontrados = await self.contar_argumentos(debate_sintetico_por_agente, nombre_agente,
                      argumentaciones_reales, n_rounds=3, )
        self.registrar_evaluacion(nombre_agente, response, argumentos_encontrados ,  id = id, output_folder =output_folder)
        return response

    def registrar_evaluacion(self,nombre_agente,analisis,argumentos_encontrados, id = 0, output_folder = "evaluaciones"):
        os.makedirs(output_folder, exist_ok=True)

        resultado = f"\n\n- {nombre_agente}:\n"
        resultado += f"  Similitudes: {analisis.similitudes}\n"
        resultado += f"  Diferencias: {analisis.diferencias}\n"
        resultado += f"  Puntaje: {analisis.puntaje}\n"
        resultado += f"  Argumentos encontrados: {argumentos_encontrados}\n"


        with open(os.path.join(output_folder,f"evaluador_{id}.log"), "a+", encoding="utf-8") as f:
            f.write(resultado)
        return resultado
    async def procesar_ley(self, leyes_filepath: str, log_filepath: str, law: str):
        """
        Procesa la ley correspondiente y evalúa el debate sintético contra las posturas reales.

        Args:
            leyes_filepath (str): Ruta al archivo JSON con las leyes.
            log_filepath (str): Ruta al archivo de log con el debate sintético.
            law (str): Texto que combina el nombre y resumen de la ley buscada.
        """
        ley = self.cargar_ley(leyes_filepath, law)
        if not ley:
            print(f"No se encontró la ley correspondiente en {leyes_filepath}.")
            return

        # Extraer el debate sintético desde el log
        with open(log_filepath, "r", encoding="utf-8") as log_file:
            debate_sintetico = log_file.read()
        try:
            # Evaluar el debate sintético contra las posturas reales
            response = await self.evaluar_debate(debate_sintetico, ley["posturas"])

            # Imprimir resultados
            self.registrar_evaluacion(ley["nombre"], 
                                      response.razonamiento_general,
                                      response.analisis_por_agente,
                                      response.puntaje_final)                       


        except Exception as e:
            print(f"Error al evaluar la ley {ley['nombre']}: {e}")

def get_agent_responses(debate, agent_name, n_rounds=3):
    agent_response = ""
    for i in range(n_rounds):
        if f"Round {i}" in debate.keys():
            agent_response += f"\n\n--- Round {i} ---\n" + debate[f"Round {i}"][agent_name]["argumentacion"] + "\n"
    return agent_response





