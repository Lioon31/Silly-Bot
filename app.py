import discord
import os
import asyncio
import datetime
from dotenv import load_dotenv, dotenv_values

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  client.loop.create_task(verificar_lembretes(client))  # Inicia a verificação

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # >> FUNÇÃO AJUDA <<
  if message.content.startswith("!ajuda"):
    Servidor = message.guild.name
    with open("BoasVindas.txt", "r", encoding="utf-8") as mensagem:
      Boas_Vindas = mensagem.read().strip()
    
    await message.channel.send(Boas_Vindas)
  
    return

  # >> FUNÇÃO LEMBRETE <<
  if message.content.startswith("!lembrar "):
    try:
      parts = message.content.split(" ", 2)
      tempo_min = int(parts[1])
      lembrete = parts[2]
      
      agora = datetime.datetime.now()
      quando = agora + datetime.timedelta(minutes=tempo_min)

      # --Salvar os lembretes no banco de dados com o canal--
      with open("lembretes.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{message.author.id}|{message.channel.id}|{quando.isoformat()}|{lembrete}\n")

      await message.channel.send(f"Okay!! to voltando daqui a {tempo_min} minutos pra te lembrar sobre `{lembrete}`")

    except (IndexError, ValueError):
      await message.channel.send(f"❌ ?????? Amigo, não é assim que funciona. Tente: `!lembrar 5 comer lanche`")

  # >> FUNÇÃO DE CALCULADORA <<
  if message.content.startswith("r "):
    expression = message.content[2:].strip()
    try:
      result = eval(expression, {"__builtins__": {}}, {})
      await message.channel.send(f"🧮 Resultado: `{result}`")
    except Exception as e:
      await message.channel.send("❌ Algo deu muito errado, porque tu não tenta `r 2 + 2`?")

    return  # Para evitar que o bot responda duas vezes e fique de xereca

  # >> FUNÇÃO DE RESPOSTA <<
  responses = {
    'Tá vivo filho?': 'To sim pai!',
    'furry': 'Gabrielfa mentioned?!',
    'gaster': 'https://tenor.com/view/gaster-undertale-dance-gif-5836109348403729714',
    'doom': 'parem de falar de doom por favor 😭',
    'skibidi': 'USA PALAVRA QUE EXISTE',
    'o jogo': 'perdi',
  }
  
  message_lower = message.content.lower()
  
  for trigger, response in responses.items():
    if trigger.lower() in message_lower:
      await message.channel.send(response)
      break

# --ACESSAR BANCO DE DADOS DOS LEMBRETES--
async def verificar_lembretes(bot):
  await bot.wait_until_ready()

  while not bot.is_closed():
    await asyncio.sleep(60)

    novos_lembretes = []
    try:
      with open("lembretes.txt", "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

      agora = datetime.datetime.now()

      for linha in linhas:
        user_id, canal_id, quando_str, texto = linha.strip().split("|")
        quando = datetime.datetime.fromisoformat(quando_str)

        if agora >= quando:
          canal = bot.get_channel(int(canal_id))
          if canal:
            await canal.send(f"🚨 <@{user_id}>, tu mando eu te lembrar de `{texto}`, então **ACORDA** 🚨")
        else:
          novos_lembretes.append(linha)

      with open("lembretes.txt", "w", encoding="utf-8") as arquivo:
        arquivo.writelines(novos_lembretes)

    except Exception as e:
      print(f"Erro ao verificar lembretes: {e}")

client.run(os.getenv('BOT_TOKEN'))
