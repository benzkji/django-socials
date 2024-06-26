# Generated by Django 3.1.2 on 2020-10-21 10:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("socials", "0013_auto_20201021_1026"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image_url",
            field=models.URLField(
                blank=True, default="", max_length=256, verbose_name="Image URL"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="url",
            field=models.URLField(
                blank=True,
                default="",
                max_length=256,
                verbose_name="Post URL (permalink)",
            ),
        ),
    ]
