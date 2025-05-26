import json
from API_Model import API_Model
from debate_agents.response_structures import EvaluadorResponse

class AgenteEvaluador:
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
        context = [
            {
                "role": "user",
                "content": f"### Debate generado por agentes (sintético):\n{debate_sintetico}\n\n"
                           f"### Posturas reales por partido:\n{json.dumps(posturas_reales, indent=2)}",
            }
        ]

        response: EvaluadorResponse = await self.model.call_api(
            previous_rounds_context=context,
            pydantic_response_structure=EvaluadorResponse,
        )
        return response

    def registrar_evaluacion(self, ley: str, razonamiento: str, puntaje: float):
        """
        Imprime la evaluación en la consola.
        """
        print(f"Evaluación para la ley: {ley}")
        print(f"Razón: {razonamiento}")
        print(f"Puntaje: {puntaje}")

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
            self.registrar_evaluacion(ley["nombre"], response.razonamiento, response.puntaje)

        except Exception as e:
            print(f"Error al evaluar la ley {ley['nombre']}: {e}")