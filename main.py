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


# @client.tree.command(name="crunchy")
# async def func(interaction: discord.Interaction):
#     response = requests.get("https://crunchy.garden/api/hello")
#     await interaction.response.send_message(response.json())


@client.tree.command(name="crunchy")
async def func(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    print(prompt)
    response = requests.get(f"https://crunchy.garden/api/agent-reply?message={prompt}")
    response_obj = response.json()
    print(response_obj)
    # reply = """{"reply": "Hello! Thank you for reaching out. It seems like you may have a typo in your message, but that's okay! To answer your question, my day has been going well. As someone who is passionate about sustainability and gardening, I have been busy researching ways to help individuals cultivate eco-friendly and thriving gardens. In terms of sustainability, I have been looking into practices such as composting, water conservation, and reducing waste in the garden. Composting is a great way to recycle organic matter and create nutrient-rich soil for plants. Additionally, using rainwater harvesting techniques can help reduce water usage and provide a natural source of irrigation for your garden. When it comes to gardening, I have been studying various planting techniques, soil health, and pest management strategies. Crop rotation, companion planting, and using organic fertilizers are just a few ways to promote healthy plant growth and maximize yields in the garden. Furthermore, using natural predators and organic pesticides can help control pests without harming beneficial insects or the environment. "}"""
    # await interaction.response.send_message(response_obj["reply"])
    await interaction.edit_original_response(content=response_obj["reply"])


client.run(TOKEN)