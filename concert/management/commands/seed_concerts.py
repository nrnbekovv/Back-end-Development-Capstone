from datetime import date
from django.core.management.base import BaseCommand
from concert.models import Concert
class Command(BaseCommand):
    help='Create the sample band tour schedule without overwriting existing concerts'
    def handle(self,*args,**kwargs):
        for name,city,day in [('Djirection: Northern Lights','London',date(2027,3,12)),('Djirection: Homecoming','Dublin',date(2027,3,20)),('Djirection: Summer Sound','Manchester',date(2027,6,5))]:
            Concert.objects.get_or_create(concert_name=name,defaults={'city':city,'date':day,'duration':2})
        self.stdout.write(self.style.SUCCESS('Concert schedule ready.'))
