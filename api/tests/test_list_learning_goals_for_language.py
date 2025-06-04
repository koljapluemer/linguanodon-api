import json
import os
from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command

class TestListLearningGoalsForLanguage(TestCase):
    def setUp(self):
        # Load fixture using absolute path
        fixture_path = os.path.join(os.path.dirname(__file__), 'test_list_learning_goals_for_language_fixture.json')
        call_command('loaddata', fixture_path)
            
        # Load expected response
        expected_response_path = os.path.join(os.path.dirname(__file__), 'test_list_learning_goals_for_language_expected_response.json')
        with open(expected_response_path) as f:
            self.expected_response = json.load(f)

    def test_list_learning_goals_for_language(self):
        url = reverse('list_learning_goals_for_language', kwargs={'language_code': 'en'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.expected_response)