import os

import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings

from part.models import Part


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--file',
                            type=str,
                            default=os.path.join('part', 'data', 'all.pkl'),
                            help='Path to .pickle file to parse')
        parser.add_argument('--delete_all',
                            type=bool,
                            default=False,
                            help='Delete all records')

    def parse_categories(self):
        df = pd.read_csv(os.path.join(
            settings.BASE_DIR, 'part', 'data', 'categories.csv'))
        df = df.rename(columns={"Статья": "clause", "Категория": "category"})
        return df.dropna().set_index('clause').T.to_dict()

    def handle(self, *args, **options):
        df = pd.read_pickle(os.path.join(
            settings.BASE_DIR, options['file']))
        df = df.where((pd.notnull(df)), None).drop(columns=['clause'])
        categories = self.parse_categories()

        obj_to_create = []
        if options['delete_all']:
            Part.objects.all().delete()

        years = set(df.year.values.tolist())
        for year in years:
            parts = set(df[(df['year'] == year)].part.values.tolist())
            for part in parts:
                parameters = df[(df['year'] == year) & (df['part'] == part)]
                year = pd.Series(parameters.iloc[0,]).year
                name = pd.Series(parameters.iloc[0,])['name']
                category = categories.get(part, {}).get('category', None)
                params = {}
                for index, row in parameters.iterrows():
                    params[row.parameter] = row.value
                obj_to_create.append(
                    Part(year=year, part=part, name=name, parameters=params, category=category))

        Part.objects.bulk_create(obj_to_create)
