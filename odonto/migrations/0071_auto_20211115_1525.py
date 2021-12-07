# Generated by Django 2.0.13 on 2021-11-15 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odonto', '0070_dental_administrator'),
    ]

    operations = [
        migrations.AddField(
            model_name='fp17clinicaldataset',
            name='custom_made_occlusal_appliance',
            field=models.CharField(blank=True, choices=[('Hard', 'Hard'), ('Soft', 'Soft'), ('Both', 'Both')], max_length=256, null=True, verbose_name='Custom made occlusal appliance'),
        ),
        migrations.AddField(
            model_name='fp17clinicaldataset',
            name='denture_additions_reline_rebase',
            field=models.BooleanField(default=False, verbose_name='Denture Additions/Reline/Rebase'),
        ),
        migrations.AddField(
            model_name='fp17clinicaldataset',
            name='phased_treatment',
            field=models.BooleanField(default=False, verbose_name='Phased treatment'),
        ),
    ]
