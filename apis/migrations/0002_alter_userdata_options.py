# Generated by Django 5.1.4 on 2025-02-18 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdata',
            options={'ordering': ['email']},
        ),
    ]
