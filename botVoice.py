import discord
import asyncio
import youtube_dl
import shutil
import os
import json
from discord.utils import get
from discord.ext import commands

# Open key file and set keyData var
with open('key.json') as json_data:
    keyData = json.load(json_data,)

# Config Variables
client = commands.Bot(command_prefix = '.')
clientKey = keyData['key']

@client.event
async def on_ready():
    print('All warmed up. Let do this.')

@client.command(aliases=['j'])
async def join(ctx):
    print('Join command sent')
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    print(f'Trying to join {channel}...')

    if voice and voice.is_connected():
        await voice.move_to(channel)
        print(f'Connected!')
    else:
        voice = await channel.connect()
        print(f'Connected!')

    voice.stop()
    
    await ctx.send(f"Joined {channel}")

@client.command(aliases=['l'])
async def leave(ctx):
    print('Leave command sent')
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    print(f'Trying to leave {channel}...')

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Bot has left {channel}')
        await ctx.send(f'Left {channel}')

@client.command(aliases=['p'])
async def play(ctx):
    print(f'Play command sent')

    voice.play(discord.FFmpegPCMAudio('song.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.6
    print(f'Music playing!')
    await ctx.send("Time to bring the heat!")

@client.command(aliases=['s'])
async def stop(ctx):
    print(f'Stop command sent')
    voice.stop()
    await ctx.send("I have been stopped :(")

@client.command()
async def pause(ctx):
    print(f'Pause command sent')
    voice.pause()
    await ctx.send("I have been paused :(")

@client.command(aliases=['r'])
async def resume(ctx):
    print(f'Resume command sent')
    voice.resume()
    await ctx.send("I have been resumed :D")

client.run(clientKey)