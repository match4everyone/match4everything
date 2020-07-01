from itertools import chain
import string
from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _
import numpy as np


class Property:

    properties = None

    def __init__(self, label=None, name=None, help_text=None, info_text=None, private=False):
        """
        Create a new property of a participant.

        label: Label of the property that is shown in the UI
        help_text: Help text that should be displayed on hover in the UI
        info_text: Information that is visible next to the property in the UI
        private: Is true if only site administrators should be able to view this property
        """
        if label is None:
            raise ValueError("You need to set the value for label.")
        self.label = _(label)  # the text that should appear when this property is referenced
        self.name = name if name is not None else label.lower().replace(" ", "_")
        if "--" in self.name:
            raise ValueError(
                f"The field name {self.name} is not allowed, since it contains '--'."
                " You can explicitly chose a suitable column name by setting the 'name' kwarg."
            )
        if len(self.name) > 12:
            raise ValueError(
                f"The field name {self.name} is too long. You can use 12 characters at max."
                f" If you did not set the 'name' before, please set in in the constructor. "
            )
        self.help_text = help_text
        self.info_text = info_text
        self.private = private

        # Since properties should be able to generate a hierarchical structure,
        # they can have their own properties (children) that they act on (e.g. to group them).
        self.properties = None

    def get_model_field_names(self, prefix=None) -> List[str]:
        """
        Return a list of column names that should be used for instantiating a model.

        The prefix should be attached to the front of a name in order to mark the hierarchical structure
        in a model (i.e. database table) that cannot represent this.
        """
        raise NotImplementedError

    def get_model_fields(self) -> List[models.Field]:
        """
        Return a list of model fields (from django.models).

        These are used to
        """
        raise NotImplementedError

    def generate_random_assignment(self, rs=None) -> List:
        """
        Return a list of values that are valid entries for each model field.

        They are chosen at random.
        rs: a numpy random seed in case the behaviour should be reproducible. Love science.
        """
        raise NotImplementedError

    def get_private_fields(self) -> List[bool]:
        """
        Return a list of booleans that indicate the privacy status of a field.

        The value is True, if the field should only be accessible to a site manager/admin.
        """
        if self.private:
            return [True for i in self.get_model_field_names()]
        else:
            if self.properties is not None:
                return list(chain(*[p.get_private_fields() for p in self.properties]))
            else:
                return [False for i in self.get_model_fields()]

    # use the ideas from playing around with filters in #40
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
    """
    A property, that has a BooleanProperty as a condition.

    If this condition is true, this makes a set of other properties editable:

    Example:
        Only ask for the experience as a medical student,
        if the participant claims to be a medical student.

    ConditionalProperty(
        name="medstud",
        label="Medical Student / Doctor",
        properties=[
            m4e.OrderedSingleChoiceProperty(
                name="experience",
                label="Experience Level",
                choices=[
                    (0, "Preclinical Section"),
                    (1, "Last Year Student"),
                    (2, "Assistant Doctor"),
                    (3, "Consultant"),
                ],
                default=0,
            )])
    """

    property_type = "conditional"

    def __init__(self, properties, **kwargs):
        # If we allowed a 'required' setting for this property,
        # we would have to insert a custom validator that checks the interdependency between
        # the  condition and its conditional properties.
        super().__init__(**kwargs)
        self.properties = properties

    def get_model_field_names(self, prefix=None):
        model_field_name = self.name if prefix is None else prefix + "--" + self.name
        conditional_fields = list(
            chain(*[p.get_model_field_names(model_field_name) for p in self.properties])
        )
        return [model_field_name + "-cond", *conditional_fields]

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
    """
    Choose several of different options, which are unordered.

    Example:
        A participant can choose several areas of his expertise.

    MultipleChoiceProperty(
            name="area",
            label="Areas of expertise",
            info_text="In which fields to you have previous expertise?",
            choices=[
                ("IM", "Internal Medicine"),
                ("IC", "Intensive Care"),
                ("EM", "Emergency Medicine"),
                ("GM", "General Medicine"),
            ],
        )
    """

    property_type = "multiple_choice"

    def __init__(self, choices, **kwargs):
        # putting a required in this property is a difficult to define behaviour
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
    """
    Choose one option out of many (like a RadioButton).

    Example:
        A participant lives in a specific type of building.

    SingleChoiceProperty(
                    name="build_type",
                    label="Type of object you are living in",
                    choices=[
                        ("AP", "Apartment"),
                        ("HO", "House"),
                        ("BO", "Boat")
                    ])

    """

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
    """
    A property where only one property can be chosen, but that implies an ordering.

    Example:
        A participant has a specific amount of time available each week.

    OrderedSingleChoiceProperty(
                    name="time_avail",
                    label="Time Availability Per Week",
                    is_required=True,
                    choices=[
                        (0, "10h per week"),
                        (1, "20h per week"),
                        (2, "30h per week"),
                        (3, "40h per week"),
                    ])
    """

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
    """
    A text is describing some more information.

    Example:
        A participant has some additional requirements that were not asked for in other properties.

    TextProperty(
            name="other",
            label="Other Qualifications",
            is_required=False,
            max_length=500,
        )
    """

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
    """
    A boolean value as a property.

    Example:
        A participant can afford to work without being compensated.

    BooleanProperty(
            name="compensation",
            label="I require compensation.",
        )
    """

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
