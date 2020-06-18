from django.db import models
from django.utils.translation import gettext_lazy as _
import numpy as np


class BoolProperty:
    """
    Info-Field that has a boolean value.

    Example:
        {
          "name": "bool",
          "default": "False"
        }
    """

    name = "bool"

    def __init__(self, field_name, config):
        self.field_name = field_name
        self.default = config.get("default", None)

    def get_field(self):
        return models.BooleanField(default=self.default)

    def get_random_value(self, rs=None):
        if rs is None:
            rs = np.random
        return bool(rs.rand())

    def get_filters(self):
        return [("exact", models.NullBooleanField(default=None))]


class ChoiceProperty:
    """
    Info-Field that allows to choice.

    No order is implied by the in the choices.
    Example:
        {
          "name": "choice",
          "choices": {
            "CH": "Only lovely chocolate",
            "VA": "My dearest Vanilla",
            "ST": "Red is the only true color"},
          "default": "chocolate"
        }
    """

    name = "choice"

    def __init__(self, field_name, config):
        self.field_name = field_name
        self.choices = [(c, _(l)) for c, l in config["choices"].items()]
        self.default = config.get("default", "")
        self.max_length = config.get("max_length", 3)

    def get_field(self):
        return models.CharField(
            choices=self.choices, default=self.default, max_length=self.max_length
        )

    def get_random_value(self, rs=None):
        if rs is None:
            rs = np.random
        return rs.choice([code for code, label in self.choices])

    def get_filters(self):
        # an 'in' Multiple Choice field would be nice as well, but we need to think a little more about how to do this
        # todo # noqa
        return [
            (
                "exact",
                models.CharField(
                    default=None, choices=[(None, "--")] + self.choices, max_length=self.max_length
                ),
            )
        ]


class OrderedChoiceProperty:
    """
    Info-Field that allows to specify an ordered choice.

    Order is implied by giving a choice list as integer values.
    Ascending order is assumed starting from 0.

    Example:
        {
          "name": "ordered_choice",
          "choices": {
            "0": "kindergarden",
            "1": "high school",
            "2": "wrote last exam years ago"
          },
          "default": 0
        }
    """

    name = "ordered_choice"

    def __init__(self, field_name, config):
        self.field_name = field_name
        self.choices = [(int(c), _(l)) for c, l in config["choices"].items()]
        self.min = min([a for a, b in self.choices])
        self.max = max([a for a, b in self.choices])
        self.default = config.get("default", "")

    def get_field(self):
        return models.IntegerField(choices=self.choices, default=self.default)

    def get_random_value(self, rs=None):
        if rs is None:
            rs = np.random
        return rs.choice([code for code, label in self.choices])

    def get_filters(self):
        # an 'in' Multiple Choice field would be nice as well, but we need to think a little more about how to do this
        # todo # noqa
        return [
            (
                "gte",
                models.IntegerField(
                    choices=[(self.min - 1, "No choice")] + self.choices, default=self.min - 1
                ),
            ),
            (
                "lte",
                models.IntegerField(
                    choices=[(self.max + 1, "No choice")] + self.choices, default=self.min - 1
                ),
            ),
        ]


class TextProperty:
    """
    Info-Field that allows to specify fee test.

    Example:
        {
          "name": "text",
          "max_length": 100,
          "default": ""
        }
    """

    name = "text"

    def __init__(self, field_name, config):
        self.field_name = field_name
        self.max_length = config["max_length"]
        self.default = config.get("default", "")

    def get_field(self):
        return models.CharField(max_length=self.max_length, default=self.default)

    def get_random_value(self, rs=None):
        return "This is a very random string."

    def get_filters(self):
        # icontains is case insensitive
        return [("icontains", models.CharField(max_length=self.max_length, default=""))]


def create_property(property_config):
    field_name = property_config["field_name"]
    col = property_config["property_type"]
    if col.get("name") is None:
        raise ValueError("The column does not specify a p_type.")
    property_field = PROPERTIES_MAP.get(col["name"], None)
    if property_field is None:
        raise NotImplementedError("The column p_type %s is not understood." % col["name"])
    return property_field(field_name, config=col)


PROPERTIES = [TextProperty, BoolProperty, OrderedChoiceProperty, ChoiceProperty]
PROPERTIES_MAP = {p.name: p for p in PROPERTIES}
