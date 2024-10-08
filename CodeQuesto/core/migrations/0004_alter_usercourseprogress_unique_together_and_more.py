# Generated by Django 5.0.6 on 2024-09-23 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_lesson_content'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usercourseprogress',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='usercourseprogress',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.lesson'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name='usercourseprogress',
            unique_together={('user_profile', 'course', 'lesson')},
        ),
    ]
