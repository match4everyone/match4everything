# Generated by Django 3.0.5 on 2020-05-26 21:56

import datetime
import uuid

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

import apps.matching_old.models.newsletter_approved_by
import apps.matching_old.models.student


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(blank=True, null=True, verbose_name="last login"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={"unique": "A user with that username already exists."},
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(blank=True, max_length=30, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(blank=True, max_length=150, verbose_name="last name"),
                ),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, verbose_name="email address"),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("is_student", models.BooleanField(default=False)),
                ("is_hospital", models.BooleanField(default=False)),
                ("validated_email", models.BooleanField(default=False)),
                ("email_validation_date", models.DateTimeField(blank=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"verbose_name": "user", "verbose_name_plural": "users", "abstract": False,},
            managers=[("objects", django.contrib.auth.models.UserManager()),],
        ),
        migrations.CreateModel(
            name="EmailGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("subject", models.CharField(default="", max_length=200)),
                ("message", models.TextField(default="", max_length=10000)),
                (
                    "uuid",
                    models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
                ),
                (
                    "registration_date",
                    models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LetterApprovedBy",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "approval_code",
                    models.IntegerField(
                        default=apps.matching_old.models.newsletter_approved_by.random_number
                    ),
                ),
                ("did_see_email", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "countrycode",
                    models.CharField(
                        choices=[("DE", "Deutschland"), ("AT", "Österreich")],
                        default="DE",
                        max_length=2,
                    ),
                ),
                (
                    "uuid",
                    models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
                ),
                (
                    "registration_date",
                    models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
                ),
                ("name_first", models.CharField(default="", max_length=50)),
                ("name_last", models.CharField(default="", max_length=50)),
                ("phone_number", models.CharField(blank=True, default="", max_length=100)),
                ("plz", models.CharField(max_length=5, null=True)),
                (
                    "umkreis",
                    models.IntegerField(
                        choices=[(1, "<10 km"), (2, "<20 km"), (3, "<40 km"), (4, ">40 km")],
                        null=True,
                    ),
                ),
                ("availability_start", models.DateField(default=datetime.datetime.now, null=True)),
                (
                    "braucht_bezahlung",
                    models.IntegerField(
                        choices=[
                            (2, "Ich freue mich über eine Vergütung, helfe aber auch ohne"),
                            (1, "Ich benötige eine Vergütung"),
                            (3, "Ich möchte ohne Bezahlung helfen"),
                        ],
                        default=2,
                    ),
                ),
                (
                    "zeitliche_verfuegbarkeit",
                    models.IntegerField(
                        choices=[
                            (1, "10h pro Woche"),
                            (2, "20h pro Woche"),
                            (3, "30h pro Woche"),
                            (4, "40h pro Woche"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "datenschutz_zugestimmt",
                    models.BooleanField(
                        default=False,
                        validators=[apps.matching_old.models.student.validate_checkbox],
                    ),
                ),
                (
                    "einwilligung_datenweitergabe",
                    models.BooleanField(
                        default=False,
                        validators=[apps.matching_old.models.student.validate_checkbox],
                    ),
                ),
                (
                    "einwilligung_agb",
                    models.BooleanField(
                        default=False,
                        validators=[apps.matching_old.models.student.validate_checkbox],
                    ),
                ),
                (
                    "sonstige_qualifikationen",
                    models.CharField(blank=True, default="keine", max_length=200),
                ),
                ("unterkunft_gewuenscht", models.BooleanField(default=False)),
                ("is_activated", models.BooleanField(default=True)),
                ("wunsch_ort_arzt", models.BooleanField(default=False)),
                ("wunsch_ort_gesundheitsamt", models.BooleanField(default=False)),
                ("wunsch_ort_krankenhaus", models.BooleanField(default=False)),
                ("wunsch_ort_pflege", models.BooleanField(default=False)),
                ("wunsch_ort_rettungsdienst", models.BooleanField(default=False)),
                ("wunsch_ort_labor", models.BooleanField(default=False)),
                ("wunsch_ort_apotheke", models.BooleanField(default=False)),
                ("wunsch_ort_ueberall", models.BooleanField(default=False)),
                ("ausbildung_typ_medstud", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_medstud_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "Vorklinischer Teil"),
                            (2, "Klinischer Teil"),
                            (3, "Praktisches Jahr"),
                            (4, "Assistenzarzt"),
                            (5, "Facharzt"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                (
                    "ausbildung_typ_medstud_famulaturen_anaesthesie",
                    models.BooleanField(default=False),
                ),
                (
                    "ausbildung_typ_medstud_famulaturen_chirurgie",
                    models.BooleanField(default=False),
                ),
                ("ausbildung_typ_medstud_famulaturen_innere", models.BooleanField(default=False)),
                ("ausbildung_typ_medstud_famulaturen_intensiv", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_medstud_famulaturen_notaufnahme",
                    models.BooleanField(default=False),
                ),
                (
                    "ausbildung_typ_medstud_famulaturen_allgemeinmedizin",
                    models.BooleanField(default=False),
                ),
                ("ausbildung_typ_medstud_anerkennung_noetig", models.BooleanField(default=False)),
                ("ausbildung_typ_mfa", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_mfa_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "1. Jahr"),
                            (2, "2. Jahr"),
                            (3, "3. Jahr"),
                            (4, "Berufstätig"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_mtla", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_mtla_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "1. Jahr"),
                            (2, "2. Jahr"),
                            (3, "3. Jahr"),
                            (4, "Berufstätig"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_mta", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_mta_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "1. Jahr"),
                            (2, "2. Jahr"),
                            (3, "3. Jahr"),
                            (4, "Berufstätig"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_ota", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_ota_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "1. Jahr"),
                            (2, "2. Jahr"),
                            (3, "3. Jahr"),
                            (4, "Berufstätig"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_ata", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_ata_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "1. Jahr"),
                            (2, "2. Jahr"),
                            (3, "3. Jahr"),
                            (4, "Berufstätig"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_notfallsani", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_notfallsani_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "1. Jahr"),
                            (2, "2. Jahr"),
                            (4, "Berufstätig"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_pflege", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_pflege_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "1. Jahr"),
                            (2, "2. Jahr"),
                            (3, "3. Jahr"),
                            (4, "Berufstätig"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_ergotherapie", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_ergotherapie_abschnitt",
                    models.IntegerField(
                        choices=[(0, "Keine Angabe"), (1, "In Ausbildung"), (2, "Berufstätig")],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_psycho", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_psycho_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "Studium"),
                            (2, "In Ausbildung"),
                            (3, "Berufstätig"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_sani", models.BooleanField(default=False)),
                ("ausbildung_typ_hebamme", models.BooleanField(default=False)),
                ("ausbildung_typ_fsj", models.BooleanField(default=False)),
                ("ausbildung_typ_zahni", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_zahni_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "Vorklinischer Teil"),
                            (2, "Klinischer Teil"),
                            (3, "Abgeschlossen"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_physio", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_physio_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "1. Jahr"),
                            (2, "2. Jahr"),
                            (3, "3. Jahr"),
                            (4, "Berufstätig"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
                ("ausbildung_typ_kinderbetreung", models.BooleanField(default=False)),
                (
                    "ausbildung_typ_kinderbetreung_ausgebildet_abschnitt",
                    models.IntegerField(
                        choices=[
                            (0, "Keine Angabe"),
                            (1, "Lediglich Erfahrungen"),
                            (2, "Abgeschlossene Ausbildung"),
                        ],
                        default=0,
                        null=True,
                    ),
                ),
            ],
            options={"ordering": ["plz"],},
        ),
        migrations.CreateModel(
            name="Newsletter",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "uuid",
                    models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
                ),
                (
                    "registration_date",
                    models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
                ),
                ("last_edited_date", models.DateTimeField(blank=True, default=None, null=True)),
                ("frozen_date", models.DateTimeField(blank=True, default=None, null=True)),
                ("send_date", models.DateTimeField(blank=True, default=None, null=True)),
                ("subject", models.CharField(default="", max_length=200)),
                ("message", models.TextField(default="", max_length=1000000)),
                ("was_sent", models.BooleanField(default=False)),
                ("send_to_hospitals", models.BooleanField(default=False)),
                ("send_to_students", models.BooleanField(default=False)),
                (
                    "user_validation_required",
                    models.IntegerField(
                        choices=[
                            (0, "validierte"),
                            (1, "nicht validierte"),
                            (2, "validierte und nicht validierte"),
                            (3, "validiert und von uns approved"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "frozen_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="frozen_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "letter_approved_by",
                    models.ManyToManyField(
                        related_name="letter_approved_by",
                        through="matching_old.LetterApprovedBy",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "letter_authored_by",
                    models.ManyToManyField(
                        related_name="letter_authored_by", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "sent_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sent_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="letterapprovedby",
            name="newsletter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="matching_old.Newsletter"
            ),
        ),
        migrations.AddField(
            model_name="letterapprovedby",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterUniqueTogether(
            name="letterapprovedby", unique_together={("user", "newsletter")},
        ),
        migrations.CreateModel(
            name="Hospital",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "countrycode",
                    models.CharField(
                        choices=[("DE", "Deutschland"), ("AT", "Österreich")],
                        default="DE",
                        max_length=2,
                    ),
                ),
                ("max_mails_per_day", models.IntegerField(default=200)),
                ("sonstige_infos", models.TextField(default="", max_length=10000)),
                ("ansprechpartner", models.CharField(default="", max_length=100)),
                ("telefon", models.CharField(default="", max_length=100)),
                ("firmenname", models.CharField(default="", max_length=100)),
                ("plz", models.CharField(max_length=5, null=True)),
                (
                    "uuid",
                    models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
                ),
                (
                    "registration_date",
                    models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
                ),
                ("is_approved", models.BooleanField(default=False)),
                ("approval_date", models.DateTimeField(null=True)),
                ("appears_in_map", models.BooleanField(default=False)),
                ("datenschutz_zugestimmt", models.BooleanField(default=False)),
                ("einwilligung_datenweitergabe", models.BooleanField(default=False)),
                (
                    "approved_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="approved_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["registration_date"],},
        ),
        migrations.CreateModel(
            name="EmailToSend",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("subject", models.CharField(default="", max_length=200)),
                ("message", models.TextField(default="", max_length=10000)),
                ("was_sent", models.BooleanField(default=False)),
                (
                    "uuid",
                    models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
                ),
                (
                    "registration_date",
                    models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
                ),
                ("send_date", models.DateTimeField(null=True)),
                (
                    "email_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="matching_old.EmailGroup",
                    ),
                ),
                (
                    "hospital",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="matching_old.Hospital"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="matching_old.Student"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmailToHospital",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("subject", models.CharField(default="", max_length=200)),
                ("message", models.TextField(default="", max_length=10000)),
                (
                    "uuid",
                    models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
                ),
                (
                    "registration_date",
                    models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
                ),
                ("send_date", models.DateTimeField(null=True)),
                (
                    "hospital",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="matching_old.Hospital"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="matching_old.Student"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="emailgroup",
            name="hospital",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="matching_old.Hospital"
            ),
        ),
    ]
