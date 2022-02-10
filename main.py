
import os 
import discord
import json
import requests

from discord.client import Client
from discord.ext import commands
from keep_alive import keep_alive

# from types import resolve_bases
# from discord import message
# from discord import user
# from discord import emoji
# from discord.abc import User
# from discord.embeds import Embed
# from discord.ext.commands.errors import CommandInvokeError, CommandOnCooldown, MissingRequiredArgument, CommandNotFound
# from discord.utils import find
# from discord.utils import get
# from random import randint, seed, random


intents = discord.Intents.default()
intents.members = True
prefix = '+'
client = commands.Bot(command_prefix=prefix,intents=intents)
client.remove_command('help')



min_crit = 111
max_crit =  9   *(1+2*2+3*3+4*4+5*4)+\
            10  *(2*2+3*3+4*4+5*3)+\
            22  *(3*3+4*4+5*3)+\
            32  *(4*4+5*4)+\
            min_crit
version = "7.1.1"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    find_text = ['bark','meow']
    send_answer = ['***hiss***','Here, Kitty Kitty!']
    
    find_text2 = ['how to change nickname']
    send_answer2 = ['1-Tap your profile pic, go to manage and tap it, type in nickname.\n2-Or try slash command: /nick `nickname | class | crit`']

    for i in range(len(find_text)):
        if message.content.lower().find(find_text[i])!=-1:
            await message.reply(send_answer[i])  

    for i in range(len(find_text2)):
        if message.content.lower().find(find_text2[i])!=-1:
            await message.channel.send(send_answer2[i])

    await client.process_commands(message)



# @client.event
# async def on_command_error(message, error):
#     if isinstance(error, CommandNotFound):
#         print(error)
#         return await message.channel.send("Command not found")
#     if isinstance(error, MissingRequiredArgument):
#         print(error)
#         message.command.reset_cooldown(message)
#         return await message.channel.send('Not enouh arguments, try something else')
#     if isinstance(error, CommandOnCooldown):
#         print(error)
#         return await message.channel.send(error)
#     raise error

#region Game functions
@client.command(pass_context=True)
async def combo(ctx, _count, _class, _level=5, bonus=False):  
    if int(_class)<7: return await ctx.message.channel.send(f'invalid class/damage argument')
    _bonus = 1.1 if bonus else 1
    if int(_class)>=7 and int(_class)<=15:
        if int(_level)<1 or int(_level)>5:
            return await ctx.message.channel.send(f'invalid level argument')
        damage = 10+(int(_class)-7)*10+(int(_level)-1)*10
        count_damage = 8+(int(_class)-7)*2+(int(_level)-1)*1
        total = (damage + (1+int(_count))*(int(_count)*count_damage/2))*_bonus
        await ctx.message.channel.send(f'result damage for combo class {_class}, level {_level} with {_count} count is {int(total):,};\napplied bonus: {int(_bonus*100)}%')
    else:
        res = 7
        total_damage = 0
        delta = int(_class)
        for i in range(7,16):
            damage = 10+(i-7)*10+(int(_level)-1)*10
            count_damage = 8+(i-7)*2+(int(_level)-1)*1
            total = (damage + (1+int(_count))*(int(_count)*count_damage/2))*_bonus
            if (abs(int(total)-int(_class))<delta):
               res = i 
               delta = abs(int(total)-int(_class))
               total_damage = int(total)
        await ctx.message.channel.send(f'closest combo class is {res}\nlevel: {_level}\nresult damage: {total_damage:,}\napplied bonus: {int(_bonus*100)}%')

@client.command(pass_context=True)
async def maxcrit(ctx):
    await ctx.message.channel.send(f'maximum possible crit is {max_crit}, version: {verison}')

@client.command(pass_context=True)
async def crit(ctx, crit_num):
    user = ctx.message.author

    if int(crit_num) < min_crit or int(crit_num) > max_crit:
        return await ctx.message.channel.send('imposible number')            
    
    for r in user.roles:
        if r.name.find('%')!=-1:
            await user.remove_roles(r)
    
    roles = user.guild.roles[1:]
    for r in roles:
        if r.name.find('%')!=-1:
            num=r.name.replace('-','').replace('+','').split(sep='%')[:-1]
            if (len(num)==2):
                if int(num[0])<=int(crit_num) and int(num[1])>int(crit_num):
                    await user.add_roles(r)
                    s = r.name + f' was added to {user.mention}'  
                    await ctx.message.channel.send(s)
            if (len(num)==1):
                if int(num[0])<=int(crit_num):
                    await user.add_roles(r)
                    s = r.name + f' was added to {user.mention}'  
                    await ctx.message.channel.send(s)

