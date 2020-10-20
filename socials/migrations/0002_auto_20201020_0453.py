# Generated by Django 3.1.2 on 2020-10-20 04:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('socials', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instagramconfiguration',
            options={'ordering': ['name'], 'verbose_name': 'Instagram Configuration', 'verbose_name_plural': 'Instagram Configurations'},
        ),
        migrations.RenameField(
            model_name='instagramconfiguration',
            old_name='long_token',
            new_name='token',
        ),
        migrations.RemoveField(
            model_name='instagramconfiguration',
            name='refresh_date',
        ),
        migrations.AddField(
            model_name='instagramconfiguration',
            name='token_refresh_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last long-lived token refresh'),
            preserve_default=False,
        ),
    ]
