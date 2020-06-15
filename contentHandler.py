import tweepy
import random
import requests
from PIL import Image
import binascii
import io
from secret_constants import *
from bs4 import BeautifulSoup
import json
from string import digits
import re

MAX_LENGTH = 280

auth_handler = tweepy.OAuthHandler(API_KEY, SEC_KEY)
auth_handler.set_access_token(TOKEN, SEC_TOKEN)
api = tweepy.API(auth_handler)


def poetrydb(endpoint):
	try:
		# get random poem from api
		resp = requests.get(endpoint)
		poem = json.loads(resp.content)
		
		# get indiv fields
		title = poem.get('title')
		author = poem.get('author')
		text = "\n".join(poem.get('lines'))
		
		# prepare tweet text and adjust length
		addons = 8
		cut_index = MAX_LENGTH - len(author) - len(title) - addons
		tt = text[:cut_index]
		tweet_text = "{0}\n{1}...\nby {2}".format(title, tt, author)
		
		api.update_status(tweet_text)
	except Exception as e:
		print(str(e))
		return str(e)


def poetryloc(endpoint):
	try:
		# get list of all poem links
		resp = requests.get(endpoint)
		soup = BeautifulSoup(resp.content, 'html.parser')
		anchor_list = soup.find('table').find_all('a')
		html_list = [item.get('href') for item in anchor_list]

		# create url of specific poem by adding the random choice of poem link
		html_choice = random.choice(html_list)
		poem_url = "http://www.loc.gov/poetry/180/{0}".format(html_choice)

		poem_page = requests.get(poem_url)
		soup = BeautifulSoup(poem_page.content, 'html.parser')
		content = soup.find('div', attrs={'class': 'section_intro'}).text

		# remove poem title, which is always the first line
		tweet_text = content[content.index('\n'):]

		if len(tweet_text) > MAX_LENGTH:
			#author is always last line of the content
			author = tweet_text.split('\n')[-1]
			info = "Full poem: {0}".format(poem_url)
			cut_index = MAX_LENGTH - len(author) - len(info) - 3
			tweet_text = "{0}\n{1}\n{2}".format(tweet_text[:cut_index], author, info)

		api.update_status(tweet_text)
	except Exception as e:
		print(str(e))
		return str(e)


def boredpanda(endpoint):
	try:
		resp = requests.get(endpoint)
		
		# find all joke containers
		soup = BeautifulSoup(resp.content, 'html.parser')
		joke_list = soup.find_all('span', attrs={'class': 'bordered-description'})

		# select a random joke out of the list
		joke_choice = random.choice(joke_list)
		joke_choice = joke_choice.text
		
		if len(joke_choice) > MAX_LENGTH:
			joke_choice = joke_choice[:MAX_LENGTH]

		api.update_status(joke_choice)
	except Exception as e:
		print(str(e))
		return str(e)	


def countryliving(endpoint):
	try:
		resp = requests.get(endpoint)

		soup = BeautifulSoup(resp.content, 'html.parser')
		joke_list = soup.find('div', attrs={'class': 'article-body-content'}).find_all('li')

		joke_choice = random.choice(joke_list)
		joke_choice = joke_choice.text
		
		if len(joke_choice) > MAX_LENGTH:
			joke_choice = joke_choice[:MAX_LENGTH]

		api.update_status(joke_choice)
	except Exception as e:
		print(str(e))
		return str(e)


def create_image_file(content, form="png"):
	try:
		stream = io.BytesIO(content)
		img = Image.open(stream)
		image_name = 'mypic.{}'.format(form)
		img.save(image_name)
		return image_name
	except Exception as e:
		print(str(e))
		return None


def unsplash(endpoint):
	try:
		response = requests.get(endpoint)
		content = json.loads(response.content.decode('ascii'))
		
		description = content.get('description')
		if description is None: 
			description = content.get('alt_description')
		
		pic_url = content['urls']['regular']

		image_response = requests.get(pic_url)
		image_name = create_image_file(image_response.content)
		
		if image_name is None:
			image_name = create_image_file(image_response.content, form = 'jpg')

		media = api.media_upload(image_name)
		api.update_status(status=description, media_ids=[media.media_id])
	except Exception as e:
		print(str(e))
		return str(e)


