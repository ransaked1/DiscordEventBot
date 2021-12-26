import os
from dotenv import load_dotenv

# Discord API imports.
import discord
from discord.ext import commands
from discord.utils import get

# Event object to store the data of an event created.
class Event:
    Title = ""
    Description = ""
    Location = ""
    LocationArea = ""
    Time = ""
    Channel = ""
    LocationPostCode = ""

    def __init__(self):
        Title = ""
        Description = ""
        Location = ""
        LocationArea = ""
        LocationPostCode = ""
        Time = ""
        Channel = ""

# Initializing an Event object
Event = Event()

# Getting the Discord Token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Enabling intents for the bot.
intents = discord.Intents.default()
intents.members = True

# Set the command prefix and intents.
bot = commands.Bot(command_prefix="!", intents=intents, description="Nothing to see here!")

# Setting up the bot on startup.
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    # Setup a channel that can only be seen by the server owner
    for guild in bot.guilds:
        owner = guild.owner
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            owner: discord.PermissionOverwrite(read_messages=True),
            }
        if not discord.utils.get(guild.text_channels, name='event_bot_admin'):
            channel = await guild.create_text_channel('event_bot_admin', overwrites=overwrites)
            await channel.send("Welcome to StateEventBot!\nType !Title <event title> to set the event title\nType !Description <event description> to set the event description\nType !Location <postcode in format XXXXXXX> to set the event location\nType !Time <event time> to set the time\nType !Channel <event channel> to set the channel the event will be posted in\nType !Saved to view your event details\nType !Post to post the event in the specified channel, otherwise the default #events channel is created\nType !Help to print the command list again\n")

    for guild in bot.guilds:
        print(guild.owner)

    # Save the channel for later use.
    channel = discord.utils.get(guild.text_channels, name='event_bot_admin')

# Watch for bot  in the owner channel.
@bot.event
async def on_message(message):

    # Don't listen to other bots.
    if message.author == bot.user:
        return

    # Don't listen to other text channels
    elif str(message.channel) != 'event_bot_admin':
        return

    # Set the title of the event.
    elif message.content.startswith("!Title"):
        print(message.channel)
        Event.Title = message.content[7:]
        await message.channel.send("Your Event Title has been saved")

    # Set the description of the event.
    elif message.content.startswith("!Description"):
        Event.Description = message.content[13:]
        await message.channel.send("Your Event Description has been saved")

    # Help command.
    elif message.content.startswith("!Help"):
        await message.channel.send("Welcome to StateEventBot!\nType !Title <event title> to set the event title\nType !Description <event description> to set the event description\nType !Location <postcode in format XXXXXXX> to set the event location\nType !Time <event time> to set the time\nType !Channel <event channel> to set the channel the event will be posted in\nType !Saved to view your event details\nType !Post to post the event in the specified channel, otherwise the default #events channel is created\nType !Help to print the command list again\n")

    # Set the location of the event from the options available.
    elif message.content.startswith("!Location"):

        def generate_google_maps_link(destination):
            return "https://www.google.com/maps/dir/?api=1&destination={}".format(destination)

        Event.LocationPostCode = generate_google_maps_link(message.content[10:17])

        await message.channel.send("Select one of the options available - '!option <option number>' ")
        locations = {"SUSU Cinema":"http://id.southampton.ac.uk/point-of-service/susu-cinema",
                        "Turner Sims Concert Hall":"http://id.southampton.ac.uk/point-of-service/turner-sims-concert-hall",
                        "John Hansard Gallery":"http://id.southampton.ac.uk/point-of-service/john-hansard-gallery",
                        "Nuffield Theatre":"http://id.southampton.ac.uk/point-of-service/nuffield-theatre"}

        count = 1
        for key in locations:
            await message.channel.send("{}. {}".format(count, key))
            count += 1

    elif message.content.startswith("!option"):
        locations = {"SUSU Cinema":"http://id.southampton.ac.uk/point-of-service/susu-cinema",
                        "Turner Sims Concert Hall":"http://id.southampton.ac.uk/point-of-service/turner-sims-concert-hall",
                        "John Hansard Gallery":"http://id.southampton.ac.uk/point-of-service/john-hansard-gallery",
                        "Nuffield Theatre":"http://id.southampton.ac.uk/point-of-service/nuffield-theatre"}

        n = int(message.content[7:])-1

        for i, key in enumerate(locations.keys()):
            if i == n :
                Event.LocationArea = locations[key]

        await message.channel.send("Your Event Location has been saved")

    # Set the time of the event.
    elif message.content.startswith("!Time"):
        Event.Time = message.content[6:]
        await message.channel.send("Your Event Time has been saved")

    # Set the channel where to advertise the event.
    elif message.content.startswith("!Channel"):
        Event.Channel = message.content[9:]
        await message.channel.send("The Event Channel has been saved")

    # Check the event info.
    elif message.content.startswith("!Saved"):
        await message.channel.send("Your Event Details:\n\nTitle - {}\n\nDescription - {}\n\nTime - {}\n\nGoogle Maps: {}\nSouthampton: {}\n\nChannel - {}\n\n".format(Event.Title, Event.Description, Event.Time, Event.LocationPostCode, Event.LocationArea, Event.Channel))

    # Read the users registered to the event.
    elif message.content.startswith("!Read"):
        titlename = message.content[6:]
 
        file = open(titlename+".txt", "r")
        Names = file.readlines()
        file.close()
 
        for i in Names:
            await message.channel.send(i)

    # Make the event public. Create an events channel if no channel specified at setup or post in the channel provided (or create it).
    elif message.content.startswith("!Post"):
        await message.channel.send("Event Details:\n\nTitle - {}\n\nDescription - {}\n\nTime - {}\n\nGoogle Maps - {}\n\nSouthampton - {}\n\nChannel - {}\n\n".format(Event.Title, Event.Description, Event.Time, Event.LocationPostCode, Event.LocationArea, Event.Channel))
        if not Event.Channel and not discord.utils.get(message.channel.guild.text_channels, name='events'):
            channel = await message.channel.guild.create_text_channel('events')
        elif not Event.Channel:
            channel = discord.utils.get(message.channel.guild.text_channels, name="events")
        elif Event.Channel and not discord.utils.get(message.channel.guild.text_channels, name=Event.Channel):
            channel = await message.channel.guild.create_text_channel(Event.Channel)
        else:
            channel = discord.utils.get(message.channel.guild.text_channels, name=Event.Channel)
        eventPost = await channel.send("""EVENT ANNOUNCEMENT!\n
{}\n\n
{}\n\n
Time: {}\n\n
Location: {}\n\n
Google Maps: {}\n\nSouthampton Location: {}\n\n
React to this message to sign up to the event.
        """.format(Event.Title, Event.Description, Event.Time, Event.Location, Event.LocationPostCode, Event.LocationArea))
    else:
        await message.channel.send("Command not recognized, type !Help for command list\n")

# Watch for users reacting to the event and register them to it.
@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    if reaction.message.author == bot.user:
        print(user)
        message = """You have registered to {}.\n\nTime: {}\n\nLocation: {}""".format(Event.Title, Event.Time, Event.LocationArea)

        embed = discord.Embed(title=message)
        await user.send(embed=embed)

        # Save the user details.
        file = open(Event.Title+".txt", "a+")
        file.write(str(user)+"\n")
        file.close()

# Start the bot.
bot.run(TOKEN)
