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
EXCLUDED_USER_IDS = os.getenv("EXCLUDED_USER_IDS")
EXCLUDED_USER_IDS = [int(user_id.strip()) for user_id in EXCLUDED_USER_IDS.split(",") if user_id.strip()]

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

# Dictionary to track the member count of channels
channel_member_count = {}

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
    global channel_member_count

    guild = member.guild
    target_channel = guild.get_channel(TARGET_CHANNEL_ID)

    if not target_channel:
        return  # Target channel doesn't exist or bot can't access it

    # Update the member count for the channel
    current_members = [m for m in target_channel.members if not m.bot and m.id not in EXCLUDED_USER_IDS]  # Exclude bots
    current_count = len(current_members)
    previous_count = channel_member_count.get(target_channel.id, 0)

    # Debug logs for tracking
    print(f"Channel {target_channel.name}: Previous count: {previous_count}, Current count: {current_count}")

    # Update the dictionary with the current count
    channel_member_count[target_channel.id] = current_count

    # Trigger message only if it goes from 3 -> 4
    if previous_count == 4 and current_count == 5:
        await post_message(guild)

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
