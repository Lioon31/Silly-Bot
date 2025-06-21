import discord
import os
import asyncio
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

  # >> FUNÇÃO AJUDA <<
  if message.content.startswith("!ajuda"):
    Servidor = message.guild.name
    Boas_Vindas = f"""
Precisa de ajuda?
Bom dia! me chamo ***Lenny Bot*** e atualmente sou um *assistente virtual* do servidor :boom: `{Servidor}` :cat: para oferecer ajuda e funções divertidas (ou chatas)
-# Criado por lioon31
# FUNÇÕES

##  ↪ Calculadora
`r (digite a expressão)` |  Some, subtraia, multiplique, divida, aceite seu cruel destino e muito mais! O resultado deve vir logo abaixo.

##  ↪ Lembrete
`!lembrar (minutos) (assunto)` | No tempo escolhido irei te marcar te lembrando de algo específico! Pode ser sobre levar o cachorro para passear, beber água, ou lembrar você do momento em que o sol virar uma gigante vermelha. Você que escolhe!

##  ↪ Inteligência Artificial (ehh, nem tanto)
`funcionalidade depende` | Posso responder palavras-chave específicas com palavras pré-definidas! Uhh, ehh, não ache estranho que eu respondo sempre com a mesma coisa. Eu sou tímido, tá bom?! Nunca viu robô tímido?

---

APROVEITE MINHA ASSISTÊNCIA ENQUANTO HÁ TEMPO, POIS EU SÓ FUNCIONO ENQUANTO O MALDITO DO LIOON ESTIVER ACORDADO PORQUE O VAGABUNDO NÃO TEM DINHEIRO PRA PAGAR UM SERVIDOR PRA ME MANTER ATIVO 24 HORAS!!!

Isso é tudinho!"""
    
    await message.channel.send(Boas_Vindas)


  # >> FUNÇÃO LEMBRETE <<
  if message.content.startswith("!lembrar "):
    try:
     parts = message.content.split(" ", 2)
     tempo_min = int(parts[1])
     lembrete = parts[2]

     await message.channel.send(f"Okay!! to voltando daqui a {tempo_min} minutos pra te lembrar sobre `{lembrete}`")
     await asyncio.sleep(tempo_min * 60)
     await message.channel.send(f"🚨 {message.author.mention}, tu mando eu te lembrar de `{lembrete}`, então **ACORDA** 🚨")

    except (IndexError, ValueError):
      await message.channel.send(f"?????? amigo não é assim que funciona. Preciso do tempo em minutos")

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

client.run(os.getenv('BOT_TOKEN'))
