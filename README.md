HostelryManage
==============


Gestor de análisis sobre características hoteleras en Canarias.
Trabajo de Fin de Grado (TFG) en Universidad de La Laguna.
Desarrollado por José Gregorio Mesa Reyes.



Overview
--------

Aplicación orientada al análisis de las características hoteleras de Tenerife,
tanto generales como por sectores turísticos, a partir de sus respectivas
descripciones en la web de servicios hoteleros establecida.

Se lleva a cabo un Análisis del Lenguaje Natural sobre cada una de las
descripciones a través de la herramienta Freeling, ampliando su funcionalidad a
través de algoritmos de creación propia, y extrayendo de las mismas las
características ofrecidas por cada hotel.

Análisis los comentarios de los clientes determinando aquéllas de las que se
hable de forma positiva y/o de forma negativa.

Desarrollo de características comunes y únicas de forma general en la isla,
así como de cada sector turístico correspondiente a la misma.

Desarrollo de estadísticas de tiempos de ejecución.

Actualmente solo se trabaja sobre los hoteles en la web www://booking.com/


Posteriormente se ha optimizado el programa incluyendo soporte para todas las
islas, así como sus sectores turísticos si los hay.



Requirements
------------

    - Python 3.5
    - PostgreSql 9.5
    - pgAdmin III (if not included with PostgreSQL)
    - PostGis 2.2 for PostgreSQL
    - Freeling 4.0
    - Works on Windows (tested on x86)



Notes
-----

Los modelos, las bases de datos, datos asociadas y scripts de interacción sobre
los mismos no han sido incluidos dado que no está alojado en ningún servidor en
este momento.

Se han trabajado e incorporado herramientas de programación para aumentar el
rendimiento del sistema; utilización del módulo Threading para la distribución
del análisis en hilos de trabajo paralelos.

El proyecto se basa en la investigación sobre el tratamiento del Lenguaje
Natural y las diferentes herramientas disponibles, actuando en la extracción de
los servicios hoteleros a través de sus descripciones.
A pesar de que dicho análisis e investigación conllevó el grueso de este
proyecto, tratando NLTK (Natural Language Toolkit), TreeTagger Wrapper,
Stanford CoreNLP, Ixa Pipes y Freeling, sólo se ha incorporado la funcionalidad
de ésta última, dada la gran funcionalidad, tiempos de respuesta y calidad de
resultados en ambos idiomas Español e Inglés.
