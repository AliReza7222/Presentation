# Generated by Django 5.0.1 on 2024-02-14 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('presentation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('section_link', models.CharField(max_length=255)),
                ('section_id', models.CharField(max_length=150)),
                ('content', models.TextField()),
                ('presentation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='presentation.presentation')),
            ],
            options={
                'db_table': 'Slide',
            },
        ),
    ]
