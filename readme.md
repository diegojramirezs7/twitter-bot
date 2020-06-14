## Twitter Bot that publishes different kind of content every time
This is a bot that tweets some smart content at a scheduled time period.
It can tweets about tech, science, poetry, some jokes and cool nasa and art images.

The program gets the content from different websites and APIs.
- When the content is obtained from websites, it's scraped using Selenium Webdriver and BeautifulSoup. In addition to other string manipulation from Python. 
- The content from APIs is obtained with Python's requests library. 
- The twitter API is used through the API wrapper Tweepy. 
- Right now, it can successfully:
	- create new content
	- tweet links to a news of the day article
	- retweet relevant tweets associated with predefined topics and subtopics. 






