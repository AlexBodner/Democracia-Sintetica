key = "a44bce33a7cc6234f7fd5ec6084a446260289206"

import http.client
import json

conn = http.client.HTTPSConnection("google.serper.dev")
payload = json.dumps({
  "q": "Como salio river?",
  "gl": "ar"
})
headers = {
  'X-API-KEY': key,
  'Content-Type': 'application/json'
}
conn.request("POST", "/search", payload, headers)
res = conn.getresponse()
data = res.read()
print(data  )
print("----------------------")
print(json.loads(data)["organic"])

import requests

busqueda = [{'title': 'River Plate Resultados, estadísticas y highlights - ESPN (AR)', 'link': 'https://www.espn.com.ar/futbol/equipo//id/16/river-plate', 'snippet': 'Visita ESPN (AR) y disfruta de resultados en vivo, highlights y las últimas noticias de River Plate. Conoce la tabla de posiciones y el calendario completo ...', 'sitelinks': [{'title': 'Calendario', 'link': 'https://www.espn.com.ar/futbol/equipo/calendario//id/16/arg.river_plate'}, {'title': 'Plantel', 'link': 'https://www.espn.com.ar/futbol/equipo/plantel//id/16/arg.river_plate'}, {'title': 'Estadísticas', 'link': 'https://www.espn.com.ar/futbol/equipo/estadisticas//id/16/river-plate'}], 'position': 1}, {'title': 'River Plate - Sitio Oficial', 'link': 'https://www.cariverplate.com.ar/', 'snippet': 'En una noche de goles y fiesta de Copa en el Mâs Monumental, el equipo de Marcelo Gallardo venció 6-2 a Independiente del Valle y se adueñó de la zona una fecha ...', 'sitelinks': [{'title': 'Museo River', 'link': 'https://www.cariverplate.com.ar/museo-river'}, {'title': 'River Plate', 'link': 'https://www.cariverplate.com.ar/en'}, {'title': 'Integridad river', 'link': 'https://www.cariverplate.com.ar/integridad-river'}, {'title': 'River Internacional', 'link': 'https://www.cariverplate.com.ar/river-internacional'}], 'position': 2}, {'title': 'River Plate (@RiverPlate) / X', 'link': 'https://x.com/riverplate', 'snippet': 'Cuenta oficial del Club Atlético River Plate. Vivir y jugar con Grandeza.', 'position': 3}, {'title': 'RIVER 3 - 0 BARRACAS CENTRAL I Resumen del partido - YouTube', 'link': 'https://www.youtube.com/watch?v=fARX5FKSJXM', 'snippet': 'El Millonario goleó y enfrentará a Platense! River derrotó 3 a 0 a Barracas Central con goles de Díaz, Fernández y Acuña por los ...', 'date': '8 days ago', 'position': 4}, {'title': '¿Cómo salió River hoy? Resultado del partido vs. Independiente del ...', 'link': 'https://www.sportingnews.com/ar/futbol/news/%C2%BFc%C3%B3mo-sali%C3%B3-river-hoy-resultado-del-partido-vs-platense/sgqe3avtlxo6yjvpm9u3dvvz', 'snippet': 'River goleó a Independiente del Valle por 6 a 2 y con ello selló su clasificación a octavos de final de la Copa Libertadores 2025.', 'date': '5 days ago', 'position': 5}, {'title': 'Otro show de River: goleada a Independiente del Valle, quinto ... - Olé', 'link': 'https://www.ole.com.ar/futbol-internacional/libertadores/river-vs-independiente-valle-vivo-partido-copa-libertadores-2025-fecha-5_0_j8qPhd7G0n.html', 'snippet': 'El Millonario derrotó 6-2 al equipo ecuatoriano y consiguió un triunfazo para asegurarse ganar el Grupo B.', 'date': '5 days ago', 'position': 6}, {'title': 'River Plate - Últimas Noticias :: Olé - ole.com.ar', 'link': 'https://www.ole.com.ar/river-plate', 'snippet': 'River · A la espera de River - Platense, los cuartos de final son de los visitantes · Cuándo se jugarían las semifinales del Torneo Apertura · A qué hora juega ...', 'position': 7}, {'title': 'La Página Millonaria: Últimas noticias de River Plate', 'link': 'https://lapaginamillonaria.com/', 'snippet': 'Goles de River. VIDEOS | Los goles de River para el 6-2 vs. IDV. Copa Libertadores ; Marcelo Gallardo. Con tres cambios, el posible once de River ante Platense.', 'sitelinks': [{'title': 'Ex-River', 'link': 'https://lapaginamillonaria.com/tema/ex-river'}, {'title': 'River Plate', 'link': 'https://lapaginamillonaria.com/river-plate/con-kevin-castano-cuales-son-las-compras-mas-caras-de-la-historia-de-river'}, {'title': 'Próximo partido de River', 'link': 'https://lapaginamillonaria.com/copa-de-la-liga-profesional/segui-en-vivo-river-vs-talleres-de-cordoba-por-el-torneo-apertura-2025-con-los-relatos-de-lito-costa-febre'}, {'title': 'Los puntajes de River vs...', 'link': 'https://lapaginamillonaria.com/copa-libertadores/los-puntajes-de-river-vs-barcelona-sc-jugador-x-jugador'}], 'position': 8}, {'title': 'Noticias sobre River Plate hoy martes 20 de mayo - El Comercio Perú', 'link': 'https://elcomercio.pe/noticias/river-plate/', 'snippet': 'River vs. Barracas (3-0): resumen y goles del partido por Torneo Apertura | VIDEO. River derrotó 3-2 a Barracas en el Más Monumental por los octavos de final ...', 'position': 9}, {'title': 'River ganó y se mantiene en lo más alto', 'link': 'https://www.cariverplate.com.ar/river-gano-y-se-mantiene-en-lo-mas-alto', 'snippet': 'El equipo de Martín Demichelis generó muchas situaciones frente a Unión, se impuso 1-0 en el Mâs Monumental con un golazo de Nacho Fernández y sigue arriba.', 'position': 10}]

for i in range(5):
    link = busqueda[i]["link"]
    data = requests.get(link) 
    if data.status_code ==200:
        print("hola")
        #print(data.text)
