import time

from django.conf import settings

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
