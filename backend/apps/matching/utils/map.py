from django.conf import settings


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
