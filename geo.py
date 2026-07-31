import http.server
import json
import socket
import threading
import time
import webbrowser
import requests
import websocket


COUNTRIES = {
    'AF': 'Afganistan', 'AL': 'Albania', 'DZ': 'Algeria', 'AD': 'Andora',
    'AO': 'Angola', 'AR': 'Argentyna', 'AM': 'Armenia', 'AU': 'Australia',
    'AT': 'Austria', 'AZ': 'Azerbejdzan', 'BS': 'Bahamy', 'BH': 'Bahrajn',
    'BD': 'Bangladesz', 'BB': 'Barbados', 'BY': 'Bialorus', 'BE': 'Belgia',
    'BZ': 'Belize', 'BJ': 'Benin', 'BT': 'Bhutan', 'BO': 'Boliwia',
    'BA': 'Bosnia i Hercegowina', 'BW': 'Botswana', 'BR': 'Brazylia',
    'BN': 'Brunei', 'BG': 'Bulgaria', 'BF': 'Burkina Faso', 'BI': 'Burundi',
    'CV': 'Republika Zielonego Przyladka', 'KH': 'Kambodza',
    'CM': 'Kamerun', 'CA': 'Kanada', 'CF': 'Republika Srodkowoafrykanska',
    'TD': 'Czad', 'CL': 'Chile', 'CN': 'Chiny', 'CO': 'Kolumbia',
    'CG': 'Kongo', 'CD': 'Demokratyczna Republika Konga', 'CR': 'Kostaryka',
    'CI': 'Wybrzeze Kosci Sloniowej', 'HR': 'Chorwacja', 'CU': 'Kuba',
    'CY': 'Cypr', 'CZ': 'Czechy', 'DK': 'Dania', 'DJ': 'Dzibuti',
    'DO': 'Dominikana', 'EC': 'Ekwador', 'EG': 'Egipt', 'SV': 'Salwador',
    'GQ': 'Gwinea Rownikowa', 'ER': 'Erytrea', 'EE': 'Estonia',
    'SZ': 'Eswatini', 'ET': 'Etiopia', 'FJ': 'Fidzi', 'FI': 'Finlandia',
    'FR': 'Francja', 'GA': 'Gabon', 'GM': 'Gambia', 'GE': 'Gruzja',
    'DE': 'Niemcy', 'GH': 'Ghana', 'GR': 'Grecja', 'GT': 'Gwatemala',
    'GN': 'Gwinea', 'GW': 'Gwinea Bissau', 'GY': 'Gujana', 'HT': 'Haiti',
    'HN': 'Honduras', 'HU': 'Wegry', 'IS': 'Islandia', 'IN': 'Indie',
    'ID': 'Indonezja', 'IR': 'Iran', 'IQ': 'Irak', 'IE': 'Irlandia',
    'IL': 'Izrael', 'IT': 'Wlochy', 'JM': 'Jamajka', 'JP': 'Japonia',
    'JO': 'Jordania', 'KZ': 'Kazachstan', 'KE': 'Kenia', 'KI': 'Kiribati',
    'KR': 'Korea Poludniowa', 'KP': 'Korea Pn', 'KW': 'Kuwejt',
    'KG': 'Kirgistan', 'LA': 'Laos', 'LV': 'Lotwa', 'LB': 'Liban',
    'LS': 'Lesoto', 'LR': 'Liberia', 'LY': 'Libia', 'LI': 'Liechtenstein',
    'LT': 'Litwa', 'LU': 'Luksemburg', 'MG': 'Madagaskar', 'MW': 'Malawi',
    'MY': 'Malezja', 'MV': 'Malediwy', 'ML': 'Mali', 'MT': 'Malta',
    'MH': 'Wyspy Marshalla', 'MR': 'Mauritania', 'MU': 'Mauritius',
    'MX': 'Meksyk', 'FM': 'Mikronezja', 'MD': 'Moldawia', 'MC': 'Monako',
    'MN': 'Mongolia', 'ME': 'Czarnogora', 'MA': 'Maroko', 'MZ': 'Mozambik',
    'MM': 'Mjanma', 'NA': 'Namibia', 'NR': 'Nauru', 'NP': 'Nepal',
    'NL': 'Holandia', 'NZ': 'Nowa Zelandia', 'NI': 'Nikaragua',
    'NE': 'Niger', 'NG': 'Nigeria', 'MK': 'Macedonia Pn', 'NO': 'Norwegia',
    'OM': 'Oman', 'PK': 'Pakistan', 'PW': 'Palau', 'PA': 'Panama',
    'PG': 'Papua-Nowa Gwinea', 'PY': 'Paragwaj', 'PE': 'Peru',
    'PH': 'Filipiny', 'PL': 'Polska', 'PT': 'Portugalia', 'QA': 'Katar',
    'RO': 'Rumunia', 'RU': 'Rosja', 'RW': 'Rwanda', 'KN': 'Saint Kitts i Nevis',
    'LC': 'Saint Lucia', 'VC': 'Saint Vincent i Grenadyny', 'WS': 'Samoa',
    'SM': 'San Marino', 'ST': 'Wyspy Swietego Tomasza i Ksiazeca',
    'SA': 'Arabia Saudyjska', 'SN': 'Senegal', 'RS': 'Serbia',
    'SC': 'Seszele', 'SL': 'Sierra Leone', 'SG': 'Singapur',
    'SK': 'Slowacja', 'SI': 'Slowenia', 'SB': 'Wyspy Salomona',
    'SO': 'Somalia', 'ZA': 'Republika Poludniowej Afryki', 'SS': 'Sudan Poludniowy',
    'ES': 'Hiszpania', 'LK': 'Sri Lanka', 'SD': 'Sudan', 'SR': 'Surinam',
    'SE': 'Szwecja', 'CH': 'Szwajcaria', 'SY': 'Syria', 'TW': 'Tajwan',
    'TJ': 'Tadzykistan', 'TZ': 'Tanzania', 'TH': 'Tajlandia', 'TL': 'Timor Wschodni',
    'TG': 'Togo', 'TO': 'Tonga', 'TT': 'Trynidad i Tobago', 'TN': 'Tunezja',
    'TR': 'Turcja', 'TM': 'Turkmenistan', 'TV': 'Tuvalu', 'UG': 'Uganda',
    'UA': 'Ukraina', 'AE': 'Zjednoczone Emiraty Arabskie', 'GB': 'Wielka Brytania',
    'US': 'Stany Zjednoczone', 'UY': 'Urugwaj', 'UZ': 'Uzbekistan',
    'VU': 'Vanuatu', 'VA': 'Watykan', 'VE': 'Wenezuela', 'VN': 'Wietnam',
    'YE': 'Jemen', 'ZM': 'Zambia', 'ZW': 'Zimbabwe', 'AX': 'Wyspy Alandzkie',
    'FO': 'Wyspy Owcze', 'GI': 'Gibraltar', 'GL': 'Grenlandia',
    'GP': 'Gwadelupa', 'MQ': 'Martynika', 'PR': 'Portoryko', 'RE': 'Reunion',
    'YT': 'Majotta', 'GF': 'Gujana Francuska', 'HK': 'Hongkong',
    'MO': 'Makau', 'PS': 'Palestyna', 'XK': 'Kosowo', 'NC': 'Nowa Kaledonia',
    'PF': 'Polinezja Francuska', 'BQ': 'Bonaire', 'CW': 'Curacao',
    'SX': 'Sint Maarten', 'JE': 'Jersey', 'GG': 'Guernsey',
    'IM': 'Wyspa Man', 'FK': 'Falklandy', 'SH': 'Wyspa Swietej Heleny',
    'PN': 'Pitcairn', 'AQ': 'Antarktyda', 'AC': 'Wyspa Wniebowstapienia',
    'TA': 'Tristan da Cunha', 'BV': 'Wyspa Bouveta',
    'TF': 'Francuskie Tereny Poludniowe',
    'GS': 'Georgia Poludniowa i Sandwich Poludniowy', 'EH': 'Sahara Zachodnia',
    'IO': 'Brytyjskie Terytorium Oceanu Indyjskiego', 'CX': 'Wyspa Bozego Narodzenia',
    'CC': 'Wyspy Kokosowe', 'NF': 'Norfolk', 'AS': 'Samoa Amerykanskie',
    'GU': 'Guam', 'MP': 'Mariany Pn', 'VI': 'Wyspy Dziewicze',
    'VG': 'Brytyjskie Wyspy Dziewicze', 'KY': 'Kajmany', 'TC': 'Turks i Caicos',
    'AI': 'Anguilla', 'MS': 'Montserrat', 'BM': 'Bermudy',
    'PM': 'Saint Pierre i Miquelon', 'BL': 'Saint Barthelemy',
    'MF': 'Saint Martin', 'SJ': 'Svalbard i Jan Mayen',
}

