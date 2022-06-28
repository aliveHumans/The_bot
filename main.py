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

print("Wait..")
client = BotAmino("", "")
client.prefix = "#"
client.self_callable = False 
client.wait = 2


def owner(data: Parameters):
    return data.authorId in ["your_id"]
@client.on_member_join_chat()
def say_hello(data: Parameters):
    words = [' just landed!', 'Hey hey, ', 'welcome here, ', 'hi, how are you?, ']
    x = random.choice(words)
    data.subClient.send_message(data.chatId, f"{data.author} {x}", replyTo=data.messageId)
@client.command('math')
def math(data):
    data.message = data.message.split(' ')
    x = int(data.message[0])
    op = str(data.message[1])
    y = int(data.message[2])
    if op == '+':
        result = float(x) + float(y)
        data.subClient.send_message(chatId=data.chatId, message=f'Result: {result}')
    elif op == '-':
        result = float(x) - float(y)
        data.subClient.send_message(chatId=data.chatId,message=f'Result: {result}')
    elif op == '*':
        result = float(x) * float(y)
        data.subClient.send_message(chatId=data.chatId,message=f'Result: {result}')
    elif op == '/':
        result = float(x) / float(y)
        data.subClient.send_message(chatId=data.chatId,message=f'Result: {result}')
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
    data.subClient.send_message(data.chatId,"Updated wall messsage!")
@client.command('wiki')
def wiki(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message='Please insert a topic')
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
    if data.message in 'http://aminoapps.com' or 'https://aminoapps.com':
        data.subClient.join_chatroom(data.message)
        data.subClient.send_message(chatId=data.chatId, message='Joined',replyTo=data.messageId)
    else:
        data.subClient.send_message(chatId=data.chatId, message='Invalid link',replyTo=data.messageId)

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
        data.subClient.send_message(chatId=data.chatId, message='Insert the city name to get praying times')
    else:
        req = requests.get(f'https://api.aladhan.com/v1/timingsByCity?city={data.message}&country=United%20Arab%20Emirates&method=8')
        data2 = json.loads(req.text)['data']['timings']
        f = "Fajr: "+data2['Fajr']
        d = "Dhuhr: "+data2['Dhuhr']
        a = "Asr: "+data2['Asr']
        m = "Maghrib: "+data2['Maghrib']
        i = "Isha: "+data2['Isha']
        data.subClient.send_message(chatId=data.chatId, message=f'[BC] Prayers in {data.message}\n[C]{f}\n[C]{d}\n[C]{a}\n[C]{m}\n[C]{i}')
@client.command('startvc')
def startvc(data):
    try:
        data.subClient.send_message(chatId=data.chatId, message='Starting vc in 5 seconds...')
        time.sleep(5)
        data.subClient.start_vc(comId=data.comId,chatId=data.chatId)
    except:
        data.subClient.send_message(chatId=data.chatId, message='Need co-host for that!')
@client.command('endvc')
def endvc(data):
    try:
        data.subClient.send_message(chatId=data.chatId, message='ending vc')
        data.subClient.end_vc(comId=data.comId, chatId=data.chatId)
    except:
        data.subClient.send_message(chatId=data.chatId, message="Need co-host for that!")
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
    data.subClient.send_message(chatId=data.chatId, message=f'[BC]Commands:\n[IC] ⬤ - {x}\n[BC] Prefix: #')
@client.command('av')
def av(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message='Example\n#av Hello')
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
        data.subClient.send_message(chatId=data.chatId, message='Example\n#at Hello')
    link = f"http://api.brainshop.ai/get?bid=153868&key=rcKonOgrUFmn5usX&uid=1&msg={data.message}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    chatbot = json_data["cnt"]
    data.subClient.send_message(chatId=data.chatId, message=chatbot, replyTo=data.messageId)
 
@client.command('name', owner)
def name(data):
    data.subClient.edit_profile(nickname=data.message)
    data.subClient.send_message(chatId=data.chatId, message=f'updated name to {data.message}')
@client.command('love')
def love(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message=f'{data.author} You need to mention 2')
    else:
        data.message = data.message.split(' ')
        data.subClient.send_message(chatId=data.chatId, message=f'[BC]ヾ(´〇｀)ﾉ\n[IC]{data.message[0].replace("@", "")} loves {data.message[1].replace("@", "")} py {random.randrange(100)}% ')
@client.command('weather')
def weather(data):
    if data.message == '':
        data.subClient.send_message(chatId=data.chatId, message='Please insert a city name')
    else:
        # YOu can get free openweathermap API key from the website
        req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={data.message}&appid=YOURAPIKEY&units=metric')
        temp = json.loads(req.text)['main']['temp']
        status = json.loads(req.text)['weather'][0]['description']
        data.subClient.send_message(chatId=data.chatId, message=f"[BC] Weather in {data.message}\n[IC]{temp} ℃ \n[IC]{status}")
@client.command('ping')
def ping(data):
    data.subClient.send_message(chatId=data.chatId, message='pong!')
@client.command('dice')
def dice(data):
    num = ['one', 'two', 'three', 'four', 'five', 'six']
    data.subClient.send_message(chatId=data.chatId, message='Rolling...')
    time.sleep(1)
    data.subClient.send_message(chatId=data.chatId, message=f'Ha, it\'s '+random.choice(num))
@client.command('unfollow')
def unfollow(data):
    x = data.subClient.get_user_id(data.author)[1]
    data.subClient.unfollow_user(x)
    data.subClient.send_message(chatId=data.chatId, message=f'unfollowed {data.author}')
@client.command('give')
def give(data):
    data.subClient.send_message(chatId=data.chatId, message=f'[I]*gives {data.message}*')
@client.command('bio', owner)
def bio(data):
    data.subClient.edit_profile(content=data.message)
    data.subClient.send_message(chatId=data.chatId, message=f'updated bio to {data.message}')
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
    data.subClient.send_message(chatId=data.chatId, message=f"Followed, {data.author}")
@client.command('about')
def about(data):
    data.subClient.send_message(chatId=data.chatId, message=f'[BC] Hey there {data.author}\n[IC] API\'s and stuff used:\n[IC]Chatbot : brainshop ai\n[IC] quotes: zenquotes\n[IC]Horse, person, cat : thisxdoesnotexist\n[IC] weather: openweathermap api\n[IC] Templates: imgflip api\n[IC] Reddit memes: praw\n[IC]Prayers : aladhan api\n[IC] screenshot :screenshotmachine api\n[BC]About me\n[IC]@Human')
client.launch()
print("Ready!")
