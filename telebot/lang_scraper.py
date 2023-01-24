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
	

# extract common word data
def extract_meaning(word, language, configs):
	"""
	This function gets a resource from where it extracts all the essential
	data of a particular Russian or English word and returns an object containing a words
	meaning, transcription and a few usage examples.
	"""

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


# extract an audio of the word
def extract_audio(word, configs):
	"""
	This function gets a source of the English word
	and returns its pronunciation.
	"""

	# get a soup
	soup = get_soup(configs['English']['pronunciation']['source'] + word)

	# # fetch an audio from the html

	# returns None by default
	voice = None

	# look up the html document to get objects
	list_of_sources = soup.find_all(configs['English']['pronunciation']['voice']['tag'])
	current_attr = configs['English']['pronunciation']['voice']['attr']
	current_attr_value = configs['English']['pronunciation']['voice']['attr_value']
	location_attr = configs['English']['pronunciation']['voice']['address']

	for s in list_of_sources:
		if current_attr in s.attrs:
			if s[current_attr] == current_attr_value:
				if location_attr in s.attrs:
					voice = s[location_attr]
					break

	return voice
