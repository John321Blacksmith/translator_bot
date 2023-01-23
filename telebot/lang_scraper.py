import requests
import json
from bs4 import BeautifulSoup as Bs

# get a config dictionary
def decode_json_data(json_file):
	
	if json_file:
		try:
			with open(json_file, mode='r', encoding='utf-8') as j_file:
				data = json.load(j_file)
		except (FileNotFoundError, json.JSONDecodeError) as error:
			print(f'An error occurred because of: {error}')
		else:
			return data
	else:
		return None


# get a soup object
def get_soup(source):
	html = requests.get(source).text
	soup = Bs(html, 'html.parser')

	return soup
	

def extract_meaning(word, language, json_file):
	"""
	This function gets a resource from where it extracts all the essential
	data of a particular Russian word and returns an object containing a words
	meaning, transcription, pronunciation and a few usage examples.
	"""

	# get a config dictionary
	configs = decode_json_data(json_file)

	# check if the current word is in a right language
	if word[0] not in configs[language]['letters']:
		word_data = None

	else:
		# compose an actual word url
		word_url = configs[language]['source'] + word

		# get a soup
		soup = get_soup(word_url)
		
		# fetch all the pieces of word data
		word = soup.find(configs[language]['word']['tag'], configs[language]['word']['class'])
		word_type = soup.find(configs[language]['word_type']['tag'], configs[language]['word_type']['class'])
		conjugate = soup.find(configs[language]['conjugate']['tag'], configs[language]['conjugate']['class'])
		transcription = soup.find(configs[language]['transcription']['tag'], configs[language]['transcription']['class'])
		meaning = soup.find(configs[language]['meaning']['tag'], configs[language]['meaning']['class'])
		# pronunciation_section = soup.find(configs['language']['pronunciation']['tag'], configs[language]['pronunciation']['class'])
		examples = soup.find(configs[language]['examples']['tag'], configs[language]['examples']['class'])
		
		# if all the data is available
		if None not in [word, word_type, conjugate, transcription, meaning, examples]:
			# construct a word object
			word_data = {
				'word': word.text,
				'word_type': word_type.text,
				'conjugate': conjugate.text.strip(),
				'transcription': transcription.text,
				'meaning': meaning.text,
				'examples': examples.text
			}

		# if anything bad happens at scraping
		else:
			word_data = None

	return word_data