import discord
import json
import os 
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
# Discord varalebes
intents = discord.Intents.default()
intents.message_content = True 
intents.messages = True 
prefics=['-','+','.']
bot = commands.Bot(command_prefix=prefics, intents=intents)
# env variables
channel_key=os.getenv("CHANNEL_KEY")
api_key=os.getenv("API_KEY")

# Work or Not
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# DB on json
def stat_rep(men=str, mrep=int, prep=int, com=str, crep=str):
    de= str.maketrans('','','<>')
    men=men.translate(de)
    if os.path.exists(f"{men}.json") == True:
        with open(f'{men}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['men']=men
        com1=data['com']
        mrep1=data['mrep']
        prep1=data['prep']
        mrep=mrep1+mrep
        prep=prep1+prep
        data={        
            "men": men,
            "mrep": mrep,
            "prep": prep,
            "com": com1+", "+crep+" "+com
        }
        with open(f'{men}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        data={        
            "men": men,
            "mrep": mrep,
            "prep": prep,
            "com": crep+" "+com
        }
        with open(f'{men}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

#How much "rep" you have 
def reads1(men1):
    men=str(men1)
    de= str.maketrans('','','<>')
    men=men.translate(de)
    with open(f'{men}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    men=data['men']
    mrep1=data['mrep']
    prep1=data['prep']
    return f'User: {men1}:\n -rep: {mrep1}\n +rep: {prep1}'

# Text in rep
def rcom(men1):
    men=str(men1)
    de= str.maketrans('','','<>')
    men=men.translate(de)
    with open(f'{men}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    com=data['com']
    return f'Comment {men1}: {com}'

# Rep Function
@bot.command(name="rep")
async def rep(ctx, member: discord.Member, com):
    prefix = ctx.prefix
    channel= bot.get_channel(channel_key)
    lox=member.mention
    if prefix == '-':
        await channel.send(f"-rep {lox}, {com}"),
        stat_rep(lox,1,0,com,"-rep") 
    elif prefix == '+':
        await channel.send(f"+rep {lox}, {com}"),
        stat_rep(lox,0,1,com,"+rep")         

# Check status report from function reads1 and return in channel 
@bot.command()
async def stats(ctx, member: discord.Member):
    prefix= ctx.prefix
    channel= bot.get_channel(channel_key)
    lox=member.mention
    if prefix == '.':
        re=reads1(lox)
        await channel.send(re) 

# Display your comment
@bot.command()
async def comment(ctx, member: discord.Member):
    prefix= ctx.prefix
    channel= bot.get_channel(channel_key)
    lox=member.mention
    if prefix == '.':
        await channel.send(f'{rcom(lox)}')

# Can delete only last 100 message
@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, amount: int):
    prefix= ctx.prefix
    if amount <= 0:
        await ctx.send("Укажите число больше 0!")
        return
    if amount > 100:
        amount = 100
    if prefix == '.':
        # Удаляем сообщения (включая команду)
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Удалено {len(deleted) - 1} сообщений!", delete_after=3)

bot.run(api_key)