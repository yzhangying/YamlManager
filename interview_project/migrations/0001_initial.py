# Generated by Django 3.0.6 on 2020-05-05 15:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('create_date_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-create_date_time'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Yamls',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('template_id', models.CharField(max_length=30)),
                ('create_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('args', models.CharField(max_length=400)),
            ],
            options={
                'ordering': ['-create_date_time'],
                'default_permissions': (),
            },
        ),
    ]