# Generated by Django 5.0.4 on 2024-04-11 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='updated_at',
        ),
    ]