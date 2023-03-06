# Generated by Django 4.1.7 on 2023-03-05 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Identifier')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=300, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Dictionary',
                'verbose_name_plural': 'Dictionaries',
            },
        ),
        migrations.CreateModel(
            name='DictionaryVersion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Identifier')),
                ('version', models.CharField(max_length=50, verbose_name='Version')),
                ('date', models.DateField(verbose_name='Date')),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionaries.dictionary', verbose_name='Dictionary identifier')),
            ],
            options={
                'verbose_name': 'Dictionary version',
                'verbose_name_plural': "Dictionary version's",
            },
        ),
        migrations.CreateModel(
            name='DictionaryElement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Identifier')),
                ('code', models.CharField(max_length=100, verbose_name='Element code')),
                ('value', models.CharField(max_length=300, verbose_name='Element value')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionaries.dictionaryversion', verbose_name='Dictionary version identifier')),
            ],
            options={
                'verbose_name': 'Dictionary element',
                'verbose_name_plural': "Dictionary element's",
            },
        ),
        migrations.AddConstraint(
            model_name='dictionaryversion',
            constraint=models.UniqueConstraint(fields=('version', 'dictionary_id'), name='unique_version_dictionary_id'),
        ),
        migrations.AddConstraint(
            model_name='dictionaryversion',
            constraint=models.UniqueConstraint(fields=('date', 'dictionary_id'), name='unique_version_date_dictionary'),
        ),
        migrations.AddConstraint(
            model_name='dictionaryelement',
            constraint=models.UniqueConstraint(fields=('code', 'version_id'), name='unique_code_version_id'),
        ),
    ]
