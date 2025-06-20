import discord

import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # Dicionário de gatilhos e respostas
  responses = {
    'Tá vivo filho?': 'To sim pai!',
    'furry': 'Gabrielfa mentioned?!',
    'gaster': 'https://tenor.com/view/gaster-undertale-dance-gif-5836109348403729714',
    'doom': 'parem de falar de doom por favor 😭',
    'skibidi': 'USA PALAVRA QUE EXISTE',
    'jogo': 'perdi',
  }
  
  # Checar se a mensagem contém algum gatilho
  message_lower = message.content.lower()
  
  for trigger, response in responses.items():
    if trigger.lower() in message_lower:
      await message.channel.send(response)
      break  # Só responde uma vez por mensagem
  
client.run(os.getenv('BOT_TOKEN'))
