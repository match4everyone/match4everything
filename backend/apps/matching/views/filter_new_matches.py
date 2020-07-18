from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import View


from apps.matching.models import Match, ParticipantInfoFilter


@method_decorator([login_required], name="dispatch")
class FilterContactNewMatchView(View):
    def post(self, request, p_type, uuid):
        filter_ = get_object_or_404(ParticipantInfoFilter[p_type], uuid=uuid)
        Match.contact_all_not_matched_to(filter_)
        messages.add_message(self.request, messages.SUCCESS, _("You contacted new people."))
        return HttpResponseRedirect(reverse("profile"))
