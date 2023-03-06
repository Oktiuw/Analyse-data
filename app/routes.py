# app/routes.py
from flask import render_template
from app import app, bootstrap
from app.models import Territoire, TypeTerritoire, Periode, InfosJob
import plotly.express as px

@app.route('/')
@app.route('/index')
def index() -> str:
    return render_template('index.html', bootstrap=bootstrap)


@app.route('/territoires')
def territoires():
    territoires = Territoire.query.all()
    return render_template('territoires.html', territoires=territoires, bootstrap=bootstrap)


@app.route('/data')
def data():
    territoires = Territoire.query.all()
    typeTerritoire = TypeTerritoire.query.all()
    periode = Periode.query.all()
    informations = InfosJob.query.all()
    return render_template('data.html', territoires=territoires, typeTerritoire=typeTerritoire, periode=periode, informations=informations, bootstrap=bootstrap)

@app.route('/python')
def python():
    territoires = Territoire.query.all()
    typeTerritoire = TypeTerritoire.query.all()
    periode = Periode.query.all()
    informations = InfosJob.query.all()
    return render_template('python/.html', territoires=territoires, typeTerritoire=typeTerritoire, periode=periode, informations=informations, bootstrap=bootstrap)

@app.route('/python/test')
def pythontest():
    informations = InfosJob.query.all()
    fig = px.box(informations, x=informations.codeTerritoire, y=informations.population)
    return render_template('python/python.html', informations=informations, graph=fig, bootstrap=bootstrap)



@app.route('/powerBI')
def powerBI():
    territoires = Territoire.query.all()
    typeTerritoire = TypeTerritoire.query.all()
    periode = Periode.query.all()
    informations = InfosJob.query.all()
    return render_template('powerBI/powerBI.html', territoires=territoires, typeTerritoire=typeTerritoire, periode=periode, Informations=informations, bootstrap=bootstrap)