from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, TransactionTestCase


def create_superuser():
    output = StringIO()
    args = ["--noinput", "--email=staff@example.com", "--username=staff"]
    opts = {}
    call_command("createsuperuser", *args, stdout=output, **opts)
    return output.getvalue()


def create_fakeusers(a=10, b=5):
    output = StringIO()
    args = [
        "--add-{a}=".format(a=settings.PARTICIPANT_SETTINGS["A"].url_name) + str(a),
        "--add-{b}=".format(b=settings.PARTICIPANT_SETTINGS["B"].url_name) + str(b),
    ]
    opts = {}
    call_command("createfakeusers", *args, stdout=output, **opts)
    output_string = output.getvalue()
    assert ("Created " + str(b) + " participants") in output_string
    return output_string


class ProvenBugsTestCase(TestCase):
    def test_superuser_creation(self):

        output = create_superuser()
        self.assertIn("Superuser created successfully", output)


class MigrationTestCase(TransactionTestCase):
    def test_migration_rollback_for_configuration(self):
        # Migrate to starting point
        output = StringIO()
        args = ["matching", "0002_permission_group_creation"]
        call_command("migrate", *args, stdout=output)

        # Test successful migration
        output = StringIO()
        call_command("migrate", stdout=output)

        self.assertNotIn("Traceback", output.getvalue())
        self.assertNotIn("Error", output.getvalue())

        create_fakeusers()

        # Test successful rollback
        output = StringIO()
        args = ["matching", "0002_permission_group_creation"]
        call_command("migrate", *args, stdout=output)

        self.assertNotIn("Traceback", output.getvalue())
        self.assertNotIn("Error", output.getvalue())
