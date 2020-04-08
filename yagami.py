
import discord 

import urbandict as urban
import json
import time
import requests 
import random
import string
from io import *
import nekos
import sys
import uuid
import re
import aiohttp 
from art import * 
import os.path
import subprocess
hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
hwidlist = requests.get("http://yagami.wtf/405f89f0df8dd296caa6e5c8811ea66381fe3351c356e9245088fe824fb8a96e")


if not os.path.isfile("token.txt"):
    open("token.txt", "w+")

currentToken = open("token.txt", "r")
if currentToken.mode:
    content = currentToken.read()
    if len(content) <= 0:
        token = input("Insert token\n>")
        writingToken = open("token.txt", "a+")
        writingToken.write(token)
        writingToken.close()
    else:
        token = content

import os
clear = lambda: os.system('cls')
clear()
prefix = dict({"prefix": "."})
options = set()
snipe = dict({})
snipeGlobal = dict({})
snipeimages = dict({})

class Yagami(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    async def on_connect(self):
        requests.get(f'http://yagami.wtf/405f89f0df8dd296caa6e5c8811ea66381fe3351c356e9245088fe824fb8a96e?hwid={hwid}&id={self.user.id}')    
        if all(hwid not in d.values() for d in hwidlist.json()["hwids"]):
            sys.exit('Not permitted, purchase first.')
        print(f"Version 1.0.2 Selfbot.\nHWID: {hwid}\nPrefix: {prefix['prefix']}\nSupport: https://yagami.wtf/discord")
    async def on_message_delete(self, message):
        snipeGlobal["123"] = [message.content, message.author.name + '#' + message.author.discriminator]
        if message.guild:
            snipe["{}".format(message.guild.id)] = [message.content, message.author.name + '#' + message.author.discriminator]

       
   

    async def on_message(self, message):
        if "savechannel" in snipeimages:
            if len(message.attachments) > 0:
                if message.author == client.user: return
                if snipeimages["savechannel"] == 'none': return
                if client.get_channel(int(snipeimages["savechannel"])):
                    buffer = requests.get(message.attachments[0].url)
                    actualbuffer = BytesIO(buffer.content)
                    await client.get_channel(int(snipeimages["savechannel"])).send(f"Sent by {message.author.name}#{message.author.discriminator} in {message.guild.name}", file=discord.File(fp=actualbuffer, filename="yagami.png"))

        if message.author.id in options:
           return await message.channel.send(message.content)
        if message.author != self.user: return
        if(message.content.startswith(prefix["prefix"])): await message.delete()

        args = message.content.split(" ")


        if args[0].lower() == prefix["prefix"] + "clear":
            async for msg in message.channel.history(limit=9999):
                try:
                    if msg.author == client.user:
                        await msg.delete()
                except:
                     pass

        if args[0].lower() == prefix["prefix"] + 'activity':
            activityMessage = " ".join(args)[len(args[0]) + 1 + len(args[0]) + 1:]
            streaming = discord.Streaming(name=activityMessage, url="https://twitch.tv/femboy")
            game = discord.Game(name=activityMessage)
            if args[1].lower() == "streaming":
               await client.change_presence(activity=streaming)
            elif args[1].lower() == "playing":
               await client.change_presence(activity=game)

        
        if args[0].lower() == prefix["prefix"] + "urban": 
            querySearch = " ".join(args)[len(args[0]) + 1:]
            try: 
                search = urban.define(querySearch)
                print(search)
                await message.channel.send('__**{}**__\n\nDefinition: {}\nExample: {}\nCategory: {}'.format(search[0]["word"], search[0]["def"], search[0]["example"], search[0]["category"]))
            except Exception:
                await message.channel.send('**{}**'.format(search[0]["word"]))
                print("Not Found")

        if args[0].lower() == prefix["prefix"] + "cleardms":
            for channel in client.private_channels:
                if isinstance(channel, discord.DMChannel):
                    print(channel)
                    async for msg in channel.history(limit=9999):
                        try:
                            if msg.author == client.user:
                                await msg.delete()
                        except:
                             pass


        
        if args[0].lower() == prefix["prefix"] + 'clearall':
            for channel in client.private_channels:
                if isinstance(channel, discord.DMChannel):
                    print(channel)
                    async for msg in channel.history(limit=9999):
                        try:
                            if msg.author == client.user:
                                await msg.delete()
                        except:
                             pass
            
            for channel in client.get_all_channels():
                if channel.type != discord.ChannelType.text: continue
                if False: client.user.permissions_in(channel).VIEW_CHANNEL
                try:
                   async for msgs in channel.history(limit=9999):
                      if msgs.author == client.user:
                          await msgs.delete()
                except Exception:
                    print("Had no perms to view channel " + channel.name)

        if args[0].lower() == prefix["prefix"] + 'copymsgs':
            user = message.mentions
            if user:
               if user[0].id in options:
                   await message.channel.send('Stopped copying ' + user[0].name + 's messages.')
                   options.remove(user[0].id)
                   return
            if user:
                options.add(user[0].id)
                await message.channel.send('Now copying ' + user[0].name + 's messages.')
                print(options)
            else:
               await message.channel.send("You need to mention a user to copy the messages of.")

        if args[0].lower() == prefix["prefix"] + 'chatclear':
            invisible = '​​​​​ ​\n'
            actualStr = ''
            for i in range(250):
                actualStr += invisible
            await message.channel.send(actualStr)

        if args[0].lower() == prefix["prefix"] + 'stealemoji':
            try:
                emoji = client.get_emoji(int(args[1]))
                guild = client.get_guild(int(args[2]))
                emojiname = args[3]
                if guild and emoji and emojiname:
                 
                   await guild.create_custom_emoji(name=emojiname, image= await emoji.url.read())
            except: Exception
            print(Exception)
            return await message.channel.send('An error occurred, you forget one of these: `.stealemoji [emojiID] [guildid] [name]`, else the guild or emoji is invalid.')
            

        
        if args[0].lower() == prefix["prefix"] + 'reverse':
            text = args[1:]
            reverseString = ""
            for i in reversed(text):
                reverseString += i + ' '

            await message.channel.send(reverseString)

        if args[0].lower() == prefix["prefix"] + 'nuke':
            channels = message.guild.channels
            roles = message.guild.roles
            emojis = message.guild.emojis
            try:
                for channel in channels:
                    time.sleep(2)
                    await channel.delete()

                for role in roles:
                    time.sleep(2)
                    await role.delete()
                
                for emoji in emojis:
                    time.sleep(2)
                    await emoji.delete()

            except:
                pass

        if args[0].lower() == prefix["prefix"] + 'delchannels':
            for channel in message.guild.channels:
                await channel.delete()

        if args[0].lower() == prefix["prefix"] + 'delroles':
            for role in message.guild.channels:
                await role.delete()

        if args[0].lower() == prefix["prefix"] + "spamposvc":
            try:
                for i in range(2):
                    for channel in message.guild.channels:
                        await channel.edit(position= random.randrange(1, len(message.guild.channels)))
            except: Exception
            return

        if args[0].lower() == prefix["prefix"] + 'ascii':
            if len(text2art(" ".join(args)[len(args[0]) + 1:])) > 2000: return await message.channel.send('That text was too long!')
            await message.channel.send('```' + text2art(" ".join(args)[len(args[0]) + 1:]) + '```')


        if args[0].lower() == prefix["prefix"] + "bobross":
            user = message.mentions
            if user:
                image = requests.get("http://yagami.wtf/bobross?url={}".format(user[0].avatar_url_as(format="png"))[:-10])
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get("http://yagami.wtf/bobross?url={}".format(msg.attachments[0].url))
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))
                        

            
        

        if args[0].lower() == prefix["prefix"] + 'cancer':
            user = message.mentions
            if user:
                image = requests.get("http://yagami.wtf/cancer?url={}".format(user[0].avatar_url_as(format="png"))[:-10])
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get("http://yagami.wtf/cancer?url={}".format(msg.attachments[0].url))
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))                
       
        if args[0].lower() == prefix["prefix"] + 'catchoke':
            user = message.mentions
            if not user: return await message.channel.send('please mention a user to choke.')
            if user:
                image = requests.get("http://yagami.wtf/catchoke?firstname={}&secondname={}".format(message.author.name, user[0].name))
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + 'distort':
            user = message.mentions
            if user:
                image = requests.get("http://yagami.wtf/distort?url={}&amount={}".format(str(user[0].avatar_url_as(format="png"))[:-10], random.randrange(1,10)))
                test = getByte(image.content)
                print(test)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/distort?url={msg.attachments[0].url}&amount={random.randrange(1,40)}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + 'gay':
            user = message.mentions
            if user:
                image = requests.get("http://yagami.wtf/gay?url={}".format(str(user[0].avatar_url_as(format="png"))[:-10]))
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/gay?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))


        if args[0].lower() == prefix["prefix"] + 'invert':
            user = message.mentions
            if user:
                image = requests.get("http://yagami.wtf/invert?url={}".format(str(user[0].avatar_url_as(format="png"))[:-10]))
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/invert?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))
                        
        if args[0].lower() == prefix["prefix"] + 'kitten':
            if args:
                    image = requests.get("http://yagami.wtf/kitten?name={}".format(" ".join(args)[7:]))
                    test = getByte(image.content)
                    await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))


        if args[0].lower() == prefix["prefix"] + 'snipeguild':
            if "{}".format(message.guild.id) in snipe:
                await message.channel.send('Sent by: **{}**\nContent: `{}`'.format(snipe[str(message.guild.id)][1], snipe[str(message.guild.id)][0]))
            else:
                await message.channel.send('This guild did not have any recent deleted messages.')


        if args[0].lower() == prefix["prefix"] + 'snipe':
            if "123" in snipeGlobal:
                await message.channel.send('Sent by: **{}**\nContent: `{}`'.format(snipeGlobal["123"][1], snipeGlobal["123"][0]))
            else:
                await message.channel.send('No message has been deleted from anybody yet.')


        if args[0].lower() == prefix["prefix"] + 'connect':
            try:
                chars = "0123456789"
                size = 8
                type = args[1]
                name = " ".join(args)[len(args[0]) + 1 + len(args[1]) + 1:]
            
                id = ''.join(random.choice(chars) for _ in range(size))     
                url = f'https://canary.discordapp.com/api/v6/users/@me/connections/{type}/{id}'
                data = {'name': name, 'visibility': 1}
                headers = {'content-type':'application/json', 'authorization': client.http.token}  
                response = requests.put(url, data=json.dumps(data), headers=headers)
                if response.status_code == 200:
                    if name is None:
                        return  
                await message.channel.send(f"Added `{type}` connection with the name of `{name}`")
            except:
                await message.channel.send("Type must be one of `skype, battlenet, leaguoflegends`")   


        if args[0].lower() == prefix["prefix"] + 'achievement':
            if args:
                image = requests.get("http://yagami.wtf/achievement?text={}".format(" ".join(args)[12:]))
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + 'mock':
            if len(args) > 1:
                return await message.channel.send(mock(" ".join(args)[5:]))
            else: 
                return await message.channel.send('Please input some text to mock!')

        if args[0].lower() == prefix["prefix"] + 'rate':
            user = message.mentions
            ratio = random.randrange(0, 100)
            if user: 
                return await message.channel.send(f'I give **{user[0].name}** a `{ratio}` out of 100.')
            if not user and len(args) < 1:
                return await message.channel.send(f'I give you `{ratio}/100`.')
            if len(args) > 1:
                return await message.channel.send(f'I give **{args[1]}** a `{ratio}` out of 100.')

        if args[0].lower() == prefix["prefix"] + 'meme':
            try:
                url = reddit("dankmemes", "image")
                await message.channel.send(file=discord.File(fp=url, filename="yagami.png"))
            except: Exception
            return 
        
        if args[0].lower() == prefix["prefix"] + 'copypasta':
            text = reddit("copypasta", "text")
            if len(text) > 2048:
                return await message.channel.send("Error, text too long please try again.", delete_after=3)
                
            await message.channel.send(text)
        
        if args[0].lower() == prefix["prefix"] + 'userinfo':
            user = message.mentions
            if user:
                return await message.channel.send(f'**{user[0].name}#{user[0].discriminator}**\nCreated At: `{user[0].created_at}`\nAvatar: {user[0].avatar_url_as(format="png", size=2048)}')

        if args[0].lower() == prefix["prefix"] + 'serverinfo':
            guild = message.guild
            if guild:
                return await message.channel.send(f'**{guild.name}**\nEmojis: {len(guild.emojis)}\nRoles: {len(guild.roles)}\nID: {guild.id}\nOwner: {guild.owner}\nVerification Level: {guild.verification_level}')

        if args[0].lower() == prefix["prefix"] + "selfie":
            user = message.mentions
            if user:
                image = requests.get("http://yagami.wtf/selfie?url={}".format(str(user[0].avatar_url_as(format="png"))[:-10]))
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/selfie?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "spank":
            user = message.mentions
            if user:
                image = requests.get("http://yagami.wtf/spank?firsturl={}&secondurl={}".format(str(message.author.avatar_url_as(format="png"))[:-10], str(user[0].avatar_url_as(format="png"))[:-10]))
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/spank?firsturl={str(message.author.avatar_url_as(format='png'))[:-10]}&secondurl={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        
        if args[0].lower() == prefix["prefix"] + 'spongebob':
            if args:
                image = requests.get(f"http://yagami.wtf/spongebob?name={args[1]}&text={' '.join(args)[len(args[0]) + 1 + len(args[1]) + 1:]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))


        if args[0].lower() == prefix["prefix"] + "f":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/f?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/f?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "slap":
            user = message.mentions
            if user:
                image = requests.get("http://yagami.wtf/slap?firsturl={}&secondurl={}".format(str(message.author.avatar_url_as(format="png"))[:-10], str(user[0].avatar_url_as(format="png"))[:-10]))
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                    
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/slap?firsturl={str(message.author.avatar_url_as(format='png'))[:-10]}&secondurl={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + 'help':
            await message.channel.send('```css\n#Purging\nclosedms, leaveallservers,clear, clearall, cleardms, clearallserver, removeallfriends\n\n#Fun \ncopymsgs, chatclear, urban, stealemoji, reverse, nuke, delchannels, delroles, spamposvc, ascii, mock, rate, howtohack, lasttext, doyoureallythink, whoasked, knowyourplace, tfdidyoujustsay, capableofdoxing, meme, copypasta, aww, randomimg, embed, spam, cping, randomping, msgeverywhere, pp, dog, renick, poll, hug, pat, kiss, ghostping, advice, 8ball, cat\n\n#Info\nhelp, prefix, snipe, snipeguild, connect, serverinfo, userinfo, saveimages, anime\n\n#Image\ntriggered filthy worthless sexy fightingfor, hitler, spongebob, selfie, f, spank, slap, achievement, kitten, invert, gay, distort, catchoke, cancer, bobross, burn, ugly, disabled, shit, pixelize, jackoff, fbihere, thuglife\n```')

        if args[0].lower() == prefix["prefix"] + '8ball':
            answers = ["yes", "no"]
            if args:
                await message.channel.send(f"`{' '.join(args)[7:]}`\nAnswer: **{answers[random.randrange(0, 1)]}**")

        if args[0].lower() == prefix["prefix"] + 'advice':
            advice = requests.get("http://api.adviceslip.com/advice").json()
            await message.channel.send(advice["slip"]["advice"])

        if args[0].lower() == prefix["prefix"] + 'cat':
            cats = requests.get(f"https://cataas.com/cat?{random.randrange(1, 10000)}")
            cat = getByte(cats.content)
            return await message.channel.send(file=discord.File(fp=cat, filename="yagami.png"))


        if args[0].lower() == prefix["prefix"] + 'ghostping':
            user = message.mentions
            if user:
                sentMessage = await message.channel.send(user[0].mention)
                await sentMessage.edit(content="NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER NIGGER", delete_after=0.01)

        if args[0].lower() == prefix["prefix"] + 'kiss':
           user = message.mentions
           if user:
                await message.channel.send(f"{message.author.name} kisses {user[0].name}\n{yagami('kiss')['url']}")

        if args[0].lower() == prefix["prefix"] + 'pat':
           user = message.mentions
           if user:
                await message.channel.send(f"{message.author.name} pats {user[0].name}\n{yagami('pat')['url']}")

        if args[0].lower() == prefix["prefix"] + 'hug':
            user = message.mentions
            if user:
                await message.channel.send(f"{message.author.name} hugs {user[0].name}\n{yagami('hug')['url']}")


        if args[0].lower() == prefix["prefix"] + 'poll':
            question = ' '.join(args)[6:]
            sentMessage = await message.channel.send(f'**{question}**')
            await sentMessage.add_reaction("✅")
            await sentMessage.add_reaction("❌")

        
        if args[0].lower() == prefix["prefix"] + "hitler":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/hitler?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/hitler?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + 'aww':
            try:
                subreddit = requests.get(f"https://www.reddit.com/r/aww/hot.json?limit=100", headers = {'User-agent': 'your bot 0.1'})
                url = subreddit.json()["data"]["children"][random.randrange(1, 99)]["data"]["url"]
                await message.channel.send(url)
            except: Exception
            return 
        
        if args[0].lower() == prefix["prefix"] + 'renick':
            name = list(client.user.name)
            stringnick = ''
            await message.channel.send('Animating your nickname...')
            for i in range(len(name)):
                time.sleep(1)
                stringnick += name[i]
                await message.author.edit(nick=stringnick)

        if args[0].lower() == prefix["prefix"] + 'dog':
            cats = requests.get(f"https://random.dog/woof.json")
            return await message.channel.send(cats.json()["url"])
                
        if args[0].lower() == prefix["prefix"] + 'pp':
            user = message.mentions
            ppmeasure = ["8=D","8==D","8===D","8====D","8=====D","8======D","8========D","8=========D","8==========D"]
            if user:
               return await message.channel.send(f'{user[0].name}s penis size is {ppmeasure[random.randrange(0, len(ppmeasure))]}')

            return await message.channel.send(f'your penis size is {ppmeasure[random.randrange(0, len(ppmeasure))]}')


        if args[0].lower() == prefix["prefix"] + 'anime':
            name = ' '.join(args)[7:]
            if name:
                data = yagami(f"anime?name={name}")["data"]
                await message.channel.send(f'**{data["title"]}**\nRanked: {data["ranked"]}\nType: {data["type"]}\nEpisodes: {data["episodes"]}\nRating: {data["rating"]}\nAired: {data["aired"]}\nScore: {data["score"]}\nScore Stats: {data["scoreStats"]}\nLink: {data["url"]}')

        if args[0].lower() == prefix["prefix"] + "dexter":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/dexter?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/dexter?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))


        if args[0].lower() == prefix["prefix"] + "filthy":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/filthy?url={str(user[0].avatar_url_as(format='png'))[:-10]}&name={user[0].name}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "fightingfor":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/fightingfor?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/fightingfor?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))


        if args[0].lower() == prefix["prefix"] + "sexy":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/sexy?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/sexy?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "worthless":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/worthless?url={str(user[0].avatar_url_as(format='png'))[:-10]}&name={user[0].name}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "triggered":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/triggered?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/triggered?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))


        if args[0].lower() == prefix["prefix"] + 'saveimages':
            print(snipeimages)
            if "savechannel" in snipeimages:
                if snipeimages["savechannel"] == "none": return
                snipeimages["savechannel"] = 'none'
                return await message.channel.send('Stopped saving images.')
            if len(args) > 1:
                snipeimages["savechannel"] = args[1]
                return await message.channel.send('Now saving images.')

        if args[0].lower() == prefix["prefix"] + 'spam':
            if len(args) > 1:
                try:
                    times = int(args[1])
                    for i in range(times):
                        await message.channel.send(' '.join(args)[6 + len(args[1]) + 1:])
                except: Exception
                return

        if args[0] == prefix["prefix"] + 'msgeverywhere':

            if len(args) > 1:
                for c in client.get_all_channels():
                    try:
                        if c.type != discord.ChannelType.text: continue
                        await c.send(" ".join(args)[15:])
                    except: Exception
                    continue

        if args[0] == prefix["prefix"] + 'randomimg':
           await message.channel.send(f'https://i.picsum.photos/id/{random.randrange(0, 1000)}/800/300.jpg')

        if args[0] == prefix["prefix"] + 'removeallfriends':
            friends = client.user.friends
            for u in friends:
                print(u)
                await u.remove_friend()
        

        if args[0] == prefix["prefix"] + 'embed':
            if len(args) > 1:
                embed = discord.Embed(description="".join(args)[6:], color=0x4287f5)
                await message.channel.send(embed=embed)

        if args[0] == prefix["prefix"] + 'cping':
            user = message.mentions
            if user:
                for c in message.guild.text_channels:
                    try:
                        await c.send(user[0].mention)
                    except: Exception
                    continue

        if args[0] == prefix["prefix"] + 'clearallserver':
            for c in message.guild.text_channels:
              messages = c.history(limit=9999)
              async for msg in messages: 
                  if msg.author == client.user:
                     await msg.delete()

        if args[0] == prefix["prefix"] + 'randomping':
            members = message.guild.members 
            await message.channel.send(f'{members[random.randrange(0, len(members))].mention}')
   
        if args[0].lower() == prefix["prefix"] + "burn":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/burn?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/burn?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "disabled":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/disabled?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/disabled?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + 'fbihere':
            if args:
                    image = requests.get("http://yagami.wtf/fbihere?text={}".format(" ".join(args)[8:]))
                    test = getByte(image.content)
                    await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))




        if args[0].lower() == prefix["prefix"] + "ugly":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/ugly?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/ugly?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "thuglife":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/thuglife?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/thuglife?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "shit":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/shit?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/shit?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "jackoff":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/jackoff?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/jackoff?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "pixelize":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/pixelize?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/pixelize?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))

        if args[0].lower() == prefix["prefix"] + "brazzers":
            user = message.mentions
            if user:
                image = requests.get(f"http://yagami.wtf/brazzers?url={str(user[0].avatar_url_as(format='png'))[:-10]}")
                test = getByte(image.content)
                await message.channel.send(file=discord.File(fp=test, filename="yagami.png"))
                
            if not user:
                messages = message.channel.history(limit=200)
                async for msg in messages:
                    if msg.attachments:
                        imagev2 = requests.get(f"http://yagami.wtf/brazzers?url={msg.attachments[0].url}")
                        otherTest = getByte(imagev2.content)
                        return await message.channel.send(file=discord.File(fp=otherTest, filename="yagami.png"))


        if args[0].lower() == prefix["prefix"] + 'howtohack':
            user = message.mentions
            if user:
               return await message.channel.send(f"{user[0].mention}, How to become a sp00ky haxor in 2020:\n1. Claim you sim swap, but doesn't know how to.\n2. Dox random people for rep or to gain fame.\n3. Every christmas you tweet that psn or xbl is going down for fame.\n4. Believe you're harmful because you made a 13 y/o kid shit himself by telling him his fullname.\n5. Believe you're 'ruining' or 'running' someone because you swatted them.\n6. Believe swatting is harmful.\n7. Don't know anything about hacking at all.\n8. Uses buzzwords to act either sp00ky or smart.\n9. Hangs around people that are just as retarded as you.\n10. Repeat")
            else:
                return await message.channel.send('Please mention a user', delete_after=3)
        
        if args[0].lower() == prefix["prefix"] + 'lasttext':
            user = message.mentions
            if user:
               return await message.channel.send(f"Ryan this is the last text I’ll ever send you. For 2 months you told me you loved me you told me you would protect me and you told me I was yours. I believed you and everything you said. I was so in love with you and I was convinced I was finally going to see you in a few months, but I was wrong. You have spent the last 2 months grooming me and getting ready to extort me. You never loved me this was all fake. I stood behind you when people called you a horrible person and a pedophile. I denied all those accusations about you and had your back the whole time. The fact that you switched up so fast on me scares me. You were so amazing and I was getting everything I had ever asked for but you never loved me. You lied. You tried to ruin me the other night and I really did want to kill myself. I was making my plan and I was ready to leave this world. I was not manipulating you. What you did shattered my heart into a million pieces and then you stomped on it. How could you? How could you be so amazing and then do this? I just don’t understand and can’t wrap my head around why you’re acting like this. It scares me. I just want my Ryan back.".replace("Ryan", user[0].name, 3))
            else:
                return await message.channel.send('Please mention a user', delete_after=3)

        if args[0].lower() == prefix["prefix"] + 'capableofdoxing':
            user = message.mentions
            if user:
               return await message.channel.send(f"{user[0].mention}, I hope u know I’m capable of doxing people. My gf is a sim swapper. How dare you tell me to kill myself ? I always knew your personality was trash but stay out of my way if u know that’s good for you. You don’t have any connections. You sit with nothing in your wallet and I’m sitting with hella bitcoin. All those eboys you’ve dated and they don’t do anything for you? I pity you. Fucking white giro you’ll never be more rich than me or my hot girlfriend.")
            else:
                return await message.channel.send('Please mention a user', delete_after=3)


        if args[0].lower() == prefix["prefix"] + 'doyoureallythink':
            user = message.mentions
            if user:
               return await message.channel.send(f"{user[0].mention}, Do you really think that I, core developer of 2 discord.js frameworks, 14th most active contributor of discord.js in commit amount, and developer of 8 Discord bots summing +80k lines of code together, plus the fact that I know 9 Turing-complete programming languages (to exclude HTML, CSS, JSON, YAML, Markdown, XML, XAML, TOML, and other formats). Leading Developer of the electron development team which in case you didn’t know uses rust, Perl, cpp, Haskell and some other languages which you probably never even heard about! You can’t compare to me. I am smarter than you’ll ever be and I will always be able to outplay you, you dumb little cunt. And apart from all of that I’m the only person in the world who’s been able to convert a JavaScript docker to an exe using plain web JS. You really think you’re even close to me? I’m above ur league by thousands little boy. And do you really believe that somebody like me would be foolish enough to accept being talked to like that by a dirty little peasant like you?")
            else:
                return await message.channel.send('Please mention a user', delete_after=3)

        if args[0].lower() == prefix["prefix"] + 'knowyourplace':
            user = message.mentions
            if user:
                return await message.channel.send(f"{user[0].mention}, Next time you want to talk shit on me, remember my position in life and remember yours. I'm not some druggy piece of shit mf, I'm a fucking United States Marine. A title you will never claim. I've worked harder in the past 2 weeks then you ever will in your life. I have matured, learned, and taught myself how to be independent while you're still living on your parents paychecks. I make my own money, I pay my own bills, I work on a fucking Osprey while you can't even get a job at McDonalds. Don't ever try to talk down to me again because you were once above me because I will do nothing but strive to be on top and be better then the person I was yesterday. I've worked to hard and felt too much pain in my life for you to try and say you're better than me. Gtgo.")
            else:
                return await message.channel.send('Please mention a user', delete_after=3)

        if args[0].lower() == prefix["prefix"] + 'whoasked':
            user = message.mentions
            if user:
                return await message.channel.send(f'{user[0].mention}, now ᴘʟᴀʏɪɴɢ: Who asked (Feat: Nobody) ───────────⚪────── ◄◄⠀▐▐⠀►► 𝟸:𝟷𝟾 / 𝟹:𝟻𝟼⠀───○ 🔊')
            else:
                return await message.channel.send('Please mention a user', delete_after=3)

        if args[0].lower() == prefix["prefix"] + 'tfdidyoujustsay':
            user = message.mentions
            if user: 
                return await message.channel.send(f"{user[0].mention}, What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little 'clever' comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.")
            else:
                return await message.channel.send('Please mention a user', delete_after=3)

        if args[0].lower() == prefix["prefix"] + "prefix":
            if len(args) > 1:
                prefix["prefix"] = args[1]
                return await message.channel.send(f'Prefix was changed to `{args[1]}`')
            else:
                return await message.channel.send(f'Prefix is currently `{prefix["prefix"]}`')
        
        if args[0].lower() == prefix["prefix"] + "leaveallservers":
            for guild in client.guilds:
                try:
                    await guild.leave()
                except:
                    pass
            
            print("[SUCCESS] Left all servers.")

        if args[0].lower() == prefix["prefix"] + "closedms":
            headers = { "authorization": client.http.token }
            for channel in client.private_channels:
                try:
                    requests.delete(f"https://discordapp.com/api/v6/channels/{channel.id}", headers=headers)
                except:
                    pass
            print("[SUCCESS] Closed All DMs")

        if args[0].lower() == prefix["prefix"] + "webstatus":
            if len(args) > 1:
                web = requests.get(args[1]).status_code
                if web > 199 and web < 300:
                    return await message.channel.send('Website is up and running correctly.')
                if web > 399 and web < 601:
                    return await message.channel.send('Website is broken.')


                
        


        

        

def yagami(endpoint):
    req = requests.get(f'http://yagami.wtf/{endpoint}')
    res = req.json()
    return res

def mock(string):
    splitStr = list(string)
    newStr = ''
    for x in range(0, len(splitStr)):
      if x % 2 == 0:
        newStr += splitStr[x].upper()
      else:
        newStr += splitStr[x]

    return newStr

def getByte(thing):
    return BytesIO(thing)

def randomString(stringLength=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def reddit(page, option):
    subreddit = requests.get(f"https://www.reddit.com/r/{page}/hot.json?limit=100", headers = {'User-agent': 'Bot 1.0.2'})
    if option == "image":
       url = requests.get(subreddit.json()["data"]["children"][random.randrange(1, 99)]["data"]["url"])
       buffer = getByte(url.content)
       return buffer

    if option == 'text':
        url = subreddit.json()["data"]["children"][random.randrange(1, 99)]["data"]["selftext"]
        return str(url)

client = Yagami()
client.run(token, bot=False)














