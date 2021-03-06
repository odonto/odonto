# Generated by Django 2.0.13 on 2020-01-15 12:48

from django.db import migrations
from django.db import transaction

def forward_iotn(instance):
    if instance.iotn:
        instance.iotn_field = str(instance.iotn)
        instance.save()

    if instance.iotn_not_applicable:
        instance.iotn_field = "N/A"
        instance.save()

def backwards_iotn(instance):
    if instance.iotn_field == "N/A":
        instance.iotn_not_applicable = True
        instance.save()

    elif instance.iotn_field:
        instance.iotn = int(instance.iotn_field)
        instance.save()


@transaction.atomic
def forwards(apps, schema_editor):
    Assessment = apps.get_model('odonto', 'OrthodonticAssessment')
    for assessment in Assessment.objects.all():
        forward_iotn(assessment)

    Treatment = apps.get_model('odonto', "OrthodonticTreatment")
    for treatment in Treatment.objects.all():
        forward_iotn(treatment)


@transaction.atomic
def backwards(apps, schema_editor):
    Assessment = apps.get_model('odonto', 'OrthodonticAssessment')
    for assessment in Assessment.objects.all():
        backwards_iotn(assessment)

    Treatment = apps.get_model('odonto', "OrthodonticTreatment")
    for treatment in Treatment.objects.all():
        backwards_iotn(treatment)


class Migration(migrations.Migration):

    dependencies = [
        ('odonto', '0039_auto_20200115_1248'),
    ]

    operations = [
        migrations.RunPython(
            forwards, backwards
        )
    ]
