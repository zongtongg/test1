# Generated by Django 3.2.4 on 2021-06-15 19:14

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, default=None, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=255, null=True, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='adverts.location')),
            ],
            options={
                'ordering': ['lft'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='adverts.category')),
            ],
            options={
                'ordering': ['lft'],
            },
        ),
        migrations.CreateModel(
            name='AdvertsAdvert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('currency', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True, null=True)),
                ('status', models.CharField(default='draft', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='category_set', to='adverts.category')),
                ('location', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='location_set', to='adverts.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('string', 'String'), ('integer', 'Integer'), ('float', 'Float')], max_length=50)),
                ('required', models.BooleanField(default=False)),
                ('variants', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='', max_length=255, null=True), blank=True, size=10)),
                ('sort', models.IntegerField()),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute_set', to='adverts.category')),
            ],
            options={
                'unique_together': {('category', 'name')},
            },
        ),
    ]
