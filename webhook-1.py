import telepot
bot = telepot.Bot(token='498400444:AAGGuVbqKQQmmPiDVmGkCrfrmDk3ZFZ_4gw')
s = bot.setWebhook('https://3b727e85.ngrok.io/HOOK')
#s = bot.deleteWebhook()
#s = bot.Webhookinfo()
print(s)
