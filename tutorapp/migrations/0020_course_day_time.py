# Generated by Django 5.0.1 on 2024-03-28 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0019_alter_courserating_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='day_time',
            field=models.CharField(default=None, max_length=250),
            preserve_default=False,
        ),
    ]
