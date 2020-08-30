from django.http import HttpResponse
from post_office import mail
from datetime import datetime
from django.conf import settings


def send_dummy_mail(request):
    counter = 0
    for _ in range(1000):
        counter += 1
        mail.send(

            ['recipient@example.com', 'mail2@asdf.de'],  # List of email addresses also accepted
            'from@example.com',
            subject=counter,
            message='Hi there!',
            html_message='Hi <strong>there</strong>!',
            priority='high'
        )

    return HttpResponse(counter)
