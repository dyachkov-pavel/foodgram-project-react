from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredient
import json


class Command(BaseCommand):
    help = 'Loaddata'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, path, *args, **options):
        with open(path[0]) as file:
            for item in json.load(file):
                Ingredient.objects.get_or_create(
                    title=item['title'],
                    dimension=item['dimension']
                )
