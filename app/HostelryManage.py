import urllib
import re
from bs4 import BeautifulSoup
from .Hotel import Hotel
from app import DependencyValues
from app.DBManage import setupDatabases, getAreas, setHotels
import os
import subprocess
import time
import threading
import geocoder
import operator
from config import portENG, portSPA, serverPath, clientPath, configSetupParsed, corefSetup
from config import basedir, POSTGRESQL_DATA as PD




class HostelryManage:
    """Gestiona el análisis de hoteles.
    
    Parámetros:
    hotelList -- lista de hoteles
    elapsedTimes -- registro de tiempos de la aplicación
    descriptionsData -- registro global de información de todos los hoteles
    sectorData -- registro de la información de los hoteles por sectores
    globalStats -- estadísticas globales de cada tipo de característica
    sectorStats -- estadísticas por sector de cada tipo de característica
    
    """
    hotelList = []
    elapsedTimes = {}
    descriptionsData = {'noun' : {}, 'verb' : {}, 'complement' : {}, 'global' : {}}
    sectorData = {}
    globalStats = {}
    sectorStats = {}
    #threadLimiter = threading.BoundedSemaphore(10)
    
    
    def __init__(self, bookingUrl, limit):
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
        spanish = True
        start = time.clock()
        if re.search(".en-gb.html", bookingUrl):
            spanish = False
            serverEng = subprocess.Popen(serverPath + configSetupParsed.replace('es', 'en') + corefSetup.replace('es', 'en') + " --server --port " + str(portENG))
            print("[English Analyze Server] Starting with Port Number :: " + str(portENG))
        else:
            serverSpa = subprocess.Popen(serverPath + configSetupParsed + corefSetup + " --server --port " + str(portSPA))
            print("[Spanish Analyze Server] Starting with Port Number :: " + str(portSPA))
        
        self.bookingHotelSearch(bookingUrl, limit, spanish)
        self.elapsedTimes['analysis'] = time.clock() - start
        timeFlag = time.clock()
        
        setupDatabases(self.hotelList)
        self.setRegions()
        self.sectorResearch()
        for hotel in self.hotelList:
            hotel.analyzeCommonsBundle(self.descriptionsData, True)
            hotel.analyzeSectorCommonsBundle(self.sectorData, True)
        self.runStatistics()
        self.runStatisticsSector()
        self.elapsedTimes['statistics'] = "%.4f" % (time.clock() - timeFlag)
        timeFlag = time.clock()
        
        self.elapsedTimes['total'] = "%.4f" % (time.clock() - start)
        self.elapsedTimes['hotel_quantity'] = len(self.hotelList)
        self.elapsedTimes['average_hotel_time'] = "%.4f" % (self.elapsedTimes['analysis'] / len(self.hotelList))
        self.elapsedTimes['analysis'] = "%.4f" % self.elapsedTimes['analysis']
        
        setHotels(PD['dbname'], self.hotelList)
        print("THREADS DONE")
        if spanish:
            serverSpa.terminate()
            print("[Spanish Analyze Server] Finished")
        else:
            serverEng.terminate()
            print("[English Analyze Server] Finished")



    def bookingHotelSearch(self, nextUrl, limit=10000, spanish=True):
        """Obtiene las url de todos los hoteles.
        
        Se lanza un hilo de trabajo por cada hotel, aumentando considerablemente
        el rendimiento y disminuyendo los tiempos de respuesta, y se espera al
        término de todos ellos para finalizar la función.
        
        Parámetros:
        nextUrl -- url de resultados de hoteles, se itera si hay varias
        limit -- límite de hoteles
        spanish -- True si se analiza en Español, False en Inglés
        
        """
        count = 0
        threadList = list()
        print("Hotel Limit: NONE") if limit == 10000 else print("Hotel Limit: " + str(limit))
        while (re.match('http://www.booking.com/searchresults', nextUrl) and count < limit):
            htmlSource = urllib.request.urlopen(nextUrl).read()
            soup = BeautifulSoup(htmlSource, 'html.parser')
            for link in soup.find_all('a', {'class' : 'hotel_name_link url'}):
                if count < limit:
                    threadName = link.get('href')
                    threadName = threadName[threadName.rfind('/hotel/') + 10:threadName.find('.')]
                    t = threading.Thread(name=threadName, target=self.bookingHotelDetails, args=('http://www.booking.com' + link.get('href'), spanish))
                    threadList.append(t)
                    t.start()
                count += 1
            if count < limit:
                if soup.find('a', {'class' : 'paging-next'}):
                    nextUrl = soup.find('a', {'class' : 'paging-next'}).get('href')
                else:
                    nextUrl = 'None'
        for thread in threadList:
            thread.join()
    
    
    
    def analyzeData(self, hotel, spanish):
        """Ejecuta los análisis de características y valoraciones.
        
        Parámetros:
        hotel -- hotel tratado
        spanish -- True si se analiza en Español, False en Inglés
        
        """
        docName = re.sub('[^0-9a-zA-Z]+', '_', hotel.name).strip()
        docPath = "tmp/" + docName
        descriptionDoc = open(docPath + '.txt', 'w', encoding='UTF-8')
        descriptionDoc.write(hotel.description)
        descriptionDoc.close()
        posDocName = docPath + "_posReviews"
        negDocName = docPath + "_negReviews"
        if spanish:
            os.system(clientPath + str(portSPA) + " <" + docPath + ".txt >" + docPath + "-parsed.txt")
            os.system(clientPath + str(portSPA) + " <" + posDocName + ".txt >" + posDocName + "-parsed.txt")
            os.system(clientPath + str(portSPA) + " <" + negDocName + ".txt >" + negDocName + "-parsed.txt")
            hotel.setValuableInfo(DependencyValues.searchGroupsGenreLemmasData(self.descriptionsData, docPath + "-parsed.txt"))
            hotel.analyzeReviews()
        else:
            os.system(clientPath + str(portENG) + " <" + docPath + ".txt >" + docPath + "-parsed.txt")
            os.system(clientPath + str(portENG) + " <" + posDocName + ".txt >" + posDocName + "-parsed.txt")
            os.system(clientPath + str(portENG) + " <" + negDocName + ".txt >" + negDocName + "-parsed.txt")
            hotel.setValuableInfo(DependencyValues.searchGroupsGenreLemmasDataEnglish(self.descriptionsData, docPath + "-parsed.txt"))
            hotel.analyzeReviewsEnglish()
        self.hotelList.append(hotel)
        os.system('del ' + docName + '*.txt /s')
        print("[THREAD] - '" + threading.currentThread().getName() + "' : Finished")
    
    
    
    def bookingHotelDetails(self, url, spanish):
        """Webscraping de hoteles.
        
        Se extrae y analiza toda la información relativa a cada hotel.
        
        Parámetros:
        url -- url del hotel
        spanish -- True si se analiza en Español, False en Inglés
        
        """
        print("[THREAD] - '" + threading.currentThread().getName() + "' : Launched")
        htmlSource = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(htmlSource, 'html.parser')
        hotelFacilities = []
        hotelLanguages = []
        reviewsUrl = 'http://www.booking.com'
        hotelName = soup.find('span', {'id' : 'hp_hotel_name'}).getText().strip()
        hotelDescriptionData = str(soup.find('div', {'id' : 'summary'}))
        if re.search('bicon-acstar', hotelDescriptionData):
            hotelDescription = hotelDescriptionData[hotelDescriptionData.find('</span>') + 7:hotelDescriptionData.rfind('<br/>')].replace('<p>', '').replace('</p>', '')
        else:
            hotelDescription = soup.find('div', {'id' : 'summary'}).getText().strip()
        #hotelAddressData = soup.find('span', {'itemprop' : 'address'})
        hotelAddressData = soup.find('span', {'class' : 'hp_address_subtitle'})
        hotelAddress = hotelAddressData.getText()
        hotelCoords = geocoder.google(hotelAddress).latlng
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
        self.analyzeData(Hotel(hotelName, hotelDescription, hotelAddress, hotelCoords, hotelFacilities, hotelLanguages, hotelReviews), spanish)
    
    
    
    def bookingHotelReviews(self, url, hotelName):
        """Extrae la información de las valoraciones del hotel.
        
        Parámetros:
        url -- url de las valoraciones del hotel
        hotelName -- nombre del hotel
        
        """
        htmlSource = urllib.request.urlopen(url).read()
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

    
    
    def setRegions(self):
        """Establece las regiones de cada hotel.
        
        """
        for result in getAreas(PD['dbname'], self.hotelList):
            for hotel in self.hotelList:
                if hotel.name == str(result[1]):
                    hotel.setRegion(str(result[0]))
        for hotel in self.hotelList:
            if not hasattr(hotel, 'region'):
                hotel.setRegion("No definida")
    
    
    
    def sectorResearch(self):
        """Genera las características de cada sector a partir de los hoteles.
        
        """
        for hotel in self.hotelList:
            if hotel.region not in self.sectorData.keys():
                self.sectorData[hotel.region] = {'noun' : {}, 'complement' : {}, 'global' : {}}
            for noun, complements in hotel.valuableInfo.items():
                if noun not in self.sectorData[hotel.region]['noun'].keys():
                    self.sectorData[hotel.region]['noun'][noun] = 1
                else:
                    self.sectorData[hotel.region]['noun'][noun] = self.sectorData[hotel.region]['noun'].get(noun) + 1
                for complement in complements:
                    if complement not in self.sectorData[hotel.region]['complement'].keys():
                        self.sectorData[hotel.region]['complement'][complement] = 1
                    else:
                        self.sectorData[hotel.region]['complement'][complement] = self.sectorData[hotel.region]['complement'].get(complement) + 1
                    bundle = noun + " " + complement
                    if bundle not in self.sectorData[hotel.region]['global'].keys():
                        self.sectorData[hotel.region]['global'][bundle] = 1
                    else:
                        self.sectorData[hotel.region]['global'][bundle] = self.sectorData[hotel.region]['global'].get(bundle) + 1
    
    
    
    def runStatistics(self):
        """Ejecuta la estadística de las características globales.
        
        """
        for dataType, data in self.descriptionsData.items():
            size = 0
            counter = 0
            for key, value in data.items():
                size += value
            sortedValues = sorted(data.items(), key=operator.itemgetter(1), reverse = True)
            valueStats = {}
            for data in sortedValues:
                if counter < 10:
                    counter += 1
                    valueStats[data[0]] = "%.2f" % (data[1] / size * 100) + "%"
            self.globalStats[dataType] = valueStats.copy()
    
    
    
    def runStatisticsSector(self):
        """Ejecuta la estadística de las características por sector.
        
        """
        for sector, sectorContent in self.sectorData.items():
            sectorStats = {}
            for dataType, data in sectorContent.items():
                size = 0
                counter = 0
                for key, value in data.items():
                    size += value
                sortedValues = sorted(data.items(), key=operator.itemgetter(1), reverse = True)
                valueStats = {}
                for data in sortedValues:
                    if counter < 10:
                        counter += 1
                        valueStats[data[0]] = "%.2f" % (data[1] / size * 100) + "%"
                sectorStats[dataType] = valueStats.copy()
            self.sectorStats[sector] = sectorStats.copy()
    
    
    def showElapsedTimes(self):
        """Muestra los tiempos de ejecución.
        
        """
        print("ELAPSED TIMES")
        print("Hotel Analysis: " + "%.4f" % self.elapsedTimes['analysis'] + " seconds")
        print("   Number of Hotels: " + str(len(self.hotelList)))
        print("   Average Time per Hotel: " + "%.4f" % (self.elapsedTimes['analysis'] / len(self.hotelList)))
        print("Global Statistics Analysis: " + "%.4f" % (self.elapsedTimes['statistics']) + " seconds")
        print("Hotel Features and Sector Analysis: " + "%.4f" % (self.elapsedTimes['self_features']) + " seconds")
        print("Total Time: " + "%.4f" % (self.elapsedTimes['total']) + " seconds")



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""