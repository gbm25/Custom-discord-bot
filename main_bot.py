import discord
from discord.ext import commands
from secrets import token
import lorem
TOKEN = token

description = '''Croquetabot ! recien salido de la sarten 😁'''
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Se ha iniciado {bot.user.name}')
    print('------')


@bot.command(name="SetSatisChannel")
async def set_satisfactory_channel(ctx, satis_channel):
    """Define el canal en el que se realizarán las acciones relacionadas con Satisfactory"""

    await ctx.send("No te voy a mentir, esto aun no esta implementado")

    # channel = discord.utils.get(ctx.guild.channels, name=satis_channel)
    # await ctx.send("world")


@bot.command(name="IdCanales")
async def listar_canales_servidor(ctx):
    """Lista los nombres e IDs de los canales del servidor"""

    messagesbuffer = []
    counter = 0

    for channel in ctx.guild.channels:

        text = f'- Nombre del canal: "{channel.name}", con ID: {channel.id}.\r\n'

        if messagesbuffer == []:
            messagesbuffer.append(text)

        elif (len(text) + len(messagesbuffer[counter])) <= 2000:
            messagesbuffer[counter] += text
        else:
            counter += 1
            messagesbuffer.append(text)

    for message in messagesbuffer:
        await ctx.send(message)

@bot.command()
async def infochannel(ctx):
    """Test del canal"""
    sender = ctx.author
    await ctx.send(f'{sender.mention} ha usado el bot.')

    channel = ctx.message.channel
    await ctx.send(f'en el canal: {channel}')

    messagesbuffer = ['Miembros del canal:\r\n']
    counter = 0

    for member in [member for member in bot.get_channel(channel.id).members if not member.bot]:

        #[member.nick for member in memberlist if not member.bot
        text = f'- {member.name}' + f'{f" alias {member.nick}"if member.nick else ""}'+'\r\n'

        if (len(text) + len(messagesbuffer[counter])) <= 2000:
            messagesbuffer[counter] += text
        else:
            counter += 1
            messagesbuffer.append(text)

    for message in messagesbuffer:
        await ctx.send(message, delete_after=15.0)


@bot.command()
async def boofear(ctx, *args):
    """Permite boofear intensamente a alguien del canal en el que se usa"""

    target_name = " ".join(args)

    # Quien invoco al bot
    sender = ctx.author

    # ID del canal donde se ha invocado al bot
    channel = ctx.message.channel

    # Lista de miembros del canal
    memberlist = bot.get_channel(channel.id).members

    target = [target_obj for target_obj in memberlist if
              (target_obj.name == target_name or target_obj.nick == target_name)]

    if target:
        target = target[0]
        if target.name == sender.name:
            await ctx.send(f'{sender.mention} se ha boofeado a si mismo ! que vanidoso ...')
        else:
            await ctx.send(f'{sender.mention} ha boofeado intensamente a {target.mention}!')
    else:
        await ctx.send(f'{sender.mention} no ha boofeado a nadie, solo pasaba a molestar, vaya pieza ...')


bot.run(TOKEN)
