import discord
from discord.ext import commands, tasks
from secrets import channel_dc_pruebas
import scraping_genshin_impact as sgi


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

    @tasks.loop(hours=2)
    async def genshin_impact_new_codes(self):
        canal_genshin = self.bot.get_channel(channel_dc_pruebas)

        codes_notification = self.genshin_data.check_new_codes()

        for code_line in codes_notification:
            embed = discord.Embed(title=f"Nuevo código promocional detectado !", color=0xf805de)
            embed.add_field(name="Código promocional", value=code_line.promotional_code, inline=False)
            embed.add_field(name="Enlace externo", value=code_line.external_link, inline=False)
            embed.add_field(name="Servidor", value=code_line.server, inline=False)
            embed.add_field(name="Recompensas", value="\r\n".join([f'- {reward.item_name} x{reward.quantity}' for reward
                                                                   in code_line.rewards]), inline=False)
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
                embed.add_field(name="Recompensas",
                                value="\r\n".join([f'- {reward.item_name} x{reward.quantity}' for reward
                                                   in code_line.rewards]), inline=False)
                embed.add_field(name="Estado", value=code_line.status, inline=False)
                embed.add_field(name="Descubierto", value=code_line.start, inline=False)
                embed.add_field(name="Expira", value=code_line.end, inline=False)

                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GenshinImpactModule(bot))
