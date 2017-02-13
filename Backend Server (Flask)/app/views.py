from flask import render_template, flash, jsonify, request

from app import app, hostelryManager
from config import BOOKING_URLS
from .forms import DataForm
import json




@app.errorhandler(406)
def not_acceptable(error):
    """Genera template para error 406.
    
    """
    return render_template('406.html'), 406


@app.errorhandler(404)
def not_found_error(error):
    """Genera template para error 404.
    
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Genera template para error 500.
    
    """
    return render_template('500.html'), 500


@app.route('/start', methods=['GET', 'POST'])
def start():
    """Enrutamiento básico de la aplicación.
    
    Recoge los parámetros del formulario y ejecuta el análisis.
    
    """
    data = json.loads(request.get_data(as_text=True))
    searchUrl = BOOKING_URLS[data['island']][data['language']]
    limit = int(data['limit'])
    limit = 10000 if limit < 0 else limit
    flash("Limited to: " + str(limit))
    hostelryManager.start(searchUrl, data['mode'], limit)
    return jsonify({'Success': True})
    


# send CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


@app.route('/hotels', methods=['GET'])
def getHotels():
    #hotList = [jsonify(hotel.__dict__) for hotel in hostelryManager.hotelList]
    #hotList = [json.dumps(hotel.__dict__) for hotel in hostelryManager.hotelList]
    hotelsJSON = hostelryManager.hotelsToJSON()
    return hotelsJSON


@app.route('/hotels/<string:hotelName>', methods=['GET'])
def getHotel(hotelName):
    selectedHotel = [hotel for hotel in hostelryManager.hotelList if (hotel.name == hotelName)][0]
    hotelJSON = hostelryManager.hotelToJSON(selectedHotel)
    return hotelJSON


@app.route('/times', methods=['GET'])
def getTimes():
    return jsonify(hostelryManager.elapsedTimes)


@app.route('/features', methods=['GET'])  #Percentages
def getFeatures():
    features = list();
    globalHotels = [{'name': hotel.name, 'uniqueInfo': hotel.uniqueInfo, 'commonInfo': hotel.commonInfo} for hotel in hostelryManager.hotelList]
    features.append({'sector': 'Global', 'sectorHotels': globalHotels})
    for sector in hostelryManager.sectorHotels.keys():
        hotels = list();
        for hotel in hostelryManager.hotelList:
            if sector == hotel.region:
                hotels.append({'name': hotel.name, 'uniqueInfo': hotel.uniqueSectorInfo, 'commonInfo': hotel.commonSectorInfo})
        features.append({'sector': sector, 'sectorHotels': hotels})
    return jsonify(features)


@app.route('/keywords', methods=['GET'])  #Percentages
def getKeywords():
    keywords = list();
    datatypeValues = list();
    for datatype, data in hostelryManager.globalStats.items():
        dataValues = list();
        [dataValues.append({'name': value[0], 'values': value[1]}) for value in data]
        datatypeValues.append({'datatype': datatype, 'datavalues': dataValues})
    keywords.append({'sector': 'Global', 'sectordata': datatypeValues})
    for sector, sectorInfo in hostelryManager.sectorStats.items():
        datatypeValues = list()
        for datatype, data in sectorInfo.items():
            dataValues = list();
            [dataValues.append({'name': value[0], 'values': value[1]}) for value in data]
            datatypeValues.append({'datatype': datatype, 'datavalues': dataValues})
        keywords.append({'sector': sector, 'sectordata': datatypeValues})
    return jsonify(keywords)