BBOXES = {
    'PL': (49.0, 14.1, 54.9, 24.2), 'DE': (47.3, 5.9, 55.1, 15.0),
    'FR': (41.3, -5.1, 51.1, 9.6), 'ES': (36.0, -9.3, 43.8, 4.3),
    'PT': (36.9, -9.5, 42.2, -6.2), 'IT': (35.5, 6.6, 47.1, 18.5),
    'GB': (49.9, -8.7, 60.9, 1.8), 'IE': (51.4, -10.5, 55.4, -6.0),
    'NL': (50.7, 3.4, 53.5, 7.2), 'BE': (49.5, 2.5, 51.5, 6.4),
    'CH': (45.8, 5.9, 47.8, 10.5), 'AT': (46.4, 9.5, 49.0, 17.2),
    'CZ': (48.5, 12.1, 51.1, 18.9), 'SK': (47.7, 16.8, 49.6, 22.6),
    'HU': (45.7, 16.1, 48.6, 22.9), 'UA': (44.4, 22.1, 52.4, 40.2),
    'RO': (43.6, 20.3, 48.3, 29.7), 'BG': (41.2, 22.4, 44.2, 28.6),
    'GR': (34.8, 19.6, 41.7, 28.2), 'SE': (55.3, 11.1, 69.1, 24.2),
    'NO': (57.9, 4.6, 71.2, 31.1), 'FI': (59.8, 20.6, 70.1, 31.6),
    'DK': (54.5, 8.1, 57.7, 15.2), 'IS': (63.4, -24.5, 66.6, -13.5),
    'EE': (57.5, 21.8, 59.7, 28.2), 'LV': (55.7, 20.9, 58.1, 28.2),
    'LT': (53.9, 20.9, 56.5, 26.9), 'RU': (41.2, 19.6, 81.9, -169.1),
    'BY': (51.3, 23.2, 56.2, 32.8), 'MD': (45.5, 26.6, 48.5, 30.2),
    'RS': (42.2, 18.8, 46.2, 23.0), 'HR': (42.4, 13.5, 46.5, 19.4),
    'SI': (45.4, 13.4, 46.9, 16.6), 'BA': (42.6, 15.7, 45.3, 19.6),
    'ME': (41.9, 18.4, 43.6, 20.4), 'MK': (40.8, 20.4, 42.4, 23.0),
    'AL': (39.6, 19.3, 42.7, 21.1), 'XK': (41.9, 20.0, 43.3, 21.8),
    'US': (24.5, -125.0, 49.4, -66.9), 'CA': (41.7, -141.0, 83.1, -52.6),
    'MX': (14.5, -117.1, 32.7, -86.7), 'BR': (-33.8, -73.9, 5.3, -34.8),
    'AR': (-55.1, -73.6, -21.8, -53.6), 'CL': (-56.0, -75.6, -17.5, -66.9),
    'PE': (-18.4, -81.4, -0.0, -68.7), 'CO': (-4.2, -79.1, 12.5, -66.9),
    'VE': (0.6, -73.4, 12.2, -59.8), 'BO': (-22.9, -69.6, -9.7, -57.5),
    'UY': (-35.0, -58.4, -30.1, -53.1), 'PY': (-27.6, -62.6, -19.3, -54.3),
    'EC': (-5.0, -81.0, 1.4, -75.2), 'GY': (1.2, -61.4, 8.6, -56.5),
    'SR': (1.8, -58.1, 6.0, -54.0), 'AU': (-43.6, 112.9, -10.7, 153.6),
    'NZ': (-47.3, 166.4, -34.4, 178.6), 'JP': (24.0, 122.9, 45.5, 145.8),
    'KR': (33.1, 125.1, 38.6, 129.6), 'IN': (6.7, 68.1, 35.5, 97.4),
    'TH': (5.6, 97.3, 20.5, 105.6), 'VN': (8.4, 102.1, 23.4, 109.5),
    'ID': (-11.0, 95.0, 6.1, 141.0), 'MY': (0.9, 99.6, 7.4, 119.3),
    'PH': (4.6, 116.9, 21.1, 126.6), 'CN': (18.0, 73.5, 53.6, 134.8),
    'ZA': (-34.8, 16.5, -22.1, 32.9), 'EG': (22.0, 24.7, 31.7, 37.0),
    'MA': (27.7, -13.2, 35.9, -1.0), 'TN': (30.2, 7.5, 37.5, 11.6),
    'NG': (4.3, 2.7, 13.9, 14.7), 'KE': (-4.7, 33.9, 5.5, 41.9),
    'TZ': (-11.7, 29.3, -1.0, 40.4), 'ET': (3.4, 33.0, 14.8, 48.0),
    'GH': (4.7, -3.3, 11.2, 1.2), 'SN': (12.3, -17.5, 16.7, -11.3),
    'CI': (4.4, -8.6, 10.7, -2.5), 'UG': (-1.5, 29.6, 4.2, 35.0),
    'ZM': (-18.1, 22.0, -8.2, 33.7), 'ZW': (-22.4, 25.2, -15.6, 33.1),
    'NA': (-29.0, 11.7, -16.9, 25.3), 'BW': (-26.9, 20.0, -17.8, 29.4),
    'MG': (-25.6, 43.2, -11.9, 50.5), 'IL': (29.5, 34.3, 33.3, 35.9),
    'JO': (29.2, 34.9, 32.4, 39.3), 'SA': (16.3, 34.6, 32.2, 55.7),
    'AE': (22.6, 51.6, 26.1, 56.4), 'QA': (24.5, 50.7, 26.2, 51.7),
    'KW': (28.5, 46.6, 30.1, 48.4), 'TR': (35.8, 26.0, 42.1, 44.8),
    'GE': (41.1, 40.0, 43.6, 46.7), 'AM': (38.8, 43.4, 41.3, 46.6),
    'AZ': (38.4, 44.8, 41.9, 50.4), 'KZ': (40.6, 46.5, 55.4, 87.3),
    'MN': (41.6, 87.7, 52.1, 119.9), 'NP': (26.3, 80.1, 30.4, 88.2),
    'BD': (20.6, 88.0, 26.6, 92.7), 'LK': (5.9, 79.7, 9.8, 81.9),
    'TW': (21.9, 119.9, 25.3, 122.0), 'KH': (10.4, 102.3, 14.7, 107.6),
    'LA': (13.9, 100.1, 22.5, 107.7), 'MM': (9.8, 92.2, 28.5, 101.2),
    'PK': (23.7, 60.9, 37.1, 77.8), 'AF': (29.4, 60.5, 38.5, 74.9),
    'IR': (25.1, 44.0, 39.8, 63.3), 'IQ': (29.1, 38.8, 37.4, 48.6),
    'SY': (32.3, 35.7, 37.3, 42.4), 'LB': (33.0, 35.1, 34.7, 36.6),
    'CY': (34.6, 32.3, 35.7, 34.6), 'CU': (19.8, -84.9, 23.2, -74.1),
    'HT': (18.0, -74.5, 20.1, -71.6), 'DO': (17.5, -72.0, 19.9, -68.3),
    'JM': (17.7, -78.4, 18.5, -76.2), 'PA': (7.2, -83.1, 9.7, -77.2),
    'CR': (8.0, -85.9, 11.2, -82.5), 'NI': (10.7, -87.7, 15.0, -83.1),
    'HN': (12.9, -89.4, 16.5, -83.1), 'GT': (13.7, -92.2, 17.8, -88.2),
    'BZ': (15.9, -89.2, 18.5, -87.8), 'SV': (13.1, -90.1, 14.4, -87.7),
    'FJ': (-19.2, 177.1, -16.0, -178.4), 'PG': (-11.7, 140.8, -1.3, 155.9),
}


