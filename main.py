import discord
from discord.ext import commands
import os
import requests
import random

# Get the token from the environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_TOKEN = os.getenv("GIPHY_TOKEN")
TEXT_CHANNEL_NAME = os.getenv("TEXT_CHANNEL_NAME")
TARGET_CHANNEL_ID = os.getenv("CHANNEL_ID")

# Ensure all required environment variables are present
if not TOKEN or not TARGET_CHANNEL_ID:
    raise ValueError("Required environment variables are missing.")

TARGET_CHANNEL_ID = int(TARGET_CHANNEL_ID)  # Convert channel ID to integer

# Set up bot
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Slash command example
@bot.tree.command(name='smell', description='Check if something smells')
async def smell(interaction: discord.Interaction):
    await post_message(interaction.guild)

# Fetch a random GIF
def get_random_gif(query):
    url = "https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": GIPHY_TOKEN,
        "q": query,
        "limit": 10,
        "rating": "pg",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        gifs = response.json().get("data")
        if gifs:
            return random.choice(gifs)["url"]
    return None

# Post a message in the target channel
async def post_message(guild):
    channel = guild.get_channel(TARGET_CHANNEL_ID)

    if channel:
        member_count = len([m for m in channel.members if not m.bot])  # Exclude bots
        if member_count == 1:  # Adjust condition as needed
            general_text_channel = discord.utils.get(guild.text_channels, name=TEXT_CHANNEL_NAME)
            if not general_text_channel:
                general_text_channel = discord.utils.get(guild.text_channels, name="general")
            if general_text_channel:
                gif_url = get_random_gif("Can you smell that?")
                if gif_url:
                    await general_text_channel.send(gif_url)
                else:
                    await general_text_channel.send("Can you smell that?")

# Event for voice state updates
@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    await post_message(guild)  # Ensure the function is awaited

# Event when the bot is ready
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()  # Sync application commands
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    print(f"Bot is ready! Logged in as {bot.user}")

# Run the bot
bot.run(TOKEN)
