import tweepy
import random
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import requests
from constants import *
import contentHandler
from bs4 import BeautifulSoup

auth_handler = tweepy.OAuthHandler(API_KEY, SEC_KEY)
auth_handler.set_access_token(TOKEN, SEC_TOKEN)
api = tweepy.API(auth_handler)

class TwitterBot:
	def __init__(self):
		self.topics = ['poetry', 'comedy', 'art', 'sports', 'science', 'technology']
		self.content_resources = {
			'poetry': [
				{"poetrydb": "http://poetrydb.org/random"},
				{"poetryloc": "http://www.loc.gov/poetry/180/p180-list.html"}
			],
			'comedy': [
				{"boredpanda": "https://www.boredpanda.com/funny-dad-jokes-puns/?utm_source=google&utm_medium=organic&utm_campaign=organic"},
				{"countryliving": "https://www.countryliving.com/life/a27452412/best-dad-jokes/"}
			],
			'art': [
				{"unsplash": "https://api.unsplash.com/photos/random?client_id=uiBKriuL0je85mzrm-aEJr29zagN3P9dzHfgat62ABQ"},
				{"metmuseum": "https://collectionapi.metmuseum.org/public/collection/v1/objects/71"}
			],
			'sports': [
				{"everydaypower": "https://everydaypower.com/motivational-sports-quotes/"},
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
			'poetry': ["depression poetry", "laughter poetry", "poetry about future", "romantic poetry", "poetry about sympathy"],
			'comedy': ["insult comedy", "cringe comedy", "blue comedy", "prop comedy", "shock humor"],
			'art': ["Aestheticism", "Baroque", "Cubism", "Feminist art", "Street Art"],
			'sports': ["soccer", "basketball", "UFC", "baseball", "NFL"],
			'science': ["physics", "chemistry", "biology", "psychology", "economics"],
			'technology': ["artificial intelligence", "nano technology", "space exploration", "robotics", "health and medicine"]	
		}


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
		#choice = random.choice(self.content_resources[topic])
		choice = {"poetrydb": "http://poetrydb.org/random"}
		#get resource key as string
		resource = [x for x in choice][0]
		endpoint = choice[resource]
		handler = getattr(contentHandler, resource)
		handler(endpoint)


	def tweet_news(self, topic):
		try:
			#build appropriate url with search params
			subtopic = random.choice(self.subtopics[topic])
			endpoint = "https://news.google.com/search?q="
			params = subtopic.replace(' ','+')
			endpoint += params

			#get webpage source
			resp = requests.get(endpoint)
			soup = BeautifulSoup(resp.content, 'html.parser')

			#get list of links from result page
			link_list = soup.find_all('a', attrs={'class': 'VDXfz'})
			links = [x.get('href')[1:] for x in link_list]

			# links are relative to its path, so they need to be made absolute
			choice = random.choice(links)
			link = "https://news.google.com"+choice

			# link obtained redirects to third link, so we get the link that request redirects to
			article = requests.get(link)
			new_link = article.url

			# build tweet content
			tweet = "{0}\nnews of the day: {1}".format(subtopic, new_link)
			api.update_status(tweet)
		except Exception as e:
			print(str(e))
			return str(e)


	def retweet(self, topic):
		try:
			subtopic = random.choice(self.subtopics[topic])
			tweets = api.search(q=subtopic, lang='en', rpp=20)
			tweet = random.choice(tweets)
			tweet.retweet()
		except Exception as e:
			print(str(e))
			return str(e)


if __name__ == '__main__':
	tb = TwitterBot()
	tb.tweet()

