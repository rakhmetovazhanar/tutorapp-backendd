# Generated by Django 5.0.1 on 2024-03-29 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0022_alter_customuser_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='language',
            field=models.CharField(choices=[('Казахский', 'Казахский'), ('Русский', 'Русский'), ('Английский', 'Английский')], max_length=250),
        ),
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('Легкий', 'Легкий'), ('Средний', 'Средний'), ('Сложный', 'Сложный')], max_length=250),
        ),
    ]
