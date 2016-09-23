
from django.core.management.base import BaseCommand, CommandError
from api import models
from experts.import_file import import_xlsx


class Command(BaseCommand):
    help = 'Import a file with GPS data'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs=1, type=str)
        parser.add_argument('name', nargs='?', default='manual', type=str)

    def handle(self, *args, **options):
            # try:
                msg = import_xlsx(file=options['file'][0],name=options['name'])
                self.stdout.write(self.style.SUCCESS('OK, imported {}'.format(options['file'][0])))

                for m in msg:
                    self.stdout.write(self.style.SUCCESS('{:>20} : {}'.format(m[0],m[1])))                    
            # except:
            #     raise CommandError('Import Error')

