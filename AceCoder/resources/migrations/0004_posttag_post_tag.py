# Generated by Django 5.0.7 on 2024-08-21 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_alter_post_banner_alter_post_pictures'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_tag', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(to='resources.posttag'),
        ),
    ]