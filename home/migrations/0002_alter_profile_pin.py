# Generated by Django 4.1.4 on 2023-11-25 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pin',
            field=models.PositiveIntegerField(),
        ),
    ]
