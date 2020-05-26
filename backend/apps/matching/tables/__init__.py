from match4healthcare.utils.imports import import_submodules

STATIC_HACK = False
if STATIC_HACK:
    """
    This code is never executed, but it is needed to trick IDEs and Python linters
    to register the dynamically loaded submodules.
    The actual modules are loaded dynamically during startup
    Inspired by https://github.com/celery/kombu/blob/4644a5e9400beac6668f326c16078286f7d60b64/kombu/__init__.py#L34
    """
    from .hospital_approval_list import *  # noqa
    from .hospital_contacted_students_list import *  # noqa
    from .hospital_list import *  # noqa
    from .newsletter_list import *  # noqa
    from .student_list import *  # noqa
    from .student_overview import *  # noqa

import_submodules(globals(), __name__, __path__)
