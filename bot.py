import BotAmino
import wikipedia
import urllib
import time
import praw
from BotAmino import BotAmino, Parameters
import json
from gtts import gTTS
import requests
import random

# Logins 
print("Wait..")
client = BotAmino("", "")
client.prefix = "#"
client.self_callable = False 
client.wait = 2

# is me lol
def owner(data: Parameters):
    return data.authorId in [""]
@client.on_member_join_chat()
def say_hello(data: Parameters):
    words = [' just landed!', 'Hey hey, ', 'welcome here, ', 'hi, how are you?, ']
    x = random.choice(words)
    data.subClient.send_message(data.chatId, f"{data.author} {x}", replyTo=data.messageId)
@client.on_message()
def on_message(data):
    if data.message == 'السلام عليكم':
        data.subClient.send_message(chatId=data.chatId, message='[BC]وعليكم السلام')
    elif data.message == 'باي':
        data.subClient.send_message(chatId=data.chatId, message='[BC]الله معاك')
    elif data.message == 'هلا':
        data.subClient.send_message(chatId=data.chatId, message='[BC]هلاوات')
@client.command('music')
def music(data):
    music = ['']
    test = 'Sending.. Please wait this will take few seconds'
    i = 1
    while i != 3:
        music.append(str(i)+".mp3")
        i +=1
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message='[BC]Music list\n[IC] 1 - Nujabes ft. Shing02 (Uyama Hiroto Remix) - Instrumental Cover', replyTo=data.messageId)
    else:
        data.subClient.send_message(chatId=data.chatId, message=test, replyTo=data.messageId)
        with open(music[int(data.message)], 'rb') as file:
            data.subClient.send_message(chatId=data.chatId, file=file, fileType='audio')
@client.command('math')
def math(data):
    data.message = data.message.split(' ')
    x = int(data.message[0])
    op = str(data.message[1])
    y = int(data.message[2])
    if len(data.message) >= 4:
        data.subClient.send_message(chatId=data.chatId, message='[IC]This is a 2term calculator, takes only two numbers', replyTo=data.messageId)
    elif op == '+':
        result = float(x) + float(y)
        data.subClient.send_message(chatId=data.chatId, message=f'Result: {result}', replyTo=data.messageId)
    elif op == '-':
        result = float(x) - float(y)
        data.subClient.send_message(chatId=data.chatId,message=f'Result: {result}', replyTo=data.messageId)
    elif op == '*':
        result = float(x) * float(y)
        data.subClient.send_message(chatId=data.chatId,message=f'Result: {result}', replyTo=data.messageId)
    elif op == '/':
        result = float(x) / float(y)
        data.subClient.send_message(chatId=data.chatId,message=f'Result: {result}', replyTo=data.messageId)
@client.command('screenshot')
def screenshot(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message='No link given', replyTo=data.messageId)
    else:
        req = requests.get(f'https://api.screenshotmachine.com/?key=e682bd&url={data.message}&dimension=1024x768')
        with open('ss.jpeg', 'wb') as file:
            file.write(req.content)
            file.close()
        with open('ss.jpeg', 'rb') as file:
            data.subClient.send_message(chatId=data.chatId, file=file, fileType='image')
@client.command('wall', owner)
def wall(data):
    data.subClient.set_welcome_message(data.message)
    data.subClient.send_message(data.chatId,"Updated wall message!", replyTo=data.messageId)
@client.command('wiki')
def wiki(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message='Please insert a topic', replyTo=data.messageId)
    else:
        data.subClient.send_message(chatId=data.chatId, message=wikipedia.summary(data.message, sentences=5))
@client.command('coins')
def coins(data):
    count = data.subClient.get_wallet_amount()
    data.subClient.send_message(chatId=data.chatId, message=f'I currently have {count} coins', replyTo=data.messageId)
@client.command('join')
def join(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message="No link given", replyTo=data.messageId)
    elif data.message in 'http://aminoapps.com' or 'https://aminoapps.com':
        data.subClient.join_chatroom(data.message)
        data.subClient.send_message(chatId=data.chatId, message='Joined',replyTo=data.messageId)
    else:
        data.subClient.send_message(chatId=data.chatId, message='Invalid link',replyTo=data.messageId)

