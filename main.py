import discord
from discord.ext import commands
from discord import app_commands
import certifi
import os
from dotenv import load_dotenv
import requests
import pdb
import urllib.parse

load_dotenv(override=True)
TOKEN = os.getenv("DISCORD_TOKEN")

# Set all permissions for discord bot
intents = discord.Intents.all()
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

@client.tree.command(name="apitest")
async def func(interaction: discord.Interaction):
    response = requests.get("https://crunchy.garden/api/hello")
    await interaction.response.send_message(response.json())

@client.tree.command(name="crunchy")
async def func(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    print(prompt)
    response = requests.get(f"https://crunchy.garden/api/agent-reply?message={prompt}")
    response_obj = response.json()
    print(response_obj)
    await interaction.edit_original_response(content=response_obj["reply"])

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        question = message.content.split(" ")[1]
        response = requests.get(f"https://crunchy.garden/api/agent-reply?message={question}")
        response_obj = response.json()
        actual_res = response_obj["reply"]

        await message.channel.send(actual_res, reference=message)

client.run(TOKEN)