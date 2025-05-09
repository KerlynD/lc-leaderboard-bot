import typing
import discord
from discord.ext import commands
from discord import app_commands
import lib.dbfuncs as dbfuncs


class Adminclear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Points cog loaded")

    @app_commands.command(
        name="zclear",
        description="clear the ENTIRE leaderboard (points and wins) (ADMIN ONLY)",
    )
    @app_commands.describe(confirmation="type CONFIRM to confirm a clear")
    async def Adminclear(
        self,
        interaction: discord.Interaction,
        confirmation: typing.Optional[str],
    ):
        await interaction.response.defer()
        admins = dbfuncs.get_admins()
        admins = set([admin[0] for admin in admins])
        if interaction.user.id in admins:
            if confirmation != "CONFIRM":
                await interaction.followup.send("No confirmation, clear cancelled")
                return
            else:
                dbfuncs.CLEAR_ALL_POINTS(wins=True)
                await interaction.followup.send("Leaderboard has been cleared")

        else:
            await interaction.followup.send("You are not an admin")


async def setup(bot):
    await bot.add_cog(Adminclear(bot))
