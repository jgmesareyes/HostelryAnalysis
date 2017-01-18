from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms.validators import Required


class DataForm(FlaskForm):
    """Formulario de entrada de datos.
    
    Recoge los valores necesarios para la búsqueda y análisis de hoteles.
    
    """
    islandChoices = [('TF', 'Tenerife'), ('LP', 'La Palma'), ('LG', 'La Gomera'),
                     ('EH', 'El Hierro'), ('GC', 'Gran Canaria'),
                     ('FV', 'Fuerteventura'), ('LZ', 'Lanzarote')]
    islands = SelectField(u'Islands', choices=islandChoices, validators=[Required()])
    languageChoices = [('SP', 'Español'), ('EN', 'Inglés')]
    languages = SelectField(u'Languages', choices=languageChoices, validators=[Required()])
    limit = IntegerField(validators=[Required()])
