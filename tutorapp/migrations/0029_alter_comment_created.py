# Generated by Django 5.0.1 on 2024-04-10 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0028_comment_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
