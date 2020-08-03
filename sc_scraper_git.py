#Import Libraries
from bs4 import BeautifulSoup
import requests
import re
import csv
import os
import pandas as pd
import numpy as np

#Read in urls
scurls = open("scurls.txt")
urls = scurls.read()
urls = urls.split("\n")
numURLS = len(urls)

#Get raw URL text
def getText (url): 
    track  = requests.get(url,timeout=5)
    data = track.content
    soup = BeautifulSoup(data)
    txt = soup.text #turn the text into usable
    return[txt]

#Followers
def followerGet (txt):
    txt_str =''.join(txt) #Convert to string
    spot_fl = txt_str.find("followers_count") #Find where follower count starts
    lengthfl = len("followers_count")
    followstring = (txt_str[(spot_fl+lengthfl+2):(spot_fl+lengthfl+10)]) #Assuming no one has over 1bil followers this returns the string after
    followers = re.sub("[^0-9]", "", followstring)
    followers = int(followers)
    return[followers]

#Likes
def likesGet (txt):
    spot_dl = txt.find("download_count")
    spot_likes = txt.find("""likes_count""",spot_dl, len(txt))
    lengthlikes = len("likes_count")
    likestring = (txt[(spot_likes+lengthlikes+2):(spot_likes+lengthlikes+10)])
    likes = re.sub("[^0-9]", "", likestring)
    likes = int(likes)
    return[likes]

#Plays
def playsGet (txt):
    spot_plays = txt.find("playback_count")
    lengthplays = len("playback_count")
    playstring = (txt[(spot_plays+lengthplays+2):(spot_plays+lengthplays+10)])
    playcount = re.sub("[^0-9]", "", playstring)
    playcount = int(playcount)
    return[playcount]

#Reposts
def repostsGet (txt):
    spot_state = txt.find("state")
    spot_reposts = txt.rfind("reposts_count",0,spot_state)
    lengthreposts = len("reposts_count")
    repoststring = (txt[(spot_reposts+lengthreposts+2):(spot_reposts+lengthreposts+10)])
    reposts = re.sub("[^0-9]", "", repoststring)
    reposts = int(reposts)
    return[reposts]

#Comments
def commentsGet (txt):
    spot_comments = txt.rfind("comment_count")
    lengthcomments = len("comment_count")
    commentstring = (txt[(spot_comments+lengthcomments+2):(spot_comments+lengthcomments+10)])
    comments = re.sub("[^0-9]", "", commentstring)
    comments = int(comments)
    return[comments]

#Username
def userGet (txt):
    spot_user = txt.find("by")
    spot_user
    spot_user2 = txt.find("|")
    spot_user2
    username = txt[spot_user+2:spot_user2]
    return[username]

#Define columns 
followers = [] 
likes = [] 
plays = [] 
reposts = []
comments = []
username = []

for i in range(0,numURLS):

    #Iterate through individual item(
    single = urls[i]

    #Convert txt into proper format
    txt = getText(single)
    txt = ''.join(txt)

    username.append(userGet(txt))
    followers.append(followerGet(txt)) 
    likes.append(likesGet(txt))
    plays.append(playsGet(txt))
    reposts.append(repostsGet(txt))
    comments.append(commentsGet(txt))
    
    #Get information from text
    print(i, single, "Username: ", userGet(txt), " Followers: ", followerGet(txt), " Likes: ", likesGet(txt), " Plays: ", playsGet(txt), " Reposts: ", repostsGet(txt), " Comments: ", commentsGet(txt))


u1 = pd.Series(username, name='Username')
f1 = pd.Series(followers, name = 'Followers')
l1 = pd.Series(likes, name='Likes')
p1 = pd.Series(plays, name='Plays')
r1 = pd.Series(reposts, name='Reposts')
c1 = pd.Series(comments, name='Comments')
df = pd.concat([u1,f1,l1,p1,r1,c1,], axis=1)

df = df.dropna()
df.to_csv('output2.csv')
