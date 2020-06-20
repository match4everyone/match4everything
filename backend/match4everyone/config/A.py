from apps.matching.configuration.participant import ParticipantConfig
import apps.matching.configuration.properties as m4e


# todo: required and private properties # noqa
class A(ParticipantConfig):
    name = "Helper"

    # todo: use this # noqa
    # requires_approval = True

    # todo: use this # noqa
    # enable_location = True
    # enable_time = False

    properties = [
        m4e.PropertyGroup(
            name="personal_information",
            label="Personal information",
            private=True,
            properties=[
                m4e.TextProperty(label="First Name", max_length=100),
                m4e.TextProperty(label="Last Name", is_required=True, max_length=100),
                m4e.TextProperty(label="Phone Number", max_length=20),
            ],
        ),
        m4e.PropertyGroup(
            name="information_about_support",
            label="Information about your support",
            help_text="We need to know this because it is important for someone.",
            properties=[
                m4e.MultipleChoiceProperty(
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
                    label="Time Availability Per Week",
                    is_required=True,
                    choices=[
                        (0, "10h per week"),
                        (1, "20h per week"),
                        (2, "30h per week"),
                        (3, "40h per week"),
                    ],
                ),
                m4e.BooleanProperty(label="I need accommodation"),
            ],
        ),
        m4e.PropertyGroup(
            name="professional_training",
            label="Professional Training",
            properties=[
                m4e.ConditionalProperty(
                    name="medical_student_or_doctor",
                    label="Medical Student / Doctor",
                    properties=[
                        m4e.OrderedSingleChoiceProperty(
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
                            label="Recognition as an internship or other study requirements is important",
                        ),
                        m4e.TextProperty(
                            label="Other Qualifications", is_required=True, max_length=500
                        ),
                    ],
                )
            ],
        ),
    ]
