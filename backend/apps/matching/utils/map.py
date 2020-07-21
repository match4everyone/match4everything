from math import asin, cos, radians, sin, sqrt
import time

from django.conf import settings

from apps.matching.data.map_data import zipcodes


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))


def get_plzs_close_to(countrycode, plz, distance_in_km):
    if type(plz) == int:
        plz = str(plz)
    lon1, lat1, _ = zipcodes[countrycode][plz]

    close = []
    for other_plz, (lon2, lat2, ort) in zipcodes[countrycode].items():
        dist = haversine(lon1, lat1, lon2, lat2)
        if dist < distance_in_km * 10:
            close.append(other_plz)

    return close


def get_zipcode_data(countrycode, zipcode):
    lat, lon, ort = zipcodes[countrycode][zipcode]
    return {"latitude": lat, "longitude": lon, "city": ort}


def group_by_zip_code(entities):
    countrycode_zipcode_details = {}

    for entity in entities:
        countrycode = entity.country_code
        zipcode = entity.plz

        if countrycode not in countrycode_zipcode_details:
            countrycode_zipcode_details[countrycode] = {}

        country = countrycode_zipcode_details[countrycode]
        if zipcode not in country:
            country[zipcode] = {
                "countrycode": countrycode,
                "plz": zipcode,
                "count": 0,
                **get_zipcode_data(countrycode, zipcode),
            }

        country[zipcode]["count"] += 1
    return countrycode_zipcode_details


def get_ttl_hash(seconds=300):
    """Return the same value within `seconds` time period."""
    return round(time.time() / seconds)


def get_tile_info():
    """Create a valid tile url from the settings and state the attribution."""
    if settings.LEAFLET_TILESERVER == "mapbox":
        return (
            settings.LEAFLET_TILESERVER,
            "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}@2x?access_token="
            + settings.MAPBOX_TOKEN,
            '<a href="https://www.mapbox.com/about/maps/">© Mapbox</a> | '
            '<a href="http://www.openstreetmap.org/copyright">© OpenStreetMap</a> | '
            '<a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a>',
        )

    elif settings.LEAFLET_TILESERVER == "open_street_map":
        return (
            settings.LEAFLET_TILESERVER,
            "https://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
            '<a href="http://www.openstreetmap.org/copyright">© OpenStreetMap</a> ',
        )

    elif settings.LEAFLET_TILESERVER == "custom_tileserver":
        return (settings.LEAFLET_TILESERVER, settings.TILE_SERVER_URL, settings.TILE_ATTRIBUTION)

    else:
        raise ValueError("Cannot find a tile server url, please check your settings.")
