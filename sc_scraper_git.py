#Import Libraries
from bs4 import BeautifulSoup
import requests
import re
import csv
import os
import pandas as pd

#Read in urls
scurls = open("scurls.txt")
urls = scurls.read()
urls = urls.split("\n")
numURLS = len(urls)

#Get raw URL text
def getText (url): 
    track  = requests.get(url)
    data = track.content
    soup = BeautifulSoup(data)
    txt = soup.text #turn the text into usable
    return[txt]

#Followers
def followerGet (txt):
    spot_fl = txt.find("followers_count") #Find where follower count starts
    lengthfl = len("followers_count")
    followstring = (txt[(spot_fl+lengthfl+2):(spot_fl+lengthfl+10)]) #Assuming no one has over 1bil followers this returns the string after


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

#Define columns 
followers = [] 
likes = [] 
plays = [] 
reposts = []
comments = []

for i in range(1,numURLS):

    #Iterate through individual item
    single = urls[i]

    #Convert txt into proper format
    txt = getText(single)
    txt = ''.join(txt)

    followers.append(followerGet(txt))
    likes.append(likesGet(txt))
    plays.append(playsGet(txt))
    reposts.append(repostsGet(txt))
    comments.append(commentsGet(txt))
    
    #Get information from text
    print(single, " Followers: ", followerGet(txt), " Likes: ", likesGet(txt), " Plays: ", playsGet(txt), " Reposts: ", repostsGet(txt), " Comments: ", commentsGet(txt))

toSave = {'Followers': followers, 
'Likes': likes,
'Plays': plays,
'Reposts': reposts,
'Comments': comments
}

df = pd.DataFrame(toSave)
