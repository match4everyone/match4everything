from itertools import chain
import string

from django.db import models
from django.utils.translation import gettext_lazy as _
import numpy as np

# default/no default logic
# every field is not required unless a default value is specified
# if a default is specified and it is None, blank is allowed.


class Property:

    properties = None

    def __init__(self, label=None, name=None, help_text=None, info_text=None, private=False):
        if label is None:
            raise ValueError("Every property needs to have a label.")
        self.label = _(label)  # the text that should appear when this property is referenced
        self.name = name if name is not None else label.lower().replace(" ", "_")
        self.help_text = help_text
        self.info_text = info_text
        self.private = private

    # we somehow need to define an iterator that can iterate over all properties

    def get_model_field_names(self, prefix=None):
        raise NotImplementedError

    def get_model_fields(self):
        raise NotImplementedError

    def generate_random_assignment(self, rs=None):
        raise NotImplementedError

    def get_private_fields(self):
        # alternative: modify properties in constructor of group
        # private statements propagate to their children regardless of their setting
        if self.private:
            return [True for i in self.get_model_field_names()]
        else:
            if hasattr(self, "properties"):
                return chain(*[p.get_private_fields() for p in self.properties])
            else:
                return [False for i in self.get_model_fields()]

    # def get_filters(self):
    #    raise NotImplementedError


class PropertyGroup(Property):
    property_type = "group"

    def __init__(self, properties, **kwargs):
        super().__init__(**kwargs)
        self.properties = properties

    def get_model_field_names(self, prefix=None):
        model_field_name = self.name if prefix is None else prefix + "--" + self.name
        return list(chain(*[p.get_model_field_names(model_field_name) for p in self.properties]))

    def get_model_fields(self):
        return list(chain(*[p.get_model_fields() for p in self.properties]))

    def generate_random_assignment(self, rs=None):
        return list(chain(*[p.generate_random_assignment(rs) for p in self.properties]))


class ConditionalProperty(Property):
    property_type = "conditional"

    def __init__(self, properties, **kwargs):
        # putting a required in this field is a difficult to define behaviour on a model basis
        super().__init__(**kwargs)
        self.properties = properties

    def get_model_field_names(self, prefix=None):
        model_field_name = self.name if prefix is None else prefix + "--" + self.name
        conditional_fields = list(
            chain(*[p.get_model_field_names(model_field_name) for p in self.properties])
        )
        return [model_field_name + "-condition", *conditional_fields]

    def get_model_fields(self):
        conditional_fields = list(chain(*[p.get_model_fields() for p in self.properties]))
        return [
            models.BooleanField(default=False),  # field for determining the condition
            *conditional_fields,
        ]

    def generate_random_assignment(self, rs=None):
        if rs is None:
            rs = np.random
        return [
            rs.choice([True, False]),
            *chain(*[p.generate_random_assignment(rs) for p in self.properties]),
        ]


class MultipleChoiceProperty(Property):
    property_type = "multiple_choice"

    def __init__(self, choices, **kwargs):
        # putting a required in this field is a difficult to define behaviour
        super().__init__(**kwargs)
        self.choices = choices

    def get_model_field_names(self, prefix=None):
        model_field_name = self.name if prefix is None else prefix + "--" + self.name

        return [model_field_name + "-" + choice for choice, label in self.choices]

    def get_model_fields(self):
        return [models.BooleanField(default=False) for choice, label in self.choices]

    def generate_random_assignment(self, rs=None):
        if rs is None:
            rs = np.random

        return [rs.choice([True, False]) for i in range(len(self.choices))]


class SingleChoiceProperty(Property):
    property_type = "single_choice"

    def __init__(self, choices, is_required=False, max_length=None, default=None, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        self.default = default
        self.is_required = is_required
        self.max_length = max_length if max_length is not None else 3

    def get_model_field_names(self, prefix=None):

        return [self.name if prefix is None else prefix + "--" + self.name]

    def get_model_fields(self):
        if self.is_required:
            return [models.CharField(choices=self.choices, max_length=self.max_length)]
        else:
            return [
                models.CharField(
                    choices=self.choices,
                    default=self.default,
                    blank=True,
                    null=True,
                    max_length=self.max_length,
                )
            ]

    def generate_random_assignment(self, rs=None):
        if rs is None:
            rs = np.random
        return [rs.choice([code for code, label in self.choices])]


class OrderedSingleChoiceProperty(Property):
    property_type = "ordered_single_choice"

    def __init__(self, choices, is_required=False, default=None, **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        self.default = default
        self.is_required = is_required

    def get_model_field_names(self, prefix=None):
        return [self.name if prefix is None else prefix + "--" + self.name]

    def get_model_fields(self):
        if self.is_required:
            return [models.IntegerField(choices=self.choices, null=False)]
        else:
            return [
                models.IntegerField(
                    choices=self.choices, blank=True, null=True, default=self.default
                )
            ]

    def generate_random_assignment(self, rs=None):
        if rs is None:
            rs = np.random
        return [rs.choice([code for code, label in self.choices])]


class TextProperty(Property):
    property_type = "text"

    def __init__(self, is_required=False, max_length=None, default=None, **kwargs):
        super().__init__(**kwargs)
        self.default = (
            "" if default is None else default
        )  # rather have emtpy strings than empty values in text fields
        self.is_required = is_required
        self.max_length = 100 if max_length is None else max_length

    def get_model_field_names(self, prefix=None):
        return [self.name if prefix is None else prefix + "--" + self.name]

    def get_model_fields(self):
        if self.is_required:
            return [models.CharField(max_length=self.max_length)]
        else:
            return [models.CharField(max_length=self.max_length, blank=True, default=self.default)]

    def generate_random_assignment(self, rs=None):
        if rs is None:
            rs = np.random
        code = rs.choice([l for l in string.ascii_uppercase], self.max_length)
        return ["".join(code)]


class BooleanProperty(Property):
    property_name = "boolean"

    def __init__(self, is_required=False, default=False, **kwargs):
        super().__init__(**kwargs)
        self.is_required = is_required
        self.default = default

    def get_model_field_names(self, prefix=None):
        return [self.name if prefix is None else prefix + "--" + self.name]

    def get_model_fields(self, prefix=None):
        if self.is_required:
            return [models.BooleanField()]
        else:
            return [models.BooleanField(blank=True, default=self.default)]

    def generate_random_assignment(self, rs=None):
        if rs is None:
            rs = np.random
        return [rs.choice([True, False])]
