import json
import os
from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command

class TestGetUnitOfMeaning(TestCase):
    def setUp(self):
        # Load fixture using absolute path
        fixture_path = os.path.join(os.path.dirname(__file__), 'test_get_unit_of_meaning_fixture.json')
        call_command('loaddata', fixture_path)
            
        # Load expected response
        expected_response_path = os.path.join(os.path.dirname(__file__), 'test_get_unit_of_meaning_expected_response.json')
        with open(expected_response_path) as f:
            self.expected_response = json.load(f)

    def test_get_unit_of_meaning(self):
        url = reverse('get_unit_of_meaning', kwargs={'unit_of_meaning_id': 1})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.expected_response) 