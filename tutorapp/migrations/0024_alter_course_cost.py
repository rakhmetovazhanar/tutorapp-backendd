# Generated by Django 5.0.1 on 2024-03-29 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0023_alter_course_language_alter_course_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='cost',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
