import asyncio
import datetime
import logging
import praw
import discord
from discord.ext import commands
from discord.ext.commands import Bot

import hidden

# Logging: observe the HTTP requests that PRAW is issuing
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
    print("Judgy Judge v0.1")
    print(f"Logged in as {bot.user.name}")
    print("==========")


@bot.command(pass_context=True)
async def test(ctx, *arg):
    message = ctx.message
    channel = message.channel
    author = message.author
    # This is currently printing the else statement regardless of whether i have unveri_id in my role; bot responds though
    if hidden.unveri_id in [x.id for x in author.roles]:
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

    if hidden.veri_id in [x.id for x in author.roles]:
        await channel.send("You are already a verified member.")

    elif hidden.unveri_id in [x.id for x in author.roles]:
        try:

            if arg[0].startswith("/u/"):
                username = arg[0][3 : len(arg[0])]
                print("elif-try-cleaned from '/u/'", username)

            elif arg[0].startswith("u/"):
                username = arg[0][2 : len(arg[0])]
                print("elif-try-cleaned from 'u/'", username)

            else:
                username = arg[0]
                print("else", username)

            account = reddit.redditor(f"{username}")

            # Grab the user account
            # if false account will produce 404 http response, so adding try/except around that parameter
            try:
                cakeday = datetime.datetime.fromtimestamp(
                    int(account.created)
                ).strftime("%m/%d/%Y %H:%M:%S")
                # Terminal Output for debugging
                print("cakeeee", cakeday)
                # Discord bot process
                await addrole(author, v_role)
                await remrole(author, uv_role)
                await channel.send("Success: You are now a verified member of /r/LSAT!")
                print("Adding verified role...")
                print("Removing unverified role from discord user...")
                print("Done.")
            except:
                # Terminal Output for debugging
                print(f"{username} not found; Response: 404")
                # Discord Bot response to user issuing command / Feedback
                await channel.send(
                    "I was not able to find a reddit account with that username. Please double check your spelling and/or formatting before trying again. If you continue to receive this error message, contact `@Staff` for assistance."
                )
        except:
            await channel.send(
                "Syntax Error: Please follow the form of ``!verify /u/username`` and try again."
            )


bot.run(hidden.token)


## Questions/Future Plans
# Need to add role, remove role... maybe auto add role for new members?

# Event loop stopped before future completed ??
# b/c i hit control+c too many times before allowing bot to clean up??
# why delay in bot logging off server?

"""
HOW DO I USE THIS... is this better for debugging?
try:
    pass
except expression as identifier:
    pass
"""
