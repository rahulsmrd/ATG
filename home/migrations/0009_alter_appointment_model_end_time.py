# Generated by Django 4.1.4 on 2024-03-15 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_appointment_model_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment_model',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]