# Generated by Django 5.0.1 on 2024-02-24 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('background', models.ImageField(blank=True, upload_to='images/presentation/')),
                ('is_published', models.BooleanField()),
                ('presenter', models.CharField(max_length=150, null=True)),
                ('cnt_view', models.PositiveIntegerField(default=0, editable=False)),
            ],
            options={
                'db_table': 'Presentation',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Tag',
            },
        ),
    ]
