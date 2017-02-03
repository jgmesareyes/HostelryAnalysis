'''
Created on 20 de ene. de 2017

@author: Jose
'''

from app import db


class Hotel(db.Model):
    name = db.Column(db.String(128), primary_key=True)
    description = db.Column(db.String(4096))
    address = db.Column(db.String(128))
    xGrid = db.Column(db.Float())
    yGrid = db.Column(db.Float())
    facilities = db.Column(db.ARRAY(db.String()))
    languages = db.Column(db.ARRAY(db.String()))
    reviews = db.Column(db.JSON())
    valuableInfo = db.Column(db.JSON())
    region = db.Column(db.String())
    positives = db.Column(db.ARRAY(db.String(), db.Integer()))
    negatives = db.Column(db.ARRAY(db.String(), db.Integer()))
    geom = db.Column(db.String())



class Area(db.Model):
    name = db.Column(db.String(128), primary_key=True)
    town = db.Column(db.String())
    sector = db.Column(db.String())
    geom = db.Column(db.String())



class Hostelry(db.Model):
    region = db.Column(db.String(128), primary_key=True)
    data = db.Column(db.JSON())
