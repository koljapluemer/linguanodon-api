import requests
from django.core.management.base import BaseCommand
from entities.models import Language, LearningGoal, UnitOfMeaning, Translation

class Command(BaseCommand):
    help = 'Creates UnitOfMeaning, Translation, and LearningGoal objects from Tatoeba sentences'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Number of sentences to fetch and create'
        )

    def handle(self, *args, **options):
        # Get or create languages
        arz_language, _ = Language.objects.get_or_create(
            name="Egyptian Arabic",
            defaults={'code': 'ar-EG'}
        )
        en_language, _ = Language.objects.get_or_create(
            name="English",
            defaults={'code': 'en'}
        )

        # Base URL for the Tatoeba API
        base_url = "https://api.dev.tatoeba.org/unstable/sentences"
        
        # Parameters for the request
        params = {
            'lang': 'arz',  # Egyptian Arabic
            'trans:lang': 'eng',  # English translations
            'trans:is_direct': 'no',  # Include indirect translations
            'sort': 'random',  # Random order
            'limit': options['limit'],  # Number of sentences to fetch
            'showtrans': 'eng'  # Show English translations in the response
        }

        try:
            # Make the API request
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            response_data = response.json()
            sentences = response_data.get('data', [])
            
            # Print the results
            self.stdout.write(self.style.SUCCESS(f'Found {len(sentences)} sentences'))
            
            created_count = 0
            for sentence in sentences:
                arz_text = sentence['text']
                
                # Create UnitOfMeaning
                unit, created = UnitOfMeaning.objects.get_or_create(
                    based_on_meaning=f"arz: {arz_text}"
                )
                
                if created:
                    # Create Egyptian Arabic Translation
                    Translation.objects.create(
                        text=arz_text,
                        language=arz_language,
                        unit_of_meaning=unit,
                        creation_context="Automated Tatoeba API script",
                        license=sentence.get('license'),
                        owner=sentence.get('owner'),
                        source="Tatoeba",
                        source_link=f"https://tatoeba.org/en/sentences/show/{sentence['id']}",
                        owner_link=f"https://tatoeba.org/en/user/profile/{sentence.get('owner', '')}" if sentence.get('owner') else None
                    )
                    
                    # Create English Translation if available
                    translations = sentence.get('translations', [])
                    if translations and len(translations) > 0:
                        direct_translations = translations[0]  # First list contains direct translations
                        for trans in direct_translations:
                            if trans.get('lang') == 'eng':
                                Translation.objects.create(
                                    text=trans['text'],
                                    language=en_language,
                                    unit_of_meaning=unit,
                                    creation_context="Automated Tatoeba API script",
                                    license=trans.get('license'),
                                    owner=trans.get('owner'),
                                    source="Tatoeba",
                                    source_link=f"https://tatoeba.org/en/sentences/show/{trans['id']}",
                                    owner_link=f"https://tatoeba.org/en/user/profile/{trans.get('owner', '')}" if trans.get('owner') else None
                                )
                    
                    # Create LearningGoal
                    LearningGoal.objects.create(
                        name=f"arz: Understand {arz_text}",
                        language=arz_language
                    )
                    
                    created_count += 1
                    self.stdout.write(f'Created data for: {arz_text}')
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created data for {created_count} sentences'))
                
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error fetching data from Tatoeba API: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc())) 