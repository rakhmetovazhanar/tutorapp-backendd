# Generated by Django 5.0.1 on 2024-03-28 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0018_remove_course_rating_course_avg_rating_courserating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courserating',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
        ),
    ]