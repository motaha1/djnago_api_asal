# Generated by Django 3.0.5 on 2023-01-11 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_patientprofile_chat_bot'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]