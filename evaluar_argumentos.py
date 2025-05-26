from API_Model import *
import json

def evaluar_argumentos_dado_resumen(ley_dict, resumen_general, api_model: API_Model):
    """Esta funcion devuelve para cada ley del diccionario delfi un diccionario que va a tener la postura como key
    y un numero entre 0 y 1 que diga que tanto se parecen los argumentos."""
    

    results_dict = {}


    for postura in ley_dict["posturas"]:
    #iterar sobre ley_dict["argumentos"]
        #tirarle al api_model consulta de si se parecen y cuanto
        postura_debate = hacer algo con resumen_general
        context = [{"role":"user", "content":"Enfocandose en los argumentos del agente {Agente}, compara la postura original: {postura} contra"
        " la postura de {Agente} en el resumen del siguiente debate: {postura_debate}"}]
        results_dict[postura] = api_model.call_api(context)
    return results_dict

def main():
    #Crear LLM que va a comparar y darle contexto
    with open("leyes.json", "r", encoding="utf-8") as f:
        leyes = json.load(f)
        
    model = API_Model(system_prompt="""Sos un evaluador experto en política argentina. Tu tarea es comparar dos debates políticos sobre una misma ley: uno generado por\
                                            agentes de IA ideológicos, y otro basado en argumentos reales utilizados por representantes de partidos políticos argentinos.

                                        Debés analizar qué tan similares son ambos debates en cuanto a:
                                        - Posturas generales adoptadas por cada ideología (izquierda, centro-izquierda, centro-derecha, derecha).
                                        - Argumentos esgrimidos (legales, éticos, económicos, etc.).
                                        - Nivel de polarización y alineamiento político.
                                        - Tono y fundamentos de cada postura.

                                        ### Debate generado por agentes (sintético):
                                        {debate_sintetico}

                                        ### Debate real:
                                        {debate_real}

                                        Respondé con:
                                        1. Una explicación clara del razonamiento comparativo (qué coincidencias encontraste, qué diferencias, si alguna ideología cambió de\
                                            posición, etc.).
                                        2. Un puntaje de similitud entre 0 y 1, donde:
                                        - 1.0 = coincidencia total (los agentes simulan perfectamente el debate real, con los mismos argumentos y posturas).
                                        - 0.5 = similitud parcial (algunos bloques alineados, otros no)
                                        - 0.0 = no hay coincidencia relevante, las posturas no corresponden a la ideologia del agente.

                                        Formato de salida esperado (en JSON):
                                        {{
                                        "razonamiento": "...",
                                        "puntaje": ...
                                        }}
                                                ".strip()
                                        }]",)""")