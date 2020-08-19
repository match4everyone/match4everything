from apps.matching.configuration.participant import ParticipantConfig
import apps.matching.configuration.properties as m4e


# todo: required and private properties # noqa
class AConfig(ParticipantConfig):
    name = "Helper"

    # todo: use this # noqa
    # enable_location = True
    # enable_time = False
    # permissions = [
    #    NewPermissions.can_contact_type_b,
    # ]
    profile_visible_for_B = True
    profile_visible_for_other_A = False

    properties = [
        m4e.PropertyGroup(
            name="pers_info",
            label="Personal information",
            private=True,
            properties=[
                m4e.TextProperty(label="First Name", max_length=100),
                m4e.TextProperty(label="Last Name", is_required=True, max_length=100),
                m4e.TextProperty(label="Phone Number", max_length=20),
            ],
        ),
        m4e.PropertyGroup(
            name="info_supp",
            label="Information about your support",
            help_text="We need to know this because it is important for someone.",
            properties=[
                m4e.MultipleChoiceProperty(
                    name="pref_area",
                    label="Preferred Area of Help",
                    # no_choice_option=True,
                    # no_choice_label="None, I help where I can",
                    choices=[
                        ("ME", "Medical Practice"),
                        ("PD", "Public Health Department and other Institutions"),
                        ("HO", "Hospital"),
                        ("ES", "Emergency Services"),
                        ("PH", "Pharmacy"),
                        ("NF", "Nursing Facilities"),
                        ("LA", "Laboratory"),
                        ("MP", "Medical Practice"),
                    ],
                ),
                m4e.OrderedSingleChoiceProperty(
                    name="time_avail",
                    label="Time Availability Per Week",
                    is_required=True,
                    choices=[
                        (0, "10h per week"),
                        (1, "20h per week"),
                        (2, "30h per week"),
                        (3, "40h per week"),
                    ],
                ),
                m4e.BooleanProperty(name="accom", label="I need accommodation"),
            ],
        ),
        m4e.PropertyGroup(
            name="prof_train",
            label="Professional Training",
            properties=[
                m4e.ConditionalProperty(
                    name="medstud",
                    label="Medical Student / Doctor",
                    properties=[
                        m4e.OrderedSingleChoiceProperty(
                            name="experience",
                            label="Experience Level",
                            # no_choice_option=True,
                            # no_choice_label="None chosen",
                            choices=[
                                (0, "Preclinical Section"),
                                (1, "Last Year Student"),
                                (2, "Assistant Doctor"),
                                (3, "Consultant"),
                            ],
                            default=0,
                        ),
                        m4e.MultipleChoiceProperty(
                            name="area",
                            label="Area of expertise",
                            info_text="Please enter your previous experience or field of study in the following fields:",
                            choices=[
                                ("AN", "Anaestesiology"),
                                ("SU", "Surgery"),
                                ("IM", "Internal Medicine"),
                                ("IC", "Intensive Care"),
                                ("EM", "Emergency Medicine"),
                                ("GM", "General Medicine"),
                            ],
                        ),
                        m4e.BooleanProperty(
                            name="internship",
                            label="Recognition as an internship or other study requirements is important",
                        ),
                        m4e.TextProperty(
                            name="other", label="Other Qualifications", max_length=500,
                        ),
                    ],
                )
            ],
        ),
    ]


A = AConfig()
