# Generated by Django 5.2 on 2025-04-27 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_resetuserpasswordcode_attempts_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="resetuserpasswordcode",
            name="is_password_reset",
            field=models.BooleanField(default=False),
        ),
    ]
