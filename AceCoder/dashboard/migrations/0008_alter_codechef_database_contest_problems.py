# Generated by Django 5.0.1 on 2024-08-21 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_codechef_database_contest_problems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codechef_database',
            name='contest_problems',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]