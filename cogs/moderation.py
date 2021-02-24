import os, sys, discord
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', pass_context=True)
    async def kick(self, context, member: discord.Member, *args):
        """
        Kick a user out of the server.
        """
        if context.message.author.guild_permissions.kick_members:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=490177
                )
                await context.send(embed=embed)
            else:
                try:
                    reason = " ".join(args)
                    embed = discord.Embed(
                        title="User Kicked!",
                        description=f"**{member}** was kicked by **{context.message.author}**!",
                        color=490177
                    )
                    embed.add_field(
                        name="Reason:",
                        value=reason
                    )
                    await context.send(embed=embed)
                    try:
                        await member.send(
                            f"You were kicked by **{context.message.author}**!\nReason: {reason}"
                        )
                    except:
                        pass
                except:
                    embed = discord.Embed(
                        title="Error!",
                        description="An error occurred while trying to kick the user.",
                        color=490177
                    )
                    await context.message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=490177
            )
            await context.send(embed=embed)

    @commands.command(name="nick")
    async def nick(self, context, member: discord.Member, *, name: str):
        """
        Change the nickname of a user on a server.
        """
        if context.message.author.guild_permissions.administrator:
            try:
                if name.lower() == "!reset":
                    name = None
                embed = discord.Embed(
                    title="Changed Nickname!",
                    description=f"**{member}'s** new nickname is **{name}**!",
                    color=490177
                )
                await context.send(embed=embed)
                await member.change_nickname(name)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to change the nickname of the user.",
                    color=490177
                )
                await context.message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=490177
            )
            await context.send(embed=embed)

    @commands.command(name="ban")
    async def ban(self, context, member: discord.Member, *args):
        """
        Bans a user from the server.
        """
        if context.message.author.guild_permissions.administrator:
            try:
                if member.guild_permissions.administrator:
                    embed = discord.Embed(
                        title="Error!",
                        description="User has Admin permissions.",
                        color=490177
                    )
                    await context.send(embed=embed)
                else:
                    reason = " ".join(args)
                    embed = discord.Embed(
                        title="User Banned!",
                        description=f"**{member}** was banned by **{context.message.author}**!",
                        color=490177
                    )
                    embed.add_field(
                        name="Reason:",
                        value=reason
                    )
                    await context.send(embed=embed)
                    await member.send(f"You were banned by **{context.message.author}**!\nReason: {reason}")
                    await member.ban(reason=reason)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to ban the user.",
                    color=490177
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=490177
            )
            await context.send(embed=embed)

    @commands.command(name="warn")
    async def warn(self, context, member: discord.Member, *args):
        """
        Warns a user in his private messages.
        """
        if context.message.author.guild_permissions.administrator:
            reason = " ".join(args)
            embed = discord.Embed(
                title="User Warned!",
                description=f"**{member}** was warned by **{context.message.author}**!",
                color=490177
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            await context.send(embed=embed)
            try:
                await member.send(f"You were warned by **{context.message.author}**!\nReason: {reason}")
            except:
                pass
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=490177
            )
            await context.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, num_messages):
      channel = ctx.message.channel
      await ctx.message.delete()
      await channel.purge(limit = num_messages, check = None, before = None)
      return True


def setup(bot):
    bot.add_cog(moderation(bot))
