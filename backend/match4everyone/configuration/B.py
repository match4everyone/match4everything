from apps.matching.configuration.participant import ParticipantConfig
import apps.matching.configuration.properties as m4e


# todo: required and private properties # noqa
class BConfig(ParticipantConfig):
    name = "Institution"

    LOCATION_SEARCH_MAX_RADIUS = 100  # km

    # todo: use this # noqa
    # enable_location = True
    # enable_time = False
    # permissions = [
    #    NewPermissions.can_contact_type_a_if_approved,
    # ]

    profile_visible_for_participants_of_different_type = True
    profile_visible_for_participants_of_same_type = False

    properties = [
        m4e.PropertyGroup(
            name="pers_info",
            label="Personal information",
            properties=[
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
            ],
        )
    ]


B = BConfig()
