import os
import subprocess
import re
import geocoder
import time
import operator

from urllib.request import urlopen
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue

from app import db, dependency_values
from config import portENG, portSPA, serverPath, clientPath, configSetupParsed, corefSetup, BOOKING_URLS, MAX_THREADS
from config import basedir
from .models import Hotel, Hostelry
from .services import HotelService




class HotelThread(Thread):
    """Hilo de Hotel.
    
    Funcionamiento del análisis de hoteles en paralelo.
    
    """
    def __init__(self, queue, instance):
        Thread.__init__(self)        
        self.queue = queue
        self.instance = instance

    def run(self):
        while True:
            threadName, url, executionMode = self.queue.get()
            self.name = threadName
            print("[THREAD] - '" + self.getName() + "' : Launched")
            self.instance.bookingHotelDetails(url, executionMode)
            print("[THREAD] - '" + self.getName() + "' : Finished")
            self.queue.task_done()
            if self.queue.empty():
                self._tstate_lock = None
                self._stop()




class HostelryManager:
    """Gestiona el análisis de hoteles.
    
    Parámetros:
    hotelList -- lista de hoteles
    elapsedTimes -- registro de tiempos de la aplicación
    globalData -- registro global de información de todos los hoteles
    sectorData -- registro de la información de los hoteles por sectores
    globalStats -- estadísticas globales de cada tipo de característica
    sectorStats -- estadísticas por sector de cada tipo de característica
    
    """
    
    def __init__(self):
        self.hotelList = []
        self.elapsedTimes = {}
        self.globalData = {'noun' : {}, 'verb' : {}, 'complement' : {}, 'global' : {}}
        self.sectorData = {}
        self.globalStats = {}
        self.sectorStats = {}
        self.sectorHotels = {}
        self.analyzedHotels = 0
        self.language = ''
    
    
    
    def start(self, island, language, executionMode, limit):
        """Gestiona el procesado y análisis de hoteles.
        
        Se inicializan los servidores de Freeling según el idioma elegido y
        las características especificadas en el archivo 'config.py'.
        Se realiza la búsqueda en http://booking.com con las opciones elegidas,
        lanzando hilos asíncronos para multiplicar el desarrollo en paralelo de
        varios hoteles simultáneamente, y esperando la conclusión de todos para
        generar las estadísticas.
        Procesado de las características y cálculo de estadísticas tanto
        globales como por sector.
        Registro de tiempos de respuesta.
        Interacción con la base de datos y cruce de referencias.
        Shutdown de servidores Freeling.
        
        Parámetros:
        bookingUrl -- url de resultados de hoteles
        limit -- límite de hoteles a buscar 
        
        """
        self.__init__()
        self.language = language
        if executionMode == 'MERGE':
            self.fetchGlobals()
        start = time.clock()
        if language == 'SP':
            serverSpa = subprocess.Popen(serverPath + configSetupParsed + corefSetup + " --server --port " + str(portSPA))
            print("[Spanish Analyze Server] Starting with Port Number :: " + str(portSPA))
        else:
            serverEng = subprocess.Popen(serverPath + configSetupParsed.replace('es', 'en') + corefSetup.replace('es', 'en') + " --server --port " + str(portENG))
            print("[English Analyze Server] Starting with Port Number :: " + str(portENG))
        
        bookingUrl = BOOKING_URLS[island][language]
        self.bookingHotelSearch(bookingUrl, executionMode, limit, language)
        self.elapsedTimes['analysis'] = time.clock() - start
        timeFlag = time.clock()
        for hotel in self.hotelList:
            hotel.analyzeCommonsBundle(self.globalData, True)
            hotel.analyzeSectorCommonsBundle(self.sectorData, True)
            hotel.updateInDB()
            hotel.parseData()
        self.runStatistics()
        self.runStatisticsSector()
        self.setFeatures()
        self.setKeywords()
        self.elapsedTimes['statistics'] = "%.4f" % (time.clock() - timeFlag)
        timeFlag = time.clock()
        self.elapsedTimes['total'] = "%.4f" % (time.clock() - start)
        self.elapsedTimes['hotel_quantity'] = "ALL" if limit == 10000 else limit
        self.elapsedTimes['analyzed_hotels'] = self.analyzedHotels
        self.elapsedTimes['average_hotel_time'] = "%.4f" % (self.elapsedTimes['analysis'] / self.analyzedHotels) if (self.analyzedHotels > 0) else 0.0
        self.elapsedTimes['analysis'] = "%.4f" % self.elapsedTimes['analysis']
        
        if executionMode == 'MERGE':
            self.setGlobals()
        
        if language == 'SP':
            serverSpa.terminate()
            print("[Spanish Analyze Server] Finished")
        else:
            serverEng.terminate()
            print("[English Analyze Server] Finished")



    def bookingHotelSearch(self, nextUrl, executionMode="MERGE", limit=10000, language='SP'):
        """Obtiene las url de todos los hoteles.
        
        Se lanza un hilo de trabajo por cada hotel, aumentando considerablemente
        el rendimiento y disminuyendo los tiempos de respuesta, y se espera al
        término de todos ellos para finalizar la función.
        
        Parámetros:
        nextUrl -- url de resultados de hoteles, se itera si hay varias
        limit -- límite de hoteles
        spanish -- True si se analiza en Español, False en Inglés
        
        """
        queue = Queue()
        threadLimit = min(MAX_THREADS, limit)
        for _ in range(threadLimit):
            hotelThread = HotelThread(queue, self)
            hotelThread.start()
        count = 0        
        print("Hotel Limit: NONE") if limit == 10000 else print("Hotel Limit: " + str(limit))
        while (re.match('http://www.booking.com/searchresults', nextUrl) and count < limit):
            htmlSource = urlopen(nextUrl).read()
            soup = BeautifulSoup(htmlSource, 'html.parser')
            for link in soup.find_all('a', {'class' : 'hotel_name_link url'}):
                if count < limit:
                    threadName = link.get('href')
                    threadName = threadName[threadName.rfind('/hotel/') + 10:threadName.find('.')]
                    queue.put((threadName, 'http://www.booking.com' + link.get('href'), executionMode))
                count += 1
            if count < limit:
                if soup.find('a', {'class' : 'paging-next'}):
                    nextUrl = soup.find('a', {'class' : 'paging-next'}).get('href')
                else:
                    nextUrl = 'None'
        queue.join()
    
    
    
    def analyzeData(self, hotel):
        """Ejecuta los análisis de características y valoraciones.
        
        Parámetros:
        hotel -- hotel tratado
        spanish -- True si se analiza en Español, False en Inglés
        
        """
        if hotel.region not in self.sectorData.keys():
            self.sectorData[hotel.region] = {'noun' : {}, 'complement' : {}, 'global' : {}}
        docName = re.sub('[^0-9a-zA-Z]+', '_', hotel.name).strip()
        docPath = "tmp/" + docName
        descriptionDoc = open(docPath + '.txt', 'w', encoding='UTF-8')
        descriptionDoc.write(hotel.description)
        descriptionDoc.close()
        posDocName = docPath + "_posReviews"
        negDocName = docPath + "_negReviews"
        if self.language == 'SP':
            os.system(clientPath + str(portSPA) + " <" + docPath + ".txt >" + docPath + "-parsed.txt")
            os.system(clientPath + str(portSPA) + " <" + posDocName + ".txt >" + posDocName + "-parsed.txt")
            os.system(clientPath + str(portSPA) + " <" + negDocName + ".txt >" + negDocName + "-parsed.txt")
            hotel.setValuableInfo(dependency_values.searchGroupsGenreLemmasData(self.globalData, self.sectorData[hotel.region], docPath + "-parsed.txt"))
            hotel.analyzeReviews()
        else:
            os.system(clientPath + str(portENG) + " <" + docPath + ".txt >" + docPath + "-parsed.txt")
            os.system(clientPath + str(portENG) + " <" + posDocName + ".txt >" + posDocName + "-parsed.txt")
            os.system(clientPath + str(portENG) + " <" + negDocName + ".txt >" + negDocName + "-parsed.txt")
            hotel.setValuableInfo(dependency_values.searchGroupsGenreLemmasDataEnglish(self.globalData, self.sectorData[hotel.region], docPath + "-parsed.txt"))
            hotel.analyzeReviewsEnglish()
        if hotel.region not in self.sectorHotels.keys():
            self.sectorHotels[hotel.region] = 1
        else:
            self.sectorHotels[hotel.region] = self.sectorHotels.get(hotel.region) + 1
        self.hotelList.append(hotel)
        os.system('del ' + docName + '*.txt /s')
    
    
    
    def bookingHotelDetails(self, url, executionMode):
        """Webscraping de hoteles.
        
        Se extrae y analiza toda la información relativa a cada hotel.
        
        Parámetros:
        url -- url del hotel
        spanish -- True si se analiza en Español, False en Inglés
        
        """
        htmlSource = urlopen(url).read()
        soup = BeautifulSoup(htmlSource, 'html.parser')
        hotelFacilities = []
        hotelLanguages = []
        reviewsUrl = 'http://www.booking.com'
        hotelName = soup.find('span', {'id' : 'hp_hotel_name'}).getText().strip()
        dbHotel = Hotel.query.get([hotelName, self.language])
        hotel = HotelService()
        if executionMode == "MERGE" and dbHotel is not None:
            hotel.fetchFromDB(dbHotel)
            self.hotelList.append(hotel)
            if dbHotel.region not in self.sectorHotels.keys():
                self.sectorHotels[dbHotel.region] = 1
            else:
                self.sectorHotels[dbHotel.region] = self.sectorHotels.get(dbHotel.region) + 1
        else:
            self.analyzedHotels += 1
            hotelDescriptionData = str(soup.find('div', {'id' : 'summary'}))
            if re.search('bicon-acstar', hotelDescriptionData):
                hotelDescription = hotelDescriptionData[hotelDescriptionData.find('</span>') + 7:hotelDescriptionData.rfind('<br/>')].replace('<p>', '').replace('</p>', '')
            else:
                hotelDescription = soup.find('div', {'id' : 'summary'}).getText().strip()
            hotelAddressData = soup.find('span', {'class' : 'hp_address_subtitle'})
            hotelAddress = hotelAddressData.getText().strip()
            hotelCoords = geocoder.google(hotelAddress).latlng
            if len(hotelCoords) == 0:
                bbox = hotelAddressData.get('data-bbox').split(',')
                hotelCoords = [float(bbox[3]), float(bbox[0])]
            for data in soup.findAll('div', {'class' : 'facilitiesChecklistSection'}):
                if re.match('Languages', data.find('h5').getText().strip()) or re.match('Idiomas', data.find('h5').getText().strip()):
                    for language in data.findAll('li'):
                        hotelLanguage = language.getText().strip()
                        if hotelLanguages.count(hotelLanguage) == 0:
                            hotelLanguages.append(hotelLanguage)
                else:
                    for facility in data.findAll('li'):
                        hotelFacility = facility.getText().strip()
                        hotelFacility = hotelFacility[:-1] if hotelFacility.endswith('.') else hotelFacility
                        if hotelFacilities.count(hotelFacility) == 0 and not re.search('!', hotelFacility):
                            if re.match('No se admiten', hotelFacility):
                                hotelFacility = hotelFacility[:-1] + " " + data.find('h5').getText().strip().lower()
                            hotelFacilities.append(hotelFacility)
            reviewsUrl += soup.find('a', {'class' : 'show_all_reviews_btn'}).get('href')
            hotelReviews = self.bookingHotelReviews(reviewsUrl, hotelName)

            hotel.createHotel(hotelName, self.language, hotelDescription, hotelAddress, hotelCoords, hotelFacilities, hotelLanguages, hotelReviews)
            self.analyzeData(hotel)
    
    
    
    def bookingHotelReviews(self, url, hotelName):
        """Extrae la información de las valoraciones del hotel.
        
        Parámetros:
        url -- url de las valoraciones del hotel
        hotelName -- nombre del hotel
        
        """
        htmlSource = urlopen(url).read()
        soup = BeautifulSoup(htmlSource, 'html.parser')
        infoList = []
        docNameBase = "tmp/" + re.sub('[^0-9a-zA-Z]+', '_', hotelName).strip()
        posDoc = open(docNameBase + "_posReviews.txt", 'w', encoding='UTF-8')
        negDoc = open(docNameBase + "_negReviews.txt", 'w', encoding='UTF-8')
        for divElement in soup.findAll('li', {'class' : 'review_item clearfix '}):
            info = {'name' : '', 'neg' : '', 'pos' : ''}
            authorElement = divElement.find('div', {'class' : 'review_item_reviewer'})
            name = authorElement.find('span', {'itemprop' : 'name'}).getText()
            info['name'] = name
            if (divElement.find('p', {'class' : 'review_neg'})):
                reviewNegElement = divElement.find('p', {'class' : 'review_neg'})
                negative = reviewNegElement.find('span', {'itemprop' : 'reviewBody'}).getText()
                info['neg'] = negative
                negDoc.write(negative)
            else:
                info['neg'] = ''
            if (divElement.find('p', {'class' : 'review_pos'})):
                reviewPosElement = divElement.find('p', {'class' : 'review_pos'})
                positive = reviewPosElement.find('span', {'itemprop' : 'reviewBody'}).getText()
                info['pos'] = positive
                posDoc.write(positive)
            else:
                info['pos'] = ''
            infoList.append(info)
        posDoc.close()
        negDoc.close()
    
        return infoList
    
    
    def defineIndex(self, spanish):
        """Genera un index para los lexicon.
        
        Parámetros:
        spanish -- True si se analiza en Español, False en Inglés
        
        """
        index = {'positive': {}, 'negative': {}}
        if spanish:
            path = os.path.join(basedir, 'lexicon', 'spanish')
        else:
            path = os.path.join(basedir, 'lexicon', 'english')
        letter = 'a'
        index['positive'][letter] = 0
        for i, line in enumerate(open(os.path.join(path, 'positive_words.txt'), encoding='UTF-8').readlines()):
            if line[0] != letter:
                letter = line[0]
                index['positive'][letter] = i
        letter = 'a'
        index['negative'][letter] = 0
        for i, line in enumerate(open(os.path.join(path, 'negative_words.txt'), encoding='UTF-8').readlines()):
            if line[0] != letter:
                letter = line[0]
                index['negative'][letter] = i
        return index
            
            
    def reviewAnalyze(self, spanish):
        """Analiza la índole de cada valoración.
        
        Parámetros:
        spanish -- True si se analiza en Español, False en Inglés
        
        """
        index = self.defineIndex(spanish)
        if spanish:
            path = os.path.join(basedir, 'lexicon', 'spanish')
        else:
            path = os.path.join(basedir, 'lexicon', 'english')
        for review in self.reviews:
            value = 0
            for word in review:
                positiveLexicon = open(os.path.join(path, 'positive_words.txt'), 'r')
                startIndexLetter = word[0]
                startLine = index['positive'][startIndexLetter]
                if startIndexLetter != 'z' or startIndexLetter != 'Z':
                    nextIndexLetter = chr(ord(startIndexLetter) + 1)
                    endLine = index['positive'][nextIndexLetter]
                else:
                    endLine = None
                positiveLexicon.seek(startLine, 0)
                for line in positiveLexicon:
                    if line.trim() == word:
                        value += 1
                    if endLine is not None and positiveLexicon.tell() >= endLine:
                        break
                negativeLexicon = open(os.path.join(path, 'negative_words.txt'), 'r')
                startIndexLetter = word[0]
                startLine = index['negative'][startIndexLetter]
                if startIndexLetter != 'z' or startIndexLetter != 'Z':
                    nextIndexLetter = chr(ord(startIndexLetter) + 1)
                    endLine = index['negative'][nextIndexLetter]
                else:
                    endLine = None
                negativeLexicon.seek(startLine, 0)
                for line in negativeLexicon:
                    if line.trim() == word:
                        value -= 1
                    if endLine is not None and negativeLexicon.tell() >= endLine:
                        break
            if value > 0:
                review['pos'] = review
            else:
                review['neg'] = review
        for review in self.reviews:
            review.pop('review', None)

    
    
    def runStatistics(self):
        """Ejecuta la estadística de las características globales.
        
        """
        for dataType, data in self.globalData.items():
            size = 0
            for key, value in data.items():
                size += value
            valueStats = {}
            for key, value in data.items():
                valueStats[key] = float("{0:.2f}".format(value / size * 100))
            sortedValues = sorted(valueStats.items(), key=operator.itemgetter(1), reverse=True)
            self.globalStats[dataType] = sortedValues[:10].copy()
    
    
    
    def runStatisticsSector(self):
        """Ejecuta la estadística de las características por sector.
        
        """
        for sector, sectorContent in self.sectorData.items():
            if sector in self.sectorHotels.keys():
                sectorStat = {}
                for dataType, data in sectorContent.items():
                    size = 0
                    for key, value in data.items():
                        size += value
                    valueStats = {}
                    for key, value in data.items():
                        valueStats[key] = float("{0:.2f}".format(value / size * 100))
                    sortedValues = sorted(valueStats.items(), key=operator.itemgetter(1), reverse=True)
                    sectorStat[dataType] = sortedValues[:10].copy()
                self.sectorStats[sector] = sectorStat
    
    
    
    def fetchGlobals(self):
        """Recoge los datos generales globales y por sectores de la BD.
        
        """
        for row in Hostelry.query.filter_by(lang=self.language):
            if row.region == 'Global':
                self.globalData = row.data
            else:
                self.sectorData[row.region] = row.data
    
    
    
    def setGlobals(self):
        """Establece los datos generales globales y por sectores en la BD.
        
        """
        hostelryData = Hostelry.query.get(['Global', self.language])
        if hostelryData is None:
            hostelryData = Hostelry()
            hostelryData.region = 'Global'
            hostelryData.lang = self.language
        hostelryData.data = self.globalData.copy()
        db.session.add(hostelryData)
        for sector, sectorData in self.sectorData.items():
            hostelryData = Hostelry.query.get([sector, self.language])
            if hostelryData is None:
                hostelryData = Hostelry()
                hostelryData.region = sector
                hostelryData.lang = self.language
            hostelryData.data = sectorData.copy()
            db.session.add(hostelryData)
        db.session.commit()



    def setFeatures(self):
        self.features = list();
        globalHotels = [{'name': hotel.name, 'uniqueInfo': hotel.uniqueInfo, 'commonInfo': hotel.commonInfo} for hotel in self.hotelList]
        self.features.append({'sector': 'Global', 'sectorHotels': globalHotels})
        for sector in self.sectorHotels.keys():
            hotels = list();
            for hotel in self.hotelList:
                if sector == hotel.region:
                    hotels.append({'name': hotel.name, 'uniqueInfo': hotel.uniqueSectorInfo, 'commonInfo': hotel.commonSectorInfo})
            self.features.append({'sector': sector, 'sectorHotels': hotels})
    
    
    
    def setKeywords(self):
        self.keywords = list();
        datatypeValues = list();
        for datatype, data in self.globalStats.items():
            dataValues = list();
            [dataValues.append({'name': value[0], 'values': value[1]}) for value in data]
            datatypeValues.append({'datatype': datatype, 'datavalues': dataValues})
        self.keywords.append({'sector': 'Global', 'sectordata': datatypeValues})
        for sector, sectorInfo in self.sectorStats.items():
            datatypeValues = list()
            for datatype, data in sectorInfo.items():
                dataValues = list();
                [dataValues.append({'name': value[0], 'values': value[1]}) for value in data]
                datatypeValues.append({'datatype': datatype, 'datavalues': dataValues})
            self.keywords.append({'sector': sector, 'sectordata': datatypeValues})
