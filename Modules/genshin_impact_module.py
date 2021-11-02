import discord
from discord.ext import commands, tasks
from secrets import channel_dc_pruebas
from Games.Genshin_Impact import GI_templates as MessageTemplate, scraping_genshin_impact as sgi


class GenshinImpactModule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.genshin_data = sgi.GenshinImpact()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Se ha iniciado el modulo de Genshin Impact')
        print('------')
        print('Lanzando el bucle genshin_impact_new_codes()')
        self.genshin_impact_new_codes.start()
        print('------')
        print('Lanzando el bucle genshin_impact_new_banner_info()')
        self.genshin_impact_new_banner_info.start()
        print('------')

    @tasks.loop(hours=2)
    async def genshin_impact_new_codes(self):
        canal_genshin = self.bot.get_channel(channel_dc_pruebas)

        codes_notification = self.genshin_data.check_new_codes()

        for code_line in codes_notification:
            embed = discord.Embed(title=f"Nuevo código promocional detectado !", color=0xf805de)
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
            embed.add_field(name="Descubierto", value=code_line.start, inline=False)
            embed.add_field(name="Expira", value=code_line.end, inline=False)
            await canal_genshin.send(embed=embed)

    @commands.command(name="GenshinCodes")
    async def get_genshin_active_codes(self, ctx):
        """Permite obtener los códigos activos de Genshin Impact"""
        active_codes = self.genshin_data.get_active_codes()

        if active_codes:
            for code_line in active_codes:
                embed = discord.Embed(title=f"Código Activo", color=0xf805de)
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
                embed.add_field(name="Descubierto", value=code_line.start, inline=False)
                embed.add_field(name="Expira", value=code_line.end, inline=False)

                await ctx.send(embed=embed)

    @commands.command(name="GenshinBanners")
    async def get_genshin_banners(self, ctx, time_filter=None):
        valid_current_filters = ["Current", "Currents", "Actual", "Actuales"]
        valid_upcoming_filters = ["Upcoming", "Upcomings", "Futuro", "Futuros"]
        if time_filter and time_filter.capitalize() not in valid_current_filters + valid_upcoming_filters:
            return await ctx.send(f"Filtro incorrecto, se esperaba uno de los siguientes:"
                                  f"{valid_current_filters + valid_upcoming_filters}")

        if time_filter and time_filter.capitalize() in valid_current_filters:
            banners = self.genshin_data.get_current_banners()
        elif time_filter and time_filter.capitalize() in valid_upcoming_filters:
            banners = self.genshin_data.get_upcoming_banners()
        else:
            banners = self.genshin_data.get_current_banners() + self.genshin_data.get_upcoming_banners()

        if banners:
            for banner in banners:
                embed_title = "Banner {}".format("actual" if banner.status == "Current" else "futuro")
                message = MessageTemplate.generate_banner_message(embed_title, banner)

                await ctx.send(embed=message)
        else:
            await ctx.send("Actualmente no existe información sobre los banners actuales y futuros")

    @tasks.loop(hours=2)
    async def genshin_impact_new_banner_info(self):
        canal_genshin = self.bot.get_channel(channel_dc_pruebas)
        new_banners = self.genshin_data.check_new_banners()

        if new_banners['currents']:
            for banner in new_banners['currents']:
                message = MessageTemplate.generate_banner_message("Nuevo banner actual/Nueva información", banner)
                await canal_genshin.send(embed=message)

        if new_banners['upcoming']:
            for banner in new_banners['upcoming']:
                message = MessageTemplate.generate_banner_message("Nuevo banner futuro/Nueva información", banner)
                await canal_genshin.send(embed=message)


def setup(bot):
    bot.add_cog(GenshinImpactModule(bot))
