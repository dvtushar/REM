import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing", "help"
]

starter_encouragements = [
    "cheer up", "hang in there", "you are great person/bot",
    "you have done great", "you are awesome"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('hello...Glad to meet you Master!')
    if message.content.startswith('$who are you'):
        await message.channel.send(
            'I am software application that is programmed to do certain tasks... inshort i am here to help you master!'
        )
    if message.content.startswith('$how are you'):
        await message.channel.send(
            'I am pretty well master,thanks for concerning for me how about you ... '
        )
    if message.content.startswith('$lol'):
        await message.channel.send('ha ha ik thats funny ')
    if message.content.startswith('$iloveyou'):
        await message.channel.send(
            'i dont know what to answer but that really makes me happy master....'
        )
    msg = message.content

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"].value

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(starter_encouragements))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("new encouraging message was added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")


keep_alive()
client.run(os.getenv('TOKEN'))
