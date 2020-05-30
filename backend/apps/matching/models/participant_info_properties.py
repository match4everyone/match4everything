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
        self.default = config.get('default', None)

    def get_field(self):
        return models.BooleanField(default=self.default)

    def get_random_value(self, rs=None):
        if rs is None:
            rs = np.random
        return bool(rs.rand())


class ChoiceProperty:
    """
    Info-Field that allows to choice.
    (no order is implied in the choices)

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
        self.default = config.get('default', "")
        self.max_length = config.get('max_length', 3)

    def get_field(self):
        return models.CharField(choices=self.choices,
                                default=self.default,
                                max_length=self.max_length)

    def get_random_value(self, rs=None):
        if rs is None:
            rs = np.random
        return rs.choice([code for code, label in self.choices])


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
        self.default = config.get('default', "")

    def get_field(self):
        return models.IntegerField(choices=self.choices,
                                   default=self.default)

    def get_random_value(self, rs=None):
        if rs is None:
            rs = np.random
        return rs.choice([code for code, label in self.choices])


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
        self.max_length = config['max_length']
        self.default = config.get('default', "")

    def get_field(self):
        return models.CharField(max_length=self.max_length, default=self.default)

    def get_random_value(self, rs=None):
        return "This is a very random string."


def create_property(property_config):
    field_name = property_config['field_name']
    col = property_config['property_type']
    if col.get('name') is None:
        raise ValueError("The column does not specify a type.")
    property = PROPERTIES_MAP.get(col['name'], None)
    if property is None:
        raise NotImplementedError("The column type %s is not understood." % col['name'])
    return property(field_name, config=col)


PROPERTIES = [TextProperty, BoolProperty, OrderedChoiceProperty, ChoiceProperty]
PROPERTIES_MAP = {p.name: p for p in PROPERTIES}