def strip_jsonp(body):
    body = body.strip()
    if body.startswith('/**/'):
        s = body.find('(')
        e = body.rfind(')')
        if s != -1 and e != -1:
            return body[s + 1:e]
    return body


def deep_coords(node, depth=0):
    if not isinstance(node, list) or depth > 12:
        return None
    if len(node) >= 4 and node[0] is None and node[1] is None:
        lat, lng = node[2], node[3]
        if isinstance(lat, (int, float)) and isinstance(lng, (int, float)):
            if abs(lat) <= 90 and abs(lng) <= 180:
                return lat, lng
    for item in node:
        r = deep_coords(item, depth + 1)
        if r:
            return r
    return None


def deep_country(node, depth=0):
    if not isinstance(node, list) or depth > 12:
        return None
    for item in node:
        if isinstance(item, str) and len(item) == 2 and item.isupper() \
                and item.isalpha() and item in COUNTRIES:
            return item
    for item in node:
        if isinstance(item, list):
            r = deep_country(item, depth + 1)
            if r:
                return r
    return None


def deep_desc(node, depth=0):
    if not isinstance(node, list) or depth > 12:
        return None
    for item in node:
        if isinstance(item, str) and 3 <= len(item) <= 80 and ',' in item \
                and not item.startswith('http') and not item.startswith('/'):
            return item
    for item in node:
        if isinstance(item, list):
            r = deep_desc(item, depth + 1)
            if r:
                return r
    return None


