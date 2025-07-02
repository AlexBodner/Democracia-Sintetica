# import json
# import matplotlib.pyplot as plt
# import os
# import numpy as np
# from matplotlib.patches import Patch

# # Archivos de resultados
# archivos = [
#     "resultados_8values.json",
#     "resultados_8values_agente_turbo.json"
# ]

# # Cargar resultados de ambos archivos
# def cargar_resultados(archivos):
#     resultados = {}
#     for archivo in archivos:
#         ruta = os.path.join(os.path.dirname(__file__), archivo)
#         with open(ruta, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             resultados.update(data)
#     return resultados

# resultados = cargar_resultados(archivos)

# # Ejes a graficar
# EJES = ["econ", "dipl", "govt", "scty"]
# NOMBRES_EJES = {
#     "econ": "Económico",
#     "dipl": "Diplomático",
#     "govt": "Gobierno",
#     "scty": "Sociedad"
# }

# # Asignar un color único a cada agente
# from itertools import cycle
# import matplotlib.colors as mcolors

# # Usar una paleta de colores tab10 extendida
# colores_base = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
# colores = cycle(colores_base)
# agentes = list(resultados.keys())
# agente_color = {agente: next(colores) for agente in agentes}

# # Crear leyenda arriba de todo
# legend_patches = [Patch(color=agente_color[agente], label=agente) for agente in agentes]

# # Crear la figura
# fig, ax = plt.subplots(figsize=(12, 6))
# plt.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=3, fontsize=9, frameon=False)

# # Espaciado entre barras
# bar_width = 0.5
# bar_positions = np.arange(len(EJES)) * 2  # Espaciado mayor entre barras

# # Graficar barras por tramos de color puro
# for i, eje in enumerate(EJES):
#     # Obtener los puntajes y colores de los agentes para este eje
#     agentes_y_puntajes = sorted([(agente, datos["puntaje"][eje]) for agente, datos in resultados.items()], key=lambda x: x[1])
#     # Agregar 0 y 100 para cubrir toda la barra
#     tramos = [(0, agentes_y_puntajes[0][1], 'lightgray')]
#     for idx, (agente, puntaje) in enumerate(agentes_y_puntajes):
#         color = agente_color[agente]
#         if idx < len(agentes_y_puntajes) - 1:
#             next_puntaje = agentes_y_puntajes[idx+1][1]
#         else:
#             next_puntaje = 100
#         tramos.append((puntaje, next_puntaje, color))
#     # Dibujar cada tramo
#     for start, end, color in tramos:
#         height = end - start
#         if height > 0:
#             ax.bar(bar_positions[i], height, bottom=start, width=bar_width, color=color, edgecolor="k", alpha=1)

# # Etiquetas y formato
# ejes_labels = [NOMBRES_EJES[e] for e in EJES]
# ax.set_xticks(bar_positions)
# ax.set_xticklabels(ejes_labels, fontsize=12)
# ax.set_ylabel("Puntaje (0-100)", fontsize=12)
# ax.set_title("Resultados 8values por eje y agente", fontsize=14, pad=40)
# ax.set_ylim(0, 105)
# plt.tight_layout(rect=[0, 0, 1, 0.95])
# plt.show()


import json
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.patches import Patch

# Archivos de resultados
archivos = [
    "resultados_8values.json",
    "resultados_8values_agente_turbo.json",
    "resultados_8values_agente_grok.json", 
    "resultados_8values_agente_DeepSeek.json" 
]

# Cargar resultados de ambos archivos
def cargar_resultados(archivos):
    resultados = {}
    for archivo in archivos:
        ruta = os.path.join(os.path.dirname(__file__), 'resultados',archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
            resultados.update(data)
    return resultados

resultados = cargar_resultados(archivos)

# Ejes a graficar
EJES = ["econ", "dipl", "govt", "scty"]
NOMBRES_EJES = {
    "econ": "Económico",
    "dipl": "Diplomático",
    "govt": "Gobierno",
    "scty": "Sociedad"
}

# Asignar un color único a cada agente
from itertools import cycle
import matplotlib.colors as mcolors

# Usar una paleta de colores tab10 extendida
colores_base = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
colores = cycle(colores_base)
agentes = list(resultados.keys())
agente_color = {agente: next(colores) for agente in agentes}

# Crear leyenda arriba de todo
legend_patches = [Patch(color=agente_color[agente], label=agente) for agente in agentes]

# Crear la figura
fig, ax = plt.subplots(figsize=(12, 6))
plt.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=3, fontsize=9, frameon=False)

