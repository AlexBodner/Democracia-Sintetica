
def evaluar_argumentos_dado_resumen(ley_dict, resumen_general):
    """Esta funcion devuelve para cada ley del diccionario delfi un diccionario que va a tener la postura como key
    y un numero entre 0 y 1 que diga que tanto se parecen los argumentos."""

    results_dict = {}


    #Crear LLM que va a comparar y darle contexto

    #iterar sobre ley_dict["argumentos"]
        #tirarle al llm consulta de si se parecen y cuanto
        results_dict[postura] = loquedigaLLM
    return {}