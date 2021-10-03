import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get

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

Event = Event()

# Getting the Discord Token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, description="Nothing to see here!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        owner = guild.owner
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            owner: discord.PermissionOverwrite(read_messages=True),
            }
        if not discord.utils.get(guild.text_channels, name='event_bot_admin'):
            channel = await guild.create_text_channel('event_bot_admin', overwrites=overwrites)
            await channel.send("Welcome to StateEventBot!\nType !Title <event title> to set the event title\nType !Description <event description> to set the event description\nType !Location <postcode in format XXXXXXX> to set the event location\nType !Time <event time> to set the time\nType !Channel <event channel> to set the channel the event will be posted in\nType !Saved to view your event details\nType !Post to post the event in the specified channel, otherwise the default #events channel is created\nType !Help to print the command list again\n")

    #print(guild.text_channels)
    for guild in bot.guilds:
        print(guild.owner)

    channel = discord.utils.get(guild.text_channels, name='event_bot_admin')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    elif str(message.channel) != 'event_bot_admin':
        return

    elif message.content.startswith("!Title"):
        print(message.channel)
        Event.Title = message.content[7:]
        await message.channel.send("Your Event Title has been saved")

    elif message.content.startswith("!Description"):
        Event.Description = message.content[13:]
        await message.channel.send("Your Event Description has been saved")

    elif message.content.startswith("!Help"):
        await message.channel.send("Welcome to StateEventBot!\nType !Title <event title> to set the event title\nType !Description <event description> to set the event description\nType !Location <postcode in format XXXXXXX> to set the event location\nType !Time <event time> to set the time\nType !Channel <event channel> to set the channel the event will be posted in\nType !Saved to view your event details\nType !Post to post the event in the specified channel, otherwise the default #events channel is created\nType !Help to print the command list again\n")

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

    elif message.content.startswith("!Time"):
        Event.Time = message.content[6:]
        await message.channel.send("Your Event Time has been saved")

    elif message.content.startswith("!Channel"):
        Event.Channel = message.content[9:]
        await message.channel.send("The Event Channel has been saved")

    elif message.content.startswith("!Saved"):
        await message.channel.send("Your Event Details:\n\nTitle - {}\n\nDescription - {}\n\nTime - {}\n\nGoogle Maps: {}\nSouthampton: {}\n\nChannel - {}\n\n".format(Event.Title, Event.Description, Event.Time, Event.LocationPostCode, Event.LocationArea, Event.Channel))

    elif message.content.startswith("!Read"):
        titlename = message.content[6:]
 
        file = open(titlename+".txt", "r")
        Names = file.readlines()
        file.close()
 
        for i in Names:
            await message.channel.send(i)

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

@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    if reaction.message.author == bot.user:
        print(user)
        message = """You have registered to {}.\n\nTime: {}\n\nLocation: {}""".format(Event.Title, Event.time, Event.LocationArea)

        embed = discord.Embed(title=message)
        await user.send(embed=embed)

        file = open(Event.Title+".txt", "a+")
        file.write(str(user)+"\n")
        file.close()

bot.run(TOKEN)
