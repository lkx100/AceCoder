# Generated by Django 5.0.7 on 2024-09-14 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_contestperformance_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestperformance',
            name='contests_participated',
        ),
        migrations.RemoveField(
            model_name='contestperformance',
            name='date',
        ),
        migrations.RemoveField(
            model_name='contestperformance',
            name='plagarisms',
        ),
        migrations.RemoveField(
            model_name='contestperformance',
            name='stars',
        ),
    ]