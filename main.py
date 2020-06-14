import tweepy
import datetime
import random
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import requests
from PIL import Image
from PIL import ImageDraw
import binascii
import io
from constants import *
import contentHandler

auth_handler = tweepy.OAuthHandler(API_KEY, SEC_KEY)
auth_handler.set_access_token(TOKEN, SEC_TOKEN)
api = tweepy.API(auth_handler)

class TwitterBot:
	def __init__(self):
		self.topics = ['poetry', 'comedy', 'art', 'sports', 'entertainment', 'science', 'technology']
		self.content_resources = {
			'poetry': [
				{"poetryfoundation": "https://www.poetryfoundation.org/poems/poem-of-the-day"},
				{"poetryloc": "http://www.loc.gov/poetry/180/p180-list.html"}
			],
			'comedy': [
				{"boredpanda": "https://www.boredpanda.com/funny-dad-jokes-puns/?utm_source=google&utm_medium=organic&utm_campaign=organic"},
				{"countryliving": "https://www.countryliving.com/life/a27452412/best-dad-jokes/"}
			],
			'art': [
				# author and picture name are attributed in the json response for both
				{"unsplash": "https://api.unsplash.com/photos/random?client_id=uiBKriuL0je85mzrm-aEJr29zagN3P9dzHfgat62ABQ"},
				{"metmuseum": "https://collectionapi.metmuseum.org/public/collection/v1/objects/71"}
			],
			'sports': [
				{"everydaypower": "https://everydaypower.com/motivational-sports-quotes/"},
				# class clearfix
				{"brainyquote": "https://www.brainyquote.com/topics/sports-quotes"}
			],
			'science': [
				{"letsgetsciencey": "https://letsgetsciencey.com/weird-science-facts/"},
				{"nasa": "https://api.nasa.gov/planetary/apod?api_key=XLxnsqCQmltNsddx0AEWfGaczdFW2RyBY8XkpFxg"}
				
			],
			'technology': [
				{"thefactsite": "https://www.thefactsite.com/top-100-technology-facts/"},
				{"orleansmarketing": "https://orleansmarketing.com/35-technology-facts-stats/"}	
			]
		}
		self.subtopics = {
			'poetry': [],
			'comedy': [],
			'art': [],
			'sports': [],
			'entertainment': [],
			'science': [],
			'technology': []	
		}

		self.driver_path = ""


	def tweet(self):
		topic = random.choice(self.topics)
		num = random.randint(1, 10)
		
		#prob of doing a retweet, tweet news or tweet generated content
		#20% retweets, 30% news, 50% original content
		if num <= 2:
			self.retweet(topic)
		elif num <= 5:
			self.tweet_news(topic)
		else:
			self.tweet_content(topic)


	def tweet_content(self, topic):
		#choose between the 2 resources
		choice = random.choice(self.content_resources[topic])
		#get resource key as string
		resource = [x for x in choice][0]
		endpoint = choice[resource]
		handler = getattr(contentHandler, resource)
		handler(endpoint)


	def tweet_news(self, topic):
		pass


	def retweet(topic):
		pass


if __name__ == '__main__':
	tb = TwitterBot()


