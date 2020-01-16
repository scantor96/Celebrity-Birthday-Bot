#So far I have only been able to get this to work on Chrome

from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import * 
import chromedriver_binary
import time
import tweepy as tp
import requests
import random

bot = webdriver.Chrome()
#Use Chrome as the browser

def twit_api():
    #Accesses the Twitter API
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    auth = tp.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    ACCESS_KEY = ''
    ACCESS_SECRET = ''
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tp.API(auth)
    return api

def get_celeb(link):
    #gets the celebrity's name and age from famousbirthdays.com
    l = requests.get(link)
    soup = BeautifulSoup(l.content, "html.parser")
    name_and_age = soup.find("div",class_="name").text
    comma = name_and_age.find(",")
    data = {}
    name = name_and_age[:comma]
    age = name_and_age[comma+2:]
    data["Name"] = name.strip("\n")
    data["Age"] = age.strip("\n")
    return data

def search(name):
    #tries to find the appropriate Twitter account to tag
    account = twit_api().search_users(name, 1)
    if len(account) > 0:
        handle = "@" + account[0]._json["screen_name"]
    else:
        handle = name #If no proper handle appears, the bot doesn't tag them
    return handle
    
def write_tweet(user, age):
    #This has a list of different tweet formats the tweet could take, and 
    #it randomly chooses a format each time
    age_min_1 = int(age) - 1
    tweet_list = []
    tweet_list.append(f"Happy Birthday {user}! Blow out {age} candles!")
    tweet_list.append(f"Crazy that {user} is {age} today. Happy Birthday!")
    tweet_list.append(f"Give {user} congratulations for {age} years around"\
                      " the sun")
    tweet_list.append(f"{user} is forgetting {age_min_1} and moving on to" \
                      f" {age}!")
    tweet_list.append(f"Congrats {user} on turning {age}!")
    tweet_list.append(f"Wow, {user}, so cool that you're {age} today!")
    tweet_list.append(f"{user}, this bot is proud to wish you a Happy" \
                      f" birthday. Cheers to {age} years!")
    tweet_list.append(f"Birthdays? {user} has gone through {age} of these.")
    tweet_list.append(f"Hey, {user}, what kind of cake do you want today?")
    tweet_list.append(f"The sun is shining brighter because it's {user}'s"\
                      f" birthday today.")
    tweet_list.append(f"Another year, another fear. Happy Birthday {user}.")
    tweet_list.append(f"Can't believe merely yesterday, {user} was only" \
                      f" {age_min_1}. Happy Birthday!")
    tweet_list.append(f"Hey everyone! How are you celebrating {user}'s" \
                      f" birthday?")
    text = random.choice(tweet_list)
    return text

def log_in(username, password):
    #Logs into the account
    bot.get("https://twitter.com/login")
    time.sleep(3)
    user = bot.find_element_by_class_name("js-username-field")
    pw = bot.find_element_by_class_name("js-password-field")
    user.clear()
    pw.clear()
    user.send_keys(username)
    pw.send_keys(password)
    pw.send_keys(Keys.RETURN)
    time.sleep(3)
    
def tweet(text):
    #Writes the message and sends it
    time.sleep(5)
    a = bot.find_element_by_css_selector("[data-testid='SideNav_NewTweet_Button']")
    a.click()
    space = bot.find_element_by_css_selector("[data-testid='tweetTextarea_0']")
    space.send_keys(text)
    time.sleep(2)
    publish = bot.find_element_by_css_selector("[data-testid='tweetButton']")
    publish.click()

#Combining the above functions into variables that are used in tweeting.
data = get_celeb("https://www.famousbirthdays.com") 
user = search(data["Name"])
age = data["Age"]
text = write_tweet(user, age)
log_in("username", "password") #put your own information here
tweet(text)