# possible classes:
# 1..20, 21..32
# 1..20, grand1, grand2..champion3
# 1..20, gold1..gold12
@client.command(pass_context=True)
async def pvpclass(ctx, _class):
    classes = ['grand1','grand2','grand3','master1','master2','master3','challenger1','challenger2','challenger3','champion1','champion2','champion3']
    roles_= ['Class 1 - Class 11', 'Class 12', 'Class 13', 'Class 14', 'Class 15','Class 16','Class 17','Class 18','Class 19','Class 20',
            'Grand 1','Grand 2','Grand 3','Master 1','Master 2','Master 3','Challenger 1','Challenger 2','Challenger 3','Champion 1','Champion 2','Champion 3']
    user = ctx.message.author
    class_num = 0
    print(f"checking {_class}")
    if _class.isdecimal():
        if int(_class)>32 or int(_class)<1:
            return await ctx.message.channel.send('incorrect class')
        else: class_num=int(_class)
    else:
        if _class.replace('gold','').isdecimal():
            if int(_class.replace('gold',''))>12 or int(_class.replace('gold',''))<1:
                return await ctx.message.channel.send('incorrect class')
            else: class_num=20+int(_class.replace('gold',''))
        else:
            if not any(ext in _class for ext in classes):
                return await ctx.message.channel.send('incorrect class')
            else: class_num = 20 + classes.index(_class)+1
    print(f"checking passed: {class_num}")
    if (class_num<=11): class_num=0
    else: class_num-=11
    for r in user.roles:
        if r.name.lower().find('class')!=-1:
            await user.remove_roles(r)
    print(class_num)
    print(roles_[class_num])
    roles = user.guild.roles[1:]
    for r in roles:
        if r.name.lower().find(roles_[class_num].lower())!=-1:   
            await user.add_roles(r)  
            s = r.name + f' was added to {user.mention}'  
            await ctx.message.channel.send(s)

@client.command(pass_context=True)
async def reset(ctx):
    classes = ['Grand 1','Grand 2','Grand 3','Master 1','Master 2','Master 3','Challenger 1','Challenger 2','Challenger 3','Champion 1','Champion 2','Champion 3']
    k=0
    flag = False
    members = ctx.guild.members
    for m in members:
        roles = m.roles
        for r in roles:
            for c in classes[1:]:
                if r.name.find(c)!=-1:
                    await m.remove_roles(r)
                    flag = True
                    break
            if (flag):
                break
        if (flag):
            roles = m.guild.roles[1:]
            for r in roles:
                if r.name.lower().find(classes[0].lower())!=-1:   
                    await m.add_roles(r)  
                    k=k+1
                    break
        flag = False
    print(f'count = {k}')
    await ctx.channel.send(f'roles reset for {k} members')

#endregion

@client.command(pass_context=True)
async def role_give(ctx, user: discord.User, role: discord.Role):
    await user.add_roles(role)
    s = role.name + f' was added to {user.mention}'  
    await ctx.message.channel.send(s)

@client.command(pass_context=True)
async def role_list(ctx, role):
    members = ctx.guild.members
    color = 0x000000
    s = ""
    for m in members:
        for r in m.roles:
            if r.name.find(role)!=-1:
                s+= m.mention+":"+m.name+"#"+m.discriminator+"\n"
    if s=="": s="no members found with this role"
    embed = discord.Embed(color = color)
    embed.description = s
    await ctx.message.channel.send(embed = embed)

@client.command(pass_comtext=True)
async def cat(ctx):
    await find(ctx.message, 'cat')
@client.command(pass_comtext=True)
async def dog(ctx):
    await find(ctx.message, 'dog')
async def find(message, animal):
    response = requests.get('https://some-random-api.ml/img/'+animal)
    json_data = json.loads(response.text)
    embed = discord.Embed(color = 0xff9900)
    embed.set_image(url = json_data['link'])
    embed.set_footer(text="requested by:" + message.author.name +'#'+ message.author.discriminator)
    await message.channel.send(embed = embed)

@client.command(pass_context=True)
async def hug(ctx, user: discord.User):
    await ctx.message.delete()
    await ctx.message.channel.send(f'{ctx.message.author.mention} hugs {user.mention}')

@client.command(pass_context=True)
async def poke(ctx, user: discord.User):
    await ctx.message.delete()
    seed(random())
    author = ctx.message.author
    poke_ = {
        1:f'{author.mention} pokes {user.mention}',
        2:f'{author.mention} fails to poke {user.mention}',
        3:f'{author.mention} fails to poke {user.mention} and slaps {user.mention} with a large trout',
        4:f'{author.mention} fails to poke {user.mention} and boop that snoot at {user.mention}',
        5:f'{author.mention} fails to poke {user.mention} and kiss {user.mention}',
        6:f'{author.mention} fails to poke {user.mention} and hug {user.mention}',
        7:f'{author.mention} fails to poke {user.mention} and hit {user.mention} with a pillow'
    }    
    k=randint(1,len(poke_))
    await ctx.message.channel.send(poke_[k])

@client.command(pass_context=True)
async def slap(ctx, user: discord.User):
    await ctx.message.delete()
    await ctx.message.channel.send(f'{ctx.message.author.mention} slaps {user.mention} with a large trout')

@client.command(pass_context=True)
async def clap(ctx):
    await ctx.message.delete()
    await ctx.message.channel.send('<a:clap:884754435631362108>')

@client.command(aliases=['help'],pass_comtext=True)
async def _help(ctx):
    s = 'prefix for this bot is `'+prefix+'`\n'
    s += 'list of commands:\n'
    s += 'sorry, nothing here yet'
#     '''help - list of commands
# clear - delete all messages in channel except pinned
# hello - say hello to the bot
# cat~~/dog~~ - random cat~~/dog~~ image
# crit - enter your crit damage
# pvpclass - enter your pvp class
# '''
    return await ctx.message.channel.send(s)


keep_alive()
token = os.environ.get("TOKEN")
client.run(token)