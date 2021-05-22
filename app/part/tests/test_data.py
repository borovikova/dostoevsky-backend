import os
import json

from django.conf import settings
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

from part.models import Part


class DataTests(TestCase):
    """Test if data were parsed correctly by fill_db command using sample data for 2019 for clause 105ч.1"""

    def test_data_parsing(self):
        call_command('fill_db', file=os.path.join(settings.BASE_DIR, 'part', 'tests', 'test_files', 'test_data.pkl'))
        parts = Part.objects.all()
        self.assertEqual(len(parts), 1)
        part = parts[0]
        self.assertEqual(part.year, 2019)
        self.assertEqual(part.name, 'Убийство')
        self.assertEqual(part.part, '105ч.1')
        self.assertEqual(part.category, 'в результате совершения которых возможна смерть потерпевших')

        with open(os.path.join(settings.BASE_DIR, 'part', 'tests', 'test_files', 'test_params.json'), 'r') as f:
            test_params = json.load(f)

        self.assertEqual(part.parameters, test_params)
