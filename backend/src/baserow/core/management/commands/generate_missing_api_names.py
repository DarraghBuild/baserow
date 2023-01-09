from django.core.management.base import BaseCommand

from baserow.contrib.database.table.handler import generate_table_api_name
from baserow.contrib.database.table.models import Table

from baserow.contrib.database.fields.handler import generate_field_api_name
from baserow.contrib.database.fields.models import Field

class Command(BaseCommand):
    help = "Generate API names for all tables and fields that don't have one."

    def handle(self, *args, **options):
        for table in Table.objects.iterator():
            if not table.api_name:
                table.api_name = generate_table_api_name(table.name)
                table.save()
        
        for field in Field.objects.iterator():
            if not field.api_name:
                field.api_name = generate_field_api_name(field.name, table)
                field.save()
