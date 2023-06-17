import discord
import utils
import json

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)


    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if not message.channel.name == "봇":
            return
        if message.content[0] == '!':
            await message.channel.send('command executed : ' + message.content[1:])
            await commands.router(command = message.content[1:],message = message)
        if message.content == 'ping':
            await message.channel.send('pong')

class commands():
    async def getLevel(args, message):
        result = musics.find_level_by_title("".join(args))
        id, songtitle = result[0], result[1]
        if id != None:
            diffarr = musics.return_difficulty_by_id(id)
            print(diffarr)
            await message.channel.send(musics.convert_diff_to_message(songtitle,diffarr))
        else:
            await message.channel.send('no such music that has title %s'%(" ".join(args)))
    async def getSongInfo(args, message):
        result = musics.find_level_by_title("".join(args))
        id, songtitle = result[0], result[1]
        if id != None:
            arr = musics.songinfo_to_array(id)
            await musics.download_jacket_and_send(arr[5],message)
            await message.channel.send(musics.songinfo_to_string(arr))
            await message.channel.send(musics.convert_diff_to_message(arr[0], musics.return_difficulty_by_id(id)))
        else:
            await message.channel.send('no such music that has title %s'%(" ".join(args)))
    async def router(command, message):
        args = command.split()
        if(args[0].lower() == "getlevel"):
            try:
                await commands.getLevel(args[1:],message)
            except(Exception):
                await message.channel.send('check arguments')
                raise Exception
        if(args[0].lower() == "songinfo"):
            try:
                await commands.getSongInfo(args[1:],message)
            except(Exception):
                await message.channel.send('check arguments')
                raise Exception

if __name__ == "__main__" :
    f = open("token",'r')
    token = f.readline()
    f.close()
    musics = utils.Musics()
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(token)