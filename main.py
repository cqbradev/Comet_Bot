import discord, asyncio, os, platform, sys
from discord.ext.commands import Bot
from discord.ext import commands
if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config
from keep_alive import keep_alive
"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents
Default Intents:
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.guild_typing = False
intents.typing = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.guild_messages = True
intents.guild_reactions = True
intents.integrations = True
intents.invites = True
intents.voice_states = False
intents.webhooks = False
Privileged Intents (Needs to be enabled on dev page):
intents.presences = True
intents.members = True
"""

intents = discord.Intents.default()

bot = Bot(command_prefix=config.BOT_PREFIX, intents=intents)

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
	bot.loop.create_task(status_task())
	print(f"Logged in as {bot.user.name}")


async def status_task():
	while True:
		await bot.change_presence(activity=discord.Game("Hi Comet !!"))
		await asyncio.sleep(15)
		await bot.change_presence(activity=discord.Game("With cqbra"))
		await asyncio.sleep(15)
		await bot.change_presence(activity=discord.Game(f"{config.BOT_PREFIX} help"))
		await asyncio.sleep(15)
		await bot.change_presence(activity=discord.Game("With cqbra"))
		await asyncio.sleep(15)


bot.remove_command("help")

if __name__ == "__main__":
	for extension in config.STARTUP_COGS:
		try:
			bot.load_extension(extension)
			extension = extension.replace("cogs.", "")
			print(f"Loaded extension '{extension}'")
		except Exception as e:
			exception = f"{type(e).__name__}: {e}"
			extension = extension.replace("cogs.", "")
			print(f"Failed to load extension {extension}\n{exception}")

@bot.event
async def on_message(message):

	if message.author == bot.user or message.author.bot:
		return
	else:
		if message.author.id not in config.BLACKLIST:
			
			await bot.process_commands(message)
		else:
		
			context = await bot.get_context(message)
			embed = discord.Embed(
				title="You're blacklisted!",
				description="Ask the owner to remove you from the list if you think it's not normal.",
				color=0x00FF00
			)
			await context.send(embed=embed)


@bot.event
async def on_command_completion(ctx):
	fullCommandName = ctx.command.qualified_name
	split = fullCommandName.split(" ")
	executedCommand = str(split[0])
	print(f"Executed {executedCommand} command in {ctx.guild.name} by {ctx.message.author} (ID: {ctx.message.author.id})")


@bot.event
async def on_command_error(context, error):
	if isinstance(error, commands.CommandOnCooldown):
		embed = discord.Embed(
			title="Error!",
			description="This command is on a %.2fs cooldown" % error.retry_after,
			color=0x00FF00
		)
		await context.send(embed=embed)
	raise error
keep_alive()

bot.run(config.TOKEN)
