from django.core.management.base import BaseCommand

from entires.models import Entry


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        entries = Entry.objects.all()
        
        for entry in entries:
            self.stdout.write("Extracting entry #%s..\n" % entry.pk)
            entry.extract_zip_file()

        self.stdout.write("Done\n")
