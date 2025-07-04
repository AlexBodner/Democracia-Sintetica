import requests
from bs4 import BeautifulSoup
import json
import re
import time

# URL de la página a scrapear
URL = "https://palabrasdelderecho.com.ar/articulo/1454/Cincuenta-decretos-de-Alberto-Fernandez"

# Descargar el HTML de la página
response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

# Buscar todos los enlaces a PDF en la página
pdf_links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.lower().endswith(".pdf"):
        pdf_links.append((a.text.strip(), href))

# Si no hay PDFs directos, buscar links a Infoleg o Boletín Oficial
if not pdf_links:
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ("infoleg" in href or "boletinoficial" in href) and ("decreto" in href or "normativa" in href):
            pdf_links.append((a.text.strip(), href))

# Extraer los decretos de las tablas de la página
decretos = []
table_rows = soup.find_all("tr")
for row in table_rows:
    cols = row.find_all("td")
    if len(cols) >= 2:
        decreto = cols[1].text.strip()
        nombre = cols[2].text.strip() if len(cols) > 2 else ""
        # Buscar link asociado al decreto
        link = None
        for a in cols[1].find_all("a", href=True):
            link = a["href"]
            break
        # Si no hay link en la tabla, buscar en los links recolectados
        if not link:
            for n, l in pdf_links:
                if decreto in n or decreto in l:
                    link = l
                    break
        # Generar un id único (por ejemplo, el número de decreto)
        match = re.search(r"(\d+/\d+)", decreto)
        id_ = match.group(1) if match else decreto
        decretos.append({
            "decreto": link if link else decreto,
            "nombre": nombre,
            "id": id_
        })

# Función para extraer el texto completo de la Boletín Oficial
def extract_boletinoficial_text(url):
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        # El texto suele estar en un div con class 'texto-dinamico' o similar
        main_text = soup.find('div', class_='texto-dinamico')
        if main_text:
            return main_text.get_text(separator='\n', strip=True)
        # Si no, buscar el texto más largo en la página
        paragraphs = soup.find_all(['p', 'div'])
        max_text = max((p.get_text(separator='\n', strip=True) for p in paragraphs), key=len, default=None)
        return max_text if max_text else "NO SE ENCONTRÓ TEXTO"
    except Exception as e:
        return f"ERROR AL EXTRAER TEXTO: {e}"

# Nueva lista para los decretos con texto completo y id secuencial
full_decretos = []
for idx, dec in enumerate(decretos, 1):
    link = dec["decreto"]
    nombre = dec["nombre"]
    # Si el link es de boletinoficial.gob.ar, extraer el texto
    if isinstance(link, str) and "boletinoficial.gob.ar" in link:
        texto = extract_boletinoficial_text(link)
        time.sleep(1)  # Para evitar rate limiting
    else:
        texto = link  # Si no es link, dejar el texto original
    full_decretos.append({
        "decreto": texto,
        "nombre": nombre,
        "id": idx
    })

with open("dataset/decretos.json", "w", encoding="utf-8") as f:
    json.dump(full_decretos, f, ensure_ascii=False, indent=2)

print(f"Extraídos {len(full_decretos)} decretos con texto completo y guardados en dataset/decretos.json")
