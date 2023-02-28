# app/models.py
from app import db

# Territoire
class Territoire(db.Model):
    __tablename__ = 'Territoire'
    codeTerritoire = db.Column(db.String(3), primary_key=True)
    libelleTerritoire = db.Column(db.String(100))
    codeTypeTerritoire = db.Column(db.String(20), db.ForeignKey('TypeTerritoire.codeTypeTerritoire'), primary_key=True)

# Type de Territoire
class TypeTerritoire(db.Model):
    __tablename__ = 'TypeTerritoire'
    codeTypeTerritoire = db.Column(db.String(20), primary_key=True)
    libelleTypeTerritoire = db.Column(db.String(200), unique=True)

# Période
class Periode(db.Model):
    __tablename__ = 'Periode'
    codePeriode = db.Column(db.String(200), primary_key=True)
    libellePeriode = db.Column(db.String(200))

# Information Job + Logement
class InfosJob(db.Model):
    __tablename__ = 'InfosJob'
    codePeriode = db.Column(db.String(200), db.ForeignKey('Periode.codePeriode'), primary_key=True)
    codeTerritoire = db.Column(db.String(200), db.ForeignKey('Territoire.codeTerritoire'), primary_key=True)
    codeTypeTerritoire = db.Column(db.String(20), db.ForeignKey('TypeTerritoire.codeTypeTerritoire'), primary_key=True)
    valeurIndic = db.Column(db.Float)
    population = db.Column(db.Integer)
    nbLogements0VOIT = db.Column(db.Integer)
    nbLogements1VOIT = db.Column(db.Integer)
    nbLogements2VOIT = db.Column(db.Integer)
    nbLogements3VOITOuPlus = db.Column(db.Integer)
    nbLogementsAvecPlacesResa = db.Column(db.Integer)
