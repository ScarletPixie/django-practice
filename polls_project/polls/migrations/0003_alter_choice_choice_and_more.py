# Generated by Django 5.1.3 on 2024-12-02 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_choice_choice_alter_question_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice',
            field=models.CharField(max_length=100),
        ),
        migrations.AddConstraint(
            model_name='choice',
            constraint=models.UniqueConstraint(fields=('question', 'choice'), name='unique_choice_per_question'),
        ),
    ]
