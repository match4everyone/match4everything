subject_prefix = "[plattform-name]"

contact_request_template_to = {
    "A": {
        "subject": "You have a new message from {{email_from}}: {{subject}}",
        "message": "Hallo, hier ist eine einladung von B: {{message}}. Answer them via our platform.  Best wishes, we",
    },
    "B": {
        "subject": "You have a new message from {{email_from}}: {{subject}}",
        "message": "Hallo, hier ist eine einladung von A: {{message}}. Answer them via our platform. Best wishes, we",
    },
}

response_template_to = {
    "B": {
        "subject": "{{email_from}} answered your contact request: {{subject}}",
        "message": "Hallo, you contacted {{email_to}}. Yey, they answered you: {{message}}. You can further communicate via email: {{email_from}} Best wishes, we",
    },
    "A": {
        "subject": "Someone answered your contact request.",
        "message": "Hallo, you contacted {{email_to}}. Yey, they answered you: {{message}}. You can further communicate via email: {{email_from}} Best wishes, we",
    },
}


def send_email(to_participant, from_participant, subject, message, email_type):
    to_p_type = to_participant.participant_type
    context = {
        "email_from": from_participant.user.email,
        "email_to": to_participant.user.email,
        "subject": subject,
        "message": message,
    }

    email_args = {"context": context, "headers": {"Reply-to": "REPLAY-EMAIL"}}

    if email_type == "response":
        template = response_template_to[to_p_type]
        email_args["cc"] = [from_participant.user.email]

    elif email_type == "contact_request":
        template = contact_request_template_to[to_p_type]

    else:
        ValueError("Email type not supported")

    email_args["subject"] = " ".join([subject_prefix, template["subject"]])
    email_args["html_message"] = template["message"]
    email_args["message"] = template["message"]  # please: convert to plain text
    email_args["to"] = [to_participant.user.email]

    print()
    print("We would like to send this message:")
    print(email_args)