# Espaciado entre barras
bar_width = 0.7
bar_positions = np.arange(len(EJES))  # Barras juntas

# Graficar barras base en gris claro
for i, eje in enumerate(EJES):
    ax.bar(bar_positions[i], 100, bottom=0, width=bar_width, color='lightgray', edgecolor="k", alpha=1)
    # Para cada agente, dibujar una línea gruesa en su puntaje
    for agente in agentes:
        puntaje = resultados[agente]["puntaje"][eje]
        color = agente_color[agente]
        ax.plot([bar_positions[i] - bar_width/2, bar_positions[i] + bar_width/2], [puntaje, puntaje], color=color, lw=5, solid_capstyle='round', label=agente)

# Etiquetas y formato
ejes_labels = [NOMBRES_EJES[e] for e in EJES]
ax.set_xticks(bar_positions)
ax.set_xticklabels(ejes_labels, fontsize=12)
ax.set_ylabel("Puntaje (0-100)", fontsize=12)
ax.set_title("Resultados 8values por eje y agente", fontsize=14, pad=60)
ax.set_ylim(0, 105)
plt.subplots_adjust(top=0.75, bottom=0.12)  # Más espacio arriba y abajo
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.show()

# ====== SEGUNDO GRÁFICO ESTILO 8VALUES ======

# Definir colores y etiquetas para los extremos de cada eje
EXTREMOS = {
    "econ": {"izq": ("#888888", "EQUALITY"), "der": ("#111111", "MARKETS")},
    "dipl": {"izq": ("#888888", "NATION"), "der": ("#111111", "WORLD")},
    "govt": {"izq": ("#888888", "LIBERTY"), "der": ("#111111", "AUTHORITY")},
    "scty": {"izq": ("#888888", "TRADITION"), "der": ("#111111", "PROGRESS")},
}

fig2, axes2 = plt.subplots(len(EJES), 1, figsize=(10, 7), gridspec_kw={'hspace': 1.1})

# Agregar leyenda de agentes arriba del segundo gráfico
fig2.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=3, fontsize=9, frameon=False)

for i, eje in enumerate(EJES):
    ax2 = axes2[i]
    # Barra base: dos colores, mitad y mitad (gris y negro)
    left_color, left_label = EXTREMOS[eje]["izq"]
    right_color, right_label = EXTREMOS[eje]["der"]
    ax2.barh(0, 50, left=0, height=0.5, color=left_color, edgecolor="k")
    ax2.barh(0, 50, left=50, height=0.5, color=right_color, edgecolor="k")
    # Líneas de agentes
    for agente in agentes:
        puntaje = resultados[agente]["puntaje"][eje]
        puntaje = 100 - puntaje
        color = agente_color[agente]
        ax2.plot([puntaje, puntaje], [-0.25, 0.25], color=color, lw=5, solid_capstyle='round')
    # Etiquetas de extremos
    ax2.text(0, 0.35, left_label, color=left_color, fontsize=13, fontweight='bold', ha='left', va='center')
    ax2.text(100, 0.35, right_label, color=right_color, fontsize=13, fontweight='bold', ha='right', va='center')
    # Título del eje
    ax2.set_title(NOMBRES_EJES[eje], fontsize=14, pad=10)
    # Etiquetas de porcentaje
    ax2.set_xlim(0, 100)
    ax2.set_ylim(-0.5, 0.7)
    ax2.set_yticks([])
    ax2.set_xticks([0, 25, 50, 75, 100])
    ax2.set_xticklabels(["0", "25", "50", "75", "100"], fontsize=10)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_linewidth(1.5)

plt.subplots_adjust(top=0.93, bottom=0.05, hspace=1.1)
plt.suptitle("Resultados 8values", fontsize=16, y=0.99)
fig2.savefig("8values_barras_horizontales.png", dpi=300, bbox_inches="tight")
plt.show()

