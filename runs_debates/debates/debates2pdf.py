import os
import json
from pathlib import Path
from fpdf import FPDF

# Mapeo de agentes y votos
AGENTE_MAP = {
    'Agente Liberal': 'LLA',
    'Agente de Juntos Por El Cambio': 'JxC',
    'Agente de Union Por La Patria': 'UxP',
    'Agente de Izquierda': 'FIT'
}
VOTO_MAP = {
    0: 'en contra',
    1: 'crítico',
    2: 'dividido',
    3: 'apoyo crítico',
    4: 'a favor'
}

# Cargar leyes
with open(r'C:\Users\delfi\OneDrive\Documents\Universidad\Democracia-Sintetica\dataset\leyes.json', encoding='utf-8') as f:
    leyes = {str(ley['id']): ley for ley in json.load(f)}

def get_ley_info(ley_id):
    ley = leyes.get(str(ley_id))
    if not ley:
        return f"Ley {ley_id}", "Sin resumen disponible."
    return ley['nombre'], ley['resumen']

import re
def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        '\u2013': '-',  # guion corto
        '\u2014': '-',  # guion largo
        '\u2018': "'", # comilla simple izq
        '\u2019': "'", # comilla simple der
        '\u201c': '"', # comilla doble izq
        '\u201d': '"', # comilla doble der
        '\u2022': '-',  # bullet
        '\u2026': '...', # puntos suspensivos
        '\u00a0': ' ',   # espacio no separable
    }
    for k, v in replacements.items():
        text = text.replace(k.encode('utf-8').decode('unicode_escape'), v)
    text = text.replace('Agente Liberal', 'Agente LLA')
    text = text.replace('Agente Centro-Derecha', 'Agente JxC')
    text = text.replace('Agente de Juntos Por El Cambio', 'Agente JxC')
    text = text.replace('Agente Centro-Izquierda', 'Agente UxP')
    text = text.replace('Agente de Union Por La Patria', 'Agente UxP')
    text = text.replace('Agente Izquierda', 'Agente FIT')
    text = text.replace('Agente de Izquierda', 'Agente FIT')
    # Permitir letras latinas con tildes y ñ (latin-1)
    # Elimina solo lo que no es latin-1
    try:
        text = text.encode('latin-1', errors='ignore').decode('latin-1')
    except Exception:
        pass
    return text

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 70, 140)
        self.cell(0, 12, 'DemocracIA Sintética', ln=1, align='C')
        self.ln(2)
        self.set_text_color(0, 0, 0)
    def ley_bullet(self, nombre, resumen):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, f'Nombre de la ley:', ln=1)
        self.set_font('Arial', '', 14)
        self.multi_cell(0, 9, clean_text(nombre))
        self.ln(1)
        self.set_font('Arial', 'B', 13)
        self.cell(0, 8, f'Resumen de la ley:', ln=1)
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 8, clean_text(resumen))
        self.ln(2)
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 70, 140)
        self.cell(0, 10, clean_text(title), ln=1)
        self.set_text_color(0, 0, 0)
        self.ln(2)
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 8, clean_text(body))
        self.ln(2)
    def agent_block(self, agente, short, arg, voto):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 70, 140)
        self.cell(0, 8, f"Agente {short} ({agente}):", ln=1)
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 8, clean_text(arg))
        self.set_font('Arial', 'I', 11)
        self.cell(0, 7, f"Voto: {voto}", ln=1)
        self.ln(1)
    def markdown(self, md):
        # Simple markdown to PDF (bold, lists, etc.)
        for line in md.split('\n'):
            if line.startswith('####'):
                self.set_font('Arial', 'B', 12)
                self.set_text_color(0, 70, 140)
                self.cell(0, 8, clean_text(line.replace('####', '').strip()), ln=1)
                self.set_text_color(0, 0, 0)
            elif line.startswith('###'):
                self.set_font('Arial', 'B', 12)
                self.set_text_color(0, 70, 140)
                self.cell(0, 8, clean_text(line.replace('###', '').strip()), ln=1)
                self.set_text_color(0, 0, 0)
            elif line.startswith('- '):
                self.set_font('Arial', '', 12)
                self.cell(5)
                self.cell(0, 8, clean_text(u'- ' + line[2:]), ln=1)
            else:
                self.set_font('Arial', '', 12)
                self.multi_cell(0, 8, clean_text(line))
        self.ln(2)

def debate2pdf(debate_path, ley_id, out_pdf):
    with open(debate_path, encoding='utf-8') as f:
        debate = json.load(f)
    nombre_ley, resumen_ley = get_ley_info(ley_id)
    pdf = PDF()
    pdf.add_page()
    pdf.ley_bullet(nombre_ley, resumen_ley)
    pdf.chapter_title('Simulacion del debate')
    for round_n in range(3):
        round_key = f'Round {round_n}'
        if round_key not in debate:
            continue
        pdf.chapter_title(f'Round {round_n}')
        ronda = debate[round_key]
        for agente, short in AGENTE_MAP.items():
            if agente in ronda:
                arg = ronda[agente]['argumentacion']
                voto = VOTO_MAP.get(ronda[agente]['voto'], str(ronda[agente]['voto']))
                pdf.agent_block(agente, short, arg, voto)
    if 'Resumen final' in debate:
        pdf.chapter_title('Resumen del reviewer')
        pdf.markdown(debate['Resumen final'])
    pdf.output(out_pdf)

def main():
    # Cambia estos nombres si tienes otras carpetas
    for tipo in ['sin_research', 'con_research']:
        base = Path(tipo)
        out_base = Path('..') / 'debates_pdfs' / tipo
        for ley_dir in sorted(base.iterdir()):
            if not ley_dir.is_dir() or not ley_dir.name.startswith('ley_'):
                continue
            ley_id = ley_dir.name.split('_')[-1]
            out_ley_dir = out_base / ley_dir.name
            out_ley_dir.mkdir(parents=True, exist_ok=True)
            for i in range(5):
                debate_file = ley_dir / f'debate_{i}.json'
                if not debate_file.exists():
                    continue
                out_pdf = out_ley_dir / f'debate_{i}.pdf'
                debate2pdf(debate_file, ley_id, out_pdf)
                print(f'PDF generado: {out_pdf}')

if __name__ == '__main__':
    main()
