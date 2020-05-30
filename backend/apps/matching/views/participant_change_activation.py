import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.base import RedirectView, TemplateView
from django.urls import reverse

from apps.matching.admin import participant_required

logger = logging.getLogger(__name__)

"""
Methods for profile activation and deactivation
"""

@method_decorator([login_required,participant_required], name="dispatch")
class ChangeActivationRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        p = self.request.user.participant()
        status = p.is_activated
        p.is_activated = not p.is_activated
        p.save()
        if status:
            messages.add_message(
                self.request,
                messages.INFO,
                _(
                    "You successfully deactivated your profile."
                ),
            )
        else:
            messages.add_message(
                self.request,
                messages.INFO,
                _(
                    "You successfully reactivated your profile."
                ),
            )
        return reverse("profile", kwargs={ 'p_type': p.type() })


@method_decorator([login_required,participant_required], name="dispatch")
class ChangeActivationAskView(TemplateView):
    template_name = "participant/participant_change_activation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_activated"] = self.request.user.participant().is_activated
        return context

