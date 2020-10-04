from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView

from apps.matching.forms import FilterEditForm
from apps.matching.models import ParticipantInfoFilter


@method_decorator([login_required], name="dispatch")
class FilterUpdateView(UpdateView):
    """Updates a filter."""

    template_name = "filters/filter_edit.html"
    slug_url_kwarg = "uuid"
    slug_field = "uuid"

    def dispatch(self, request, *args, **kwargs):
        """Make sure only creators of the filter can edit it."""
        obj = self.get_object()
        if not obj.created_by == request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return FilterEditForm[self.kwargs["p_type"]]

    def get_queryset(self):
        return ParticipantInfoFilter[self.kwargs["p_type"]].objects.all()

    def get_success_url(self):
        return reverse("profile", kwargs={"p_type": self.kwargs["p_type"]})

    def form_valid(self, form):
        res = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, _("Successfully updated your filter."))
        return res
