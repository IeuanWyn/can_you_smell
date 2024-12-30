import discord
from discord.ext import commands
import os

# Get the token from the environment variable
TOKEN = os.getenv("DISCORD_TOKEN")

# Replace with your target voice channel ID
TARGET_CHANNEL_ID = 123456789012345678

# Set up bot
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joins or leaves the target channel
    guild = member.guild
    channel = guild.get_channel(TARGET_CHANNEL_ID)

    if channel:
        # Get the number of members in the channel
        member_count = len([m for m in channel.members if not m.bot])  # Exclude bots

        # Send a message if there are exactly 4 people
        if member_count == 4:
            general_text_channel = discord.utils.get(guild.text_channels, name="general")  # Replace with your text channel name
            if general_text_channel:
                await general_text_channel.send(f"There are now exactly 4 people in {channel.name}!")

# Run the bot
if TOKEN is None:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")
bot.run(TOKEN)
