from flask import Flask, render_template, request
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# grafica a imagen , luego a imagen binario
from io import BytesIO
# luego convertir la imagen a base 64
import base64
# manejo de archivos mas facilmente , como una base del S.O
import os
app = Flask(__name__) #Se crea una instancia de la clase Flask y se le pasa __name__, que es una variable especial de Python que representa el nombre del módulo actual. 

def cargar_datos_renovables(ruta_csv):
    datos=[]
    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as archivo_csv:
            
            lector = csv.DictReader(archivo_csv)
            for fila in lector:
                datos.append({
                    'entity': fila['Entity'],
                    'code': fila['Code'],
                    'year': int(fila['Year']),
                    'renewables': float(fila['Renewables (% equivalent primary energy)'])
                })
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
    return datos

RUTA_CSV = 'static/archivo/data.csv'
datos_renovables = cargar_datos_renovables(RUTA_CSV)

DATA_DIR = 'static/archivo/'
FILES = {
    'Wind' : ('08 wind-generation.csv', 'Electricity from wind (TWh)'),
    'Solar' : ('12 solar-energy-consumption.csv', 'Electricity from solar (TWh)'),
    'Hydropower' : ('05 hydropower-consumption.csv', 'Electricity from hydro (TWh)'),
    'Biofuels' : ('16 biofuel-production.csv', 'Biofuels Production - TWh - Total'),
    'Geothermal' : ('17 installed-geothermal-capacity.csv', 'Geothermal Capacity')
}

def load_data():
    data = {}
    for key, (file_name, column) in FILES.items():
        # acceder a ese archivo con la info de arriba
        # abrir esos arhivos en el dataname
        # abra el archivo en el directorio data
        file_path =os.path.join(DATA_DIR, file_name)
        # si la variablle existe le manda ese archivo a pandas para que lo lea
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            total_production = df[column].sum()
            data[key] = total_production
    return data

@app.route('/', methods=['GET', 'POST'])#@app.route('/'): Este es un decorador que se usa para vincular una URL (en este caso, la raíz '/') con una función. La función index() se ejecutará cuando un usuario acceda a la raíz de la aplicación.

