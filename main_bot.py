import discord
from discord.ext import commands
from secrets import token
from config import command_prefix
import re
from typing import Union, List

TOKEN = token

description = '''Croquetabot ! recién salido de la sartén 😁'''

intents = discord.Intents().all()

bot = commands.Bot(command_prefix=command_prefix, description=description, intents=intents)

bot.load_extension('Modules.genshin_impact_module')


@bot.event
async def on_ready():
    print(f'Se ha iniciado {bot.user.name}')
    print('------')
    print('Se cambia el estado del bot')
    print('------')
    await bot.change_presence(activity=discord.Game(name=f'Croquetabot! | {command_prefix}help'))


@bot.command(name="SetSatisChannel")
async def set_satisfactory_channel(ctx, satis_channel=""):
    """Define el canal en el que se realizarán las acciones relacionadas con Satisfactory"""

    await ctx.send(f"No te voy a mentir, esto aun no esta implementado, y {satis_channel} no se usa")


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

    # Borramos el mensaje que activa el comando
    await ctx.message.delete()

    # Quien invoco al bot
    sender = ctx.author

    # ID del canal donde se ha invocado al bot
    channel = ctx.message.channel

    # Lista de miembros del canal
    member_list = bot.get_channel(channel.id).members

    def _get_target_user(user_to_search: Union[str, int], channel_members_list: List[discord.Member]):
        """
        Devuelve una lista de discord.Member que contiene el/los usuario/s que coincidan con el contenido pasado en
        el parámetro user_to_search.

        :param user_to_search: user id, name or nick
        :param channel_members_list: list of members where user_to_search will be search

        :return: list of matched user
        :rtype: list of discord.Member
        """

        retrieved_users = []

        # Comprobamos si lo que se nos pasa es un int (id del usuario) o un string (el nombre o nick del usuario)
        # Dependiendo del tipo, contrastamos contra la lista de miembros que nos pasan filtrando por el id
        # de los miembros de esa lista, o pr su nombre o nick
        if isinstance(user_to_search, int):
            retrieved_users = [member for member in channel_members_list if member.id == user_to_search]
        elif isinstance(user_to_search, str):
            retrieved_users = [member for member in channel_members_list if
                               (member.name == user_to_search or member.nick == user_to_search)]

        return retrieved_users

    targets = []

    for user in args:

        # Comprobamos si el usuario es una mención.
        # Las menciones pueden tener los siguientes formatos:
        # <@!00000000000000000> : Si el usuario usa un nick en ese servidor
        # <@00000000000000000> : Si el usuario no usa un nick en ese servidor
        # El id de usuario esta formado por 17 o más números
        user_id_pattern = r'<@!?([0-9]{17,})>'

        user_id = re.match(user_id_pattern, user)

        if user_id and int(user_id.group(1)) in [member.id for member in member_list]:
            target = _get_target_user(int(user_id.group(1)), member_list)
        else:
            target = _get_target_user(user, member_list)

        if len(target) > 1:
            await ctx.send(f'Existe más de un usuario con el nombre o nick "{user}"'
                           f'en este servidor, ¡ necesito que te decidas !')
            return
        if not target:
            await ctx.send(f'No encontre a ningún usuario que se llame "{user}".\r\n'
                           f'Recuerda, el formato es `{command_prefix}boofear "nombre o nick del usuario"`'
                           f' o `{command_prefix}boofear @MenciónUsuario`\r\n'
                           f'(Este mensaje se borrará a los 25 segundos de ser publicado.)',
                           delete_after=25.0)
            return
        else:
            targets.append(*target)

    # Si se ha podido recuperar el usuario como objeto (y por lo tanto existe)
    if targets:
        # Se comprueba si el nombre del usuario objetivo es igual al del usuario que mando el mensaje
        if sender in targets:
            await ctx.send(f'{sender.mention} ha intentado boofearse a si mismo ! que vanidoso ...')

        # En caso de que el nombre del usuario objetivo no sea igual al del usuario que mando el mensaje
        else:
            await ctx.send(f'{sender.mention} ha boofeado intensamente a '
                           f'{", ".join([user.mention for user in targets])}!')

    # Si no se ha podido recuperar ningún usuario
    else:
        await ctx.send(f'Mmmmm parece que algo ha salido mal ... \r\n'
                       f'Recuerda, el formato es `{command_prefix}boofear "nombre o nick del usuario"`'
                       f' o `{command_prefix}boofear @MenciónUsuario`\r\n'
                       f'(Este mensaje se borrará a los 25 segundos de ser publicado.)',
                       delete_after=25.0)


bot.run(TOKEN)
