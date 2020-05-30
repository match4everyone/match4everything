from math import asin, cos, radians, sin, sqrt
import time

from apps.matching.files.map_data import plzs


def get_plz_data(countrycode, plz):
    lat, lon, ort = plzs[countrycode][plz]
    return {"latitude": lat, "longitude": lon, "city": ort}


def group_by_zip_code(entities):
    countrycode_plz_details = {}

    for entity in entities:
        countrycode = entity.country_code
        plz = entity.plz

        if countrycode not in countrycode_plz_details:
            countrycode_plz_details[countrycode] = {}

        country = countrycode_plz_details[countrycode]
        if plz not in country:
            country[plz] = {
                "countrycode": countrycode,
                "plz": plz,
                "count": 0,
                **get_plz_data(countrycode, plz),
            }

        country[plz]["count"] += 1
    return countrycode_plz_details


def get_ttl_hash(seconds=300):
    """Return the same value withing `seconds` time period."""
    return round(time.time() / seconds)
