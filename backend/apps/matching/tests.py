from io import StringIO

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
    args = ["--add-a=" + str(a), "--add-b=" + str(b)]
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
    def test_migration_with_data(self):
        # Migrate to starting point
        output = StringIO()
        args = ["matching", "0001_initial"]
        call_command("migrate", *args, stdout=output)

        # Create testdata, otherwise a data migration would be easy
        create_superuser()
        create_fakeusers()

        # Test successful migration
        output = StringIO()
        call_command("migrate", stdout=output)

        self.assertNotIn("Traceback", output.getvalue())
        self.assertNotIn("Error", output.getvalue())

        # Test successful rollback
        output = StringIO()
        args = ["matching", "0001_initial"]
        call_command("migrate", *args, stdout=output)

        self.assertNotIn("Traceback", output.getvalue())
        self.assertNotIn("Error", output.getvalue())
