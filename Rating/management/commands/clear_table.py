from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Clears data from a specific table'

    def add_arguments(self, parser):
        parser.add_argument('table', type=str, help='Name of the table to clear')

    def handle(self, *args, **options):
        table_name = options['table']
        model = apps.get_model(table_name)

        if model:
            model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Table "{table_name}" cleared successfully.'))
        else:
            self.stdout.write(self.style.ERROR(f'Table "{table_name}" does not exist.'))

