from sqlalchemy import create_engine

import pymysql
import random
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib
import plotly.graph_objs as go
import math
import statsmodels
dicoAnnee={}
dicoAnnee['2015']=None
dicoAnnee['2016']=None
dicoAnnee['2017']=None
dicoAnnee['2018']=None
dicoAnnee['2019']=None
dicoAnnee['2020']=None
sqlEngine       = create_engine('mysql+pymysql://distant:azerty02@10.31.5.227/vinc0064_data', pool_recycle=3600)
dbConnection    = sqlEngine.connect()
frame = pd.read_sql("select * from InfosJob where codePeriode LIKE '____' AND  codeTypeTerritoire='REG' AND codePeriode NOT IN ('2020','2021','2022','2023')", dbConnection);
pd.set_option('display.expand_frame_repr', False)
dico=dicoAnnee.copy()



t1,t2=st.tabs(["Bilan sur les logements","Recherche d'un lien avec le dynamisme d'un territoire"])



with t1:
    for index,element in frame.iterrows():
        if dico[element['codePeriode']] is None:
            dico[element['codePeriode']]=element['population']
        else:
            dico[element['codePeriode']]+=element['population']
    fig = px.line(x=list(dico.keys()), y=list(dico.values()),title= 'Evolution de la population en France de 2016 à 2019 ( FRANCE HORS MAYOTTE )',markers=True)
    fig.update_xaxes(title='Années', tickmode='linear', dtick=1)
    fig.update_yaxes(title='Population en millions')
    fig.update_layout(yaxis_range=[0,70000000])  
    st.write(fig)
    st.write('La croissance de la population française stagne')
    st.write("Fait intéréssant, si on manipule l'échelle sur la gauche, on pourrait croire que la france dispose d'une croissance exponentielle.")
    fig.update_layout(yaxis_range=[66000000,67000000])  
    st.write(fig)

    dico=dicoAnnee.copy()
    for index,element in frame.iterrows():
        if dico[element['codePeriode']] is None:
            dico[element['codePeriode']]=[element['nbLogements0VOIT'],element['nbLogements1VOIT'],element['nbLogements2VOIT'],element['nbLogements3VOITOuPlus']]
        else:
            dico[element['codePeriode']][0]+=element['nbLogements0VOIT']
            dico[element['codePeriode']][1]+=element['nbLogements1VOIT']
            dico[element['codePeriode']][2]+=element['nbLogements2VOIT']
            dico[element['codePeriode']][3]+=element['nbLogements3VOITOuPlus']
    import plotly.graph_objs as go

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
        trace = go.Bar(x=x_values, y=y_values, name=name)
        data.append(trace)


    layout = go.Layout(title='Répartition des logements selon le nombre de voitures ( FRANCE HORS MAYOTTE )', barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    st.write(fig)




    st.write("Cette visualisation en histogrammes empilés n'est pas très représentative, en effet vu que la population augmente le nombre de logements également, il faut donc voir la répartition de ceux-ci ")
    for year in dicoAnnee.keys():
        if year!='2015' and year!='2020':
            names=['Logements avec 0 voiture','Logements avec 1 voiture','Logements avec 2 voitures','Logements avec 3 voitures ou plus']
            fig=px.pie(values=dico[year],names=names,title=f"Année {year}", hole=.5)
            st.write(fig)
    st.write("On remarque une hausse de nombres de logements avec 3 voitures et une baisse des logements avec 2 voitures. On peut suppposer que cette baisse est la conséquence de l'augmentation du nombre de divorces.") 


    st.write("Passons aux différents types de chauffage ")
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
    trace1 = go.Scatter(x=years, y=collectif, name='Chauffage collectif')
    trace2 = go.Scatter(x=years, y=indiv, name='Chauffage individuel (fioul/gaz)')
    trace3 = go.Scatter(x=years, y=electric, name='Chauffage électrique individuel ')
    trace4 = go.Scatter(x=years, y=autre, name='Autre chauffage comme bois')
    layout = go.Layout(title='Répartition du chauffage par année',
                       xaxis=dict(title='Année'),
                       yaxis=dict(title='Nombre de logements'))

    fig = go.Figure(data=[trace1, trace2, trace3, trace4], layout=layout)
    st.write(fig)
    st.write("Meme constat que pour le graphique à barres empilées ci-dessus, il faut voir la répartition")
    for year in dicoAnnee.keys():
        if year!='2015' and year!='2020':
            names=['Chauffage collectif','Chauffage individuel (chaudière)','Chauffage électrique individuel','Autre chauffage comme bois']
            fig=px.pie(values=dico[year],names=names,title=f"Année {year}")
            st.write(fig)
    st.write("On voit bien que les logements à chauffage électrique sont en hausse lorsque ceux au fioul/gaz sont en baisse mais restent majoritaire. Cela montre bien la politique gouvernementale.") 

with t2:
    st.write("Rappelons la définition d'un coefficient de corrélation")
    st.write("Ci celui ci s'approche de 1, cela montre un lien positif entre une variable et une autre")
    st.write("Au contraire, s'il s'approche de -1, cela montre un lien négatif")
    st.write("Finalement,s'il se rapproche de 0, cela montre l'absence de lien")
    frame = pd.read_sql("select * from InfosJob where codePeriode LIKE '____' AND  codeTypeTerritoire='REG' AND codePeriode NOT IN ('2020','2021','2022','2023')", dbConnection);
    df=frame.query('codePeriode=="2019"')
    st.write('Calculons tous les coefficients de corrélations avec un nuage de points pour visualiser: ') 
    champs=['nbLogements0VOIT','nbLogements1VOIT','nbLogements2VOIT','nbLogements3VOITOuPlus','population','nbLogementsAvecPlacesResa','chauffageCollectif','chauffageIndiv','chauffageElect','chauffageAutre']
    names=['du nombre de logements avec 0 voiture','du nombre de logements avec 1 voiture','du nombre de logements avec 2 voitures','du nombre de logements avec 3 voitures ou plus','de la population','du nombre de logements avec une place réservée pour leur voiture','du nombre de logements avec le chauffage collectif','du nombre de logements avec le chauffage chaudière','du nombre de logements avec le chauffage electrique','du nombre de logements avec tout autre type de chauffage']
    i=0
    for champ in champs:
        fig=px.scatter(df,x=champ,y='valeurIndic',trendline="ols",hover_name="codeTerritoire",title=f"Valeur de l'indicateur de dynamisme d'une région en fonction {names[i]}")
        st.write(fig)
        st.write("Coefficient de corrélation :")
        st.write(df[champ].corr(df['valeurIndic']))
        i+=1
    st.write("On observe 2 coefficients de corrélations valant environ -0,6. C'est trop peu pour établir un lien mais en regardant les variables concernées, nombre de logements à 2 voitures et nombre de logements à 3 voiture ou plus, nous pouvons déduire une tendance. Plus les logements d'un territoire ont plusieurs voitures, moins ce territoire sera dynamique. Cela fait sens, les territoires ayant le plus de logements avec plusieurs voitures sont les territoires où la densité de population est plus faible, et donc, avec moins de villes et de moins grandes tailles.")
    st.write("Si on regarde les 2 graphiques concernés, on voit que 2 fois, une région dispose du plus grand nombre de logements à 2 et 3 voitures ou plus. Il s'agit de la région Auvergne-Rhône-Alpes. On sait que cette région, à part quelques grandes villes comme Lyon ou Clermont-Ferrand, est surtout constituée de villages.")
dbConnection.close()