import disnake
from disnake.ext import commands

class clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 1):

        delete_embed = disnake.Embed(
            title="",
            description=f"""
            ## Успешно!
            
            `❌` Удалено **{amount}** сообщений.
            """,
        )


        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(embed=delete_embed, delete_after=5)

def setup(bot):
    bot.add_cog(clear(bot))