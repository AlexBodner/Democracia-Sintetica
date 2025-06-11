import json
from API_Model import API_Model
from response_structures import LeyResponse


class SepararArgumentos:
    def __init__(self, system_prompt: str):
        self.model = API_Model(system_prompt={"role": "system", "content": system_prompt})
        self.system_prompt = {"role": "system", "content": system_prompt}
        with open('testing/leyes_limpias.json', 'r') as file:
            self.leyes = json.load(file)
        with open('testing/leyes_limpias_lista_argumentos.json', 'r') as file:
            self.few_shot_example = json.load(file)
        self.output_file = 'testing/leyes_limpias_procesadas.json'
        # Inicializar el archivo de salida si no existe
        try:
            with open(self.output_file, 'r') as file:
                self.leyes_procesadas = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.leyes_procesadas = []
            with open(self.output_file, 'w') as file:
                json.dump(self.leyes_procesadas, file, indent=4, ensure_ascii=False)

    async def procesar_argumentos(self, ley):
        prompt = f"""
        A continuación, se presenta un ejemplo de cómo transformar una ley con argumentos en texto plano a una ley con argumentos separados en listas por agente.

        El único campo que debes modificar es `posturas`. Cada valor en `posturas` debe contener:
        - `argumentacion`: una **lista de strings**, cada uno representando un argumento único expresado por el agente.
        - `voto`: un **string** que indique la postura del agente (por ejemplo: "A favor", "En contra", etc.).

        ⚠️ Asegúrate de que la respuesta conserve **todos los campos originales** de la ley y cumpla con el siguiente formato:

        - `id`: entero
        - `nombre`: string
        - `año`: entero
        - `estado`: string
        - `resumen`: string
        - `posturas`: diccionario de agentes con `argumentacion: List[str]` y `voto: str`
        - `resultado_final`: string

        ❗ No cambies los nombres de los campos ni su tipo de dato. La estructura debe ser exactamente la misma, solo modificando el contenido del campo `posturas`.

        Ejemplo:
        Ley antes:
        {json.dumps(self.leyes[0], indent=4)}

        Ley después:
        {json.dumps(self.few_shot_example, indent=4)}

        Ahora, realiza la misma transformación para la siguiente ley:
        {json.dumps(ley, indent=4)}
        """
        response = await self.model.call_api(
            previous_rounds_context=[{"role": "user", "content": prompt}],
            pydantic_response_structure=LeyResponse, 
        )
        return response


    async def procesar_todas_las_leyes(self):
        for ley in self.leyes:
            # Verificar si la ley ya fue procesada
            if any(procesada['id'] == ley['id'] for procesada in self.leyes_procesadas):
                continue
            try:
                ley_procesada = await self.procesar_argumentos(ley)
                self.leyes_procesadas.append(ley_procesada.model_dump())
                print(f"Procesada ley {ley['id']} con éxito.")
                # Guardar la ley procesada en el archivo JSON
                with open(self.output_file, 'w') as file:
                    json.dump(self.leyes_procesadas, file, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Error procesando la ley {ley['id']}: {e}")

# Ejecutar el procesamiento
async def main():
    system_prompt = "Transforma leyes con argumentos en texto plano a argumentos separados en listas por agente."
    separador = SepararArgumentos(system_prompt=system_prompt)
    await separador.procesar_todas_las_leyes()

# Para ejecutar el script
import asyncio
asyncio.run(main())
