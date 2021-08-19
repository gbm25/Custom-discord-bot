import discord

def generate_code_message(embed_title: str, code_line):
    embed = discord.Embed(title=f"{embed_title}", color=0xf805de)
    embed.add_field(name="Código promocional", value=code_line.promotional_code, inline=False)
    embed.add_field(name="Enlace externo", value=code_line.external_link, inline=False)
    embed.add_field(name="Servidor", value=code_line.server, inline=False)
    if code_line.rewards:
        embed.add_field(name="Recompensas",
                        value="\r\n".join([f'- {reward.item_name} x{reward.quantity}' for reward
                                           in code_line.rewards]
                                          ), inline=False)
    else:
        embed.add_field(name="Recompensas", value="Recompensa no especificada", inline=False)
    embed.add_field(name="Estado", value=code_line.status, inline=False)
    embed.add_field(name="Descubierto", value=code_line.start, inline=True)
    embed.add_field(name="Expira", value=code_line.end, inline=True)

    return embed

def generate_banner_message(embed_title: str, banner):
    embed = discord.Embed(title=f"{embed_title}", color=0xf805de)
    embed.set_thumbnail(url=banner.image)
    embed.add_field(name="Nombre del evento: ", value=banner.name, inline=False)
    embed.add_field(name="Tipo de banner: ", value=banner.wish_type, inline=False)

    if banner.url_fandom:
        embed.add_field(name="URL fandom: ", value=banner.url_fandom, inline=False)
        embed.add_field(name="URL anuncio oficial: ", value=banner.url_official, inline=False)

        for time in banner.start:
            embed.add_field(name=f"Hora de inicio ({time.region.capitalize().replace('_', ' ')}): ",
                            value=banner.get_start_time(time.region), inline=True)
        for time in banner.end:
            embed.add_field(name=f"Hora de fin ({time.region.capitalize().replace('_', ' ')}): ",
                            value=banner.get_end_time(time.region), inline=True)
    if banner.status == "Current":
        for time in banner.end:
            embed.add_field(name=f"Tiempo restante ({time.region.capitalize().replace('_', ' ')}): ",
                            value=banner.remain_time(time.region, True), inline=True)
    elif banner.status == "Upcoming":
        for time in banner.start:
            embed.add_field(name=f"Tiempo hasta comienzo ({time.region.capitalize().replace('_', ' ')}): ",
                            value=banner.time_until(time.region, True), inline=True)

    return embed
