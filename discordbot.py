from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print('봇이 온라인으로 전환되었습니다.')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("보스 타임 체크"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!컷'):
        target = message.content.split()[1] #입력된 메시지에서 2번째 단어 추출
        now = datetime.utcnow() + timedelta(hours=12) #KST (UTC+9)

        reply = []
        for name, info in BOSS_INFO.items():
            if name == target:
                next_spawn = now + timedelta(minutes=info["젠주기"])
                BOSS_INFO[name]["다음 젠 시간"] = next_spawn.strftime('%H:%M')
                reply.append(f"{next_spawn.hour}:{next_spawn.minute}, {name}, , {info['젠위치']}, {info['레벨']}")
            else:
                reply.append(f"{info['다음 젠 시간']} , {name},  {info['젠위치']}, {info['레벨']}")
        await message.reply('\n'.join(reply))


try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
