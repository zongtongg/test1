# Generated by Django 3.2.4 on 2021-07-25 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0008_remove_advertsadvert_value'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='value',
            unique_together={('advert', 'attribute')},
        ),
    ]
