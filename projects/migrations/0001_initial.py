# Generated by Django 4.1.13 on 2024-10-24 09:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('volunteers_needed', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('volunteers', models.ManyToManyField(blank=True, related_name='joined_projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]