def metmuseum(endpoint):
	try:
		# get list of object ids
		response = requests.get(endpoint)
		content = json.loads(response.content)

		#choose random id and create url of object 
		object_ids = content.get("objectIDs")
		chosen_id = random.choice(object_ids)
		object_url = endpoint + "/"+str(chosen_id)

		# get object data
		object_response = requests.get(object_url)
		object_content = json.loads(object_response.content)

		# get key date from the object
		image_url = object_content.get('primaryImage')
		title = object_content.get('title')
		department = object_content.get('department')
		date = object_content.get('objectDate')
		if image_url:
			image_response = requests.get(image_url)
			image_name = create_image_file(image_response.content, form='jpg')
			media = api.media_upload(image_name)
			tweet_text = "title: {0}\ndepartment: {1}\ndate: {2}".format(title, department, date)
			api.update_status(status=tweet_text, media_ids=[media.media_id])
		else:
			tweet_text = "title: {0}\ndepartment: {1}\ndate: {2}\nImage not available".format(title, department, date)
			api.update_status(status=tweet_text)
	except Exception as e:
		print(str(e))
		return str(e)


def everydaypower(endpoint):
	try:
		resp = requests.get(endpoint)

		# get all paragraphs in the container
		soup = BeautifulSoup(resp.content, 'html.parser')
		paragraph_list = soup.find('div', attrs={'id': 'mvp-content-main'}).find_all('p')

		# get all quotes (i.e. the paragraph that have a number at the beginning)
		quote_list = [x.text for x in paragraph_list if (len(x.text) > 0 and x.text[0].isdigit())]
		final_list = []

		# remove number and . at the beginning
		for item in quote_list:
			remove_digits = str.maketrans('', '', digits)
			res = item.translate(remove_digits)
			res = res[2:]
			final_list.append(res)

		quote = random.choice(final_list)

		if len(quote) > MAX_LENGTH:
			quote = quote[:275] + "..."

		api.update_status(quote)
	except Exception as e:
		print(str(e))
		return str(e)


def brainyquote(endpoint):
	try:
		# get all paragrams where the quotes are
		resp = requests.get(endpoint)
		soup = BeautifulSoup(resp.content, 'html.parser')
		paragraph_list = soup.find_all('div', attrs={'class': 'clearfix'})
		
		# get actual quotes and remove white spaces
		quote_list = [x.text.strip() for x in paragraph_list]
		quote = random.choice(quote_list)

		api.update_status(quote)
	except Exception as e:
		print(str(e))
		return str(e)


def letsgetsciencey(endpoint):
	try:
		# get all cards where facts are kept, then get the list of facts
		resp = requests.get(endpoint)
		soup = BeautifulSoup(resp.content, 'html.parser')
		paragraph_list = soup.find('div', attrs={'class': "et_builder_inner_content"}).find_all('div', attrs={'class': 'article-fact'})
		fact_list = [x.find('p').text for x in paragraph_list]

		fact = random.choice(fact_list)
		
		#if fact is long than Twitter's max characters
		if len(fact) > MAX_LENGTH:
			info = "full list: {0}".format(endpoint)
			cut_index = MAX_LENGTH - len(info) - 5
			fact = fact[:cut_index]
			fact = "{0}...\n{1}".format(fact, info)

		api.update_status(fact)
	except Exception as e:
		print(str(e))
		return str(e)


def nasa(endpoint):
	try:
		response = requests.get(endpoint)
		content = json.loads(response.content)
		image_url = content.get('url')

		image_response = requests.get(image_url)
		image_name = create_image_file(image_response.content, form='jpg')

		media = api.media_upload(image_name)
		text = content.get('explanation')

		if len(text) > MAX_LENGTH:
			text = text[:275] + "..."

		api.update_status(status = text, media_ids=[media.media_id])
	except Exception as e:
		print(str(e))
		return str(e)


def thefactsite(endpoint):
	try:
		resp = requests.get(endpoint)
		soup = BeautifulSoup(resp.content, 'html.parser')
		elements = soup.find('div', attrs={'class': "entry-content"}).find_all(re.compile('^[hp]'))
		elements = elements[8:]
		elements = [x for x in elements if len(x.text) > 0]
		
		fact = ""
		fact_list = []
		for item in elements:
			if item.name == 'h2':
				fact_list.append(fact)
				fact = item.text+"\n"
			elif item.name == 'p':
				fact += " "+item.text

		fact_list = fact_list[1:]

		fact = random.choice(fact_list)

		if len(fact) > MAX_LENGTH:
			fact = fact[:275] + "..."

		api.update_status(fact)
	except Exception as e:
		print(str(e))
		return str(e)


def orleansmarketing(endpoint):
	try:
		resp = requests.get(endpoint)

		soup = BeautifulSoup(resp.content, 'html.parser')
		elements = soup.find('ol').find_all('li')

		fact_list = [x.text for x in elements]
		fact = random.choice(fact_list)

		api.update_status(fact)

	except Exception as e:
		print(str(e))
		return str(e)
