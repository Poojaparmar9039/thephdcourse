# Generated by Django 5.2 on 2025-05-13 07:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0002_alter_user_details_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_details',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
