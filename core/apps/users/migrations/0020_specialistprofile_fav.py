# Generated by Django 3.0.5 on 2023-01-15 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20230113_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialistprofile',
            name='Fav',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
