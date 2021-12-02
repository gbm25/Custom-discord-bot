import discord
from discord.ext import commands
from secrets import token

allowed_icons = ["\U00000030\U0000FE0F\U000020E3",
                 "\U00000031\U0000FE0F\U000020E3",
                 "\U00000032\U0000FE0F\U000020E3",
                 "\U00000033\U0000FE0F\U000020E3",
                 "\U00000034\U0000FE0F\U000020E3",
                 "\U00000035\U0000FE0F\U000020E3",
                 "\U00000036\U0000FE0F\U000020E3",
                 "\U00000037\U0000FE0F\U000020E3",
                 "\U00000038\U0000FE0F\U000020E3",
                 "\U00000039\U0000FE0F\U000020E3",
                 "\U0001F51F"]

TOKEN = token

description = '''Croquetabot ! recién salido de la sartén 😁'''
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='?', description=description, intents=intents)


# bot.load_extension('Modules.genshin_impact_module')


@bot.event
async def on_ready():
    print(f'Se ha iniciado {bot.user.name}')
    print('------')


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


@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)

    # Caso en el que la reacción se produzca en un mensaje privado
    if channel.guild is None:
        return

    message = await channel.fetch_message(payload.message_id)

    # Comprueba que el mensaje sea del bot, que quien reacciona no sea el bot, y que sea una encuesta
    if message.author == bot.user and payload.member != bot.user \
            and message.embeds and message.embeds[0].title.startswith(f"\U0001F4CA Encuesta: "):

        embed = message.embeds[0]

        users_per_icon = {}

        for reaction in message.reactions:
            users_list = await reaction.users().flatten()
            users_per_icon[reaction] = users_list

        # Se borran las reacciones con iconos no presentes en la encuesta (reacción no iniciada por el bot)
        # Se eliminan también (de ser necesario) la clave de ese icono en el diccionario de usuarios por reacción
        for reaction, users_per_reaction in users_per_icon.copy().items():
            if bot.user not in users_per_reaction:
                for user in users_per_reaction:
                    await reaction.remove(user)
                del users_per_icon[reaction]

        users_per_reactions = [user for users in users_per_icon.values() for user in users]

        users_more_than_one_reaction = [user for user in set(users_per_reactions)
                                        if user != bot.user and users_per_reactions.count(user) > 1]

        # Si el usuario tiene mas de una reacción incluida en la encuesta, borra sus reacciones
        if users_more_than_one_reaction:
            for reaction, users in users_per_icon.copy().items():
                users_remove_reaction = [user for user in users_more_than_one_reaction if user in users]
                if users_remove_reaction:
                    for user in users_remove_reaction:
                        await reaction.remove(user)
                        users_per_icon[reaction].remove(user)

        poll_embed_dict = embed.to_dict()

        # TODO pasar conteo de votos y modificación de la encuesta a una función separada

        # Votos que hay en la encuesta
        list_votes_last_recount = {field.name.split()[0]: int(field.value.split()[1]) for field in embed.fields}
        # Votos que hay en las reacciones
        list_votes_now = {reaction.emoji: len(users_per_reaction) - 1 for reaction, users_per_reaction in
                          users_per_icon.items()}

        total_votes_now = sum(list_votes_now.values())

        new_fields_data = []

        if list_votes_now != list_votes_last_recount:
            for reaction, users_per_reaction in users_per_icon.items():
                reaction_count = len(users_per_reaction) - 1
                vote_percentage = reaction_count / total_votes_now * 100 if reaction_count > 0 else 0

                target_field = [field for field in embed.to_dict()['fields'] if
                                field['name'].split()[0] == reaction.emoji]

                if not target_field:
                    continue

                target_field = target_field[0]
                # Estructura = ["Votes:", Nº de votos, "(porcentaje%)"]
                vote_info = target_field['value'].split()

                vote_info[1] = str(reaction_count)
                vote_info[2] = f'({vote_percentage}%)'
                target_field['value'] = ' '.join(vote_info)

                new_fields_data.append(target_field)

            poll_embed_dict['fields'] = new_fields_data

            await message.edit(embed=discord.Embed.from_dict(poll_embed_dict))


@bot.event
async def on_raw_reaction_remove(payload):
    channel = bot.get_channel(payload.channel_id)

    # Caso en el que la reacción se produzca en un mensaje privado
    if channel.guild is None:
        return

    message = await channel.fetch_message(payload.message_id)

    if message.author == bot.user and message.embeds and message.embeds[0].title.startswith(f"\U0001F4CA Encuesta: "):

        users_per_icon = {}

        for reaction in message.reactions:
            users_list = await reaction.users().flatten()
            users_per_icon[reaction] = users_list

        embed = message.embeds[0]

        poll_embed_dict = embed.to_dict()

        # TODO pasar conteo de votos y modificación de la encuesta a una función separada

        # Votos que hay en la encuesta
        list_votes_last_recount = {field.name.split()[0]: int(field.value.split()[1]) for field in embed.fields}
        # Votos que hay en las reacciones
        list_votes_now = {reaction.emoji: len(users_per_reaction) - 1 for reaction, users_per_reaction in
                          users_per_icon.items()}

        total_votes_now = sum(list_votes_now.values())

        new_fields_data = []

        if list_votes_now != list_votes_last_recount:
            for reaction, users_per_reaction in users_per_icon.items():
                reaction_count = len(users_per_reaction) - 1
                vote_percentage = reaction_count / total_votes_now * 100 if reaction_count > 0 else 0

                target_field = [field for field in embed.to_dict()['fields'] if
                                field['name'].split()[0] == reaction.emoji]

                if not target_field:
                    continue

                target_field = target_field[0]
                # Estructura = ["Votes:", Nº de votos, "(porcentaje%)"]
                vote_info = target_field['value'].split()

                vote_info[1] = str(reaction_count)
                vote_info[2] = f'({vote_percentage}%)'
                target_field['value'] = ' '.join(vote_info)

                new_fields_data.append(target_field)

            poll_embed_dict['fields'] = new_fields_data

            await message.edit(embed=discord.Embed.from_dict(poll_embed_dict))


@bot.command(name="CreatePoll")
async def poll(ctx, *args):
    await ctx.message.delete()

    poll_title = args[0]
    poll_options = args[1:]

    # TODO Forzar los limites de los embebidos
    # title: 256 characters
    # description: 4096 characters
    # fields: Up to 25 field objects
    # field.name: 256 characters
    # field.value: 1024 characters
    # footer.text: 2048 characters
    # author.name: 256 characters

    if len(poll_options) > len(allowed_icons):
        await ctx.send("Overflow \U0001F92C", delete_after=15.0)
        return
    await ctx.send("Working ...", delete_after=15.0)

    message = [f"{allowed_icons[i]} {option}" for i, option in enumerate(poll_options)]

    embed = discord.Embed(title=f"\U0001F4CA Encuesta: {poll_title}", color=0xf805de)
    for i in range(len(poll_options)):
        embed.add_field(name=f"{message[i]}", value="Votos: 0 (0%)", inline=False)

    poll_embed = await ctx.send(embed=embed)

    for i in range(len(poll_options)):
        await poll_embed.add_reaction(allowed_icons[i])


bot.run(TOKEN)
