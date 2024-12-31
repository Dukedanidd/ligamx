from flask import Flask, render_template, jsonify
import pandas as pd
import requests
import time
import schedule
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Cargamos las variables de entorno
load_dotenv('.env')

# Configuracion de la API
API_KEY = os.getenv('API_KEY')
API_HOST = os.getenv('API_HOST')

# Verificar que las variables de entorno se cargaron correctamente
if not API_KEY or not API_HOST:
    raise ValueError("Error: No se pudieron cargar API_KEY o API_HOST desde el archivo .env")

LEAGUE_ID = 262
SEASON = '2024'

url = f"https://{API_HOST}/v3/standings"

headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': API_HOST
}
querystring = {'league': LEAGUE_ID, 'season': SEASON}

# Funcion para obtener los datos de la API
def fetch_standings():
    try:
        # Enviamos la solicitud a la API
        response = requests.get(url, headers=headers, params=querystring)
        
        # Verificamos que la solicitud fue exitosa
        response.raise_for_status()
        
        # Imprimimos la respuesta para debug
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        # Obtenemos los datos de la API y la convertimos a JSON
        data = response.json()
        
        # Verificamos la estructura de la respuesta
        if not data.get('response'):
            print(f"Respuesta inesperada de la API: {data}")
            return
            
        if not data['response'] or not data['response'][0].get('league'):
            print(f"No se encontraron datos de la liga: {data}")
            return
        
        # Obtenemos los datos de la tabla de posiciones
        standings = data['response'][0]['league']['standings'][0]
        
        # Creamos una lista con los datos de la tabla de posiciones
        standings_data = [
            {
                "Posición": team['rank'],
                "Equipo": team['team']['name'],
                "Puntos": team['points'],
                "Partidos Jugados": team['all']['played'],
                "Victorias": team['all']['win'],
                "Empates": team['all']['draw'],
                "Derrotas": team['all']['lose']
            }
            for team in standings
        ]
        
        # Convertimos la lista a un DataFrame
        df = pd.DataFrame(standings_data)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

# Funcion para crear un grafico de la tabla de posiciones
def create_graph(df):
    """Crea un gráfico de barras de los puntos de cada equipo."""
    try:
        df_sorted = df.sort_values(by="Posición")
        equipos = df_sorted["Equipo"]
        puntos = df_sorted["Puntos"]
        
        # Creamos el grafico
        plt.figure(figsize=(10, 6))
        plt.bar(equipos, puntos, color='skyblue')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel("Equipos")
        plt.ylabel("Puntos")
        plt.title("Tabla de posiciones - Liga MX")
        plt.tight_layout()
        
        # Guardamos en static para que Flask pueda servirlo
        plt.savefig("static/liga_mx_standings_graph.png")
        plt.close()  # Importante cerrar la figura
        
    except Exception as e:
        print(f"Error al generar el gráfico: {e}")

@app.route('/')
def index():
    df = fetch_standings()
    if df is not None:
        # Crear el gráfico
        create_graph(df)
        
        # Convertir DataFrame a HTML con clases personalizadas
        tabla_html = df.to_html(
            classes='table table-hover table-striped',
            index=False,
            table_id='standings-table',
            escape=False
        )
        
        # Modificar el HTML para agregar las clases de posición a las filas
        tabla_html = tabla_html.replace('<tr>', lambda x: '<tr class="{}">'.format(
            'libertadores' if df.iloc[len(df.index) - 1]['Posición'] <= 4
            else 'liguilla' if df.iloc[len(df.index) - 1]['Posición'] <= 12
            else 'descenso'
        ))
        
        # Aplicar formato personalizado a las celdas
        tabla_html = tabla_html.replace('<td>', '<td class="text-center">')
        tabla_html = tabla_html.replace(
            '<td class="text-center">',
            lambda x: '<td class="team-name text-start">',
            1  # Solo reemplazar la primera ocurrencia (columna Equipo)
        )
        
        return render_template('index.html', tabla=tabla_html)
    return "Error al obtener los datos"

if __name__ == "__main__":
    # Asegurarse de que existe el directorio static
    os.makedirs('static', exist_ok=True)
    app.run(debug=True)
