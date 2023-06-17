import discord
import json
from constants_ko import Constants
import aiohttp
import io
import os

class Musics:
    def __init__(self, musicspath = './sekai-master-db-diff-main/musics.json', difficultiespath = './sekai-master-db-diff-main/musicDifficulties.json'):
        with open(musicspath, encoding="UTF-8") as f:
            self.musicsdata = json.load(f)
        with open(difficultiespath, encoding="UTF-8") as f:
            self.difficultydata = json.load(f)
        with open('./sekai-i18n-main/ko/music_titles.json', encoding="UTF-8") as f:
            self.koreansongnames = json.load(f)
    def bootstrap(self, musicspath = './sekai-master-db-diff-main/musics.json', difficultiespath = './sekai-master-db-diff-main/musicDifficulties.json'):
        with open(musicspath) as f:
            self.musicsdata = json.load(f)
        with open(difficultiespath) as f:
            self.difficultydata = json.load(f)
    def find_level_by_title(self, title):
        for i in self.musicsdata:
            if title.lower().replace(' ','') in i['title'].lower().replace(' ',''):
                return [i['id'], i['title']]
        for i in self.koreansongnames:
            if title.lower().replace(' ','') in self.koreansongnames[str(i)].lower().replace(' ',''):
                return [int(i), self.koreansongnames[str(i)]]
        return None, None
    def return_difficulty_by_id(self,musicid):
        difficulties = ['?' for _ in range(5)]
        for i in self.difficultydata:
            if i['musicId'] == musicid:
                diff = Constants.musicDifficulties.index(i['musicDifficulty'])
                difficulties[diff] = i['playLevel']
        return difficulties
    def convert_diff_to_message(self,songname, arr):
        rtstring = "PlayLevel of " + songname + "\n"
        for i,j in enumerate(arr):
            rtstring += Constants.musicDifficulties[int(i)] + " : " + str(j) + " "
        return rtstring
    def songinfo_to_array(self,musicid):
        rtarr = []
        idx = 0
        for i, j in enumerate(self.musicsdata):
            if j['id'] == musicid:
                return list(map(str,[j['title'],j['creator'],j['lyricist'],j['composer'],j['arranger'],j['assetbundleName']]))
    def songinfo_to_string(self,arr):
        rtstring = ""
        for i in range(len(arr)-1):
            rtstring += Constants.songInfoNames[i] + str(arr[i]) + "\n"
        return rtstring
    async def download_jacket_and_send(self,jacketname,message):
        url = "https://assets.pjsek.ai/file/pjsekai-assets/startapp/music/jacket/" + jacketname + "/" + jacketname + ".png"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                img = await resp.read()
                if(os.path.exists("./jackets/"+jacketname+".png")):
                    with open("./jackets/"+jacketname+".png",'rb') as file:
                        await message.channel.send(file=discord.File(file, jacketname+".png"))
                else:
                    with open("./jackets/"+jacketname+".png",'wb') as file:
                        file.write(img)
                    with open("./jackets/"+jacketname+".png",'rb') as file:
                        await message.channel.send(file=discord.File(file, jacketname+".png"))