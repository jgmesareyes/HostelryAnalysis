import os
basedir = os.path.abspath(os.path.dirname(__file__))


CSRF_ENABLED = True
SECRET_KEY = 'a-key'



SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/your-db?user=your-user&password=your-password'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Freeling Settings
portSPA = 40005
portENG = 40003
serverPath = "route-to-freeling-4_0-dir/bin/analyzer.bat"
clientPath = "route-to-freeling-4_0-dir/bin/analyzer_client localhost:"
configSetupParsed = " -f route-to-freeling-4_0-dir/data/config/es.cfg --outlv parsed"
corefSetup = " -C route-to-freeling-4_0-dir/data/es/coref/adaboost/coref.dat"

# Booking.com URLS Matchs
BOOKING_URLS = {'CI' : {
                    'EN' : 'http://www.booking.com/searchresults.en-gb.html?label=gen173nr-1FCAEoggJCAlhYSDNiBW5vcmVmaEaIAQGYAQq4AQbIAQzYAQHoAQH4AQuoAgM;sid=406a5980fee604602b58a0a4b115cc4e;class_interval=1&dest_id=730&dest_type=region&dtdisc=0&group_adults=2&group_children=0&hlrd=0&hyb_red=0&inac=0&label_click=undef&nha_red=0&no_rooms=1&offset=0&postcard=0&raw_dest_type=region&redirected_from_city=0&redirected_from_landmark=0&redirected_from_region=0&room1=A%2CA&sb_price_type=total&search_selected=1&src=index&src_elem=sb&ss=Islas%20Canarias%2C%20Espa%C3%B1a&ss_all=0&ss_raw=canarias&ssb=empty&sshis=0&',
                    'SP' : 'http://www.booking.com/searchresults.es.html?label=gen173nr-1FCAEoggJCAlhYSDNiBW5vcmVmaEaIAQGYAQq4AQbIAQzYAQHoAQH4AQuoAgM&sid=406a5980fee604602b58a0a4b115cc4e&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.es.html%3Flabel%3Dgen173nr-1FCAEoggJCAlhYSDNiBW5vcmVmaEaIAQGYAQq4AQbIAQzYAQHoAQH4AQuoAgM%3Bsid%3D406a5980fee604602b58a0a4b115cc4e%3Bsb_price_type%3Dtotal%26%3B&ss=Islas+Canarias%2C+Espa%C3%B1a&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&ss_raw=canarias&ac_position=0&ac_langcode=es&dest_id=730&dest_type=region&search_pageview_id=398a89332dfb02a9&search_selected=true&search_pageview_id=398a89332dfb02a9&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0'},
                'TF' : {
                    'EN' : 'http://www.booking.com/searchresults.en-gb.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&lang=en-gb&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=Tenerife%2C+Spain&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=Tenerife&ac_position=0&ac_langcode=en&dest_id=777&dest_type=region&ac_pageview_id=e5cf009b95f60299&search_selected=true&ac_pageview_id=e5cf009b95f60299&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
                    'SP' : 'http://www.booking.com/searchresults.es.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.es.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=Tenerife%2C+Espa%C3%B1a&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=tenerife&ac_position=0&ac_langcode=es&dest_id=777&dest_type=region&ac_pageview_id=ad370034e689011a&search_selected=true&ac_pageview_id=ad370034e689011a&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0'},
                'LP': {
                    'EN' : 'http://www.booking.com/searchresults.en-gb.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&lang=en-gb&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=La+Palma+Island%2C+Spain&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=La+Palma&ac_position=0&ac_langcode=en&dest_id=1405&dest_type=region&ac_pageview_id=364800a7e9a50194&search_selected=true&ac_pageview_id=364800a7e9a50194&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
                    'SP' : 'http://www.booking.com/searchresults.es.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.es.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=La+Palma+%28isla%29%2C+Espa%C3%B1a&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=La+Palma&ac_position=0&ac_langcode=es&dest_id=1405&dest_type=region&ac_pageview_id=ad370034e689011a&search_selected=true&ac_pageview_id=ad370034e689011a&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0'},
                'LG': {
                    'EN' : 'http://www.booking.com/searchresults.en-gb.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&lang=en-gb&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=La+Gomera%2C+Spain&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=La+Gomera&ac_position=0&ac_langcode=en&dest_id=1775&dest_type=region&ac_pageview_id=b18e00ca0e220115&search_selected=true&ac_pageview_id=b18e00ca0e220115&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
                    'SP' : 'http://www.booking.com/searchresults.es.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.es.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=La+Gomera%2C+Espa%C3%B1a&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=La+Gomera&ac_position=0&ac_langcode=es&dest_id=1775&dest_type=region&ac_pageview_id=1df0005fec660091&search_selected=true&ac_pageview_id=1df0005fec660091&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0'},
                'EH': {
                    'EN' : 'http://www.booking.com/searchresults.en-gb.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&lang=en-gb&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=El+Hierro%2C+Spain&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=El+Hierro&ac_position=0&ac_langcode=en&dest_id=3450&dest_type=region&ac_pageview_id=b18e00d2c542017e&search_selected=true&ac_pageview_id=b18e00d2c542017e&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
                    'SP' : 'http://www.booking.com/searchresults.es.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.es.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=El+Hierro%2C+Espa%C3%B1a&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=El+Hierro&ac_position=0&ac_langcode=es&dest_id=3450&dest_type=region&ac_pageview_id=f4a70070fe9c018c&search_selected=true&ac_pageview_id=f4a70070fe9c018c&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0'},
                'GC': {
                    'EN' : 'http://www.booking.com/searchresults.en-gb.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&lang=en-gb&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=Gran+Canaria%2C+Spain&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=Gran+Canaria&ac_position=0&ac_langcode=en&dest_id=754&dest_type=region&ac_pageview_id=e74900dc3e8800a1&search_selected=true&ac_pageview_id=e74900dc3e8800a1&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
                    'SP' : 'http://www.booking.com/searchresults.es.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.es.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=Gran+Canaria%2C+Espa%C3%B1a&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=Gran+Canaria&ac_position=0&ac_langcode=es&dest_id=754&dest_type=region&ac_pageview_id=f4a7007824e00067&search_selected=true&ac_pageview_id=f4a7007824e00067&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0'},
                'FV': {
                    'EN' : 'http://www.booking.com/searchresults.en-gb.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&lang=en-gb&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=Fuerteventura%2C+Spain&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=Fuerteventura&ac_position=0&ac_langcode=en&dest_id=752&dest_type=region&ac_pageview_id=a71700e6f47e0124&search_selected=true&ac_pageview_id=a71700e6f47e0124&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
                    'SP' : 'http://www.booking.com/searchresults.es.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.es.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=Fuerteventura%2C+Espa%C3%B1a&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=Fuerteventura&ac_position=0&ac_langcode=es&dest_id=752&dest_type=region&ac_pageview_id=f4a70082cc4a02f3&search_selected=true&ac_pageview_id=f4a70082cc4a02f3&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0'},
                'LZ': {
                    'EN' : 'http://www.booking.com/searchresults.en-gb.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&lang=en-gb&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.en-gb.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=Lanzarote%2C+Spain&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=Lanzarote&ac_position=0&ac_langcode=en&dest_id=760&dest_type=region&ac_pageview_id=b18e00ee75a8021b&search_selected=true&ac_pageview_id=b18e00ee75a8021b&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0',
                    'SP' : 'http://www.booking.com/searchresults.es.html?aid=376371&label=es-plivt*et7uZ0t35JwT4XYAS59325969983%3Apl%3Ata%3Ap1%3Ap21.022.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-65526620%3Alp1005465%3Ali%3Adec%3Adm&sid=9bdd1b15b961d46692e466bebf86fec1&sb=1&src=index&src_elem=sb&error_url=http%3A%2F%2Fwww.booking.com%2Findex.es.html%3Faid%3D376371%3Blabel%3Des-plivt%252Aet7uZ0t35JwT4XYAS59325969983%253Apl%253Ata%253Ap1%253Ap21.022.000%253Aac%253Aap1t1%253Aneg%253Afi%253Atikwd-65526620%253Alp1005465%253Ali%253Adec%253Adm%3Bsid%3D9bdd1b15b961d46692e466bebf86fec1%3Bsb_price_type%3Dtotal%26%3B&ss=Lanzarote%2C+Espa%C3%B1a&checkin_monthday=&checkin_month=&checkin_year=&checkout_monthday=&checkout_month=&checkout_year=&sb_acc_types=1&room1=A%2CA&no_rooms=1&group_adults=2&group_children=0&no_pets=0&ss_raw=Lanzarote&ac_position=0&ac_langcode=es&dest_id=760&dest_type=region&ac_pageview_id=f4a7008c39d5000f&search_selected=true&ac_pageview_id=f4a7008c39d5000f&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0'}
                }