# Generated by Django 3.2.13 on 2023-01-25 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0100_airtableimportjob_user_ip_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="formulafield",
            name="nullable",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
