import asyncio

import disnake
from disnake.ui import Button, View
from disnake.ext import commands

embed = disnake.Embed(
    title="",
    description="""
    # Поддержка сервера

    Нашли баг на сервере? 
    Нужна помощь администрации?
    
    **Мы готовы помочь вам решить любые проблемы!**
    """,
    colour=0x2b2d31
)
embed.set_footer(
    text="Вам ответят в ближайшее время",
)
embed.set_image(
    url="https://img.freepik.com/free-photo/little-grey-kitten-with-blue-eyes-lies-grey-couch_8353-7261.jpg?semt=ais_hybrid&w=740"
)

welcome_embed = disnake.Embed(
    title="",
    description="""
    # Помощь

    Опишите вашу проблему ниже, 
    администрация скоро ответит.
    """,
    color=0x2b2d31
)
welcome_embed.set_footer(
    text="Среднее время ответа: до 24 часов."
)
welcome_embed.set_image(
    url="https://preview.redd.it/5unn16axx1v81.jpg?width=640&crop=smart&auto=webp&s=19fcd170aadc63147c0a4492f43017a17f052a02"
)

class CloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="❌ Закрыть тикет", style=disnake.ButtonStyle.red, custom_id="close")
    async def close(self, button: Button, interaction: disnake.Interaction):

        author_id = int(interaction.channel.topic)
        author = await interaction.guild.fetch_member(author_id)

        close_embed = disnake.Embed(
            title="",
            description=f"""
            ## Обращение закрыто

            `❌` Ваш тикет был закрыт участником **{interaction.user}**.
            
            `❗` Если вы **не согласны** с решением - откройте тикет вновь.
            """,
        )

        await interaction.response.send_message(">>> `🔒` Тикет закрывается...")
        await asyncio.sleep(2)
        await interaction.channel.delete(reason=f"Тикет закрыт пользователем {interaction.author}")
        await author.send(embed=close_embed)


class SupportButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="🎫 Создать тикет", style=disnake.ButtonStyle.grey, custom_id="support_ticket")
    async def support_ticket(self, button: Button, interaction: disnake.Interaction):

        guild = interaction.guild

        # Создаем категорию если её нет
        category = disnake.utils.get(guild.categories, name="Тикеты")
        if not category:
            category = await guild.create_category("Тикеты")

        # Создаем канал тикета
        ticket_channel = await guild.create_text_channel(
            name=f"помощь-{interaction.user.name}",
            category=category,
            topic=str(interaction.user.id),
            reason=f"Тикет создан пользователем {interaction.user}"
        )

        # Настраиваем права доступа
        await ticket_channel.set_permissions(
            interaction.user,
            send_messages=True,
            read_messages=True,
            view_channel=True
        )

        # Отправляем подтверждение
        await interaction.response.send_message(
            f">>> `✅` Тикет создан: {ticket_channel.mention}",
            ephemeral=True
        )

        # Отправляем приветственное сообщение в тикет
        await ticket_channel.send(
            embed=welcome_embed,
            view=CloseButton()
        )

        await ticket_channel.send(
            content=f"@everyone",
            delete_after=1
        )


class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.persistent_views_added:
            self.bot.add_view(SupportButton())
            self.bot.add_view(CloseButton())
            self.persistent_views_added = True
            print("[Support] Персистентные View зарегистрированы")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def support(self, ctx):
        """Создает панель поддержки"""
        await ctx.send(embed=embed, view=SupportButton())


def setup(bot):
    bot.add_cog(SupportCog(bot))