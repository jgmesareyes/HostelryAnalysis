'''
Created on 9 de abr. de 2016

@author: Jose
'''

import re



class Hotel(object):
    """Representa un Hotel
    
    Almacena los datos relativos a un hotel, así como los datos extraídos
    después de llevar a cabo el análisis tanto global como por sectores.
    
    """
    def __init__(self, name, description, address, coords, facilities, languages, reviews):
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
        self.name = name
        self.description = description
        self.address = address
        self.coords = coords
        self.facilities = facilities
        self.languages = languages
        self.reviews = reviews
    
    
    
    def setValuableInfo(self, valuableInfo):
        """Establece la información extraída del análisis de descripciones.
        
        Parámetros:
        valuableInfo -- lista de pares {servicio: atributos de dicho servicio}
        
        """ 
        self.valuableInfo = valuableInfo.copy()
    
    
    
    def setRegion(self, region):
        """Establece el sector al que pertenece.
        
        Parámetros:
        region -- sector turístico
        
        """        
        self.region = region



    def analyzeReviews(self):
        """Análisis de las opiniones.
        
        Se busca en cada opinión los valores extraídos del análisis de las
        descripciones, almacenando aquellos de los que se hable positivamente o
        negativamente, y el número de veces que se mencionan en cada caso.
        
        """
        self.positives = {}
        self.negatives = {}
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
                        if key not in self.positives:
                            self.positives[key] = 1
                        else:
                            self.positives[key] = self.positives.get(key) + 1
        posDoc.close()
        for line in negDoc:
            line = line.strip()
            if re.search("NC", line) or re.search("TV", line):
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



    def analyzeCommonsBundle(self, descriptionsData, bundle):
        """Determina las características comunes y únicas del hotel.
        
        Extrae qué características de este hotel son comunes y cuáles únicas
        entre todos los hoteles analizados.
        
        Parámetros:
        descriptionsData -- datos globales de todos los hoteles
        bundle -- True si evaluamos nombre+complemento, False si complementos.
        
        """
        self.uniqueInfo = {}
        self.commonInfo = {}
        nouns = [noun for noun in self.valuableInfo.keys() if (descriptionsData['noun'].get(noun) > 1)] #Asimilando que 1 es mayoritariamente un error
        if not nouns:
            self.uniqueSectorInfo = self.valuableInfo.copy()
        else:
            for noun in nouns:
                if bundle:
                    uniqueComplements = [complement for complement in self.valuableInfo.get(noun) if (descriptionsData.get('global').get(noun + " " + complement) == 1)]
                    commonComplements = [complement for complement in self.valuableInfo.get(noun) if (descriptionsData.get('global').get(noun + " " + complement) > 1)]
                else:
                    uniqueComplements = [complement for complement in self.valuableInfo.get(noun) if (descriptionsData.get('complement').get(complement) == 1)]
                    commonComplements = [complement for complement in self.valuableInfo.get(noun) if (descriptionsData.get('complement').get(complement) > 1)]
                if uniqueComplements:
                    self.uniqueInfo[noun] = uniqueComplements
                if commonComplements:
                    self.commonInfo[noun] = commonComplements



    def analyzeSectorCommonsBundle(self, sectorData, bundle):
        """Determina las características comunes y únicas del hotel en sector.
        
        Extrae qué características de este hotel son comunes y cuáles únicas
        entre los hoteles pertenecientes a su mismo sector turístico.
        
        Parámetros:
        descriptionsData -- datos globales de todos los hoteles
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



    def showInfo(self, withReviews):
        """Muestra la información del hotel.
        
        Parámetros:
        withReviews -- True si queremos mostrar también los comentarios.
        
        """
        print("Hotel Name: " + self.name)
        print("Hotel Description: " + self.description)
        print("Hotel Address: " + self.address)
        print("Hotel Coords: " + str(self.coords))
#        print("Hotel Facilities: " + str(self.facilities))
        print("Hotel Spoken Languages: " + str(self.languages))
        print("Hotel Reviews:")
        if withReviews:
            for review in self.reviews:
                print("Review Author: " + review['name'])
                print("Review Neg: " + review['neg'])
                print("Review Pos: " + review['pos'])



    def showValuableInfo(self):
        """Muestra las características extraídas de la descripción del hotel.
        
        """
        for noun, complements in self.valuableInfo.items():
            print("Noun: " + noun)
            print("Values: " + str(complements) + " ")



    def commonUniqueInfo(self):
        """Muestra las características comunes y únicas del hotel en global.
        
        """
        print("<<< HOTEL " + self.name + " Services Analysis >>>")
        print("Unique Hotel Services:")
        for key, value in self.uniqueInfo.items():
            print("[" + key + "] => " + str(value))
        print("Common Hotel Services:")
        for key, value in self.commonInfo.items():
            print("[" + key + "] => " + str(value))
    
    
    
    def commonUniqueSectorInfo(self):
        """Muestra las características comunes y únicas del hotel en su sector.
        
        """
        print("<<< HOTEL " + self.name + " Services Analysis >>>")
        print("Unique Hotel Services:")
        for key, value in self.uniqueSectorInfo.items():
            print("[" + key + "] => " + str(value))
        print("Common Hotel Services:")
        for key, value in self.commonSectorInfo.items():
            print("[" + key + "] => " + str(value))



    def reviewsInfo(self):
        """Muestra los servicios valorados de forma positiva y negativa.
        
        """
        print(" === Positive Services === ")
        for key, value in self.positives.items():
            print("[" + key + "] found " + str(value) + " times")
        print(" === Negative Services === ")
        for key, value in self.negatives.items():
            print("[" + key + "] found " + str(value) + " times")


