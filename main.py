from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
import scdl
import os

updater = Updater(token='621576630:AAGBjQdLZtnc-AJoVSGaW2OEjQZ58trWn5E')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
global musicas
musicas=[]
global urls
urls=[]

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Bem vindo ao sound cloud player bot")
    bot.send_message(chat_id=update.message.chat_id, text="digite /pesquisar + nome da musica para pesquisar por musicas")
    
def pesquisar(bot, update, args):
    global musicas
    musicas=[]
    global urls
    urls=[]
    user_says = " ".join(args)
    
    if user_says != "":
        update.message.reply_text("Você pesquisou por: " + user_says)
        url = "https://soundcloud.com/search/sounds?q="+str(user_says)
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        songlist = soup.findAll('li',{'class':""})
        for songs in songlist :
            if songs.get_text() != '' and songs.get_text() != 'Search for Everything' and songs.get_text() != 'Search for Tracks' and songs.get_text() != 'Search for Playlists' and songs.get_text() != 'Search for People':
                musicas.append(songs.get_text())
        linklist = soup.findAll('a',href=True)
        cont = 0
        for links in linklist :
            if songs.get_text() != '' and cont > 5 and cont < 16:
                urls.append(links['href'])
            cont = cont + 1
    cont=0
    for cont in range(0,10):
        artista=urls[cont]
        artista=artista.split('/')
        #print(str(cont+1)+"-"+artista[1]+" - "+musicas[cont])
        bot.send_message(chat_id=update.message.chat_id, text=str(cont+1)+"-"+artista[1]+" - "+musicas[cont])
        bot.send_message(chat_id=update.message.chat_id, text="Digite um numero correspondente a musica desejada")
    

def opt(bot, update):
    print(update.message.text)
    global urls
    global musicas
    opts=['1','2','3','4','5','6','7','8','9','10']
    cont=0
    msg=update.message.text
    for cont in range(0,10):
        if str(msg)==str(opts[cont]) and len(urls)!=0:
            #print(update.message.text)
            os.system(' scdl -l https://soundcloud.com'+str(urls[cont])+' --path C:\BotMusic')
            try:
                bot.send_audio(chat_id=update.message.chat_id, audio=open('C:/BotMusic/'+musicas[cont]+'.mp3', 'rb'), timeout=50000)
            except:
                bot.send_message(chat_id=update.message.chat_id, text="Não foi possivel enviar a musica, por favor tente novamente ou selecione outra musica")
                #os.rename('C:/BotMusic/'+musicas[cont]+'.mp3','C:/BotMusic/semTitulo.mp3')
                #bot.send_audio(chat_id=update.message.chat_id, audio=open('C:/BotMusic/semTitulo.mp3', 'rb'), timeout=50000)
                #os.remove('C:/BotMusic/semTitulo.mp3')


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

dispatcher.add_handler(CommandHandler("pesquisar", pesquisar, pass_args=True))

opt_handler = MessageHandler(Filters.text, opt)
dispatcher.add_handler(opt_handler)

updater.start_polling()


