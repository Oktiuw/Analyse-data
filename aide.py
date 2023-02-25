# encoding: utf-8

import streamlit as st
import plotly.express as px
import pandas as pd
import itertools

@st.cache
def load_data_from_csv(url):
    """
    Fonction de chargement des données dans un data frame
    à partir d'un fichier csv distant dont l'URL est passée
    en paramètre
    """
    df = pd.read_csv(url)
    for c in ["PassengerId", "Name", "Ticket", "Cabin"]:
        df[c] = df[c].astype('object')
    for c in ["Survived", "Pclass", "Sex", "Embarked"]:
        df[c] = df[c].astype('category')
    for c in ["Age", "Fare"]:
        df[c] = df[c].astype('float64')
    for c in ["SibSp", "Parch"]:
        df[c] = df[c].astype("int64")
    return df


# Main

st.title("Tableau de bord - titanic")
st.write("---")

df = load_data_from_csv("https://iut-info.univ-reims.fr/users/blanchard/infovis/data/titanic.csv")

tab1, tab2, tab3 = st.tabs(["Données","Desc. univariée","Desc. bivariée"])

with tab1:
    st.write(df)

with tab2:
    for c in df.columns:
        if df[c].dtype == "int64" or df[c].dtype == "float64":
            st.subheader(c)
            st.write(df[c].dtype)
            fig = px.histogram(df, x=c)
            st.plotly_chart(fig, use_container_width=True)
        if df[c].dtype == "category":
            st.subheader(c)
            st.write(df[c].dtype)
            dfg = df.groupby(c).size().reset_index(name='Effectif')
            fig = px.bar(dfg, x=c, y='Effectif')
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    for combi in itertools.combinations(df.columns,2):
        if df[combi[0]].dtype in ['int64','float64'] and df[combi[1]].dtype in ['int64','float64']:
            st.subheader(combi[0] + " vs. " +combi[1])
            fig = px.scatter(df, x=combi[0], y=combi[1])
            st.plotly_chart(fig, use_container_width=True)
        if df[combi[0]].dtype in ['int64','float64'] and df[combi[1]].dtype in ['category']:
            st.subheader(combi[0] + " vs. " +combi[1])
            fig = px.box(df, x=combi[1], y=combi[0])
            st.plotly_chart(fig, use_container_width=True)
        if df[combi[0]].dtype in ['category'] and df[combi[1]].dtype in ['int64','float64']:
            st.subheader(combi[0] + " vs. " +combi[1])
            fig = px.box(df, x=combi[0], y=combi[1])
            st.plotly_chart(fig, use_container_width=True)
        if df[combi[0]].dtype in ['category'] and df[combi[1]].dtype in ['category']:
            st.subheader(combi[0] + " vs. " +combi[1])
            fig = px.density_heatmap(df, x=combi[0], y=combi[1], text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
