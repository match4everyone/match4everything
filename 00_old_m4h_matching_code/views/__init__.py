from match4healthcare.utils.imports import import_submodules

STATIC_HACK = False
if STATIC_HACK:
    """
    This code is never executed, but it is needed to trick IDEs and Python linters
    to register the dynamically loaded submodules.
    The actual modules are loaded dynamically during startup
    Inspired by https://github.com/celery/kombu/blob/4644a5e9400beac6668f326c16078286f7d60b64/kombu/__init__.py#L34
    """
    from .approve_hospitals import *  # noqa
    from .change_hospital_approval_redirect import *  # noqa
    from .delete_hospital_redirect import *  # noqa
    from .emailtostudent_edit import *  # noqa
    from .emailtostudent_success import *  # noqa
    from .hospital_contact_possibilities import *  # noqa
    from .hospital_data_consent import *  # noqa
    from .hospital_detail import *  # noqa
    from .hospital_list import *  # noqa
    from .hospital_map import *  # noqa
    from .hospital_positions import *  # noqa
    from .hospital_posting_edit import *  # noqa
    from .index import *  # noqa
    from .newsletter_approve_via_mail import *  # noqa
    from .newsletter_detail import *  # noqa
    from .newsletter_list import *  # noqa
    from .newsletter_new import *  # noqa
    from .participant_edit_profile import *  # noqa
    from .participant_signup import *  # noqa
    from .profile_dashboard_redirect import *  # noqa
    from .staff_db_stats import *  # noqa
    from .staff_profile import *  # noqa
    from .student_detail import *  # noqa
    from .student_positions import *  # noqa
    from .student_selection import *  # noqa
    from .user_change_activation import *  # noqa
    from .user_count import *  # noqa
    from .user_custom_login import *  # noqa
    from backend.apps.matching.views.user_deletion import *  # noqa
    from .user_login_redirect import *  # noqa
    from .user_validate_email import *  # noqa

import_submodules(globals(), __name__, __path__)
