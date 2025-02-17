# Generated by Django 5.0.7 on 2024-10-04 04:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("upsolve", "0005_alter_contestproblem_problem_tags"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contest",
            name="contest_problems",
        ),
        migrations.AddField(
            model_name="contestproblem",
            name="contest",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="upsolve.contest",
            ),
        ),
    ]
