'''
Created on 9 de abr. de 2016

@author: Jose
'''

import re
import operator

from app import db
from .models import Hotel



class HotelService:
    """Representa un Hotel
    
    Almacena los datos relativos a un hotel, así como los datos extraídos
    después de llevar a cabo el análisis tanto global como por sectores.
    
    """
    def createHotel(self, name, description, address, coords, facilities, languages, reviews):
        """Constructor de un Hotel
        
        Crea el hotel con la información básica extraida del webscraping.
        
        Parámetros:
        name -- nombre del hotel
        description -- descripción
        address -- dirección completa
        coords -- par de coordenadas [x, y] extraídas con Geocoder de Google
        facilities -- lista de servicios ofrecidos
        languages -- lenguajes hablados
        reviews -- lista hash de las valoraciones de clientes de la forma:
        [{'author': 'author_name',
          'pos': '...pos_review...',
          'neg': '...neg_review...'},
          ...]
        
        """
        dbHotel = Hotel.query.get(name)
        if dbHotel is None:
            dbHotel = Hotel()
            dbHotel.name = name
            dbHotel.description = description
            dbHotel.address = address
            dbHotel.facilities = facilities
            dbHotel.languages = languages
            dbHotel.reviews = reviews
            if len(coords) > 0:
                dbHotel.xGrid = coords[0]
                dbHotel.yGrid = coords[1]
            else:
                dbHotel.region = "No definida"
            db.session.add(dbHotel)
            db.session.commit()
        
            if dbHotel.region is None:
                dbConnection = db.engine
                dbConnection.connect()
                
                updateQuery = """UPDATE Hotel SET geom = ST_AsEWKT(ST_Transform(ST_GeomFromText('POINT(%s %s)',4326), 99990)) WHERE name = %s;"""
                dbConnection.execute(updateQuery, [dbHotel.yGrid, dbHotel.xGrid, dbHotel.name])
        
                intersectionQuery = """SELECT a.name FROM Area a, Hotel b WHERE ST_Contains(ST_GeomFromText(a.geom), ST_GeomFromText(b.geom)) AND b.name = %s;"""
                region = dbConnection.execute(intersectionQuery, dbHotel.name).first()
                
                dbHotel.region = str(region[0])
                db.session.add(dbHotel)
                db.session.commit()
    
        self.name = dbHotel.name
        self.description = dbHotel.description
        self.address = dbHotel.address
        self.facilities = dbHotel.facilities
        self.languages = dbHotel.languages
        self.reviews = dbHotel.reviews
        self.coords = [dbHotel.xGrid, dbHotel.yGrid] if dbHotel.xGrid is not None else []
        self.region = dbHotel.region
    
    
    
    def updateInDB(self):
        """Actualiza el modelo Hotel de la BD.
        
        Actualiza un Hotel almacenando los valores obtenidos del análisis del
        Lenguaje Natural, servicios del hotel y valoración de los clientes.
        
        """
        dbHotel = Hotel.query.get(self.name)
        dbHotel.valuableInfo = self.valuableInfo
        dbHotel.positives = self.positives
        dbHotel.negatives = self.negatives
        db.session.add(dbHotel)
        db.session.commit()
    
    
    
    def fetchFromDB(self, dbHotel):
        """Extrae un Hotel de la BD.
        
        Obtiene los datos de un hotel ya almacenado en la BD.
        
        Parámetros:
        dbHotel -- modelo de Hotel de la BD
        
        """
        self.name = dbHotel.name
        self.description = dbHotel.description
        self.address = dbHotel.address
        self.coords = [dbHotel.xGrid, dbHotel.yGrid]
        self.facilities = dbHotel.facilities
        self.languages = dbHotel.languages
        self.reviews = dbHotel.reviews
        positives = [positive[1:-1].split(',') for positive in dbHotel.positives]
        self.positives = [(positive[0], int(positive[1])) for positive in positives]
        negatives = [negative[1:-1].split(',') for negative in dbHotel.negatives]
        self.negatives = [(negative[0], int(negative[1])) for negative in negatives]
        self.valuableInfo = dbHotel.valuableInfo
        self.region = dbHotel.region
    
    
    
    def parseData(self):
        valuableInfo = []
        positives = []
        negatives = []
        uniqueInfo = []
        commonInfo = []
        uniqueSectorInfo = []
        commonSectorInfo = []
        [valuableInfo.append({'name': facility, 'ccomplements': califications}) for facility, califications in self.valuableInfo.items()]
        [positives.append({'name': positive[0], 'value': int(positive[1])}) for positive in self.positives]
        [negatives.append({'name': negative[0], 'value': int(negative[1])}) for negative in self.negatives]
        [uniqueInfo.append({'name': noun, 'complements': comp}) for noun, comp in self.uniqueInfo.items()]
        [commonInfo.append({'name': noun, 'complements': comp}) for noun, comp in self.commonInfo.items()]
        [uniqueSectorInfo.append({'name': noun, 'complements': comp}) for noun, comp in self.uniqueSectorInfo.items()]
        [commonSectorInfo.append({'name': noun, 'complements': comp}) for noun, comp in self.commonSectorInfo.items()]
        self.valuableInfo = valuableInfo
        self.positives = positives
        self.negatives = negatives
        self.uniqueInfo = uniqueInfo
        self.commonInfo = commonInfo
        self.uniqueSectorInfo = uniqueSectorInfo
        self.commonSectorInfo = commonSectorInfo
    
    
    
    def setValuableInfo(self, valuableInfo):
        """Establece la información extraída del análisis de descripciones.
        
        Parámetros:
        valuableInfo -- lista de pares {servicio: atributos de dicho servicio}
        
        """ 
        self.valuableInfo = valuableInfo.copy()



    def analyzeReviews(self):
        """Análisis de las opiniones.
        
        Se busca en cada opinión los valores extraídos del análisis de las
        descripciones, almacenando aquellos de los que se hable positivamente o
        negativamente, y el número de veces que se mencionan en cada caso.
        
        """
        positives = {}
        negatives = {}
        posName = "tmp/" + re.sub('[^0-9a-zA-Z]+', '_', self.name).strip() + '_posReviews-parsed.txt'
        negName = "tmp/" + re.sub('[^0-9a-zA-Z]+', '_', self.name).strip() + '_negReviews-parsed.txt'
        posDoc = open(posName, 'r', encoding='UTF-8')
        negDoc = open(negName, 'r', encoding='UTF-8')
        for line in posDoc:
            line = line.strip()
            if re.search("NC", line) or re.search("TV", line):
                lemma = line.split()[1]
                for key in self.valuableInfo.keys():
                    if lemma == key:
                        if key not in positives:
                            positives[key] = 1
                        else:
                            positives[key] = positives.get(key) + 1
        posDoc.close()
        for line in negDoc:
            line = line.strip()
            if re.search("NC", line) or re.search("TV", line):
                lemma = line.split()[1]
                for key in self.valuableInfo.keys():
                    if re.search(key, line) and key != "":
                        if key not in negatives:
                            negatives[key] = 1
                        else:
                            negatives[key] = negatives.get(key) + 1
        negDoc.close()
        
        self.positives = sorted(positives.items(), key=operator.itemgetter(1), reverse=True)
        self.negatives = sorted(negatives.items(), key=operator.itemgetter(1), reverse=True)
        
        """
        positiveDeletes = []
        for positiveKey, positiveValue in positives.items():
            if positiveKey in negatives.keys():
                if positiveValue > negatives.get(positiveKey):
                    positives[positiveKey] = positiveValue - negatives.get(positiveKey)
                    negatives.pop(positiveKey)
                elif positiveValue < negatives.get(positiveKey):
                    negatives[positiveKey] = negatives.get(positiveKey) - positiveValue
                    positiveDeletes.append(positiveKey)
        for key in positiveDeletes:
            positives.pop(key)
        
        self.positives = sorted(positives.items(), key=operator.itemgetter(1), reverse=True)
        self.negatives = sorted(negatives.items(), key=operator.itemgetter(1), reverse=True)
        """



    def analyzeReviewsEnglish(self):
        """Análisis de opiniones. Idioma Inglés.
        
        """
        self.positives = {}
        self.negatives = {}
        posName = "tmp/" + re.sub('[^0-9a-zA-Z]+', '_', self.name).strip() + '_posReviews-parsed.txt'
        negName = "tmp/" + re.sub('[^0-9a-zA-Z]+', '_', self.name).strip() + '_negReviews-parsed.txt'
        posDoc = open(posName, 'r', encoding='UTF-8')
        negDoc = open(negName, 'r', encoding='UTF-8')
        for line in posDoc:
            line = line.strip()
            if re.search("NN", line) or re.search("TV", line) or re.search("wi-fi", line):
                lemma = line.split()[1]
                for key in self.valuableInfo.keys():
                    if lemma == key:
                        if key not in self.positives:
                            self.positives[key] = 1
                        else:
                            self.positives[key] = self.positives.get(key) + 1
        posDoc.close()
        for line in negDoc:
            line = line.strip()
            if re.search("NN", line) or re.search("TV", line) or re.search("wi-fi", line):
                lemma = line.split()[1]
                for key in self.valuableInfo.keys():
                    if re.search(key, line) and key != "":
                        if key not in self.negatives:
                            self.negatives[key] = 1
                        else:
                            self.negatives[key] = self.negatives.get(key) + 1
        negDoc.close()
        
        positiveDeletes = []
        for positiveKey, positiveValue in self.positives.items():
            if positiveKey in self.negatives.keys():
                if positiveValue > self.negatives.get(positiveKey):
                    self.negatives.pop(positiveKey)
                elif positiveValue < self.negatives.get(positiveKey):
                    positiveDeletes.append(positiveKey)
        for key in positiveDeletes:
            self.positives.get(key)



    def analyzeCommonsBundle(self, globalData, bundle):
        """Determina las características comunes y únicas del hotel.
        
        Extrae qué características de este hotel son comunes y cuáles únicas
        entre todos los hoteles analizados.
        
        Parámetros:
        globalData -- datos globales de todos los hoteles
        bundle -- True si evaluamos nombre+complemento, False si complementos.
        
        """
        self.uniqueInfo = {}
        self.commonInfo = {}
        nouns = [noun for noun in self.valuableInfo.keys() if (globalData['noun'].get(noun) > 1)] #Asimilando que 1 es mayoritariamente un error
        if not nouns:
            self.uniqueSectorInfo = self.valuableInfo.copy()
        else:
            for noun in nouns:
                if bundle:
                    uniqueComplements = [complement for complement in self.valuableInfo.get(noun) if (globalData.get('global').get(noun + " " + complement) == 1)]
                    commonComplements = [complement for complement in self.valuableInfo.get(noun) if (globalData.get('global').get(noun + " " + complement) > 1)]
                else:
                    uniqueComplements = [complement for complement in self.valuableInfo.get(noun) if (globalData.get('complement').get(complement) == 1)]
                    commonComplements = [complement for complement in self.valuableInfo.get(noun) if (globalData.get('complement').get(complement) > 1)]
                if uniqueComplements:
                    self.uniqueInfo[noun] = uniqueComplements
                if commonComplements:
                    self.commonInfo[noun] = commonComplements



    def analyzeSectorCommonsBundle(self, sectorData, bundle):
        """Determina las características comunes y únicas del hotel en sector.
        
        Extrae qué características de este hotel son comunes y cuáles únicas
        entre los hoteles pertenecientes a su mismo sector turístico.
        
        Parámetros:
        sectorData -- datos globales de todos los hoteles por sector.
        bundle -- True si evaluamos nombre+complemento, False si complementos.
        
        """
        self.uniqueSectorInfo = {}
        self.commonSectorInfo = {}
        nouns = [noun for noun in self.valuableInfo.keys() if (sectorData[self.region]['noun'].get(noun) > 1)] #Asimilando que 1 es mayoritariamente un error
        if not nouns:
            self.uniqueSectorInfo = self.valuableInfo.copy()
        else:
            for noun in nouns:
                if bundle:
                    uniqueComplements = [complement for complement in self.valuableInfo.get(noun) if (sectorData.get(self.region).get('global').get(noun + " " + complement) == 1)]
                    commonComplements = [complement for complement in self.valuableInfo.get(noun) if (sectorData.get(self.region).get('global').get(noun + " " + complement) > 1)]
                else:
                    uniqueComplements = [complement for complement in self.valuableInfo.get(noun) if (sectorData.get(self.region).get('complement').get(complement) == 1)]
                    commonComplements = [complement for complement in self.valuableInfo.get(noun) if (sectorData.get(self.region).get('complement').get(complement) > 1)]
                if uniqueComplements:
                    self.uniqueSectorInfo[noun] = uniqueComplements
                if commonComplements:
                    self.commonSectorInfo[noun] = commonComplements
