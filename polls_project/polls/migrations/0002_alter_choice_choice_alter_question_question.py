# Generated by Django 5.0.3 on 2024-11-29 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
