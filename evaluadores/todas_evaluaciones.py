import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from evaluadores.llm_judge_agentes import main as judge_main

def main():
    with open("testing/leyes.json", "r", encoding="utf-8") as f:
        leyes = json.load(f)

    evaluaciones = [judge_main]
    for ley in leyes:
        for evaluacion in evaluaciones:
            asyncio.run( evaluacion(f"debates/debate_{ley['id']}.json", ley, n_rounds=3, output_folder="evaluaciones"))

if __name__ == "__main__":
    main()