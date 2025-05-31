import json
from API_Model import API_Model
from debate_agents.response_structures import EvaluadorResponse
import re

class AgenteEvaluador:
    puntaje_base_general = 0
    analisis_agente = {}

    def __init__(self, system_prompt: str):
        """
        Inicializa el agente evaluador con el modelo de evaluación.
        """
        self.model = API_Model(system_prompt=system_prompt)

    def cargar_ley(self, filepath: str, law: str):
        """
        Busca y carga la ley correspondiente desde el archivo JSON.

        Args:
            filepath (str): Ruta al archivo JSON con las leyes.
            law (str): Texto que combina el nombre y resumen de la ley buscada.

        Returns:
            dict: La ley correspondiente o None si no se encuentra.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            leyes = json.load(f)
            for ley in leyes:
                ley_texto = f"{ley['nombre']} {ley['resumen']}"
                if ley_texto.strip() == law.strip():
                    return ley
        return None

    async def evaluar_debate(self, debate_sintetico: str, posturas_reales: dict):
        """
        Evalúa un debate sintético contra las posturas reales y devuelve el razonamiento y puntaje.
        """

        # Contexto para el LLM 
        context = [ 
            {
                "role": "user",
                "content": f"### Debate generado por agentes (sintético):\n{debate_sintetico}\n\n"
                           f"### Posturas reales por partido:\n{json.dumps(posturas_reales, indent=2)}\n\n"
                           f"Estructura la respuesta de la siguiente manera:\n\n"
                           f"1. Análisis detallado por agente:\n"
                           f"   - Para cada agente, analiza los argumentos del debate sintético y del debate real.\n"
                           f"   - Identifica similitudes y diferencias.\n"
                           f"   - Calcula un puntaje de similaridad por agente.\n"
                           f"2. Un párrafo general sobre el debate.\n"
                           f"3. Puntaje global del debate.\n"
            }
        ]

        response: EvaluadorResponse = await self.model.call_api(
            previous_rounds_context=context,
            pydantic_response_structure=EvaluadorResponse,
        )
        return response
    

    # def registrar_evaluacion(self, ley: str, razonamiento_general: str, analisis_por_agente: dict, puntaje_final: float):
    #     print(f"\nEvaluación para la ley: {ley}")
    #     print("\nAnálisis por agente:")
    #     for agente, analisis in analisis_por_agente.items():
    #         print(f"\n\n- {agente}:")
    #         print(f"  \nDebate sintético: {analisis.debate_sintetico}")
    #         print(f"  \nPostura real: {analisis.postura_real}")
    #         print(f"  \nSimilitudes: {analisis.similitudes}")
    #         print(f"  \nDiferencias: {analisis.diferencias}")
    #         print(f"  \nPuntaje: {analisis.puntaje}")

    #     print(f"\n\nRazón general:\n{razonamiento_general}")
    #     print(f"\nPuntaje final ajustado: {puntaje_final}")

    def registrar_evaluacion(self, ley: str, razonamiento_general: str, analisis_por_agente: dict, puntaje_final: float):
        resultado = f"\nEvaluación para la ley: {ley}\n"
        resultado += "\nAnálisis por agente:\n"
        for agente, analisis in analisis_por_agente.items():
            resultado += f"\n\n- {agente}:\n"
            resultado += f"  Debate sintético: {analisis.debate_sintetico}\n"
            resultado += f"  Postura real: {analisis.postura_real}\n"
            resultado += f"  Similitudes: {analisis.similitudes}\n"
            resultado += f"  Diferencias: {analisis.diferencias}\n"
            resultado += f"  Puntaje: {analisis.puntaje}\n"

        resultado += f"\n\nRazón general:\n{razonamiento_general}\n"
        resultado += f"\nPuntaje final ajustado: {puntaje_final}\n"
        resultado += f"{'-'*80}\n"

        # Imprimir en consola
        print(resultado)

        # Guardar en archivo evaluador.log (modo append)
        with open("evaluador.log", "w", encoding="utf-8") as f:
            f.write(resultado)



            
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