from flask import render_template, flash
from app import app, hostelryManage
from .forms import DataForm
from config import BOOKING_URLS
from .HostelryManage import HostelryManage



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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Enrutamiento básico de la aplicación.
    
    Recoge los parámetros del formulario y ejecuta el análisis.
    
    """
    form = DataForm()
    if form.validate_on_submit():
        searchUrl = BOOKING_URLS[form.islands.data][form.languages.data]
        limit = form.limit.data
        limit = 10000 if limit < 0 else limit
        flash("Limited to: " + str(limit))
        hostelryManage = HostelryManage(searchUrl, limit)
        return render_template('results.html',
                               title='Hostelry Analysis Results')
    return render_template('index.html',
                           title='Hostelry Analysis',
                           form=form)


@app.route('/results', methods=['GET'])
@app.route('/results/<int:result>', methods=['GET'])
def results(result=0):
    """Enrutamiento de los resultados.
    
    Muestra los resultados elegidos en cada caso (9 opciones).
    
    Parámetros:
    result -- resultado o tarea a mostrar
    
    """
    try:
        hotel = hostelryManage.hotelList[0]
    except:
        hotel = None
    if hotel is None:
        return not_acceptable(406)
    #hotelList = json.loads(session['hotelList'])[0]
    """
    if result in range(1,7):
        hotelList = hostelryManage.hotelList
        return render_template('results.html',
                           title='Hostelry Analysis Results',
                           hotelList=hotelList,
                           result=result)
    if result == 7:
        globalStats = hostelryManage.globalStats
        return render_template('results.html',
                           title='Hostelry Analysis Results',
                           globalStats=globalStats,
                           result=result)
    if result == 8:
        sectorStats = hostelryManage.sectorStats
        return render_template('results.html',
                           title='Hostelry Analysis Results',
                           sectorStats=sectorStats,
                           result=result)
    if result == 9:
        elapsedTimes = hostelryManage.elapsedTimes
        return render_template('results.html',
                           title='Hostelry Analysis Results',
                           elapsedTimes=elapsedTimes,
                           result=result)
    """
    return render_template('results.html',
                           title='Hostelry Analysis Results',
                           hotelList=hostelryManage.hotelList,
                           globalStats=hostelryManage.globalStats,
                           sectorStats=hostelryManage.sectorStats,
                           elapsedTimes=hostelryManage.elapsedTimes,
                           result=result)
    return render_template('results.html',
                           title='Hostelry Analysis Results')
