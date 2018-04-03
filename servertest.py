import json
from bottle import get, post, request, run, route
import telebot
import curiouscomm
import uuid
import sys

TOKEN = "498400444:AAGGuVbqKQQmmPiDVmGkCrfrmDk3ZFZ_4gw" #telegram
CLIENT_ACCESS_TOKEN = "6571248de3fa4d299e9d8322b748496b" #google
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
cURL = "https://fb97494f.ngrok.io/HOOK"
session_id = uuid.uuid4().hex

def main():
    telebot.createHook(TOKEN,URL,cURL)

@route('/HOOK', method='POST')
def getUpdate():
    text,chat_id,update_id = telebot.parseText(request.body.read())
    telebot.sendChatAction(URL,chat_id,'typing')
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    print("IP: "+text.translate(non_bmp_map))
    resp = curiouscomm.communicate(session_id,CLIENT_ACCESS_TOKEN,text)
    print("OP: "+resp)
    telebot.send_message(URL,resp.replace("&",""),chat_id)
    #f = open(r'C:\Users\sdcuser.US2B4QER0H\Desktop/26C4.png','rb')
    #telebot.send_photo(chat_id,f)

if __name__ == '__main__':
    main()
    run(host='localhost', port=80)
