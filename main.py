import discord
from discord.ext import commands
import os

# Get the token from the environment variable
TOKEN = os.getenv("DISCORD_TOKEN")

# Replace with your target voice channel ID
TARGET_CHANNEL_ID = os.getenv("CHANNEL_ID")

# Set up bot
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")
    
    # List all channels in all guilds the bot is a part of
    for guild in bot.guilds:
        print(f"Guild: {guild.name} (ID: {guild.id})")
        for channel in guild.channels:
            print(f" - Channel: {channel.name} (ID: {channel.id}) [{channel.type}]")

@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joins or leaves the target channel
    guild = member.guild
    channel_id = int(TARGET_CHANNEL_ID)  # Ensure it's an integer
    channel = guild.get_channel(channel_id)

    if channel:
        # Get the number of members in the channel
        member_count = len([m for m in channel.members if not m.bot])  # Exclude bots

        # Send a message if there are exactly 4 people
        if member_count == 4:
            general_text_channel = discord.utils.get(guild.text_channels, name="general")  # Replace with your text channel name
            if general_text_channel:
                await general_text_channel.send(f"Can you smell that?")

# Run the bot
if TOKEN is None:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")
bot.run(TOKEN)
