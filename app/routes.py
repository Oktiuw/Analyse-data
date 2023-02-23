# app/routes.py
from flask import render_template
from app import app
from app.models import Territoire, TypeTerritoire, Periode, InfosJob, InfosLogement

@app.route('/')
@app.route('/index')
def index() -> str:
    return render_template('index.html')


@app.route('/territoires')
def territoires():
    territoires = Territoire.query.all()
    return render_template('territoires.html', territoires=territoires)


@app.route('/data')
def data():
    territoires = Territoire.query.all()
    typeTerritoire = TypeTerritoire.query.all()
    periode = Periode.query.all()
    infosJob = InfosJob.query.all()
    infosLogement = InfosLogement.query.all()
    return render_template('data.html', territoires=territoires, typeTerritoire=typeTerritoire, periode=periode, infosJob=infosJob, infosLogement=infosLogement)

@app.route('/python')
def python():
    territoires = Territoire.query.all()
    typeTerritoire = TypeTerritoire.query.all()
    periode = Periode.query.all()
    infosJob = InfosJob.query.all()
    infosLogement = InfosLogement.query.all()
    return render_template('python/python.html', territoires=territoires, typeTerritoire=typeTerritoire, periode=periode, infosJob=infosJob, infosLogement=infosLogement)

@app.route('/powerBI')
def powerBI():
    territoires = Territoire.query.all()
    typeTerritoire = TypeTerritoire.query.all()
    periode = Periode.query.all()
    infosJob = InfosJob.query.all()
    infosLogement = InfosLogement.query.all()
    return render_template('powerBI/powerBI.html', territoires=territoires, typeTerritoire=typeTerritoire, periode=periode, infosJob=infosJob, infosLogement=infosLogement)
