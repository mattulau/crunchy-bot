import discord
from discord.ext import commands
from discord import app_commands
import certifi
import os
from dotenv import load_dotenv


load_dotenv(override=True)
TOKEN = os.getenv("DISCORD_TOKEN")

# Set all permissions for discord bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Set bot prefix as slash

client = commands.Bot(command_prefix='/', intents=intents)
@client.event # listener
async def on_ready():
    print(F'{client.user} is running.')
    try:
        synced = await client.tree.sync()
        print(F'Synced {len(synced)} tree commands.')
    except Exception as e:
        print(F'Could Not Sync Tree: {e}')
@client.tree.command(name="test")
async def func(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")

client.run(TOKEN)