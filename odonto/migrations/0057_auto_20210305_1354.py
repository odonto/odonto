# Generated by Django 2.0.13 on 2021-03-05 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odonto', '0056_covidstatus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='covidstatus',
            options={'verbose_name': 'Covid status', 'verbose_name_plural': 'Covid statuses'},
        ),
        migrations.AlterField(
            model_name='covidstatus',
            name='other_covid_status',
            field=models.IntegerField(blank=True, null=True, verbose_name='Other covid status'),
        ),
        migrations.AlterField(
            model_name='covidstatus',
            name='symptom_free',
            field=models.IntegerField(blank=True, null=True, verbose_name='Symptom free'),
        ),
    ]