## Twitter Bot that publishes different kind of content every time
This is a bot that tweets some smart content at a scheduled time period.
It can tweets about tech, science, poetry, some jokes and cool nasa and art images.

The program gets the content from different websites and APIs.
- When the content is obtained from websites, it's scraped using BeautifulSoup. In addition to other string manipulation from Python. 
- The content from APIs is obtained in JSON format with Python's requests library. 
- The twitter API is used through the Python API wrapper Tweepy. 
- It can successfully:
	- create new content
	- tweet links to articles of the day from different subtopics. 
	- retweet relevant tweets associated with predefined topics and subtopics. 


The program is containerized using Docker (with the Python Alpine image)

The container is uploaded to AWS and runs on an EC2 instance. 

Docker Image can be found [here](https://hub.docker.com/r/diegojramirezs7/twitter-bot/)

