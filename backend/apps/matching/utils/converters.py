from django.conf import settings
from django.shortcuts import Http404


class DecimalPointFloatConverter:
    """
    Custom Django converter for URLs.

    Parses floats with a decimal point (not with a comma!)
    Allows for integers too, ciateparses values in this or similar form:
    - 100.0
    - 100

    Will NOT work for these forms:
    - 100.000.000
    - 100,0
    """

    regex = "[0-9]*[.]?[0-9]*"

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)


class ParticipantTypeConverter:
    """
    Custom Django converter for participant types.

    useful for managing pages with the same functionality for different
    participants, e.g "A/profile" and "B/profile" from "<p:p_type>/profile"
    """

    regex = "{A}|{B}".format(
        A=settings.PARTICIPANT_SETTINGS["A"].url_name, B=settings.PARTICIPANT_SETTINGS["B"].url_name
    )

    def to_python(self, value):
        if value == settings.PARTICIPANT_SETTINGS["A"].url_name:
            return "A"
        if value == settings.PARTICIPANT_SETTINGS["B"].url_name:
            return "B"
        raise Http404

    def to_url(self, value):
        if value == "A":
            return settings.PARTICIPANT_SETTINGS["A"].url_name
        if value == "B":
            return settings.PARTICIPANT_SETTINGS["B"].url_name
        raise Http404