@client.command('tod')
def tod(data):
    if data.message== '':
        data.subClient.send_message(chatId=data.chatId, message='[BC] Welcome to truth or dare\n[IC]Example: #tod <dare, truth>', replyTo=data.messageId)
    elif data.message == 'dare':
        dares = []
        with open('dare.txt', 'rb') as file:
            for dare in file:
                dares.append(dare)
            file.close()
        x = random.choice(dares)
        data.subClient.send_message(chatId=data.chatId, message=f'[BC]{data.author} I dare you to:\n[IC]{x}')
    elif data.message == 'truth':
        t = []
        with open('truth.txt', 'rb') as file:
            for _ in file:
                t.append(_)
            file.close()
        x = random.choice(t)
        data.subClient.send_message(chatId=data.chatId, message=f'[BC]{data.author},\n[IC]{x}')
@client.command('say')
def say(data):
    myobj = gTTS(text=data.message, lang='ar', slow=False)
    myobj.save('tts.mp3')
    with open('tts.mp3', 'rb') as file:
        data.subClient.send_message(chatId=data.chatId, file=file, fileType='audio')
@client.command('send')
def send(data):
    data.subClient.send_message(chatId=data.chatId, message=data.message)
@client.command('howgay')
def howgay(data):
    perc = random.randrange(100)
    if data.message == '':
        y = data.subClient.get_user_id(data.author)[1]
        if y == 'Your id':
            data.subClient.send_message(chatId=data.chatId, message=f'[BC]{data.author} You are not gay!')
        else:
            data.subClient.send_message(chatId=data.chatId, message=f"{data.author} You are {perc}% gay!", replyTo=data.messageId)
    else:
        x = data.message.replace("@", "")
        data.subClient.send_message(chatId=data.chatId, message=f"{x} is {perc}% gay!", replyTo=data.messageId)
@client.command('stat')
def stat(data):
    chosen = data.subClient.get_user_id(data.author)[1]
    level = data.subClient.get_member_level(chosen)
    titles = data.subClient.get_member_titles(chosen)
    data.subClient.send_message(chatId=data.chatId, message=f"[IC] status of {data.author}\n[c] level: {level}\n[c] titles: {titles}", replyTo=data.messageId)
@client.command('meme')
def meme(data):
    reddit = praw.Reddit(client_id = "",
                        client_secret = "",
                        username = "",
                        password = "",
                        user_agent = "")
    subreddit = reddit.subreddit("memes")
    top = subreddit.new(limit = 20)
    all_subs = []
    for post in top:
        all_subs.append(post.url)
    req = requests.get(random.choice(all_subs))
    with open('meme.jpg', 'wb') as file:
        file.write(req.content)
        file.close()
    with open('meme.jpg', 'rb') as file:
        data.subClient.send_message(chatId=data.chatId, file=file, fileType='image')
@client.command('prayers')
def prayers(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message='Insert the city name and country to get praying times\n[IC] Example: #prayers Cairo Egypt')
    else:
        msg = data.message.split(' ')
        req = requests.get(f'https://api.aladhan.com/v1/timingsByCity?city={msg[0]}&country={msg[1]}')
        data2 = json.loads(req.text)['data']['timings']
        f = "Fajr: "+data2['Fajr']
        d = "Dhuhr: "+data2['Dhuhr']
        a = "Asr: "+data2['Asr']
        m = "Maghrib: "+data2['Maghrib']
        i = "Isha: "+data2['Isha']
        x = str(msg[1])+", "+str(msg[0])
        data.subClient.send_message(chatId=data.chatId, message=f'[BC] Prayers in {x}\n[C]{f}\n[C]{d}\n[C]{a}\n[C]{m}\n[C]{i}', replyTo=data.messageId)
@client.command('hey')
def hey(data):
    data.subClient.send_message(chatId=data.chatId, message=f'[BC]Good morning, {data.author}!', replyTo=data.messageId)
@client.command('startvc', owner)
def startvc(data):
    try:
        data.subClient.start_vc(comId=data.comId, chatId=data.chatId)
    except:
        data.subClient.send_message(chatId=data.chatId, message='Need co-host', replyTo=data.messageId)
@client.command('endvc', owner)
def endvc(data):
    try:
        data.subClient.end_vc(comId=data.comId, chatId=data.chatId)
    except:
        data.subClient.send_message(chatId=data.chatId, message='Need co-host', replyTo=data.messageId)
@client.command('bg')
def bg(data):
    image = data.subClient.get_chat_thread(data.chatId).backgroundImage
    if image is not None:
        filename = image.split("/")[-1]
        urllib.request.urlretrieve(image, filename)
        with open(filename, 'rb') as fp:
            data.subClient.send_message(chatId=data.chatId, file=fp, fileType='image')
