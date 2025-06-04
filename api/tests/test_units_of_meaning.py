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
        # Create test languages
        self.english = Language.objects.create(
            code='en',
            name='English'
        )
        self.spanish = Language.objects.create(
            code='es',
            name='Spanish'
        )
        
        # Create test learning goal
        self.learning_goal = LearningGoal.objects.create(
            name='Basic Greetings',
            language=self.english
        )
        
        # Create test units of meaning in English
        self.uom1 = UnitOfMeaning.objects.create(
            text='Hello',
            language=self.english
        )
        self.uom1.learning_goals.set([self.learning_goal])
        
        self.uom2 = UnitOfMeaning.objects.create(
            text='Goodbye',
            language=self.english
        )
        self.uom2.learning_goals.set([self.learning_goal])

        # Create Spanish translations
        self.uom1_es = UnitOfMeaning.objects.create(
            text='Hola',
            language=self.spanish
        )
        self.uom2_es = UnitOfMeaning.objects.create(
            text='Adiós',
            language=self.spanish
        )

        # Set up translations
        self.uom1.translations.add(self.uom1_es)
        self.uom2.translations.add(self.uom2_es)

    def test_list_units_of_meaning(self):
        """Test retrieving list of units of meaning"""
        url = reverse('unit-of-meaning-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Filter results to only include English units
        english_units = [u for u in response.data['results'] if u['language'] == 'en']
        self.assertEqual(len(english_units), 2)

    def test_filter_units_of_meaning_by_learning_goal(self):
        """Test filtering units of meaning by learning goal ID"""
        url = reverse('unit-of-meaning-list')
        response = self.client.get(url, {'learning_goal_id': self.learning_goal.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Filter results to only include English units
        english_units = [u for u in response.data['results'] if u['language'] == 'en']
        self.assertEqual(len(english_units), 2)

    def test_filter_units_of_meaning_by_updated_after(self):
        """Test filtering units of meaning by updated_after"""
        # Create a timestamp from 1 hour ago
        one_hour_ago = timezone.now() - datetime.timedelta(hours=1)
        
        url = reverse('unit-of-meaning-list')
        response = self.client.get(url, {'updated_after': one_hour_ago.isoformat()})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Filter results to only include English units
        english_units = [u for u in response.data['results'] if u['language'] == 'en']
        self.assertEqual(len(english_units), 2)

    def test_pagination(self):
        """Test pagination of units of meaning"""
        # Create 13 more English units of meaning
        for i in range(13):
            uom = UnitOfMeaning.objects.create(
                text=f'Test text {i}',
                language=self.english
            )
            uom.learning_goals.set([self.learning_goal])
        
        url = reverse('unit-of-meaning-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Filter results to only include English units
        english_units = [u for u in response.data['results'] if u['language'] == 'en']
        self.assertEqual(len(english_units), 10)  # Default page size
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_custom_page_size(self):
        """Test custom page size parameter"""
        url = reverse('unit-of-meaning-list')
        response = self.client.get(url, {'page_size': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Filter results to only include English units
        english_units = [u for u in response.data['results'] if u['language'] == 'en']
        self.assertEqual(len(english_units), 1)

    def test_get_translations_for_unit_of_meaning(self):
        """Test retrieving translations for a unit of meaning in a specific language"""
        url = reverse('unit-of-meaning-translations-translations', kwargs={'pk': self.uom1.id})
        response = self.client.get(url, {'language_code': 'es'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['translations']), 1)
        self.assertEqual(response.data['translations'][0]['text'], 'Hola')
        self.assertEqual(response.data['translations'][0]['language'], 'es')

    def test_get_translations_invalid_language(self):
        """Test retrieving translations with an invalid language code"""
        url = reverse('unit-of-meaning-translations-translations', kwargs={'pk': self.uom1.id})
        response = self.client.get(url, {'language_code': 'invalid'})
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Language with code invalid does not exist')

    def test_get_translations_missing_language_code(self):
        """Test retrieving translations without providing a language code"""
        url = reverse('unit-of-meaning-translations-translations', kwargs={'pk': self.uom1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'language_code parameter is required')

    def test_get_translations_nonexistent_unit(self):
        """Test retrieving translations for a nonexistent unit of meaning"""
        url = reverse('unit-of-meaning-translations-translations', kwargs={'pk': 99999})
        response = self.client.get(url, {'language_code': 'es'})
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Unit of meaning not found') 