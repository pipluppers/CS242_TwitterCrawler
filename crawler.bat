:: Disables displaying the command
@echo off

:: Clear the terminal
cls

:: input.txt will be the input file containing a single string denoting the screen name of the user the crawler will start from
python twitter_crawler.py keys.txt output.txt