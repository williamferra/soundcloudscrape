#Import Libraries
from bs4 import BeautifulSoup
import requests
import re
import csv
import os

#Read in urls
scurls = open(r"C:\Users\willi\Documents\soundsplit\scurls.txt")
urls = scurls.read()
urls = urls.split("\n")
numURLS = len(urls)

#Get raw URL text
def getText (url): 
    track  = requests.get(url)
    data = track.content
    soup = BeautifulSoup(data)
    txt = soup.text
    return[txt]

#Followers
def followerGet (txt):
    spot_fl = txt.find("followers_count")
    lengthfl = len("followers_count")
    followstring = (txt[(spot_fl+lengthfl+2):(spot_fl+lengthfl+10)])
    followers = re.findall(r'\d+', followstring) 
    followers = list(map(int, followers))
    return[followers]

#Likes
def likesGet (txt):
    spot_dl = txt.find("download_count")
    spot_likes = txt.find("""likes_count""",spot_dl, len(txt))
    lengthlikes = len("likes_count")
    likestring = (txt[(spot_likes+lengthlikes+2):(spot_likes+lengthlikes+10)])
    likes = re.findall(r'\d+', likestring)
    likes = list(map(int, likes))
    return[likes]

#Plays
def playsGet (txt):
    spot_plays = txt.find("playback_count")
    lengthplays = len("playback_count")
    playstring = (txt[(spot_plays+lengthplays+2):(spot_plays+lengthplays+10)])
    playcount = re.findall(r'\d+', playstring)
    playcount = list(map(int, playcount))
    return[playcount]

#Reposts
def repostsGet (txt):
    spot_state = txt.find("state")
    spot_reposts = txt.rfind("reposts_count",0,spot_state)
    lengthreposts = len("reposts_count")
    repoststring = (txt[(spot_reposts+lengthreposts+2):(spot_reposts+lengthreposts+10)])
    reposts = re.findall(r'\d+', repoststring)
    reposts = list(map(int, reposts))
    return[reposts]

#Comments
def commentsGet (txt):
    spot_comments = txt.rfind("comment_count")
    lengthcomments = len("comment_count")
    commentstring = (txt[(spot_comments+lengthcomments+2):(spot_comments+lengthcomments+10)])
    comments = re.findall(r'\d+', commentstring)
    comments = list(map(int, comments))
    return[comments]



#Iterate through individual item
single = urls[1]

#Convert txt into proper format
txt = getText(single)
txt = ''.join(txt)

#Get information from text
followerGet(txt)
likesGet(txt)
playsGet(txt)
repostsGet(txt)
commentsGet(txt)