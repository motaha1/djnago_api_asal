# Generated by Django 3.0.5 on 2023-01-13 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20230112_0302'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='location',
            field=models.CharField(blank=True, max_length=1000000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar1',
            field=models.CharField(blank=True, max_length=100000000, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('specialist', 'patient')},
        ),
    ]
