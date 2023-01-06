from django.db import connection, migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("database", "0093_add_auto_number_to_webhook_log"),
    ]

    operations = [
        migrations.AddField(
            model_name="field",
            name="api_name",
            field=models.CharField(max_length=255, default=""),
        ),
        migrations.AddField(
            model_name="table",
            name="api_name",
            field=models.CharField(max_length=255, default=""),
        ),
    ]