def parse_gm_response(body):
    try:
        data = json.loads(strip_jsonp(body))
    except Exception:
        return None
    if not isinstance(data, list):
        return None

    try:
        pano = data[1][0]
        desc = pano[3][2][1][0]
        loc = pano[5][0][1]
        lat = loc[0][2]
        lng = loc[0][3]
        cc = loc[4]
        if isinstance(lat, (int, float)) and isinstance(lng, (int, float)) \
                and abs(lat) <= 90 and abs(lng) <= 180:
            return lat, lng, cc, desc
    except (IndexError, TypeError, KeyError):
        pass

    coords = deep_coords(data)
    if not coords:
        return None
    lat, lng = coords
    cc = deep_country(data) or ''
    desc = deep_desc(data) or ''
    return lat, lng, cc, desc


reverse_cache = {}


def reverse_geocode(lat, lng):
    key = (round(lat, 4), round(lng, 4))
    if key in reverse_cache:
        return reverse_cache[key]
    try:
        r = requests.get(
            'https://nominatim.openstreetmap.org/reverse',
            params={'lat': lat, 'lon': lng, 'format': 'json', 'zoom': 18,
                    'accept-language': 'pl'},
            headers={'User-Agent': 'geoguessr-map/1.0'},
            timeout=6
        )
        d = r.json()
        a = d.get('address', {})
        parts = {}
        road = a.get('road') or a.get('pedestrian') or a.get('footway')
        if road:
            parts['Ulica'] = road
        sub = (a.get('suburb') or a.get('neighbourhood') or a.get('quarter')
               or a.get('city_district') or a.get('hamlet'))
        if sub:
            parts['Dzielnica'] = sub
        city = (a.get('city') or a.get('town') or a.get('village')
                or a.get('municipality'))
        if city:
            parts['Miasto'] = city
        region = a.get('state') or a.get('county') or a.get('region')
        if region and region != city:
            parts['Region'] = region
        cc = (a.get('country_code') or '').upper()
        country = a.get('country') or ''
        result = (parts, cc, country)
        reverse_cache[key] = result
        return result
    except (requests.RequestException, KeyError, ValueError):
        result = ({}, '', '')
        reverse_cache[key] = result
        return result


