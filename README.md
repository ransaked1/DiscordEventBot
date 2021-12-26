# DiscordEventBot

Nanohack project developed in less than 10h by our team of 3. The hackathon was organized in October at the University of Southampton as part of the introduction week. 

The university community uses Discord for most of the societies that provide a multitude of events. Our idea was to write a Discord bot that would let these communities to create and advertise their events on their text channels and then keep track of the users registered to the event. 

To register for an event the user has to react to an event post and then receives a notification that they are registered to the event. This way users can have a single channel keeping track of all the events they registered to and admins have a convinient way to manage and advertise their events without emails or other third party software.

This MVP achieved the 3rd place at the competition. The project didn't get a full release because just a few weeks later [Discord released their own Event Feature](https://wersm.com/discord-announces-server-avatars-scheduled-events-and-new-accessibility-features/) making our solution obsolete. 

## Built With
* [Python-dotenv 0.15.0](https://pypi.org/project/python-dotenv/) - .env storing API keys
* [Discord API v9](https://discordpy.readthedocs.io/en/latest/api.html) - Discord API used to interact with Discord
* [Flask 1.1.2](https://discordpy.readthedocs.io/en/latest/api.html) - the server used to keep the repl.it VM always on
