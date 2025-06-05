from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from entities.models import LearningGoal, UnitOfMeaning

MAX_SENTENCES = 2  # Limit the number of sentences to scrape
SLEEP_TIME = 2  # Sleep time between requests in seconds

class Command(BaseCommand):
    help = 'Scrape example sentences from Lisaan Masry and create learning data'

    def setup_driver(self):
        options = FFOptions()
        # options.add_argument('--headless')  # Uncomment to run in headless mode
        service = Service(executable_path='/snap/bin/geckodriver')
        driver = webdriver.Firefox(service=service, options=options)
        return driver

    def scrape_sentence(self, driver, url):
        try:
            driver.get(url)
            # Wait for the example div to be present
            example_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "example"))
            )
            
            # Find the Arabic sentence
            try:
                arz_p = example_div.find_element(By.CSS_SELECTOR, "p.ar")
                sentence_arz = arz_p.text.strip()
            except NoSuchElementException:
                self.stdout.write(self.style.ERROR('Could not find Arabic sentence'))
                self.stdout.write(self.style.WARNING('Available p tags in example div:'))
                for p in example_div.find_elements(By.TAG_NAME, "p"):
                    self.stdout.write(f'- Class: {p.get_attribute("class")}, Text: {p.text[:100]}')
                return None

            # Find the transliteration
            transliteration_p = None
            for p in example_div.find_elements(By.TAG_NAME, "p"):
                if 'Individual words:' in p.text:
                    transliteration_p = p
                    break
            
            if not transliteration_p:
                self.stdout.write(self.style.ERROR('Could not find transliteration'))
                self.stdout.write(self.style.WARNING('Available p tags in example div:'))
                for p in example_div.find_elements(By.TAG_NAME, "p"):
                    self.stdout.write(f'- Text: {p.text[:100]}')
                return None
                
            sentence_transliteration = transliteration_p.text.replace('Individual words:', '').strip()

            # Find the English translation
            try:
                translation_h3 = example_div.find_element(By.XPATH, ".//h3[text()='Translation']")
                sentence_en = translation_h3.find_element(By.XPATH, "following-sibling::p[1]").text.strip()
            except NoSuchElementException:
                self.stdout.write(self.style.ERROR('Could not find translation heading'))
                self.stdout.write(self.style.WARNING('Available h3 tags in example div:'))
                for h3 in example_div.find_elements(By.TAG_NAME, "h3"):
                    self.stdout.write(f'- Text: {h3.text}')
                return None

            # Find sentence notes
            sentence_notes = ''
            try:
                notes_h3 = example_div.find_element(By.XPATH, ".//h3[text()='Notes']")
                notes_p = notes_h3.find_element(By.XPATH, "following-sibling::p[1]")
                sentence_notes = notes_p.text.strip()
            except NoSuchElementException:
                pass  # Notes are optional

            return {
                'sentence_arz': sentence_arz,
                'sentence_transliteration': sentence_transliteration,
                'sentence_en': sentence_en,
                'sentence_notes': sentence_notes
            }

        except TimeoutException:
            self.stdout.write(self.style.ERROR('Timeout waiting for page to load'))
            return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {str(e)}'))
            return None

    def create_learning_data(self, data):
        # Create LearningGoal
        learning_goal = LearningGoal.objects.create(
            name=data['sentence_arz'],
            description='',
            language_code='arz'
        )

        # Create UnitOfMeaning for Arabic sentence
        arz_uom = UnitOfMeaning.objects.create(
            text=data['sentence_arz'],
            language_code='arz',
            pronunciation=data['sentence_transliteration'],
            notes=data['sentence_notes'],
            creation_context='Lisaan Masry Script',
            license='Copyright © 2007-2020 Mike Green — non-commercial use',
            owner='Lisaan Masry',
            owner_link='https://eu.lisaanmasry.org/info/en/copyright.html',
            source='Lisaan Masry Examples',
            source_link='https://eu.lisaanmasry.org/online/example.php'
        )
        arz_uom.learning_goals.add(learning_goal)

        # Create UnitOfMeaning for English sentence
        en_uom = UnitOfMeaning.objects.create(
            text=data['sentence_en'],
            language_code='en',
            creation_context='Lisaan Masry Script',
            license='Copyright © 2007-2020 Mike Green — non-commercial use',
            owner='Lisaan Masry',
            owner_link='https://eu.lisaanmasry.org/info/en/copyright.html',
            source='Lisaan Masry Examples',
            source_link='https://eu.lisaanmasry.org/online/example.php'
        )
        en_uom.learning_goals.add(learning_goal)
        en_uom.translations.add(arz_uom)

        return learning_goal

    def handle(self, *args, **options):
        base_url = "https://eu.lisaanmasry.org/online/example.php"
        sentences_processed = 0

        driver = self.setup_driver()
        try:
            while sentences_processed < MAX_SENTENCES:
                self.stdout.write(f'Attempting to scrape sentence {sentences_processed + 1} of {MAX_SENTENCES}...')
                data = self.scrape_sentence(driver, base_url)
                if not data:
                    self.stdout.write(self.style.ERROR('Failed to scrape sentence, stopping...'))
                    break

                learning_goal = self.create_learning_data(data)
                self.stdout.write(self.style.SUCCESS(f'Successfully created learning data for sentence: {data["sentence_arz"]}'))
                
                sentences_processed += 1
                if sentences_processed < MAX_SENTENCES:
                    self.stdout.write(f'Sleeping for {SLEEP_TIME} seconds before next request...')
                    time.sleep(SLEEP_TIME)
        finally:
            driver.quit()
