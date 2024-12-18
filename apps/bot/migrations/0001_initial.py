# Generated by Django 5.1.4 on 2024-12-16 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(help_text='Name', max_length=128)),
                ('slug', models.SlugField(help_text='Slug', unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
