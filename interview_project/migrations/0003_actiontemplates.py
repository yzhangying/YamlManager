# Generated by Django 3.0.6 on 2020-05-07 23:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('interview_project', '0002_yamls_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionTemplates',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('template_id', models.CharField(max_length=30)),
                ('template_value', models.TextField()),
                ('create_date_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-create_date_time'],
                'default_permissions': (),
            },
        ),
    ]
