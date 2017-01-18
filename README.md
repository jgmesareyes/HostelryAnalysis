HostelryManage
==============


Analysis management about hotel services in Tenerife.
Final Grade Dissertation at University of La Laguna.
Developed by José G. Mesa Reyes.



Overview
--------

Application oriented on the analysis of hotel characteristics and services in
Tenerife, both general and by tourist sectors, from their respective
descriptions on the selected hotel booking website.

A Natural Language Analysis is carried out on each description using the
Freeling tool, extending its functionality through own algorithms extracting
the features offered by each hotel.

Analyze customer comments by determining which customers are leaving positive
and / or negative reviews.

Development of common and unique characteristics at global in the island, as
well as for each tourist sector respectively.

Development of execution time statistics.

Bilingual development, carrying out the analysis in both English and Spanish.

Currently only working on hotels at website www://booking.com/


Subsequently, the program has been optimized including support for all the
Canary Islands, as well as their tourist sectors.



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

Models, databases, associated data, and interaction scripts have not been
included due since it is not hosted at the moment.

Programming tools have been worked on and incorporated to increase the system
performance; use of the Threading module for distributing the analysis in
parallel threads.

This project is strongly based on research of Natural Language treatment and
the different tools available, which are the point in the extraction of the
hotel services through their descriptions.
Despite the fact that this analysis and research carried the bulk of this
project, dealing with several tools such as NLTK (Natural Language Toolkit),
TreeTagger Wrapper, Stanford CoreNLP, Ixa Pipes and Freeling, only Freeling
functionality has been incorporated to this final project, due to its best
balance in functionality, response times and quality of results in both
languages English and Spanish.
