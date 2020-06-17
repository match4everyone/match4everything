from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class ProvenBugsTestCase(TestCase):
    def test_superuser_creation(self):

        output = StringIO()
        args = ["--noinput", "--email=staff@example.com", "--username=staff"]
        opts = {}
        call_command("createsuperuser", *args, stdout=output, **opts)
        self.assertIn("Superuser created successfully", output.getvalue())
