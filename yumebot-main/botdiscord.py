import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
import os
import asyncio
import random
#import youtube_dl

client = commands.Bot(command_prefix = "noe ")
player = {}
songs = asyncio.Queue()
play_next_song = asyncio.Event()
@client.event

async def on_ready():
    await client.change_presence(activity=discord.Game('Noe'))

async def audio_player_task():
    while True:
        play_next_song.clear()
        current = await songs.get()
        current.start()
        await play_next_song.wait()


def toggle_next():
    client.loop.call_soon_threadsafe(play_next_song.set)

@client.event

async def on_member_join(member):
    print(f'{member} has joined the server.')

async def on_member_remove(member):
    print(f'{member}has left the server.')

@client.command()
async def Help(ctx):
    embed=discord.Embed(name= None,value="Commands")
    embed.add_field(name='Luck',value= 'ask me question :pleading_face:')
    embed.add_field(name='compliment',value= 'I am sweet to everyone :pleading_face:')
    embed.add_field(name='roast',value= 'I can hurt :pleading_face:')
    embed.add_field(name='ping',value= 'you are laggy and you know it :pleading_face:')
    embed.add_field(name='pfp',value= 'is he/she cute :yns_what:')
    await ctx.send(embed=embed)

@client.command(aliases=['8ball','billard','luck'])
async def _8ball(ctx,*, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command(aliases=['flert','compliment'])
async def seduce(ctx,*,member: discord.Member = None):
    if not member:
        member = ctx.author
    quotes = ["You look great."
    ,"You look phenomenal."
    ,"You look nice."
    ,"You look amazing!"
    ,"The dress looks stunning."
    ,"What a lovely necklace!"
    ,"I like your shirt – where did you get it?"
    ,"I love your new shoes."
    ,"You look very good in that suit."
    ,"This tie looks nice on you."
    ,"That color looks great on you."
    ,"You look very handsome."
    ,"You’re looking very beautiful today."
    ,"I like your new haircut."
    ,"rak ghaya a khoya(khty)"
    ,"You have a lovely voice."
    ,"Wow, you look hot!"
    ,"Reshmi, what a beautiful dress!"
    ,"Cool glasses, totally suit you."
    ,"I really love your haircut. It makes you look like a movie star."]
    await ctx.send(f'{member.mention} {random.choice(quotes)}')

@client.command(aliases=['insult','hate'])
async def roast(ctx,*,member: discord.Member = None):
    if not member:
        member = ctx.author
    roastes = ["You’re the reason God created the middle finger."
    ,"You’re a grey sprinkle on a rainbow cupcake."
    ,"If your brain was dynamite, there wouldn’t be enough to blow your hat off."
    ,"You are more disappointing than an unsalted pretzel."
    ,"Light travels faster than sound which is why you seemed bright until you spoke."
    ,"We were happily married for one month, but unfortunately we’ve been married for 10 years."
    ,"Your kid is so annoying, he makes his Happy Meal cry."
    ,"You have so many gaps in your teeth it looks like your tongue is in jail."
    ,"Your secrets are always safe with me. I never even listen when you tell me them."
    ,"I’ll never forget the first time we met. But I’ll keep trying."
    ,"I forgot the world revolves around you. My apologies, how silly of me."
    ,"I only take you everywhere I go just so I don’t have to kiss you goodbye."
    ,"Hold still. I’m trying to imagine you with personality."
    ,"Our kid must have gotten his brain from you! I still have mine."
    ,"Your face makes onions cry."
    ,"The only way my husband would ever get hurt during an activity is if the TV exploded."
    ,"You look so pretty. Not at all gross, today."
    ,"It’s impossible to underestimate you."]
    await ctx.send(f'{member.mention} {random.choice(roastes)}')

@client.command(aliases=['latency','ping'])
async def idk(ctx):
    embed=discord.Embed(title='Pong!', colour=discord.Colour.blue())
    embed.add_field(name='Ping:', value=f'{round(client.latency * 1000)} ms')
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member :discord.Member, *, reason=None):
    embed = discord.Embed(title=f"You have been kicked from {ctx.message.guild.name}.", color=0xff6161)
    embed.add_field(name=None,value= member.avatar_url)
    embed.add_field(name="Reason: ", value = reason)
    await member.kick(reason = reason)
    client.get_user(member)
    await client.send(embed=embed)

@client.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member :discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await client.get_user(member)
    embed = discord.Embed(title=f"You have been banned from {ctx.message.guild.name}.", color=0xff6161)
    embed.add_field(name=None,value= member.avatar_url)
    embed.add_field(name="Reason: ", value = reason)
    await member.send(embed=embed)
@client.command()
async def unban(ctx,*, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name,user.discriminator) == (member_name,member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(title=f"You have been unbanned from {ctx.message.guild.name}.", color=0xff6161)
            embed.add_field(name=None,value= member.avatar_url)
            await member.send(embed=embed)
            return

@client.command(aliases=['getprofilepic','getprofilepicture','pfp','profilepic','profilepicture','avatar'])
async def getpfp(ctx, member: discord.Member = None):
 if not member:
  member = ctx.author
 await ctx.send(member.avatar_url)

@client.command(aliases=['clean','purge','clear'])
@has_permissions(administrator = True)
async def wipe(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Message deleted")
@wipe.error
async def wipe_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You dont have the permission uwu")
    else:
        raise error

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command(pass_contex=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()
@client.command()
@commands.is_owner()
async def nuke(ctx, channel_name):
    channel_id = int(''.join(i for i in channel_name if i.isdigit())) 
    existing_channel = client.get_channel(channel_id)
    if channel_name is not None:
        await ctx.channel.clone(reason="Has been nuked")
        await ctx.channel.delete()
    else:
        await ctx.send(f'No channel named **{channel_name}** was found')
@nuke.error
async def nuke_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You dont have the permission uwu")
    else:
        raise error
""" @client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.1

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n") """

"""@client.command(pass_context=True)
async def play(ctx, url):
    if not Client.is_voice_connected(ctx.message.server):
        voice = await Client.join_voice_channel(ctx.message.author.voice_channel)
    else:
        voice = Client.voice_client_in(ctx.message.server)

    player = await voice.create_ytdl_player(url, after=toggle_next)
    await songs.put(player)""" 

client.loop.create_task(audio_player_task())

client.run('NzUxNzA0Nzk1ODk0Nzc1ODM4.X1M9pQ.HGkqHZ2IY5QeGjK9K61tKa--AGk')