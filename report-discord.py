import discord
from discord.ext import commands
import json
import os

def stat_rep(men=str, mrep=int, prep=int):
    de= str.maketrans('','','<>')
    men=men.translate(de)
    if os.path.exists(f"{men}.json") == True:
        with open(f'{men}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['men']=men
        mrep1=data['mrep']
        prep1=data['prep']
        mrep=mrep1+mrep
        prep=prep1+prep
        data={        
            "men": men,
            "mrep": mrep,
            "prep": prep
        }
        with open(f'{men}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        data={        
            "men": men,
            "mrep": mrep,
            "prep": prep
        }
        with open(f'{men}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

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


# Define intents (specifies what events your bot receives)
intents = discord.Intents.default()
intents.message_content = True # Required for reading message content in most cases
intents.messages = True 

# Create the bot client with a command prefix and intents
prefics=['-','+','.']
bot = commands.Bot(command_prefix=prefics, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command(name="rep")
async def rep(ctx, member: discord.Member):
    prefix = ctx.prefix
    channel= bot.get_channel()
    lox=member.mention
    if prefix == '-': 
        await channel.send(f"-rep {lox}"),
        stat_rep(lox,1,0)
    elif prefix == '+':
        await channel.send(f"+rep {lox}"),
        stat_rep(lox,0,1)

@bot.command()
async def stats(ctx, member: discord.Member):
    prefix= ctx.prefix
    channel= bot.get_channel()
    lox=member.mention
    if prefix == '.':
        re=reads1(lox)
        await channel.send(re) 
@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, amount: int):
    """Удаляет указанное количество сообщений"""
    prefix= ctx.prefix
    if amount <= 0:
        await ctx.send("Укажите число больше 0!")
        return
    # Ограничиваем максимальное количество для удаления
    if amount > 100:
        amount = 100
    
    if prefix == '.':
        # Удаляем сообщения (включая команду)
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Удалено {len(deleted) - 1} сообщений!", delete_after=3)


# Replace "YOUR_BOT_TOKEN" with your actual bot token from the Developer Portal
bot.run("")