import os
import discord
from discord.ext import commands

# Configure these via environment variables; never hardcode credentials.
TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("DISCORD_OWNER_ID", "0"))
JOIN_CHANNEL_ID = int(os.environ.get("DISCORD_JOIN_CHANNEL_ID", "0"))
LEAVE_CHANNEL_ID = int(os.environ.get("DISCORD_LEAVE_CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

def is_owner(ctx):
    return ctx.author.id == OWNER_ID

@bot.event
async def on_ready():
    print(f"Bot online als {bot.user}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(JOIN_CHANNEL_ID)
    if channel:
        await channel.send(f"Willkommen auf dem Server, {member.mention}! 👋")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(LEAVE_CHANNEL_ID)
    if channel:
        await channel.send(f"{member.name} ist leider geleavt. 👋")

@bot.command()
@commands.check(is_owner)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"{amount} Nachrichten gelöscht.", delete_after=3)

@bot.command()
@commands.check(is_owner)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} wurde gekickt.")

@bot.command()
@commands.check(is_owner)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} wurde gebannt.")

@bot.command()
@commands.check(is_owner)
async def ping(ctx):
    await ctx.send("Wie geht's dir?")

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("DISCORD_BOT_TOKEN environment variable is not set.")
    bot.run(TOKEN)
