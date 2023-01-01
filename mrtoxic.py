import discord
import random
import aiohttp
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions
import time
import io

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', help_command=None, case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    print("bot online")
    await bot.change_presence(activity=discord.Streaming(name='!help', url='https://www.twitch.tv/mrtoxic7866'),
                              status=discord.Status.online)


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)


@bot.listen()
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    if channel is not None:
        embed = discord.Embed(color=0x4a3d9a)
        embed.add_field(name="Welcome", value=f"{member.mention} has joined {member.guild.name}, remember to be nice!",
                        inline=False)
        await channel.send(embed=embed)
    else:
        pass


@bot.listen()
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    if channel is not None:
        embed = discord.Embed(color=0x4a3d9a)
        embed.add_field(name="Goodbye", value=f"{member.mention} has left {member.guild.name}", inline=False)
        await channel.send(embed=embed)
    else:
        pass


@bot.command()
async def cheese(ctx):
    await ctx.send(':cheese:')


@bot.command(aliases=['8ball'], help='usage: `!8ball {question}`')
async def _8ball(ctx, message=None):
    if message is not None:
        the_list = ['my sources say yes', 'hell no', 'ask again later', "idk man you're on your own", 'sure, why not?',
                    'how about... no?', '*sigh*, not right now I am busy!']
        await ctx.reply(random.choice(the_list))
    else:
        await ctx.reply('ask me a question')


@bot.command(aliases=['trigger', 'trig'])
async def triggered(ctx, user: discord.User = None):
    if user is None:
        user = ctx.message.author
    else:
        pass
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://some-random-api.ml/canvas/triggered?avatar={user.avatar.url}') as response:
            buffer = io.BytesIO(await response.read())

    await ctx.send(file=discord.File(buffer, filename='triggered.gif'))


@bot.command(aliases=['doggo', 'dogs', 'dogfacts', 'dogfact', 'pup', 'pupper', 'puppy'],
             help='cute dog images, usage: `!dog`')
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
        request2 = await session.get('https://some-random-api.ml/facts/dog')
        factjson = await request2.json()
    dogbed = discord.Embed(title='DOGGY', colour=discord.Colour.dark_gold())
    dogbed.set_image(url=dogjson['link'])
    dogbed.set_footer(text=factjson['fact'])
    await ctx.send(embed=dogbed)


@bot.command(aliases=['kitty', 'kitten', 'meow', 'catfact', 'catfacts'], help='cute cat images, usage: `m!cat`')
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        request1 = await session.get('https://some-random-api.ml/img/cat')
        catjson = await request1.json()
        request22 = await session.get('https://some-random-api.ml/facts/cat')
        factjson1 = await request22.json()
    catty = discord.Embed(title='KITTY', colour=discord.Colour.dark_gold())
    catty.set_image(url=catjson['link'])
    catty.set_footer(text=factjson1['fact'])
    await ctx.send(embed=catty)


@bot.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    pingas = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong! My ping is `{int(pingas)}ms`")
    print(f'Ping: `{int(pingas)} ms`')


@bot.command(help='locks down a channel, only admins can talk and unlock it', aliases=['lock', 'ld'])
@has_permissions(administrator=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + " ***is now in lockdown.***")


@bot.command(help='unlocks a channel', aliases=['unlockdown', 'uld', 'ul'])
@has_permissions(administrator=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")


@bot.command()
async def echo(ctx, *, message=None):
    await ctx.message.delete()
    await ctx.send(message)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title='HELP PAGE', colour=discord.Colour.dark_orange())
    embed.add_field(name='COMMAND 1: cheese', value='responds with :cheese:', inline=False)
    embed.add_field(name='COMMAND 2: aboutme | info', value='responds with info about mrtoxic7866', inline=False)
    embed.add_field(name='COMMAND 3: ping', value='get the current ping of the bot', inline=False)
    embed.add_field(name='COMMAND 4: dog', value='cute doggo pics from the internet', inline=False)
    embed.add_field(name='COMMAND 5: cat', value='cute kitty pics from the internet', inline=False)
    embed.add_field(name='COMMAND 6: 8ball', value='a mysterious magic eight ball with attitude', inline=False)
    embed.add_field(name='COMMAND 7: lockdown | lock - **ADMIN ONLY**',
                    value='locks down a channel so only admins can speak in it', inline=False)
    embed.add_field(name='COMMAND 8: unlockdown | unlock - **ADMIN ONLY**', value='unlocks a locked channel',
                    inline=False)
    embed.add_field(name='COMMAND 9: triggered', value='makes a gif of you or a specified person being triggered',
                    inline=False)
    embed.add_field(name='COMMAND 10: echo', value='the bot will say what you said', inline=False)
    embed.set_footer(text='made by unseeyou')
    embed.set_author(name='my prefix is !')
    await ctx.send(embed=embed)


@bot.command(name='aboutme', aliases=['info'])
async def about_me(ctx):
    the_about_me = """I’m pretty new to twitch I love gaming even if I’m not good at a game I do my best hope everyone enjoys my content come chill with me while we go on multiple adventures together"""
    info = discord.Embed(title='All about MrToxic7866', description='**__SOCIALS__**', colour=discord.Colour.yellow())
    info.add_field(name='**TWITCH**', value='https://twitch.tv/mrtoxic7866')
    info.add_field(name='**FACEBOOK**', value='still finding link lol')
    info.add_field(name='**SNAPCHAT**', value='https://t.snapchat.com/q6CCcDnl')
    info.add_field(name='**INSTAGRAM**', value='link go here')
    info.add_field(name='**YOUTUBE**', value='https://m.youtube.com/channel/UCM12fKwdlw_wAKFerUJQhNQ')
    info.add_field(name='**__ABOUT ME__**', value=the_about_me, inline=False)
    info.set_footer(text='made by unseeyou')
    info.set_author(name='mrtoxic7866',
                    icon_url='https://static-cdn.jtvnw.net/jtv_user_pictures/675fcc9b-78d6-4770-99fc-8e0991405ed8-profile_image-70x70.png',
                    url='https://twitch.tv/mrtoxic7866')
    await ctx.send(embed=info)


async def main():
    async with bot:
        await bot.start('OTg3NjgzMzY4NjE3NTI1MjQ4.GgTokO.RKM-2YAS1tlhnHbrYZ0nMf-4SOkjQAxRgr2XoY')


asyncio.run(main())
