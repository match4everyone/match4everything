from .map import map_JSON, map_view  # noqa
from .participant_change_activation import ChangeActivationAskView, ChangeActivationRedirect  # noqa
from .participant_dashboard import ParticipantDashboard  # noqa
from .participant_profile_edit import ParticipantInfoUpdateView  # noqa
from .participant_signup import ParticipantSignup  # noqa
from .profile_dashboard_redirect import ProfileDashboardRedirect  # noqa
from .user_custom_login import CustomLoginView  # noqa
from .user_deletion import delete_me, delete_me_ask  # noqa
from .user_email_validation import resend_validation_email, validate_email  # noqa
from .user_login_redirect import LoginRedirect  # noqa
