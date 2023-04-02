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
    # Carte pour les Départements
    territoires = Territoire.query.filter_by(codeTypeTerritoire='DEP').all()
    
    geoms = []
    for t in territoires:
        if t.geojson:
            geoms.append(json.loads(t.geojson))
    gdf = gpd.GeoDataFrame.from_features(geoms)

    m = folium.Map(location=[46.2276, 2.2137], zoom_start=5)

    for _, row in gdf.iterrows():
        name = row.loc['nom']
        if row.geometry.geom_type == 'Polygon':
            folium.GeoJson(row.geometry, tooltip=name
            ).add_child(folium.Popup(f'<div style="width: 140px; text-align: center;"> {name} <br> <a href="/python/{name}" target="_top">Voir le tableau de bord</a> </div>')
            ).add_to(m)
        elif row.geometry.geom_type == 'MultiPolygon':
            folium.GeoJson(row.geometry, tooltip=name
            ).add_child(folium.Popup(f'<div style="width: 140px; text-align: center;"> {name} <br> <a href="/python/{name}" target="_top">Voir le tableau de bord </a> </div>')
            ).add_to(m)

    map_departement_html = m._repr_html_()

    # Carte pour les Régions
    territoires = Territoire.query.filter_by(codeTypeTerritoire='REG').all()
    
    geoms = []
    for t in territoires:
        if t.geojson:
            geoms.append(json.loads(t.geojson))
    gdf = gpd.GeoDataFrame.from_features(geoms)

    m = folium.Map(location=[46.2276, 2.2137], zoom_start=5)

    for _, row in gdf.iterrows():
        name = row.loc['nom']
        if row.geometry.geom_type == 'Polygon':
            folium.GeoJson(row.geometry, tooltip=name
            ).add_child(folium.Popup(f'<div style="width: 140px; text-align: center;"> {name} <br> <a href="/python/{name}" target="_top">Voir le tableau de bord</a> </div>')
            ).add_to(m)
        elif row.geometry.geom_type == 'MultiPolygon':
            folium.GeoJson(row.geometry, tooltip=name
            ).add_child(folium.Popup(f'<div style="width: 140px; text-align: center;"> {name} <br> <a href="/python/{name}" target="_top">Voir le tableau de bord </a> </div>')
            ).add_to(m)

    map_region_html = m._repr_html_()

    
    return render_template('python/python.html', map_region_html=map_region_html, map_departement_html=map_departement_html, bootstrap=bootstrap)

@app.route('/python/<libelleTerritoire>')
def territoire(libelleTerritoire: str) -> str:
    territoire = Territoire.query.filter_by(libelleTerritoire=libelleTerritoire).first()
    informations = InfosJob.query.filter_by(codeTerritoire=territoire.codeTerritoire, codeTypeTerritoire=territoire.codeTypeTerritoire).all()    
    df = pd.DataFrame.from_records([i.__dict__ for i in informations])

    # Visuel du territoire
    if territoire.geojson:
        geoms = [json.loads(territoire.geojson)]
        gdf = gpd.GeoDataFrame.from_features(geoms)
        centroid = gdf.centroid.iloc[0]
        m = folium.Map(location=[centroid.y, centroid.x], zoom_start=6)        
        if gdf.geometry.type[0] == 'Polygon':
            folium.GeoJson(gdf.geometry[0]).add_to(m)
        elif gdf.geometry.type[0] == 'MultiPolygon':
            folium.GeoJson(gdf.geometry[0]).add_to(m)
        map_html = m._repr_html_()


    #Création Graph
    fig = px.line(df, x='codePeriode', y='valeurIndic')
    # Configuration Graph
    fig.update_traces(legendgroup="", showlegend=True)
    fig.update_layout(title="Valeur Indicateur - Dynamisme",
                    legend=dict( yanchor="top", y=0.99, xanchor="left", x=0.01),
                    xaxis_title="Période",
                    yaxis_title="Valeur Indic",
                    yaxis=dict(range=[0, 5.2]))

    graph_valeurIndic = fig.to_html(full_html=False)

    return render_template('python/territoire.html',map_html=map_html,territoire=territoire, informations=informations, graph_valeurIndic=graph_valeurIndic, bootstrap=bootstrap)

@app.route('/powerBI')
def powerBI():
    territoires = Territoire.query.all()
    typeTerritoire = TypeTerritoire.query.all()
    periode = Periode.query.all()
    informations = InfosJob.query.all()
    return render_template('powerBI/powerBI.html', territoires=territoires, typeTerritoire=typeTerritoire, periode=periode, Informations=informations, bootstrap=bootstrap)