# app/routes.py
from flask import render_template
from app import app, bootstrap
from app.models import Territoire, TypeTerritoire, Periode, InfosJob
import plotly.express as px
import pandas as pd
from sqlalchemy import func, not_
import json, folium, ast, random, math, statsmodels
from geopy import distance
import geopandas as gpd
import ast, random, math
from shapely.geometry import Polygon
import plotly.graph_objs as go


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
# Graphiques Cartes Territoires
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
            ).add_child(folium.Popup(f'<div style="width: 140px; text-align: center;"> {name} <br> <a href="/python/DEP/{name}" target="_top">Voir le tableau de bord</a> </div>')
            ).add_to(m)
        elif row.geometry.geom_type == 'MultiPolygon':
            folium.GeoJson(row.geometry, tooltip=name
            ).add_child(folium.Popup(f'<div style="width: 140px; text-align: center;"> {name} <br> <a href="/python/DEP/{name}" target="_top">Voir le tableau de bord </a> </div>')
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
            ).add_child(folium.Popup(f'<div style="width: 140px; text-align: center;"> {name} <br> <a href="/python/REG/{name}" target="_top">Voir le tableau de bord</a> </div>')
            ).add_to(m)
        elif row.geometry.geom_type == 'MultiPolygon':
            folium.GeoJson(row.geometry, tooltip=name
            ).add_child(folium.Popup(f'<div style="width: 140px; text-align: center;"> {name} <br> <a href="/python/REG/{name}" target="_top">Voir le tableau de bord </a> </div>')
            ).add_to(m)

    map_region_html = m._repr_html_()


