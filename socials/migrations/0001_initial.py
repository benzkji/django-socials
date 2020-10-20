# Generated by Django 3.1.2 on 2020-10-20 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_changed', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='', max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='InstagramConfiguration',
            fields=[
                ('configuration_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='socials.configuration')),
                ('username', models.URLField(blank=True, verbose_name='Instagram Username')),
                ('app_id', models.CharField(blank=True, max_length=255, verbose_name='App ID')),
                ('app_secret', models.CharField(blank=True, max_length=255, verbose_name='App Secret')),
                ('long_token', models.CharField(blank=True, max_length=255, verbose_name='Long-lived access token')),
                ('refresh_date', models.DateTimeField(verbose_name='Last long token refresh')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
                'ordering': ['name'],
            },
            bases=('socials.configuration',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_changed', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Is visible')),
                ('originalid', models.BigIntegerField(blank=True, default=None, null=True, verbose_name='Original ID')),
                ('data', models.JSONField(blank=True, default=dict, verbose_name='Original Data')),
                ('configuration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='socials.configuration')),
            ],
            options={
                'verbose_name': 'Posts',
                'verbose_name_plural': 'Posts',
                'ordering': ['-date'],
                'unique_together': {('configuration', 'originalid')},
            },
        ),
    ]