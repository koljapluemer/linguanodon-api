from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from entities.models.learning_goal import LearningGoal
from entities.models.language import Language

class LearningGoalTests(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create test language
        self.language = Language.objects.create(
            code='en',
            name='English'
        )
        
        # Create test learning goals
        self.learning_goal1 = LearningGoal.objects.create(
            name='Basic Greetings',
            language=self.language
        )
        self.learning_goal2 = LearningGoal.objects.create(
            name='Numbers 1-10',
            language=self.language
        )

    def test_list_learning_goals(self):
        """Test retrieving list of learning goals"""
        url = reverse('learning-goal-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Get the names from the response
        names = [item['name'] for item in response.data['results']]
        # Check that both expected names are in the response
        self.assertIn('Basic Greetings', names)
        self.assertIn('Numbers 1-10', names)

    def test_filter_learning_goals_by_language(self):
        """Test filtering learning goals by language code"""
        url = reverse('learning-goal-list')
        response = self.client.get(url, {'language_code': 'en'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Get the names from the response
        names = [item['name'] for item in response.data['results']]
        # Check that both expected names are in the response
        self.assertIn('Basic Greetings', names)
        self.assertIn('Numbers 1-10', names)

    def test_filter_learning_goals_by_updated_after(self):
        """Test filtering learning goals by updated_after"""
        url = reverse('learning-goal-list')
        response = self.client.get(url, {'updated_after': '2024-01-01T00:00:00Z'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Get the names from the response
        names = [item['name'] for item in response.data['results']]
        # Check that both expected names are in the response
        self.assertIn('Basic Greetings', names)
        self.assertIn('Numbers 1-10', names)

    def test_pagination(self):
        """Test pagination of learning goals"""
        # Create 15 learning goals
        for i in range(13):  # 2 already exist
            LearningGoal.objects.create(
                name=f'Test Goal {i}',
                language=self.language
            )
        
        url = reverse('learning-goal-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Default page size
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_custom_page_size(self):
        """Test custom page size parameter"""
        url = reverse('learning-goal-list')
        response = self.client.get(url, {'page_size': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) 