# Generated by Django 2.0.13 on 2022-10-05 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odonto', '0078_merge_20221003_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orthodonticassessment',
            name='assessment',
            field=models.CharField(blank=True, choices=[('Assessment & review', 'Assessment & review'), ('Assess & refuse treatment', 'Assess & refuse treatment'), ('Assess & appliance fitted', 'Assess & appliance fitted'), ('Assessment and Debond – Overseas Patient', 'Assessment and Debond – Overseas Patient')], max_length=256, null=True, verbose_name='Assessment Type'),
        ),
    ]
