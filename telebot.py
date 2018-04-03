import json 
import requests
import telepot
import urllib

bot = 0
TOKEN = 0
URL = 0

TOKEN = "498400444:AAGGuVbqKQQmmPiDVmGkCrfrmDk3ZFZ_4gw"

bot = telepot.Bot(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def checkHook(url):
    url += "getWebhookInfo"
    js = get_json_from_url(url)
    if len(js["result"]["url"])>0:
        return True
    else: return False

def createHook(l_TOKEN,l_URL,cURL):
    TOKEN = l_TOKEN
    URL=l_URL
    bot = telepot.Bot(token=l_TOKEN)
    if(checkHook(l_URL) is False):
        print("webhook not available")
        s = bot.setWebhook(cURL)
        if (s):
            print("webhook completed")
            return True
        else:
            print("error setting webhook")
            return False
    else:
        print("webhook exists")
        return True

def parseText(mBody):
    updates = json.loads(mBody)
    if "text" in updates["message"]:
        if type(updates["message"]["text"]) == "unicode":
            text = ord(updates["message"]["text"])
        else:
            text=updates["message"]["text"].replace("/start","Hello")
            #print("i/p : "+text)

    if "location" in updates["message"]:
        text = "that's bad"

    chat_id = updates["message"]["chat"]["id"]
    update_id = updates["update_id"]
    return (text, chat_id,update_id)

def send_message(l_URL,text, chat_id):
    #url = l_URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    #get_url(url)
    #bot = telepot.Bot(token=TOKEN)
    bot.sendMessage(chat_id,text)
def sendChatAction(l_URL,chat_id,text):
    #url = l_URL + "sendChatAction?chat_id={}&text={}".format(chat_id, text)
    #get_url(url)
    bot.sendChatAction(chat_id,text)
def send_photo(chat_id,f):
    bot.sendPhoto(chat_id,f)

    
