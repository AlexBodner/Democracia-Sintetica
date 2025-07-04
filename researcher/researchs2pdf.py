import os
from pathlib import Path
from fpdf import FPDF
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
    try:
        text = text.encode('latin-1', errors='ignore').decode('latin-1')
    except Exception:
        pass
    return text

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 18)
        self.set_text_color(0, 70, 140)
        self.cell(0, 12, 'Informe de Deep Research', ln=1, align='C')
        self.ln(2)
        self.set_text_color(0, 0, 0)
    def markdown(self, md):
        for line in md.split('\n'):
            if line.startswith('# '):
                self.set_font('Arial', 'B', 16)
                self.set_text_color(0, 70, 140)
                self.multi_cell(0, 10, clean_text(line[2:].strip()))
                self.set_text_color(0, 0, 0)
            elif line.startswith('## '):
                self.set_font('Arial', 'B', 14)
                self.set_text_color(0, 70, 140)
                self.multi_cell(0, 9, clean_text(line[3:].strip()))
                self.set_text_color(0, 0, 0)
            elif line.startswith('### '):
                self.set_font('Arial', 'B', 12)
                self.set_text_color(0, 70, 140)
                self.multi_cell(0, 8, clean_text(line[4:].strip()))
                self.set_text_color(0, 0, 0)
            elif line.startswith('- '):
                self.set_font('Arial', '', 12)
                self.cell(5)
                self.multi_cell(0, 8, clean_text(u'- ' + line[2:]))
            elif line.strip() == '':
                self.ln(2)
            else:
                self.set_font('Arial', '', 12)
                self.multi_cell(0, 8, clean_text(line))
        self.ln(2)

def research2pdf(md_path, out_path):
    with open(md_path, encoding='utf-8') as f:
        md = f.read()
    pdf = PDF()
    pdf.add_page()
    pdf.markdown(md)
    pdf.output(out_path)

def main():
    base = Path('researchs')
    out_base = Path('..') / 'researchs_pdfs'
    out_base.mkdir(exist_ok=True)
    for txt_file in base.glob('*.txt'):
        ley_num = txt_file.stem
        out_pdf = out_base / f'{ley_num}.pdf'
        research2pdf(txt_file, out_pdf)
        print(f'PDF generado: {out_pdf}')

if __name__ == '__main__':
    main()
