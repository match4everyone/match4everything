from django.http import HttpResponse
from django.template import Context, Template
from django.views.generic.base import View
from post_office.models import EmailTemplate


class EmailTemplatePreview(View):
    def get(self, request, *args, **kwargs):
        # Fetch template from database
        email_template = EmailTemplate.objects.filter(name__exact=str(kwargs['template_name']))

        # Check if there is only one template
        if len(email_template):
            # Render HTML template
            email_html = Template(email_template[0].html_content).render(Context({}))
        else:
            # Display error
            email_html = """
            Error could not load template. Please try again.
            """
        return HttpResponse(email_html)
