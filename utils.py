import discord
import json
from constants_ko import Constants_Ko
import aiohttp
import io
import os
import filepaths
import utils
import urls

class Musics:
    def __init__(self, musicspath = filepaths.musics, difficultiespath = filepaths.difficulties):
        with open(musicspath, encoding="UTF-8") as f:
            self.musicsdata = json.load(f)
        with open(difficultiespath, encoding="UTF-8") as f:
            self.difficultydata = json.load(f)
        with open(Constants_Ko.musictitlespath, encoding="UTF-8") as f: #todo: change languages dynamic
            self.koreansongnames = json.load(f)
    def bootstrap(self, musicspath = filepaths.musics, difficultiespath = filepaths.difficulties):
        with open(musicspath) as f:
            self.musicsdata = json.load(f)
        with open(difficultiespath) as f:
            self.difficultydata = json.load(f)
        with open(Constants_Ko.musictitlespath, encoding="UTF-8") as f:
            self.koreansongnames = json.load(f)
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
                diff = Constants_Ko.musicDifficulties.index(i['musicDifficulty'])
                difficulties[diff] = i['playLevel']
        return difficulties
    def convert_diff_to_message(self,songname, arr):
        rtstring = "PlayLevel of " + songname + "\n"
        for i,j in enumerate(arr):
            rtstring += Constants_Ko.musicDifficulties[int(i)] + " : " + str(j) + " "
        return rtstring
    def songinfo_to_array(self,musicid):
        rtarr = []
        idx = 0
        for i in self.musicsdata:
            if i['id'] == musicid:
                return list(map(str,[i['title'],i['creator'],i['lyricist'],i['composer'],i['arranger'],i['assetbundleName']]))
    def songinfo_to_string(self,arr):
        '''
        rtstring = ""
        for i in range(len(arr)-1):
            rtstring += Constants_Ko.songInfoNames[i] + str(arr[i]) + "\n"
        return rtstring
        '''
        return Constants_Ko.songInfoFormat.format(*(Constants_Ko.songInfoNames + arr))
    async def download_jacket_and_send(self,jacketname,message):
        url = urls.jacket + jacketname + "/" + jacketname + ".png"
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