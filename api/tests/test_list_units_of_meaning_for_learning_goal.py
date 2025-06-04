import json
import os
from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command

class TestListUnitsOfMeaningForLearningGoal(TestCase):
    def setUp(self):
        # Load fixture using absolute path
        fixture_path = os.path.join(os.path.dirname(__file__), 'test_list_units_of_meaning_for_learning_goal_fixture.json')
        call_command('loaddata', fixture_path)
            
        # Load expected response
        expected_response_path = os.path.join(os.path.dirname(__file__), 'test_list_units_of_meaning_for_learning_goal_expected_response.json')
        with open(expected_response_path) as f:
            self.expected_response = json.load(f)

    def test_list_units_of_meaning_for_learning_goal(self):
        # Given
        learning_goal_id = 1
        url = reverse('list_units_of_meaning_for_learning_goal', kwargs={'learning_goal_id': learning_goal_id})

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.expected_response) 