@client.command('temp')
def temp(data):
    req = requests.get('https://api.imgflip.com/get_memes')
    data1 = json.loads(req.text)
    x = random.randrange(100)
    y = data1['data']['memes'][x]['url']
    req2 = requests.get(y)
    with open('test.jpg', 'wb') as file:
        file.write(req2.content)
        file.close()
    with open('test.jpg', 'rb') as file:
        data.subClient.send_message(data.chatId, file=file, fileType='image')
@client.command('help')
def help(data):
    c = client.commands_list()
    x = '\n[IC] ⬤ - '.join(c)
    y = len(c)
    data.subClient.send_message(chatId=data.chatId, message=f'[BC]Commands:\n[IC] ⬤ - {x}\n[IC]Total commands: {y}\n[BC] Prefix: #', replyTo=data.messageId)
@client.command('av')
def av(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message='Example\n#av Hello', replyTo=data.messageId)
    link = f"http://api.brainshop.ai/get?bid=153868&key=rcKonOgrUFmn5usX&uid=1&msg={data.message}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    chatbot = json_data["cnt"]
    myobj = gTTS(text=chatbot, lang='en', slow=False)
    myobj.save('ai.mp3')
    with open('ai.mp3', 'rb') as file:
        data.subClient.send_message(chatId=data.chatId, file=file, fileType='audio')
@client.command('dance')
def dance(data):
    moves = ['└@(･◡･)@┐', '〜(￣▽￣〜)', 'ヘ(￣ー￣ヘ)', 'ヾ(´〇｀)ﾉ', '(´▽｀)ノ♪']
    data.subClient.send_message(chatId=data.chatId, message=random.choice(moves))
@client.command('at')
def at(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message='Example\n#at Hello', replyTo=data.messageId)
    link = f"http://api.brainshop.ai/get?bid=153868&key=rcKonOgrUFmn5usX&uid=1&msg={data.message}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    chatbot = json_data["cnt"]
    data.subClient.send_message(chatId=data.chatId, message=chatbot, replyTo=data.messageId)
 
@client.command('name', owner)
def name(data):
    data.subClient.edit_profile(nickname=data.message)
    data.subClient.send_message(chatId=data.chatId, message=f'updated name to {data.message}', replyTo=data.messageId)
@client.command('love')
def love(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message=f'{data.author} You need to mention 2', replyTo=data.messageId)
    else:
        data.message = data.message.split(' ')
        if len(data.message) == 1:
            data.subClient.send_message(chatId=data.chatId, message=f'[BC] You love {data.message[0].replace("@","")} by {random.randrange(100)}%')
        else:
            data.subClient.send_message(chatId=data.chatId, message=f'[BC]ヾ(´〇｀)ﾉ\n[IC]{data.message[0].replace("@", "")} loves {data.message[1].replace("@", "")} by {random.randrange(100)}% ', replyTo=data.messageId)
@client.command('weather')
def weather(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message='Please insert a city name')
    else:
        req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={data.message}&appid=APIKEY&units=metric')
        temp = json.loads(req.text)['main']['temp']
        status = json.loads(req.text)['weather'][0]['description']
        data.subClient.send_message(chatId=data.chatId, message=f"[BC] Weather in {data.message}\n[IC]{temp} ℃ \n[IC]{status}", replyTo=data.messageId)
@client.command('ping')
def ping(data):
    data.subClient.send_message(chatId=data.chatId, message='pong!', replyTo=data.messageId)
@client.command('dice')
def dice(data):
    num = ['one', 'two', 'three', 'four', 'five', 'six']
    data.subClient.send_message(chatId=data.chatId, message='Rolling...', replyTo=data.messageId)
    time.sleep(1)
    data.subClient.send_message(chatId=data.chatId, message=f'Ha, it\'s '+random.choice(num), replyTo=data.messageId)
@client.command('unfollow')
def unfollow(data):
    x = data.subClient.get_user_id(data.author)[1]
    data.subClient.unfollow_user(x)
    data.subClient.send_message(chatId=data.chatId, message=f'unfollowed {data.author}', replyTo=data.messageId)
@client.command('give')
def give(data):
    data.subClient.send_message(chatId=data.chatId, message=f'[I]*gives {data.message}*', replyTo=data.messageId)
@client.command('bio', owner)
def bio(data):
    data.subClient.edit_profile(content=data.message)
    data.subClient.send_message(chatId=data.chatId, message=f'updated bio to {data.message}', replyTo=data.messageId)
