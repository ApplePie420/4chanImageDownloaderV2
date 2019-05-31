import json
import urllib.request as urllib2
import os
from tinydb import TinyDB, Query

#TinyDB init
threadsDB = TinyDB("database/present-threads.json")

#URL parsing
#http://boards.4channel.org/g/thread/69449213           example thread URL
#http://boards.4channel.org/vip/thread/88037            exampel URL 2
#https://a.4cdn.org/board/thread/threadnumber.json      example json URL

threadNo = input("Enter the URL of the thread:")

URLstring = threadNo[24:] #switch to 27 if using "boards.4channel.org site instead of 4chan
delimiter = URLstring.find("/")
board = URLstring[:delimiter]

threadnumber = URLstring[7:]
delimiter = threadnumber.find("/")
threadnumber = threadnumber[delimiter:]

#'''
#Creating JSON URL
jsonURL = "https://a.4cdn.org/" + board + "/thread" + threadnumber + ".json"
jsonName = threadnumber + ".json"

#Search if thread exists in tinyDB, enter it if not, update hits
Thread = Query()
search = threadsDB.search(Thread.thread == threadnumber)
if(search == []):
    print("New database entry!")
    threadsDB.insert({"thread": threadnumber, "completed": 0, "hits": 1})
else:
    print("Thread already in database!")
    hits = int(search[0]["hits"]) + 1
    threadsDB.update({"hits": hits}, Thread.thread == threadnumber)

#Folder structure creation
currentFolder = ""
if(os.path.isdir("images") == False):
    print("First time running, creating /images/")
    os.mkdir("images")
currentFolder += "images/"

if(os.path.isdir(currentFolder + board) == False):
    print("First time using board {}, creating {}".format(board, board))
    os.mkdir(currentFolder + board)
currentFolder += board

if(os.path.isdir(currentFolder + threadnumber) == False):
    print("Creating folder", threadnumber)
    os.mkdir(currentFolder + threadnumber)
currentFolder += threadnumber + "/"

print(currentFolder)

#JSON retrieval and parsing
print(jsonURL)
urllib2.urlretrieve(jsonURL, currentFolder + jsonName)

json_data = open(currentFolder + jsonName).read()

data = json.loads(json_data)
type(data)


#Image downloading 
for post in data["posts"]:
    try:
        extension = post["ext"]
        fileName = str(post["tim"])
        site = "https://i.4cdn.org/" + board + "/" + fileName + extension
        saveFileName = fileName + extension
        if(os.path.exists(currentFolder + saveFileName)):
            print("File already exists")
            continue
        urllib2.urlretrieve(site, currentFolder + saveFileName)
        print("Downloading file {} to {}".format(saveFileName, currentFolder))
    except:
        pass

#Update tinyDB
status = Query()
threadsDB.update({"completed": 1}, status.thread == threadnumber)

#'''
