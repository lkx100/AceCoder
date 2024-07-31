# Generated by Django 5.0.7 on 2024-07-30 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('roll_no', models.CharField(max_length=10)),
                ('department', models.CharField(choices=[('Ai&Ds', 'Ai&Ds'), ('CSE', 'CSE'), ('ECE', 'ECE')], max_length=5)),
                ('year', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1)),
                ('sections', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], max_length=1)),
            ],
        ),
    ]