# Generated by Django 3.2.4 on 2021-06-08 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0002_alter_attribute_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute_set', to='adverts.category'),
        ),
    ]