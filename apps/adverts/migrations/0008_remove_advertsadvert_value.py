# Generated by Django 3.2.4 on 2021-06-18 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0007_advertsadvert_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertsadvert',
            name='value',
        ),
    ]
