# CS242_TwitterCrawler

### Project provided by Prof. Vagelis Hristidis for CS 242 Information Retrieval at UCR.

Mainly used the tweepy module to access Twitter's APIs. Started with some popular twitter account and crawled their tweets along with those of their followers and the accounts they are following. Then recursively crawled through all of those accounts in order to collect a large mass of tweets in their json format. 

The main rule was to only crawl tweets that were geo-tagged. In order to ensure this, a check was performed to check a user's geo_enabled field, and the program will only crawl the user's tweets if it was enabled.

Download the batch file and navigate the directory containing all of the files. In the file input.txt, the screen name of the first user to crawl should be in the file. Type crawler to run the batch script and the crawler.

Used Modules: json, requests.packages.urllib3, sys, os, tweepy