# Graphiques Analyse France ()

    dicoAnnee={'2015':None, '2016':None, '2017':None, '2018':None, '2019':None, '2020':None}
    informations = InfosJob.query.filter(InfosJob.codeTypeTerritoire=='REG', func.length(InfosJob.codePeriode) == 4, not_(InfosJob.codePeriode.in_(['2020','2021','2022','2023']))).all() 
    frame = pd.DataFrame.from_records([i.__dict__ for i in informations])
    colors=['rgb(129,217,255)','rgb(90,190,185)', 'rgb(0,123,255)', 'rgb(0,78,165)']
    
  # Bilan sur les logements

    # Population
    graphs_pop = []
    dico=dicoAnnee.copy()
    for index,element in frame.iterrows():
        if dico[element['codePeriode']] is None:
            dico[element['codePeriode']]=element['population']
        else:
            dico[element['codePeriode']]+=element['population']
    
    fig = px.line(x=list(dico.keys()), y=list(dico.values()),title= 'Évolution de la population en France de 2016 à 2019 ( FRANCE HORS MAYOTTE )')
    fig.update_xaxes(title='Années', tickmode='linear', dtick=1)
    fig.update_yaxes(title='Population en millions')
    fig.update_layout(yaxis_range=[0,70000000])  
    graphs_pop.append(fig.to_html(full_html=False))
    fig.update_layout(yaxis_range=[66000000,67000000])  
    graphs_pop.append(fig.to_html(full_html=False))

    # Voiture logements
    graphs_voiture = []
    dico=dicoAnnee.copy()
    for index,element in frame.iterrows():
        if dico[element['codePeriode']] is None:
            dico[element['codePeriode']]=[element['nbLogements0VOIT'],element['nbLogements1VOIT'],element['nbLogements2VOIT'],element['nbLogements3VOITOuPlus']]
        else:
            dico[element['codePeriode']][0]+=element['nbLogements0VOIT']
            dico[element['codePeriode']][1]+=element['nbLogements1VOIT']
            dico[element['codePeriode']][2]+=element['nbLogements2VOIT']
            dico[element['codePeriode']][3]+=element['nbLogements3VOITOuPlus']

    data = []
    traces=[]
    x_values = list(dico.keys())
    for i in range(4):
        y_values = []
        name = f"Logements avec {i} voiture(s)"
        for value in dico.values():
            if value is None:
                y_values.append(0)
            else:
                y_values.append(value[i])
        trace = go.Bar(x=x_values, y=y_values, name=name, marker_color=colors[i])
        data.append(trace)
    layout = go.Layout(title='Répartition des logements selon le nombre de voitures ( FRANCE HORS MAYOTTE )', barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    graphs_voiture.append(fig.to_html(full_html=False))

    for year in dicoAnnee.keys():
        if year!='2015' and year!='2020':
            names=['Logements avec 0 voiture','Logements avec 1 voiture','Logements avec 2 voitures','Logements avec 3 voitures ou plus']
            fig=px.pie(values=dico[year],names=names,title=f"Année {year}", hole=.5, color_discrete_sequence=colors)
            graphs_voiture.append(fig.to_html(full_html=False))

    # Chauffage logements
    graphs_chauffage = []
    dico={"2016":None,"2017":None,"2018":None,"2019":None}
    for index,element in frame.iterrows():
        if  math.isnan(element['chauffageCollectif']):
            element['chauffageCollectif']=0
            element['chauffageIndiv']=0
            element['chauffageElect']=0
            element['chauffageAutre']=0
        if dico[element['codePeriode']] is None:
            dico[element['codePeriode']]=[element['chauffageCollectif'],element['chauffageIndiv'],element['chauffageElect'],element['chauffageAutre']]
        else:
            dico[element['codePeriode']][0]+=element['chauffageCollectif']
            dico[element['codePeriode']][1]+=element['chauffageIndiv']
            dico[element['codePeriode']][2]+=element['chauffageElect']
            dico[element['codePeriode']][3]+=element['chauffageAutre']
    
    years = list(dico.keys())
    collectif = [dico[year][0] for year in years]
    indiv = [dico[year][1] for year in years]
    electric = [dico[year][2] for year in years]
    autre = [dico[year][3] for year in years]
    trace1 = go.Scatter(x=years, y=collectif, name='Chauffage collectif', marker_color=colors[0])
    trace2 = go.Scatter(x=years, y=indiv, name='Chauffage individuel (Ex: fioul/gaz)', marker_color=colors[1])
    trace3 = go.Scatter(x=years, y=electric, name='Chauffage électrique individuel ', marker_color=colors[2])
    trace4 = go.Scatter(x=years, y=autre, name='Autre chauffage (Ex: bois)', marker_color=colors[3])
    layout = go.Layout(title='Répartition du chauffage par année',
                       xaxis=dict(title='Année'),
                       yaxis=dict(title='Nombre de logements'))
    fig = go.Figure(data=[trace1, trace2, trace3, trace4], layout=layout)
    graphs_chauffage.append(fig.to_html(full_html=False))

    for year in dicoAnnee.keys():
        if year!='2015' and year!='2020':
            names=['Chauffage collectif','Chauffage individuel (Ex: fioul/gaz)','Chauffage électrique individuel','Autre chauffage (Ex: bois)']
            fig=px.pie(values=dico[year],names=names,title=f"Année {year}", color_discrete_sequence=colors)
            graphs_chauffage.append(fig.to_html(full_html=False))

  # Recherche d'un lien avec le dynamisme d'un territoire
    graphs_dynamisme = []
    df=frame.query('codePeriode=="2019"')
    champs=['nbLogements0VOIT','nbLogements1VOIT','nbLogements2VOIT','nbLogements3VOITOuPlus','population','nbLogementsAvecPlacesResa','chauffageCollectif','chauffageIndiv','chauffageElect','chauffageAutre']
    names=['du nombre de logements avec 0 voiture','du nombre de logements avec 1 voiture','du nombre de logements avec 2 voitures','du nombre de logements avec 3 voitures ou plus','de la population','du nombre de logements avec une place réservée pour leur voiture','du nombre de logements avec le chauffage collectif','du nombre de logements avec le chauffage chaudière','du nombre de logements avec le chauffage electrique','du nombre de logements avec tout autre type de chauffage']
    i=0
    for champ in champs:
        fig=px.scatter(df,x=champ,y='valeurIndic',trendline="ols",hover_name="codeTerritoire",title=f"Valeur de l'indicateur de dynamisme d'une région en fonction {names[i]}")
        graphs_dynamisme.append((fig.to_html(full_html=False),df[champ].corr(df['valeurIndic']))) #(Graph, Coefficient de corrélation )
        i+=1

    return render_template('python/python.html', map_region_html=map_region_html, graphs_dynamisme=graphs_dynamisme, graphs_chauffage=graphs_chauffage, graphs_voiture=graphs_voiture ,graphs_pop=graphs_pop, map_departement_html=map_departement_html, bootstrap=bootstrap)

@app.route('/python/<codeTypeTerritoire>/<libelleTerritoire>')
def territoire(codeTypeTerritoire: str, libelleTerritoire: str) -> str:
    territoire = Territoire.query.filter_by(codeTypeTerritoire=codeTypeTerritoire, libelleTerritoire=libelleTerritoire).first()
    informations = InfosJob.query.filter_by(codeTerritoire=territoire.codeTerritoire, codeTypeTerritoire=codeTypeTerritoire).all()    
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

    #Création Graph Valeur Indicateur Dynamisme
    fig = px.line(df[df['codePeriode'].str.len() != 4], x='codePeriode', y='valeurIndic')
    fig.update_layout(title=f"Valeur Indicateur - Dynamisme par trimestre",
                    legend=dict( yanchor="top", y=0.99, xanchor="left", x=0.01),
                    xaxis_title="Période",
                    yaxis_title="Valeur Indic",
                    yaxis=dict(range=[0, 5.2]))
    graph_valeurIndic = fig.to_html(full_html=False)

    #Création des Graph
    graphs = []
    for annee in ['2016', '2017', '2018', '2019']:
        df_base = df.loc[(df['codePeriode'].str.len() == 4) & (df['codePeriode'] == annee)]
        #concernant le nombre de voitures
        lst_voiture = df_base[['nbLogements0VOIT', 'nbLogements1VOIT', 'nbLogements2VOIT'  ,'nbLogements3VOITOuPlus']].iloc[0].to_list()
        df_voitures = pd.DataFrame({'Logement': ['sans voiture', 'avec 1 voiture', 'avec 2 voitures', 'avec 3 voitures ou plus'], annee : lst_voiture})
        fig = px.pie(df_voitures, values=annee, names='Logement', title=f"Proportion de voitures par logement - Année {annee}")
        graphs.append(fig.to_html(full_html=True))
        #concernant les places de parking
        lst_place = df_base[['nbLogementsAvecPlacesResa']].iloc[0].to_list()[0]
        df_places = pd.DataFrame({'Logement': ['avec places réservées', 'sans places réservées'], annee : [lst_place, sum(lst_voiture)-lst_place]})
        fig = px.pie(df_places, values=annee, names='Logement', title=f"Proportion de place de parking reservées - Année {annee}")
        graphs.append(fig.to_html(full_html=True))
        #concernant le chauffage
        lst_chauffage = df_base[['chauffageCollectif', 'chauffageIndiv', 'chauffageElect', 'chauffageAutre']].iloc[0].to_list()
        df_chauffage = pd.DataFrame({'Logement': ['avec chauffage collectif','avec chauffage individuel', 'avec chauffage electrique', 'avec autre chauffage',], annee : lst_chauffage})
        fig = px.pie(df_chauffage, values=annee, names='Logement', title=f"Proportion des différents type de chauffage - Année {annee}")
        graphs.append(fig.to_html(full_html=True))
    

    return render_template('python/territoire.html',map_html=map_html,territoire=territoire, informations=informations, graphs=graphs, graph_valeurIndic=graph_valeurIndic, bootstrap=bootstrap)

@app.route('/powerBI')
def powerBI():
    territoires = Territoire.query.all()
    typeTerritoire = TypeTerritoire.query.all()
    periode = Periode.query.all()
    informations = InfosJob.query.all()
    return render_template('powerBI/powerBI.html', territoires=territoires, typeTerritoire=typeTerritoire, periode=periode, Informations=informations, bootstrap=bootstrap)