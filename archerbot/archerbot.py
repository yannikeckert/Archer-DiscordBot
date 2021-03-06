import json
import logging
import os
import sys
from io import FileIO
import imagerandomizer

import discord

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
# TODO Use sys/os funcs to specify log path
handler = logging.FileHandler(filename='../archer.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Essential stuff like token and so on
auth_file = FileIO('../bot.json', mode='r')
json_object = json.load(auth_file)
bot_token = json_object['bot_token']
dev_id = int(json_object['dev_id'])
dev_command_prefix = json_object['dev_command_prefix']
auth_file.close()
client = discord.Client()
command_prefix = '>'

# Not so essential stuff
bot_activity = discord.Activity(name='EMIYA', type=discord.ActivityType.listening)
dev_user = None
chant = 'I am the bone of my sword\n' \
        'Steel is my body and fire is my blood\n' \
        'I have created over a thousand blades\n' \
        'Unknown to Death,\n' \
        'Nor known to Life.\n' \
        'Have withstood pain to create many weapons\n' \
        'Yet, those hands will never hold anything\n' \
        'So as I pray, Unlimited Blade Works.'


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    global dev_user
    dev_user = client.get_user(dev_id)
    await client.change_presence(activity=bot_activity)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(command_prefix):
        cmd = message.content[len(command_prefix):]
        if cmd == 'chant':
            await message.channel.send(chant)

        elif cmd == 'rin':
            await message.channel.send(file=imagerandomizer.image())

        elif cmd == 'embed':
            embed = discord.Embed(title='Unlimited Blade Works', color=discord.Colour.red())
            await message.channel.send(embed=embed)

    # TODO 'emiya' -> go to voice and play EMIYA

    elif message.content.startswith(dev_command_prefix) and message.author == dev_user:
        cmd = message.content[len(dev_command_prefix):]
        if cmd == 'restart':
            await message.channel.send('Restarting connection...')
            os.execl(sys.executable, sys.executable, *sys.argv)
            return

        elif cmd == 'close':
            await message.channel.send('Closing connection...')
            await client.close()


client.run(bot_token)
