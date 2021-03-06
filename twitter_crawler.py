import tweepy
import csv
import json
import requests.packages.urllib3    # To disable pip warning msg
import sys  # Used to find the size of a list in bytes
import time
import os

# to disable pip warning message
requests.packages.urllib3.disable_warnings()

if len(sys.argv) < 3:
    print('Not enough command line arguments. Should have the python file, file with Twitter keys, and output file')
    sys.exit()

l = []
with open(sys.argv[1]) as f:
    l = f.read().splitlines()
    consumer_key = l[0]
    consumer_secret = l[1]
    access_token = l[2]
    access_token_secret = l[3]

# Set access tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')
    sys.exit()

# Set up the API instance
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Holds the tweets
tweets = []
tweets.clear()

#   Fetch some popular twitter account from the first line of the input file
username = input('Enter the screen name of the first account to crawl: ')
try:
    user = api.get_user(username)
    print("user: ", user.screen_name)
    print("follower count: ", user.followers_count)
except tweepy.TweepError:
    print('User doesn\' exist. Exiting program')
    sys.exit()

i = 0

#   List of seen usernames. Don't reiterate over them
seen_user = [user]

#   File Format
#   [{tweet},{tweet},{tweet},...]

#   Get the output file from the command line
filename = str(sys.argv[2])

with open(filename, mode='w') as f:
    #   In the event of a keyboard interrupt, flush everything to the file
    f.write('[')
    try:
        try:
            for x in seen_user:
                try:
                    for friend in tweepy.Cursor(api.friends, id=x.screen_name, count=50).items():
                        #   Print progress every now and then
                        if i % 800 == 0:
                            print('Current size of list: ' + str(sys.getsizeof(tweets)))

                        #   Ignore users that we have seen already
                        if friend in seen_user:
                            # print('\t\t\t\tSeen this user before. Skipping ...')
                            continue

                        i += 1

                        #   If list gets too big, flush it to the file and clear everything in it. Also reset i
                        #   Avoids inenvitable memory error
                        if i % 1600 == 0:
                            print('Writing to file ' + filename)
                            for q in tweets:
                                try:
                                    f.write(q + ',')
                                    f.flush()
                                except UnicodeEncodeError:
                                    continue
                            tweets.clear()
                            i = 0
                            print('Size of ' + filename + ' so far: ' + str(os.stat(filename).st_size))
                            #   Stop crawling once the file size is greater than 2.5 GB
                            if os.stat(filename).st_size >= 2500000000:
                                f.write(']')
                                print('Got 2.5 GB. Done!')
                                sys.exit()

                        #   Add user to seen list
                        seen_user.append(friend)

                        #   Ignore non-geotagged tweets
                        if not friend.geo_enabled:
                            # print('\t\t\t\tGeo-tag not enabled for ' + str(friend.screen_name) + '. Skipping..')
                            continue

                        try:
                            # print('Looking through ' + str(friend.screen_name) + ' tweets')
                            for stat in api.user_timeline(friend.screen_name, count=200):
                                #   Add the tweets to the list
                                tweets.append(json.dumps(stat._json))

                        except tweepy.TweepError:
                            # print('\t' + str(friend.screen_name) + ' has protected tweets. Skipping ...')
                            pass
                except tweepy.TweepError:
                    # print(str(x.screen_name) + '\'s profile is private. Skipping ...')
                    pass
        except KeyboardInterrupt:
            #   Don't print the last json on the last part. Might be incomplete
            for q in tweets[0:-2]:
                try:
                    f.write(q + ',')
                    f.flush()
                except UnicodeEncodeError:
                    continue
            f.write(']')
            print('Keyboard Interrupt')

    except MemoryError:
        # Write everything to the file if a memory error occurs
        for q in tweets[0:-2]:
            try:
                f.write(q + ',')
                f.flush()
            except UnicodeEncodeError:
                continue
        f.write(']')
        print('This should not print')

print('Number of bytes retrieved: ' + str(os.stat(filename).st_size))
print('End of program')
