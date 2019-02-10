# CS242_TwitterCrawler

### Project provided by Prof. Vagelis Hristidis for CS 242 Information Retrieval at UCR.

Mainly used the tweepy module to access Twitter's APIs. Started with some popular twitter account and crawled their tweets along with those of their followers and the accounts they are following. Then recursively crawled through all of those accounts in order to collect a large mass of tweets in their JSON format. 

The main rule was to only crawl tweets that were geo-tagged. In order to ensure this, a check was performed to check a user's geo_enabled field, and the program will only crawl the user's tweets if it was enabled.

Download the batch file and navigate the directory containing all of the files. In order to run the script and the crawler, do the following according the operating system type:

**Windows**: Type crawler 

**Linux/Unix**: Type ./crawler.sh 

Then input the screen name of the user from which to begin crawling from. Tweets will be written to the file output.txt in JSON format.

Used Modules: json, requests.packages.urllib3, sys, os, tweepy
