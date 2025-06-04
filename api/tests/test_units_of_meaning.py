from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from entities.models.unit_of_meaning import UnitOfMeaning
from entities.models.learning_goal import LearningGoal
from entities.models.language import Language
from django.utils import timezone
import datetime

class UnitOfMeaningTests(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create test language
        self.language = Language.objects.create(
            code='en',
            name='English'
        )
        
        # Create test learning goal
        self.learning_goal = LearningGoal.objects.create(
            name='Basic Greetings',
            language=self.language
        )
        
        # Create test units of meaning
        self.uom1 = UnitOfMeaning.objects.create(
            text='Hello',
            language=self.language
        )
        self.uom1.learning_goals.set([self.learning_goal])
        
        self.uom2 = UnitOfMeaning.objects.create(
            text='Goodbye',
            language=self.language
        )
        self.uom2.learning_goals.set([self.learning_goal])

    def test_list_units_of_meaning(self):
        """Test retrieving list of units of meaning"""
        url = reverse('unit-of-meaning-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_units_of_meaning_by_learning_goal(self):
        """Test filtering units of meaning by learning goal ID"""
        url = reverse('unit-of-meaning-list')
        response = self.client.get(url, {'learning_goal_id': self.learning_goal.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_units_of_meaning_by_updated_after(self):
        """Test filtering units of meaning by updated_after"""
        # Create a timestamp from 1 hour ago
        one_hour_ago = timezone.now() - datetime.timedelta(hours=1)
        
        url = reverse('unit-of-meaning-list')
        response = self.client.get(url, {'updated_after': one_hour_ago.isoformat()})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_pagination(self):
        """Test pagination of units of meaning"""
        # Create 15 units of meaning
        for i in range(13):  # 2 already exist
            uom = UnitOfMeaning.objects.create(
                text=f'Test text {i}',
                language=self.language
            )
            uom.learning_goals.set([self.learning_goal])
        
        url = reverse('unit-of-meaning-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Default page size
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_custom_page_size(self):
        """Test custom page size parameter"""
        url = reverse('unit-of-meaning-list')
        response = self.client.get(url, {'page_size': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) 