from io import StringIO

from django.core.management import call_command
from django.test import TestCase


def create_superuser():
    output = StringIO()
    args = ["--noinput", "--email=staff@example.com", "--username=staff"]
    opts = {}
    call_command("createsuperuser", *args, stdout=output, **opts)
    return output.getvalue()


class ProvenBugsTestCase(TestCase):
    def test_superuser_creation(self):

        output = create_superuser()
        self.assertIn("Superuser created successfully", output)
