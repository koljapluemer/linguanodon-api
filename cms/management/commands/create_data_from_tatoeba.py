import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fetches Egyptian Arabic sentences and their English translations from Tatoeba API'

    def handle(self, *args, **options):
        # Base URL for the Tatoeba API
        base_url = "https://api.dev.tatoeba.org/unstable/sentences"
        
        # Parameters for the request
        params = {
            'lang': 'arz',  # Egyptian Arabic
            'trans:lang': 'eng',  # English translations
            'trans:is_direct': 'no',  # Include indirect translations
            'sort': 'random',  # Random order
            'limit': 10,  # Number of sentences to fetch
            'showtrans': 'eng'  # Show English translations in the response
        }

        try:
            # Make the API request
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            response_data = response.json()
            sentences = response_data.get('data', [])
            
            # Print the results
            self.stdout.write(self.style.SUCCESS(f'Found {len(sentences)} sentences:'))
            self.stdout.write('')
            
            for sentence in sentences:
                # Print the Egyptian Arabic sentence
                self.stdout.write(f'Egyptian Arabic: {sentence["text"]}')
                
                # Print English translations
                translations = sentence.get('translations', [])
                if translations and len(translations) > 0:
                    # The first list contains direct translations
                    direct_translations = translations[0]
                    for trans in direct_translations:
                        if trans.get('lang') == 'eng':
                            self.stdout.write(f'English: {trans.get("text", "")}')
                self.stdout.write('---')
                
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error fetching data from Tatoeba API: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {str(e)}'))
            # Print more detailed error information
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc())) 