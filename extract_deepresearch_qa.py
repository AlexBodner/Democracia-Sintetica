import os
import json

def extract_deep_research_qa(debate_file):
    with open(debate_file, 'r', encoding='utf-8') as f:
        debate = json.load(f)
    if 'preguntas y respuestas deep research' in debate:
        return debate['preguntas y respuestas deep research']
    return None

def main():
    base_dirs = [
        'debates/con_research',
    ]
    qa_dict = {}
    for base_dir in base_dirs:
        for fname in os.listdir(base_dir):
            if not fname.endswith('.json'):
                continue
            debate_file = os.path.join(base_dir, fname)
            qa = extract_deep_research_qa(debate_file)
            if qa is not None:
                # Use debate id (number) as key, remove extension
                debate_id = os.path.splitext(fname)[0]
                qa_dict[debate_id] = qa
    output_path = 'deepresearch_qa_reports/deepresearch_qa_con_research.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(qa_dict, f, indent=2, ensure_ascii=False)
    print(f'Results saved to {output_path}')

if __name__ == "__main__":
    main()
