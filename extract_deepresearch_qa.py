import os
import json

def get_debate_files(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.json')]

def extract_deep_research_qa(debate_path):
    with open(debate_path, 'r', encoding='utf-8') as f:
        debate = json.load(f)
    print(debate.keys())
    return debate['preguntas y respuestas deep research']

def main():
    base_dirs = [
        'debates/con_research',
    ]
    output_dir = 'deepresearch_qa_reports'
    os.makedirs(output_dir, exist_ok=True)
    for base_dir in base_dirs:
        report_lines = []
        report_lines.append(f'--- Deep Research Q&A in {base_dir} ---\n')
        for debate_file in sorted(get_debate_files(base_dir)):
            qa = extract_deep_research_qa(debate_file)
            report_lines.append(f'Debate: {os.path.basename(debate_file)}')
            if qa:
                report_lines.append(qa.strip())
            else:
                report_lines.append('  [No deep research Q&A found]')
            report_lines.append('')
        out_file = os.path.join(output_dir, f'deepresearch_qa_{os.path.basename(base_dir)}.txt')
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        print(f'Results saved to {out_file}')

if __name__ == "__main__":
    main()
