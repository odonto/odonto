# Generated by Django 2.0.13 on 2022-04-05 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odonto', '0075_fp17commissioning'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fp17commissioning',
            name='flexible_commissioning_flag',
        ),
        migrations.AddField(
            model_name='fp17commissioning',
            name='flexible_commissioning',
            field=models.CharField(blank=True, choices=[('Securing Access for Urgent Care', 'Securing Access for Urgent Care'), ('Promoting Access to Routine Care', 'Promoting Access to Routine Care'), ('Providing Care of High Needs Groups', 'Providing Care of High Needs Groups'), ('Starting Well', 'Starting Well'), ('Enhanced Health in Care Homes', 'Enhanced Health in Care Homes'), ('Collaboration in Local Care Networks', 'Collaboration in Local Care Networks')], max_length=255, null=True, verbose_name='Flexible commissioning'),
        ),
    ]
