import discord
from discord.ext import commands, tasks
from secrets import token, channel_dc_pruebas
import scraping_genshin_impact as sgi

TOKEN = token

description = '''Croquetabot ! recién salido de la sartén 😁'''
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='?', description=description, intents=intents)

genshin_data = sgi.GenshinImpact()


@bot.event
async def on_ready():
    print(f'Se ha iniciado {bot.user.name}')
    print('------')
    print('Lanzando el bucle genshin_impact_new_codes()')
    genshin_impact_new_codes.start()


@tasks.loop(hours=12)
async def genshin_impact_new_codes():
    canal_genshin = bot.get_channel(channel_dc_pruebas)

    codes_notification = genshin_data.check_new_codes()

    for line in codes_notification:

        text = f'Código: {line["code"]}\r\nEnlace externo: {line["external_link"]}\r\nValido en el servidor:' \
               f' {line["server"]}\r\nRecompensas:\r\n'

        for reward in line["rewards"]:
            text += f'\t-{reward["item_name"]} x{reward["quantity"]}\r\n'
        text += f'Con fechas:\r\n\t-{line["start"]}\r\n\t-{line["end"]}'
        embed = discord.Embed(title=f"Nuevo código", description=text, color=0xf805de)
        await canal_genshin.send(embed=embed)


@bot.command(name="GenshinCodes")
async def get_genshin_active_codes(ctx):
    """Permite obtener los códigos activos de Genshin Impact"""
    active_codes = genshin_data.get_active_codes()

    if active_codes:
        for line in active_codes:

            text = f'Código: {line["code"]}\r\nEnlace externo: {line["external_link"]}\r\nValido en el servidor:' \
                   f' {line["server"]}\r\nRecompensas:\r\n'

            for reward in line["rewards"]:
                text += f'\t-{reward["item_name"]} x{reward["quantity"]}\r\n'
            text += f'Con fechas:\r\n\t-{line["start"]}\r\n\t-{line["end"]}'
            embed = discord.Embed(title=f"Código Activo", description=text, color=0xf805de)
            await ctx.send(embed=embed)


@bot.command(name="SetSatisChannel")
async def set_satisfactory_channel(ctx, satis_channel):
    """Define el canal en el que se realizarán las acciones relacionadas con Satisfactory"""

    await ctx.send("No te voy a mentir, esto aun no esta implementado")

    # channel = discord.utils.get(ctx.guild.channels, name=satis_channel)
    # await ctx.send("world")


@bot.command(name="ListChannels")
async def listar_canales_servidor(ctx):
    """Lista los nombres e IDs de los canales del servidor"""

    # Se crea un array que almacenará strings. Los strings nunca superaran ni igualar los 2000 caracteres
    messages_buffer = []
    counter = 0

    # Se itera sobre los canales del servidor
    for channel in ctx.guild.channels:

        # Se crea un string con formato "- Nombre del canal: "NombreDelCanal", con ID: IdDelCanal."
        text = f'- Nombre del canal: "{channel.name}", con ID: {channel.id}.\r\n'

        # Se comprueba si el array esta vacío
        if not messages_buffer:
            # Se añade el string al array
            messages_buffer.append(text)
        # Comprobamos si añadiendo el nuevo string al ultimo string almacenado no se superan los 2000 caracteres
        elif (len(text) + len(messages_buffer[counter])) <= 2000:
            # En caso de ser menos de 2000 caracteres, concatenamos nuestro string con el ultimo string del array
            messages_buffer[counter] += text
        else:
            # En caso de ser 2000 caracteres o más, sumamos +1 al contador que nos indica la posición del ultimo
            # string en el array y añadimos un nuevo string al array
            counter += 1
            messages_buffer.append(text)

    for message in messages_buffer:
        await ctx.send(message)


@bot.command(name="bot_test")
async def info_channel(ctx):
    """Test del canal"""

    # Se almacena el autor del mensaje
    sender = ctx.author

    # Se envía un mensaje con formato "@autor ha usado el bot." y se borra automática tras 15 segundos
    await ctx.send(f'{sender.mention} ha usado el bot.', delete_after=15.0)

    # Se almacena el canal por el que a sido mandado el mensaje
    channel = ctx.message.channel

    # Se envía un mensaje con formato "En el canal: NombreDElCanal. Con el id: IdDelCanal." y se borra automática
    # tras 15 segundos
    await ctx.send(f'En el canal: {channel}. Con el id: {channel.id}.', delete_after=15.0)

    # Se crea un array que almacenará strings. Los strings nunca superaran ni igualar los 2000 caracteres
    messages_buffer = ['Miembros del canal:\r\n']
    counter = 0

    # Iteramos sobre todos los miembros (no bots) del canal sobre el que fue mandado el comentario que invoco el bot
    for member in [member for member in bot.get_channel(channel.id).members if not member.bot]:

        # Creamos un string con formato "- NombreMiembroCanal" o "- NombreMiembroCanal alias NickMiembroCanal" si
        # tiene nick.
        text = f'- {member.name}' + f'{f" alias {member.nick}" if member.nick else ""}' + '\r\n'

        # Comprobamos si añadiendo el nuevo string al ultimo string almacenado no se superan los 2000 caracteres
        if (len(text) + len(messages_buffer[counter])) <= 2000:
            # En caso de ser menos de 2000 caracteres, concatenamos nuestro string con el ultimo string del array
            messages_buffer[counter] += text
        else:
            # En caso de ser 2000 caracteres o más, sumamos +1 al contador que nos indica la posición del ultimo
            # string en el array y añadimos un nuevo string al array
            counter += 1
            messages_buffer.append(text)

    # Se itera sobre el array, y se publica un mensaje por cada string que contenga. #
    # Estos mensajes se borran tras 15 segundos.
    for message in messages_buffer:
        await ctx.send(message, delete_after=15.0)


@bot.command()
async def boofear(ctx, *args):
    """Permite boofear intensamente a alguien del canal en el que se usa"""

    # Recuperamos el nombre o nick del usuario a boofear
    # En caso de estar compuesto por más de una palabra las juntamos por espacio
    target_name = " ".join(args)

    # Quien invoco al bot
    sender = ctx.author

    # ID del canal donde se ha invocado al bot
    channel = ctx.message.channel

    # Lista de miembros del canal
    member_list = bot.get_channel(channel.id).members

    # Recuperamos el usuario objetivo si existe
    target = [target_obj for target_obj in member_list if
              (target_obj.name == target_name or target_obj.nick == target_name)]

    # Si se a podido recuperar el usuario como objeto (y por lo tanto existe)
    if target:
        target = target[0]
        # Se comprueba si el nombre del usuario objetivo es igual al del usuario que mando el mensaje
        if target.name == sender.name:
            await ctx.send(f'{sender.mention} se ha boofeado a si mismo ! que vanidoso ...')

        # En caso de que el nombre del usuario objetivo no sea igual al del usuario que mando el mensaje
        else:
            await ctx.send(f'{sender.mention} ha boofeado intensamente a {target.mention}!')

    # Si no se ha podido recuperar ningún usuario
    else:
        await ctx.send(f'{sender.mention} no ha boofeado a nadie, solo pasaba a molestar, vaya pieza ...')


bot.run(TOKEN)