@client.command('quote')
def quote(data):
    req =requests.get('https://zenquotes.io/api/random')
    data1 = json.loads(req.text)
    quote = data1[0]['q']
    lol = data1[0]['a']
    data.subClient.send_message(chatId=data.chatId, message=f'{quote}\n-{lol}\n', replyTo=data.messageId)
@client.command('horse')
def horse(data):
    req = requests.get('https://thishorsedoesnotexist.com/')
    with open('horse.jpg', 'wb') as file:
        file.write(req.content)
        file.close()
    with open('horse.jpg', 'rb') as file:
        data.subClient.send_message(chatId=data.chatId, file=file, fileType='image')
@client.command('cat')
def cat(data):
    req = requests.get('https://thiscatdoesnotexist.com/')
    with open('cat.jpg', 'wb') as file:
        file.write(req.content)
        file.close()
    with open('cat.jpg', 'rb') as file:
        data.subClient.send_message(chatId=data.chatId, file=file, fileType='image')
@client.command('person')
def person(data):
    req = requests.get('https://thispersondoesnotexist.com/image')
    with open('person.jpg', 'wb') as file:
        file.write(req.content)
        file.close()
    with open('person.jpg', 'rb') as file:
        data.subClient.send_message(chatId=data.chatId, file=file, fileType='image')
@client.command('follow')
def follow(data):
    x = data.subClient.get_user_id(data.author)[1]
    data.subClient.follow_user(x)
    data.subClient.send_message(chatId=data.chatId, message=f"Followed, {data.author}", replyTo=data.messageId)
@client.command('source')
def source(data):
    data.subClient.send_message(chatId=data.chatId, message=f'[BC]Hello {data.author} this bot was made by @Human\n[IC] Bot source code: https://github.com/aliveHumans/The_bot/', replyTo=data.messageId)
@client.command('rpc')
def rpc(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message=f'[BC] Hello {data.author}\n[IC] To play rock, paper, scissors\n[IC] #rpc <rock, paper, scissors>', replyTo=data.messageId)
    else:
        choice = ['rock', 'paper', 'scissors']
        if data.message in choice[0] or choice[1] or choice[2]:
            computer = random.choice(choice)
            if computer == data.message:
                data.subClient.send_message(chatId=data.chatId, message=f'[BC]{computer}\n[IC] Draw', replyTo=data.messageId)
            elif data.message == choice[0] and computer == choice[1]:
                data.subClient.send_message(chatId=data.chatId, message=f'[BC]{computer}\n[IC] I win', replyTo=data.messageId)
            elif data.message == choice[1] and computer == choice[2]:
                data.subClient.send_message(chatId=data.chatId, message=f'[BC]{computer}\n[IC] I win', replyTo=data.messageId)
            elif data.message == choice[2] and computer == choice[0]:
                data.subClient.send_message(chatId=data.chatId, message=f'[BC]{computer}\n[IC] I win', replyTo=data.messageId)
            else:
                data.subClient.send_message(chatId=data.chatId, message=f'[BC]{computer}\n[IC] I lost', replyTo=data.messageId)
        else:
            data.subClient.send_message(chatId=data.chatId, message='Invalid option', replyTo=data.messageId)
@client.command('anime')
def anime(data):
    names = []
    with open('anime.txt', 'r') as file:
        for anime in file:
            names.append(anime)
        file.close()
    final = random.choice(names)
    data.subClient.send_message(chatId=data.chatId, message=f'[BC]{data.author} You should try:\n[IC]{final}', replyTo=data.messageId)
@client.command('donate')
def donate(data):
    data.subClient.send_message(chatId=data.chatId, message=f'[BC]Hello, {data.author}\n[IC] Visit @Human profile last post to donate', replyTo=data.messageId)
@client.command('about')
def about(data):
    data.subClient.send_message(chatId=data.chatId, message=f'[BC] Hey there {data.author}\n[IC] API\'s and stuff used:\n[IC]Chatbot : brainshop ai\n[IC] quotes: zenquotes\n[IC]Horse, person, cat : thisxdoesnotexist\n[IC] weather: openweathermap api\n[IC] Templates: imgflip api\n[IC] Reddit memes: praw\n[IC]Prayers : aladhan api\n[IC] screenshot :screenshotmachine api\n[BC]About me\n[IC]@Human or Sponge\n[IC]Age: 14', replyTo=data.messageId)
client.launch()
print("Ready!")
