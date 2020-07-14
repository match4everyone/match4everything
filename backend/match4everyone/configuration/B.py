from apps.matching.configuration.participant import ParticipantConfig
import apps.matching.configuration.properties as m4e


# todo: required and private properties # noqa
class B(ParticipantConfig):
    name = "Institution"

    # todo: use this # noqa
    # enable_location = True
    # enable_time = False
    # permissions = [
    #    NewPermissions.can_contact_type_a_if_approved,
    # ]

    properties = [
        m4e.TextProperty(
            name="name",
            label="Official name of your institution",
            is_required=True,
            max_length=100,
        ),
        m4e.TextProperty(
            name="contact",
            label="Full name of the person to contact",
            is_required=True,
            max_length=100,
        ),
        m4e.TextProperty(
            name="phone_number",
            label="Phone number of contact person",
            is_required=True,
            max_length=100,
        ),
    ]
