import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag
from users.models import CustomUser


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="file path")

    def handle(self, *args, **options):
        file_path = options["path"]

        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
            if 'measurement_unit' in data[0]:
                for item in data:
                    Ingredient.objects.create(
                        name=item['name'],
                        measurement_unit=item['measurement_unit']
                    )
            elif 'color' in data[0]:
                for item in data:
                    Tag.objects.create(
                        name=item['name'],
                        color=item['color'],
                        slug=item['slug'],
                    )
            elif 'password' in data[0]:
                for item in data:
                    CustomUser.objects.create(
                        email=item['email'],
                        username=item['username'],
                        first_name=item['first_name'],
                        password=item['password'],
                        last_name=item['last_name'],

                    )
