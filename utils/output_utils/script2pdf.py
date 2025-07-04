import json
import markdown
from weasyprint import HTML

# Cargar el resumen desde el JSON
with open("evaluaciones/debate_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

resumen_markdown = data["Resumen final"]

# Convertir Markdown a HTML
html_content = markdown.markdown(resumen_markdown, extensions=["extra"])

# Opcional: agregar CSS para estilos
html_template = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resumen del Debate</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }}
        h1, h2, h3, h4 {{
            color: #2e3d49;
        }}
        ul {{
            list-style-type: disc;
            margin-left: 20px;
        }}
        p {{
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

# Guardar el PDF
HTML(string=html_template).write_pdf("resumen_debate.pdf")
