import csv

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from phones.models import Phone
from datetime import datetime


import requests

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            if Phone.objects.filter(pk=phone.get('id')).exists():
                print("Record exists")
            else:
                release_date = datetime.strptime( phone.get('release_date'), '%Y-%m-%d').date()
                phone_obj = Phone(
                    id = phone.get('id'),
                    name = phone.get('name'),
                    price = phone.get('price'),
                    release_date = release_date,
                    lte_exists = phone.get('lte_exists'),
                )

                url = phone.get('image')
                response = requests.get(url)
                filename = 'phone.jpg'

                if response.status_code == 200:
                    content = ContentFile(response.content)
                    phone_obj.image.save(filename, content, save=True)
                phone_obj.save()
                print("Record created")