def country_geocode(lat, lng):
    key = ('bdc', round(lat, 4), round(lng, 4))
    if key in reverse_cache:
        return reverse_cache[key]
    try:
        r = requests.get(
            'https://api.bigdatacloud.net/data/reverse-geocode-client',
            params={'latitude': lat, 'longitude': lng,
                    'localityLanguage': 'pl'},
            timeout=6
        )
        d = r.json()
        cc = (d.get('countryCode') or '').upper()
        name = d.get('countryName') or ''
        result = (cc, name)
        reverse_cache[key] = result
        return result
    except (requests.RequestException, KeyError, ValueError):
        result = ('', '')
        reverse_cache[key] = result
        return result


seen = set()
state = {'lat': None, 'lng': None, 'text': '', 'country': ''}

PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Geoguessr Map</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
html,body{margin:0;height:100%;background:#111}
#map{height:100vh;width:100vw}
</style>
</head>
<body>
<div id="map"></div>
<script>
var map = L.map('map', { zoomControl: true }).setView([20, 0], 3);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);
var marker = null;
var lastLat = null, lastLng = null;
function load() {
  fetch('/data').then(function (r) { return r.json(); }).then(function (d) {
    document.title = 'Geoguessr Map' + (d.country ? ' - ' + d.country : '');
    if (!d.lat) return;
    if (!marker) {
      marker = L.marker([d.lat, d.lng]).addTo(map);
    } else {
      marker.setLatLng([d.lat, d.lng]);
    }
    var country = d.country || '';
    marker.bindTooltip(country, {
      permanent: true,
      direction: 'top',
      offset: [0, -12],
      opacity: 0.95
    });
    if (d.lat !== lastLat || d.lng !== lastLng) {
      marker.openTooltip();
      map.panTo([d.lat, d.lng]);
      lastLat = d.lat;
      lastLng = d.lng;
    }
  });
}
load();
setInterval(load, 1500);
</script>
</body>
</html>
"""


def extract_from_body(body):
    global seen
    res = parse_gm_response(body)
    if not res:
        return
    lat, lng, cc, desc = res
    rid = f'{lat:.4f}_{lng:.4f}'
    if rid in seen:
        return
    seen.add(rid)

    precise, rcc, rcountry = reverse_geocode(lat, lng)
    if cc not in COUNTRIES:
        cc = rcc if rcc in COUNTRIES else ''
    if cc not in COUNTRIES or not rcountry:
        bcc, bname = country_geocode(lat, lng)
        if cc not in COUNTRIES:
            cc = bcc if bcc in COUNTRIES else ''
        if not rcountry:
            rcountry = bname
    country = COUNTRIES.get(cc)
    if not country:
        country = rcountry or 'Nieznany'

    lines = []
    if precise:
        for k, v in precise.items():
            lines.append(f'{k}: {v}')
    elif desc:
        lines.append(desc)
    text = '\n'.join(lines)
    print(f'[geoguessr map] {lat}, {lng} | {country}')
    state['lat'] = lat
    state['lng'] = lng
    state['text'] = text
    state['country'] = country


class Sniffer:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.pending = {}
        self.msg_id = 100

    def run(self):
        try:
            ws = websocket.create_connection(
                self.ws_url, timeout=30,
                header=['Origin: http://127.0.0.1:9222',
                        'User-Agent: Mozilla/5.0']
            )
            ws.send(json.dumps({'id': 1, 'method': 'Network.enable'}))
            ws.send(json.dumps({'id': 2, 'method': 'Page.enable'}))
            while True:
                msg = ws.recv()
                data = json.loads(msg)

                if data.get('id') and data['id'] in self.pending:
                    self.pending.pop(data['id'])
                    body = (data.get('result') or {}).get('body')
                    if body:
                        extract_from_body(body)
                    continue

                method = data.get('method', '')
                if method == 'Network.responseReceived':
                    url = data['params']['response'].get('url', '')
                    req_id = data['params'].get('requestId', '')
                    if 'GetMetadata' in url:
                        self.msg_id += 1
                        self.pending[self.msg_id] = url
                        ws.send(json.dumps({
                            'id': self.msg_id,
                            'method': 'Network.getResponseBody',
                            'params': {'requestId': req_id}
                        }))
        except Exception as e:
            print(f'[target closed: {str(e)[:60]}]')


def sniffer_main():
    print('[geoguessr map] waiting for port 9222...')
    while True:
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect(('127.0.0.1', 9222))
            s.close()
            break
        except (socket.timeout, ConnectionRefusedError, OSError):
            time.sleep(3)

    attached = set()
    while True:
        try:
            targets = requests.get('http://127.0.0.1:9222/json', timeout=5).json()
        except Exception:
            time.sleep(3)
            continue

        for t in targets:
            ws_url = t.get('webSocketDebuggerUrl')
            if ws_url and ws_url not in attached:
                attached.add(ws_url)
                print(f'[{t.get("type", "?")}] {t.get("url", "?")[:100]}')
                threading.Thread(target=Sniffer(ws_url).run,
                                 daemon=True).start()

        time.sleep(3)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            body = json.dumps(state).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            body = PAGE.encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, *args):
        pass


def main():
    threading.Thread(target=sniffer_main, daemon=True).start()
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 8123), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = 'http://127.0.0.1:8123'
    print(f'[geoguessr map] mapa: {url}')
    webbrowser.open(url)
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
