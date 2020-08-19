from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, Http404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import View

from apps.matching.forms import ContactForm
from apps.matching.models import Match, MATCH_STATE_OPTIONS


@method_decorator([login_required], name="dispatch")
class MatchDetailView(View):
    def dispatch(self, request, *args, **kwargs):
        self.uuid = kwargs["uuid"]
        self.match = get_object_or_404(Match, uuid=self.uuid)

        # ensure that the visitor is also the participant requested by this match
        if not self.match.requested_participant().user == request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self):
        initial_subject, initial_msg = self.match.inital_message

        context = {
            "initial_subject": initial_subject,
            "email_initiator_url": self.match.email_initiator_url,
            "initial_msg": initial_msg,
            "options": MATCH_STATE_OPTIONS,
            "value": self.match.state,
            "uuid": self.match.uuid,
            "response_subject": self.match.response_subject,
            "response_msg": self.match.response_message,
            "initiator_email": self.match.email_initiator,
            "filter_criteria": self.match.filter_uuid,
            "p_type_own": self.match.contacted_via_filter[1],
            "form": ContactForm(),
            "filter": self.match.contacted_via_filter[0],
        }
        return context

    def get(self, request, uuid):

        context = self.get_context_data()

        return render(request, "matches/contact_request.html", context)

    def post(self, request, uuid):

        if "decline" in request.POST:
            self.match.state = MATCH_STATE_OPTIONS.DECLINE
            self.match.save()
            messages.add_message(
                self.request,
                messages.INFO,
                f"You declined an offer by {self.match.initiator_participant().user.email}.",
            )
            return HttpResponseRedirect(reverse("matches-requests-to-me"))
        elif "send_message" in request.POST:

            form = ContactForm(request.POST)
            if form.is_valid():
                # send a message to the participant who contacted me and set the email to shared
                self.match.state = MATCH_STATE_OPTIONS.SUCCESSFUL
                self.match.response_subject = form.cleaned_data["subject"]
                self.match.response_message = form.cleaned_data["message"]
                # SEND MAIL with cc
                # send_mail(to=match.initiator_participant().user.email, cc=match.receriver().user.email,
                # POst subject und post message...
                self.match.save()

                messages.add_message(
                    self.request,
                    messages.INFO,
                    f"You responded to {self.match.initiator_participant().user.email}. "
                    f"A copy of the response was sent to your own email.",
                )
                return HttpResponseRedirect(reverse("matches-requests-to-me"))
            else:
                context = self.get_context_data()
                context["form"] = form
                return render(request, "matches/contact_request.html", context)

        raise Http404
