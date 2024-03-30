# Generated by Django 5.0.1 on 2024-03-29 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0024_alter_course_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='avg_rating',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='cost',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
