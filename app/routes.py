# app/routes.py
from flask import render_template
from app import app, bootstrap
from app.models import Territoire, TypeTerritoire, Periode, InfosJob
import plotly.express as px
import pandas as pd
from sqlalchemy import func
import json
import folium
from geopy import distance
import geopandas as gpd
import ast
from shapely.geometry import Polygon


@app.route('/')
@app.route('/index')
def index() -> str:
    return render_template('index.html', bootstrap=bootstrap)

@app.route('/data')
def data():
    territoires = Territoire.query.all()
    typeTerritoire = TypeTerritoire.query.all()
    periode = Periode.query.all()
    informations = InfosJob.query.all()
    return render_template('data.html', territoires=territoires, typeTerritoire=typeTerritoire, periode=periode, informations=informations, bootstrap=bootstrap)

@app.route('/python')
def python():
    territoires = Territoire.query.filter_by(codeTypeTerritoire='DEP').all()
    
    m = folium.Map(location=[46.2276, 2.2137], zoom_start=5)

    for territoire in territoires:
        if territoire.geojson :
            territoire.geojson = ast.literal_eval(territoire.geojson)
            territoire.geojson = territoire.geojson[0]
            territoire.geojson  = [(c[0], c[1]) for c in territoire.geojson]
            territoire.geojson.pop()
            
            coordonnees = territoire.geojson
            polygon = Polygon(coordonnees)

            folium.GeoJson(
                data={
                    "type": "Feature",
                    "geometry": polygon.__geo_interface__,
                    "properties": {
                        "name": territoire.libelleTerritoire
                        }
                },
                name="Contour du territoire",
                style_function=lambda x: {
                    'fillColor': '#318CE7',
                    'color': '#318CE7',
                    'weight': 2,
                    'fillOpacity': 0.2
                }
            ).add_child(folium.Popup(f'Voir le tableau de bord : <a href="/python/{territoire.libelleTerritoire}" target="_blank">{territoire.libelleTerritoire}</a>')).add_to(m)

    map_html = m._repr_html_()
    
    return render_template('python/python.html', map_html=map_html, bootstrap=bootstrap)

@app.route('/python/test')
def pythontest():
    informations = InfosJob.query.all()
    df = pd.DataFrame.from_records([i.__dict__ for i in informations])
    fig = px.box(df, x='codeTerritoire', y='population')
    graph_html = fig.to_html(full_html=False)
    return render_template('python/graphtest.html', informations=informations, graph_html=graph_html, bootstrap=bootstrap)

@app.route('/python/<libelleTerritoire>')
def territoire(libelleTerritoire: str) -> str:
    territoire = Territoire.query.filter_by(libelleTerritoire=libelleTerritoire).first()
    informations = InfosJob.query.filter_by(codeTerritoire=territoire.codeTerritoire, codeTypeTerritoire=territoire.codeTypeTerritoire).filter(func.length(InfosJob.codePeriode) == 4).all()    
    df = pd.DataFrame.from_records([i.__dict__ for i in informations])
    df['codePeriode'] = df['codePeriode'].astype(int)

    # Affichage de l'emplacement du territoire
    if territoire.geojson :
        territoire.geojson = ast.literal_eval(territoire.geojson)
        territoire.geojson = territoire.geojson[0]
        territoire.geojson  = [(c[0], c[1]) for c in territoire.geojson]
        territoire.geojson.pop()

        coordonnees = territoire.geojson
        polygon = Polygon(coordonnees)
    
        m = folium.Map(location=[46.2276, 2.2137], zoom_start=5)
        
        folium.GeoJson(
            data={
                "type": "Feature",
                "geometry": polygon.__geo_interface__
            },
            name="Contour du territoire"
        ).add_to(m)

        map_html = m._repr_html_()


    #Création Graph
    fig = px.bar(df.query('codePeriode >= 2018'), x='codePeriode', y='valeurIndic')
    # Configuration Graph
    fig.update_traces(legendgroup="", showlegend=True)
    fig.update_layout(title="Valeur Indicateur - Dynamisme",
                    legend=dict( yanchor="top", y=0.99, xanchor="left", x=0.01),
                    xaxis_title="Période",
                    yaxis_title="Valeur Indic",
                    yaxis=dict(range=[0, 5]))

    graph_valeurIndic = fig.to_html(full_html=False)

    return render_template('python/territoire.html',map_html=map_html,territoire=territoire, informations=informations, graph_valeurIndic=graph_valeurIndic, bootstrap=bootstrap)

@app.route('/powerBI')
def powerBI():
    territoires = Territoire.query.all()
    typeTerritoire = TypeTerritoire.query.all()
    periode = Periode.query.all()
    informations = InfosJob.query.all()
    return render_template('powerBI/powerBI.html', territoires=territoires, typeTerritoire=typeTerritoire, periode=periode, Informations=informations, bootstrap=bootstrap)