def index():
    porcentaje_renovable = None
    error = None

    #---------------Gráfica de barras-----------
    data = load_data()
    # permite crear varias formas de gráfico, recopila toda la info en una tabla virtual
    plt.subplots(figsize = (3, 2))
    # alias a la info 
    df = pd.DataFrame(list(data.items()),columns = ['Fuente', 'Producción (TWh)'])    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize = (5, 4))
    ax.bar(df['Fuente'], df['Producción (TWh)'], color = ['blue', 'orange', 'green', 'red', 'purple'])

    ax.set_title('Producción de Energía renovable por Fuente', fontsize = 12)
    ax.set_xlabel('Fuente de Energía', fontsize = 12)
    ax.set_ylabel('Producción (TWh)', fontsize = 12)
    # convertir gráfica en imagen

    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format = 'png')
    img.seek(0)
    # pasar la imagen codificada
    graph_url = base64.b64encode(img.getvalue()).decode('utf-8')

    #-----------FIN GRÁFICA DE BARRAS-----------
    #---------------Gráfica de barras-----------
    df_renewables = pd.read_csv('static/archivo/04 share-electricity-renewables.csv')
    df_wind = pd.read_csv('static/archivo/11 share-electricity-wind.csv')
    df_solar = pd.read_csv('static/archivo/15 share-electricity-solar.csv')
    df_hydro = pd.read_csv('static/archivo/07 share-electricity-hydro.csv')

    year = df_renewables['Year'].max()
    renewables_data = df_renewables[df_renewables['Year'] == year]

    wind_data = df_wind[df_wind['Year'] == year]
    solar_data = df_solar[df_solar['Year'] == year]
    hydro_data = df_hydro[df_hydro['Year'] == year]

    df = pd.merge(renewables_data[['Entity','Renewables (% electricity)']], wind_data[['Entity', 'Wind (% electricity)']], on = 'Entity')

    df = pd.merge(df, solar_data[['Entity', 'Solar (% electricity)']], on = 'Entity')
    df = pd.merge(df, hydro_data[['Entity', 'Hydro (% electricity)']], on = 'Entity')

    wind_percentage = df['Wind (% electricity)'].values[0]
    solar_percentage = df['Solar (% electricity)'].values[0]
    hydro_percentage = df['Hydro (% electricity)'].values[0]

    total_renewables = wind_percentage + solar_percentage +hydro_percentage
    data = {
        'Energía Renovable' : ['Eólica', 'Solar', 'Hidráulica'],'Participación' : [wind_percentage, solar_percentage,hydro_percentage]
    }
    df_graph = pd.DataFrame(data)
    fig, ax = plt.subplots()
    ax.set_title ('Partipación de Energías Renovables', fontsize = 14)
    ax.pie(df_graph['Participación'], labels = df_graph['Energía Renovable'], autopct = '%1.1f%%', startangle = 90)
    # para que la torta sea redonda
    ax.axis('equal')
    img = BytesIO()
    plt.savefig(img, format = 'png')
    img.seek(0)
    graph_url2 = base64.b64encode(img.getvalue()).decode('utf-8')
     #------------fin Gráfica de barras-----------
     #------------GRÁFICO DE LINEAS---------------
    wind_data = pd.read_csv('static/archivo/09 cumulative-installed-wind-energy-capacity-gigawatts.csv')
    solar_data = pd.read_csv('static/archivo/13 installed-solar-PV-capacity.csv')
    # dato más relevante por año dropna
    wind_data = wind_data[['Year', 'Wind Capacity']].dropna()
    solar_data = solar_data[['Year', 'Solar Capacity']].dropna()
    #convertir todos los años en un valor númerico
    wind_data['Year'] = pd.to_numeric(wind_data['Year'], errors = 'coerce')
    solar_data['Year'] = pd.to_numeric(solar_data['Year'], errors = 'coerce')
    plt.figure(figsize=(6,5))
    # los puntos de referencia van ha estar marcados por o
    plt.plot(wind_data['Year'],wind_data['Wind Capacity'],label = 'Capacidad Eólica', color = 'blue', marker = 'o')
    plt.plot(solar_data['Year'], solar_data['Solar Capacity'], label = 'Capacidad Solar', color = 'orange', marker = 'x')

    plt.title('Tendencia en la Capacidad Instalada (Eólica vs Solar)')
    plt.xlabel('Año')
    plt.ylabel('Capacidad Instalada (Gigawatts)')
    plt.legend()
    plt.grid(True)
    img = BytesIO()
    plt.savefig(img, format = 'png')
    img.seek(0)
    graph_url3 = base64.b64encode(img.getvalue()).decode('utf-8')

     #--------FIN-GRÁFICO DE LINEAS---------------
    #  comparar energia renobable con la tradicional pero como no tengo la tradicional dejo un dato estático
     #------------GRÁFICO DE AREA---------------
    renewable_data = pd.read_csv('static/archivo/02 modern-renewable-energy-consumption.csv')

    renewable_data = renewable_data[renewable_data['Entity'] =='World']
    renewable_data['Total Renewable Energy'] = (renewable_data['Geo Biomass Other - TWh']+ renewable_data['Solar Generation - TWh'] + renewable_data['Wind Generation - TWh'] + renewable_data['Hydro Generation - TWh'])
    fig, ax = plt.subplots(figsize = (6, 5))

    ax.fill_between(renewable_data['Year'], renewable_data['Total Renewable Energy'], color = 'green', alpha = 0.5, label = 'Energía Renovable')

    conventional_data = pd.DataFrame({
        'Year': renewable_data['Year'],
        'Total Conventional Energy' :[1000]*len(renewable_data['Year'])
        })
    ax.fill_between(conventional_data['Year'],conventional_data['Total Conventional Energy'],color = 'red', alpha = 0.5, label = 'Energía Convencional')
    ax.set_title('Comparación entre Consumo de Energía Renovable y convencional', fontsize = 12)
    ax.set_xlabel('Año', fontsize = 12)
    ax.set_ylabel('Consumo de Energía (TWh)', fontsize = 12)
    ax.legend(loc = 'upper left')
    img = BytesIO()
    plt.savefig(img, format = 'png')
    img.seek(0)
    graph_url4 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
     #--------FIN-GRÁFICO DE AREA---------------


    with open('static/archivo/data_pagina.csv', newline='',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data = [row for row in reader]


    if request.method == 'POST':
        try:
            consumo_total = float(request.form['consumo_total'])
            if consumo_total <= 0:
                error = "El consumo total debe ser un valor positivo."
            else:
                produccion_total_renovable = sum(energia['renewables'] for energia in datos_renovables)
                if produccion_total_renovable >= consumo_total:
                    porcentaje_renovable = (consumo_total/produccion_total_renovable)*100
                else:
                    porcentaje_renovable = 100
            
        except ValueError:
            error ="Por Favor ingrese un valor válido para el consumo total."
    
    return render_template('index.html',porcentaje_renovable = porcentaje_renovable, error = error, graph_url = graph_url, graph_url2 = graph_url2, graph_url3 = graph_url3, graph_url4 = graph_url4, data=data)

if __name__ == '__main__':
    app.run(debug=True)#Este bloque verifica si el script está siendo ejecutado directamente (y no importado como un módulo en otro programa). Si es así, ejecuta el servidor de desarrollo de Flask con app.run(debug=True)