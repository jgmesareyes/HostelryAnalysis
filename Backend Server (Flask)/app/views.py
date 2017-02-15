from flask import flash, jsonify, request

from app import app, hostelryManager
import jsonpickle



@app.route('/', methods=['GET', 'POST'])
@app.route('/start', methods=['GET', 'POST'])
def start():
    """Enrutamiento básico de la aplicación.
    
    Recoge los parámetros del formulario y ejecuta el análisis.
    
    """
    data = json.loads(request.get_data(as_text=True))
    limit = int(data['limit'])
    limit = 10000 if limit < 0 else limit
    flash("Limited to: " + str(limit))
    hostelryManager.start(data['island'], data['language'], data['mode'], limit)
    return jsonpickle.encode({'Success': True})
    


# CORS headers
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
    return jsonpickle.encode(hostelryManager.hotelList)


@app.route('/hotels/<string:hotelName>', methods=['GET'])
def getHotel(hotelName):
    selectedHotel = [hotel for hotel in hostelryManager.hotelList if (hotel.name == hotelName)][0]
    return jsonpickle.encode(selectedHotel)


@app.route('/times', methods=['GET'])
def getTimes():
    return jsonpickle.encode(hostelryManager.elapsedTimes)


@app.route('/features', methods=['GET'])  #Percentages
def getFeatures():
    return jsonpickle.encode(hostelryManager.features)


@app.route('/keywords', methods=['GET'])  #Percentages
def getKeywords():
    return jsonpickle.encode(hostelryManager.keywords)
