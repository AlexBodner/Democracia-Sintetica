from API_Model import *
def evaluar_argumentos_dado_resumen(ley_dict, resumen_general, api_model: API_Model):
    """Esta funcion devuelve para cada ley del diccionario delfi un diccionario que va a tener la postura como key
    y un numero entre 0 y 1 que diga que tanto se parecen los argumentos."""

    results_dict = {}


    for postura in ley_dict["posturas"]:
    #iterar sobre ley_dict["argumentos"]
        #tirarle al api_model consulta de si se parecen y cuanto
        postura_debate = hacer algo con resumen_general
        context = [{"role":"user", "content":"Compara la postura original: {postura} contra la postura: {postura_debate}"}]
        results_dict[postura] = api_model.call_api(context)
    return results_dict

def main():
    #Crear LLM que va a comparar y darle contexto
    model = API_Model(system_prompt="",)
