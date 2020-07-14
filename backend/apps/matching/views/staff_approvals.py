import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.text import format_lazy
from django.utils.translation import gettext as _
from django.views import View
from django_tables2.config import RequestConfig

from apps.matching.models import Participant
from apps.matching.tables import ApproveParticipantTable

logger = logging.getLogger(__name__)


# TODO: Only user with 'can_approve_type_a' or 'can_approve_type_b' should see the corresponding approval interfaces and be able to approve someone https://github.com/match4everyone/match4everything/issues/121
@method_decorator([login_required, staff_member_required], name="dispatch")
class ApproveParticipantsView(View):
    template_name = "approve_hospitals.html"

    def get(self, request, p_type):
        search_unapproved_mails = request.GET.get("search_unapproved_mails", "")
        search_approved_mails = request.GET.get("search_approved_mails", "")
        table_approved = ApproveParticipantTable[p_type](
            Participant[p_type].objects.filter(
                is_approved=True, user__email__icontains=search_approved_mails
            )
        )
        table_approved.prefix = "approved"
        RequestConfig(
            request,
            paginate={"page": request.GET.get(table_approved.prefix + "page", 1), "per_page": 5},
        ).configure(table_approved)

        # table_approved.paginate(page=request.GET.get(table_approved.prefix + "page", 1), per_page=5)

        table_unapproved = ApproveParticipantTable[p_type](
            Participant[p_type].objects.filter(
                is_approved=False, user__email__icontains=search_unapproved_mails
            )
        )
        table_unapproved.prefix = "unapproved"
        RequestConfig(
            request,
            paginate={"page": request.GET.get(table_unapproved.prefix + "page", 1), "per_page": 5},
        ).configure(table_unapproved)

        return render(
            request,
            "staff/approve_participants.html",
            {
                "table_approved": table_approved,
                "table_unapproved": table_unapproved,
                "p_type": p_type,
            },
        )

    def post(self, request, *args, **kwargs):
        post_params = self.request.POST
        if "delete" in post_params:
            p = get_object_or_404(Participant[self.kwargs["p_type"]], uuid=post_params["uuid"])
            name = p.user
            p.user.delete()
            text = format_lazy(_("You deleted the participant with email '{name}'."), name=name)
            messages.add_message(self.request, messages.INFO, text)
        elif "change_approval" in post_params:
            p = get_object_or_404(Participant[self.kwargs["p_type"]], uuid=post_params["uuid"])
            p.change_approval(self.request.user)
            name = p.user
            text = format_lazy(
                _("You changed the approval of the participant with email '{name}'."), name=name
            )
            messages.add_message(self.request, messages.INFO, text)
        return self.get(request, self.kwargs["p_type"])
