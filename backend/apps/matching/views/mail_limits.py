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
from apps.matching.tables import MailLimitsTable

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required], name="dispatch")
class IncreaseMailLimitView(View):
    def get(self, request, p_type):
        search_mail_limits = request.GET.get("search_mail_limits", "")
        table_mail_limits = MailLimitsTable[p_type](
            Participant[p_type].objects.filter(user__email__icontains=search_mail_limits)
        )
        RequestConfig(
            request,
            paginate={
                "page": request.GET.get(table_mail_limits.prefix + "page", 1),
                "per_page": 10,
            },
        ).configure(table_mail_limits)

        return render(
            request,
            "staff/increase_mail_limits.html",
            {"table_mail_limits": table_mail_limits, "p_type": p_type,},
        )

    def post(self, request, *args, **kwargs):
        post_params = self.request.POST
        p = get_object_or_404(Participant[self.kwargs["p_type"]], uuid=post_params["uuid"])
        p.increase_mail_limit(mail_limit=post_params["mail_limit"])
        name = p.user
        text = format_lazy(_("You increased the mail limit for '{name}'."), name=name)
        messages.add_message(self.request, messages.INFO, text)
        return self.get(request, self.kwargs["p_type"])
