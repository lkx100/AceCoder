# Generated by Django 5.0.7 on 2024-10-01 15:39

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("discuss", "0002_category_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name="Text"),
        ),
    ]
