from itertools import chain
import urllib


class ParticipantConfig:

    properties = None

    @property
    def url_name(self):
        return urllib.parse.quote(self.name.lower())

    def get_model_field_names(self):
        return chain(*[p.get_model_field_names() for p in self.properties])

    def get_model_fields(self):
        names = self.get_model_field_names()
        fields = chain(*[p.get_model_fields() for p in self.properties])
        return zip(names, fields)

    def generate_random_assignment(self):
        names = self.get_model_field_names()
        random_values = chain(*[p.generate_random_assignment() for p in self.properties])
        return zip(names, random_values)

    def get_private_fields(self):
        names = self.get_model_field_names()
        privates = chain(*[p.get_private_fields() for p in self.properties])
        return [name for name, private in zip(names, privates) if private]

    def get_filter_fields(self):
        names = self.get_model_field_names()
        filters = chain(*[p.get_filters() for p in self.properties])
        return zip(names, filters)
