from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import re
from entities.models import LearningGoal, UnitOfMeaning

MAX_SENTENCES = 10  # Limit the number of sentences to scrape
SLEEP_TIME = 1  # Sleep time between requests in seconds
WORD_CLICK_WAIT = 0.3  # Wait time after clicking a word

class Command(BaseCommand):
    help = 'Scrape example sentences from Lisaan Masry and create learning data'

    def setup_driver(self):
        options = FFOptions()
        # options.add_argument('--headless')  # Uncomment to run in headless mode
        service = Service(executable_path='/snap/bin/geckodriver')
        driver = webdriver.Firefox(service=service, options=options)
        return driver

    def wait_for_element(self, driver, by, value, timeout=10):
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def get_sentence_number(self, driver):
        try:
            td = self.wait_for_element(driver, By.XPATH, "//td[contains(text(), 'example')]")
            match = re.search(r'example (\d+) of', td.text)
            if match:
                return match.group(1)
        except (NoSuchElementException, TimeoutException):
            pass
        return None

    def get_word_info(self, driver):
        try:
            # Get element type
            element_tr = self.wait_for_element(driver, By.XPATH, "//tr[contains(., 'Element:')]")
            word_base_type = element_tr.find_element(By.XPATH, ".//td[2]").text

            # Get language
            lang_tr = self.wait_for_element(driver, By.XPATH, "//tr[contains(., 'Language:')]")
            lang_td = lang_tr.find_element(By.XPATH, ".//td[2]").text
            word_lang = "arb" if lang_td == "MS" else "arz"

            return word_base_type, word_lang
        except (NoSuchElementException, TimeoutException):
            return None, None

    def process_word_forms(self, driver, word_lang, word_base_type, sentence_learning_goal):
        forms = []
        try:
            forms_table = self.wait_for_element(driver, By.XPATH, "//h1[text()='Forms']/following-sibling::table[1]")
            rows = forms_table.find_elements(By.TAG_NAME, "tr")
            
            # First create all forms to have references for similar_but_not_synonyms
            for row in rows:
                try:
                    td2 = row.find_element(By.XPATH, ".//td[2]")
                    form_transliteration = td2.find_element(By.TAG_NAME, "b").text
                    try:
                        form_type = td2.find_element(By.TAG_NAME, "i").text
                    except NoSuchElementException:
                        form_type = ""
                    
                    td3 = row.find_element(By.XPATH, ".//td[3]")
                    form_arabic = td3.text

                    # Create learning goal for first form only
                    if row == rows[0]:
                        word_learning_goal, created = LearningGoal.objects.get_or_create(
                            language_code="arz",
                            name=form_arabic,
                            defaults={'description': ''}
                        )
                        if created:
                            word_learning_goal.parents.set([sentence_learning_goal])
                    else:
                        word_learning_goal = None

                    # Create UnitOfMeaning for the form
                    uom, created = UnitOfMeaning.objects.get_or_create(
                        text=form_arabic,
                        language_code=word_lang,
                        type_info=f"{word_base_type} {form_type}".strip(),
                        defaults={
                            'pronunciation': form_transliteration,
                            'creation_context': "Lisaan Masry Script",
                            'license': "Copyright © 2007-2020 Mike Green — non-commercial use",
                            'owner': "Lisaan Masry",
                            'owner_link': "https://eu.lisaanmasry.org/info/en/copyright.html",
                            'source': "Lisaan Masry Examples",
                            'source_link': "https://eu.lisaanmasry.org/online/example.php"
                        }
                    )
                    if word_learning_goal:
                        uom.learning_goals.add(word_learning_goal)
                    
                    forms.append(uom)
                except (NoSuchElementException, StaleElementReferenceException):
                    continue

            # Now update similar_but_not_synonyms for all forms
            for form in forms:
                form.similar_but_not_synonyms.set([f for f in forms if f != form])

            return forms
        except (NoSuchElementException, TimeoutException):
            return []

    def process_word_meanings(self, driver, forms):
        meanings = []
        try:
            meanings_table = self.wait_for_element(driver, By.XPATH, "//h1[text()='Meanings']/following-sibling::table[1]")
            rows = meanings_table.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                try:
                    td2 = row.find_element(By.XPATH, ".//td[2]")
                    form_en = td2.find_element(By.TAG_NAME, "a").text
                    
                    try:
                        form_type = td2.find_element(By.TAG_NAME, "i").text
                    except NoSuchElementException:
                        form_type = None
                    
                    # Get text between <a> and <i> if it exists
                    form_note = None
                    if form_type:
                        text_parts = td2.text.split(form_en)
                        if len(text_parts) > 1:
                            form_note = text_parts[1].split(form_type)[0].strip()

                    uom, created = UnitOfMeaning.objects.get_or_create(
                        text=form_en,
                        language_code="en",
                        type_info=form_type,
                        defaults={
                            'notes': form_note,
                            'creation_context': "Lisaan Masry Script",
                            'license': "Copyright © 2007-2020 Mike Green — non-commercial use",
                            'owner': "Lisaan Masry",
                            'owner_link': "https://eu.lisaanmasry.org/info/en/copyright.html",
                            'source': "Lisaan Masry Examples",
                            'source_link': "https://eu.lisaanmasry.org/online/example.php"
                        }
                    )
                    
                    # Add translations and synonyms
                    uom.translations.set(forms)
                    meanings.append(uom)
                    
                except (NoSuchElementException, StaleElementReferenceException):
                    continue

            # Add synonyms between meanings
            for meaning in meanings:
                meaning.synonyms.set([m for m in meanings if m != meaning])

            return meanings
        except (NoSuchElementException, TimeoutException):
            return []

    def process_word(self, driver, span, sentence_learning_goal):
        try:
            # Get the word text before clicking
            word_text = span.text
            
            # Click the word and wait for the page to update
            span.click()
            time.sleep(WORD_CLICK_WAIT)  # Wait for dynamic content to load
            
            # Wait for the word details to appear
            self.wait_for_element(driver, By.ID, "word")
            
            sentence_number = self.get_sentence_number(driver)
            word_base_type, word_lang = self.get_word_info(driver)
            
            if not word_base_type or not word_lang:
                return
            
            forms = self.process_word_forms(driver, word_lang, word_base_type, sentence_learning_goal)
            if forms:
                self.process_word_meanings(driver, forms)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing word "{word_text}": {str(e)}'))

    def scrape_sentence(self, driver, url):
        try:
            driver.get(url)
            self.stdout.write('Page loaded, waiting for content...')
            
            # Wait for any content to be present
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                self.stdout.write('Body element found')
            except TimeoutException:
                self.stdout.write(self.style.ERROR('Timeout waiting for body element'))
                return None

            # Debug: Print all div IDs on the page
            self.stdout.write('Available div IDs:')
            for div in driver.find_elements(By.TAG_NAME, "div"):
                div_id = div.get_attribute("id")
                if div_id:
                    self.stdout.write(f'- {div_id}')

            # Wait for the example div to be present
            try:
                example_div = self.wait_for_element(driver, By.ID, "example")
                self.stdout.write('Example div found')
            except TimeoutException:
                self.stdout.write(self.style.ERROR('Timeout waiting for example div'))
                self.stdout.write('Page source:')
                self.stdout.write(driver.page_source[:1000])  # Print first 1000 chars of page source
                return None

            # Find the Arabic sentence
            try:
                arz_p = example_div.find_element(By.CSS_SELECTOR, "p[class='ar']")
                sentence_arz = arz_p.text.strip()
                self.stdout.write(f'Found Arabic sentence: {sentence_arz}')
            except NoSuchElementException:
                self.stdout.write(self.style.ERROR('Could not find Arabic sentence'))
                self.stdout.write(self.style.WARNING('Available p tags in example div:'))
                for p in example_div.find_elements(By.TAG_NAME, "p"):
                    self.stdout.write(f'- Class: {p.get_attribute("class")}, Text: {p.text[:100]}')
                return None

            # Find the transliteration
            self.stdout.write('Looking for transliteration...')
            transliteration_p = None
            for p in example_div.find_elements(By.TAG_NAME, "p"):
                p_text = p.text
                self.stdout.write(f'Checking p tag with text: {p_text[:100]}')
                if 'Individual words:' in p_text:
                    transliteration_p = p
                    self.stdout.write('Found transliteration paragraph')
                    break
            
            if not transliteration_p:
                self.stdout.write(self.style.ERROR('Could not find transliteration'))
                self.stdout.write(self.style.WARNING('Available p tags in example div:'))
                for p in example_div.find_elements(By.TAG_NAME, "p"):
                    self.stdout.write(f'- Text: {p.text[:100]}')
                return None
                
            sentence_transliteration = transliteration_p.text.replace('Individual words:', '').strip()
            self.stdout.write(f'Found transliteration: {sentence_transliteration}')

            # Find the English translation
            self.stdout.write('Looking for English translation...')
            try:
                translation_h3 = example_div.find_element(By.XPATH, ".//h3[text()='Translation']")
                self.stdout.write('Found translation heading')
                sentence_en = translation_h3.find_element(By.XPATH, "following-sibling::p[1]").text.strip()
                self.stdout.write(f'Found English translation: {sentence_en}')
            except NoSuchElementException:
                self.stdout.write(self.style.ERROR('Could not find translation heading'))
                self.stdout.write(self.style.WARNING('Available h3 tags in example div:'))
                for h3 in example_div.find_elements(By.TAG_NAME, "h3"):
                    self.stdout.write(f'- Text: {h3.text}')
                return None

            # Find sentence notes
            self.stdout.write('Looking for sentence notes...')
            sentence_notes = ''
            try:
                notes_h3 = example_div.find_element(By.XPATH, ".//h3[text()='Notes']")
                self.stdout.write('Found notes heading')
                notes_p = notes_h3.find_element(By.XPATH, "following-sibling::p[1]")
                sentence_notes = notes_p.text.strip()
                self.stdout.write(f'Found notes: {sentence_notes}')
            except NoSuchElementException:
                self.stdout.write('No notes found (this is optional)')
                pass  # Notes are optional

            # Create LearningGoal for the sentence
            self.stdout.write('Creating learning goal...')
            learning_goal = LearningGoal.objects.create(
                name=sentence_arz,
                description='',
                language_code='arz'
            )
            self.stdout.write('Learning goal created')

            # Create UnitOfMeaning for Arabic sentence
            self.stdout.write('Creating Arabic UnitOfMeaning...')
            arz_uom = UnitOfMeaning.objects.create(
                text=sentence_arz,
                language_code='arz',
                pronunciation=sentence_transliteration,
                notes=sentence_notes,
                creation_context='Lisaan Masry Script',
                license='Copyright © 2007-2020 Mike Green — non-commercial use',
                owner='Lisaan Masry',
                owner_link='https://eu.lisaanmasry.org/info/en/copyright.html',
                source='Lisaan Masry Examples',
                source_link='https://eu.lisaanmasry.org/online/example.php'
            )
            arz_uom.learning_goals.add(learning_goal)
            self.stdout.write('Arabic UnitOfMeaning created')

            # Create UnitOfMeaning for English sentence
            self.stdout.write('Creating English UnitOfMeaning...')
            en_uom = UnitOfMeaning.objects.create(
                text=sentence_en,
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
            self.stdout.write('English UnitOfMeaning created')

            # Process individual words
            self.stdout.write('Processing individual words...')
            word_spans = arz_p.find_elements(By.TAG_NAME, "span")
            self.stdout.write(f'Found {len(word_spans)} word spans')
            
            # Process each word by index
            for i in range(len(word_spans)):
                try:
                    # Get fresh reference to the paragraph and spans
                    arz_p = example_div.find_element(By.CSS_SELECTOR, "p[class='ar']")
                    spans = arz_p.find_elements(By.TAG_NAME, "span")
                    if i >= len(spans):
                        self.stdout.write(self.style.WARNING(f'Index {i} out of range, skipping'))
                        continue
                        
                    span = spans[i]
                    word_text = span.text
                    self.stdout.write(f'Processing word {i+1} of {len(word_spans)}: {word_text}')
                    
                    # Click the span
                    span.click()
                    time.sleep(WORD_CLICK_WAIT)  # Wait for dynamic content to load
                    
                    # Wait for the word details to appear
                    try:
                        self.wait_for_element(driver, By.ID, "word")
                    except TimeoutException:
                        self.stdout.write(self.style.ERROR(f'Timeout waiting for word details for word {i+1}'))
                        continue
                    
                    sentence_number = self.get_sentence_number(driver)
                    word_base_type, word_lang = self.get_word_info(driver)
                    
                    if not word_base_type or not word_lang:
                        self.stdout.write(self.style.WARNING(f'Skipping word {i+1} - no type or language info'))
                        continue
                    
                    forms = self.process_word_forms(driver, word_lang, word_base_type, learning_goal)
                    if forms:
                        self.process_word_meanings(driver, forms)
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing word {i+1}: {str(e)}'))
                    continue

            return {
                'sentence_arz': sentence_arz,
                'sentence_transliteration': sentence_transliteration,
                'sentence_en': sentence_en,
                'sentence_notes': sentence_notes
            }

        except TimeoutException as e:
            self.stdout.write(self.style.ERROR(f'Timeout waiting for page to load: {str(e)}'))
            return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {str(e)}'))
            return None

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

                self.stdout.write(self.style.SUCCESS(f'Successfully created learning data for sentence: {data["sentence_arz"]}'))
                
                sentences_processed += 1
                if sentences_processed < MAX_SENTENCES:
                    self.stdout.write(f'Sleeping for {SLEEP_TIME} seconds before next request...')
                    time.sleep(SLEEP_TIME)
        finally:
            driver.quit()
