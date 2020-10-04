from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
import numpy as np
from tqdm import tqdm

from apps.matching.models import Participant, ParticipantInfo, ParticipantInfoLocation, User

FAKE_MAIL = "@example.com"


def new_mail(x):
    return ("%s" % x) + FAKE_MAIL


class Command(BaseCommand):
    # has to be "help" because we inherit from django manage.py Command, thus ignore A003
    help = (  # noqa
        "Populates the database with fake users or deletes them."
        "Every user has their email as their password."
    )

    def add_arguments(self, parser):

        parser.add_argument(
            "--delete",
            action="store_true",
            help='Delete all users with an email ending in "%s"' % FAKE_MAIL,
        )

        parser.add_argument(
            "--add-{a}".format(a=settings.PARTICIPANT_SETTINGS["A"].url_name),
            nargs=1,
            help="Add [N] new {a} to the dataset".format(a=settings.PARTICIPANT_SETTINGS["A"].name),
        )

        parser.add_argument(
            "--add-{b}".format(b=settings.PARTICIPANT_SETTINGS["B"].url_name),
            nargs=1,
            help="Add [N] new {b} to the dataset".format(b=settings.PARTICIPANT_SETTINGS["B"].name),
        )

        parser.add_argument(
            "--no-input", action="store_true", help="Answer yes to all questions.",
        )

    def handle(self, *args, **options):
        if (
            not options["delete"]
            and options["add_{a}".format(a=settings.PARTICIPANT_SETTINGS["A"].url_name)] is None
            and options["add_{b}".format(b=settings.PARTICIPANT_SETTINGS["B"].url_name)] is None
        ):
            self.print_help("", "")
            return None

        self.all_yes = options["no_input"]

        if options["delete"]:
            self.delete_all_fakes()
        if options["add_{a}".format(a=settings.PARTICIPANT_SETTINGS["A"].url_name)] is not None:
            self.add_fake(
                participant_type="A",
                n=int(options["add_{a}".format(a=settings.PARTICIPANT_SETTINGS["A"].url_name)][0]),
            )
        if options["add_{b}".format(b=settings.PARTICIPANT_SETTINGS["B"].url_name)] is not None:
            self.add_fake(
                participant_type="B",
                n=int(options["add_{b}".format(b=settings.PARTICIPANT_SETTINGS["B"].url_name)][0]),
            )

    def delete_all_fakes(self):
        qs = User.objects.filter(email__contains=FAKE_MAIL)

        n = qs.count()
        if n == 0:
            self.stdout.write(self.style.SUCCESS("No fake users detected."))
            return

        is_sure = (
            input(
                'You are about to delete %s users with emails including "%s". '
                "Are you sure you want to delete them? [y/n]" % (n, FAKE_MAIL)
            )
            if not self.all_yes
            else "y"
        )
        if is_sure != "y":
            self.stdout.write(self.style.WARNING("Users NOT deleted."))
            return

        qs.delete()
        self.stdout.write(self.style.SUCCESS("Successfully deleted these %s fake users." % n))

    def add_fake(self, participant_type, n):
        n_users = User.objects.all().count()

        for i in tqdm(range(n)):
            m = participant_type + new_mail(i + n_users)
            u = User.new(
                email=m,
                pwd=m,
                is_A=participant_type == "A",
                is_B=participant_type == "B",
                is_participant=True,
                validated_email=True,
                date_joined=datetime.now() - timedelta(days=np.random.randint(0, 30)),
            )

            p = Participant[participant_type].objects.create(user=u, is_activated=True)
            pi = ParticipantInfo[participant_type].generate_fake(participant=p)
            ParticipantInfoLocation[participant_type].generate_fake(participant_info=pi)

            # if we do not require approvals, add everyone to the approved group on creation
            if (
                participant_type == "A"
                and not settings.PARTICIPANT_SETTINGS["A"].needs_manual_approval_from_staff
            ):
                approved_participants = Group.objects.get(name="approved_a")
                p.is_approved = True
                p.approval_date = datetime.now()
                approved_participants.user_set.add(u)
            if (
                participant_type == "B"
                and not settings.PARTICIPANT_SETTINGS["B"].needs_manual_approval_from_staff
            ):
                approved_participants = Group.objects.get(name="approved_b")
                p.is_approved = True
                p.approval_date = datetime.now()
                approved_participants.user_set.add(u)
            p.save()

        self.stdout.write(
            self.style.SUCCESS("Created %s participants of p_type %s." % (n, participant_type))
        )
