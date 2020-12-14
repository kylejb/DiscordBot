import datetime
import logging
import discord
import hidden
import praw
from discord.ext import commands

# Logging: observe the HTTP requests
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger = logging.getLogger("prawcore")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Initialize Reddit to access API
reddit = praw.Reddit("discord-bot")
# Initialize Bot (discord) to access API
bot = commands.Bot(command_prefix="!")
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!verify"))
    print("Bot Online!")
    print("Discord Manager v0.1.0")
    print(f"Logged in as {bot.user.name}")
    print("==========")


@bot.command(pass_context=True)
async def test(ctx, *arg):
    message = ctx.message
    channel = message.channel
    author = message.author
    """This is currently printing the else statement even with unveri_id in role."""
    if hidden.unveri_id in (x.id for x in author.roles):
        await channel.send("You need to verify.")
    else:
        await channel.send("You are a verified member. Thanks! :)")


@bot.command(pass_context=True)
async def verify(ctx, *arg):
    member = discord.Member
    message = ctx.message
    channel = message.channel
    author = message.author
    v_role = discord.Object(id=hidden.veri_id)
    uv_role = discord.Object(id=hidden.unveri_id)
    addrole = member.add_roles
    remrole = member.remove_roles

    if hidden.veri_id in (x.id for x in author.roles):
        await channel.send("You are already a verified member.")

    elif hidden.unveri_id in (x.id for x in author.roles):
        try:

            if arg[0].startswith("/u/"):
                username = arg[0][3:len(arg[0])]
                print("elif-try-cleaned from '/u/'", username)

            elif arg[0].startswith("u/"):
                username = arg[0][2:len(arg[0])]
                print("elif-try-cleaned from 'u/'", username)

            else:
                username = arg[0]
                print("else", username)

            account = reddit.redditor(f"{username}")

            # Grab the user account
            try:
                cakeday = datetime.datetime.fromtimestamp(
                    int(account.created)
                ).strftime("%m/%d/%Y %H:%M:%S")
                # Terminal Output for debugging
                print("cakeeee", cakeday)
                # Discord bot process
                await addrole(author, v_role)
                await remrole(author, uv_role)
                await channel.send("Success: You are now a verified member!")
                # message author for confirmation and info
            except Exception:
                # Terminal Output for debugging
                print(f"{username} not found; Response: 404")
                # Discord Bot response to user issuing command / Feedback
                await channel.send(
                    """I was not able to find a reddit account with that username. Please check your spelling.
                    If you continue to receive this error message, contact `@Staff` for assistance.
                    """
                )
        except Exception:
            await channel.send(
                "Syntax Error: Please follow the form of ``!verify /u/username`` and try again."
            )


bot.run(hidden.token)
