# Generated by Django 2.0.13 on 2019-06-25 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odonto', '0018_extractionchart_ll_b'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosis',
            name='details',
            field=models.TextField(blank=True),
        ),
    ]