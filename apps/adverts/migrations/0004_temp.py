# Generated by Django 3.2.4 on 2021-06-17 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0003_alter_location_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('lat', models.FloatField()),
                ('lan', models.FloatField()),
            ],
            options={
                'db_table': 'temp',
                'ordering': ['region', 'district'],
            },
        ),
    ]