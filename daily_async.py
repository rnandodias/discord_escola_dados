import discord
import asyncio
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

# Configura o loop de eventos correto no Windows (somente necessário para rodar os tesstes locais)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configurações do Bot
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("❌ ERRO: O token do Discord não foi carregado. Verifique o GitHub Secrets.")

GUILD_ID = 1176999745043042355  # ID do servidor Discord
CHANNEL_ID = 1176999745043042358  # ID do canal onde a thread será criada

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    """Essa função é chamada quando o bot estiver pronto e conectado"""
    print(f"✅ {bot.user} conectado com sucesso!")

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Servidor não encontrado.")
        await bot.close()
        return

    channel = guild.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Canal não encontrado.")
        await bot.close()
        return

    # Criando um nome único para a thread com a data atual
    thread_name = f"Daily - {datetime.now().strftime('%d/%m')}"
    thread = await channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)
    
    # Mensagem inicial na thread
    await thread.send("Bom dia, pessoal! Segue a thread da daily de hoje. Por favor preencham até 10:30. 😁💚")

    print(f"✅ Thread '{thread_name}' criada com sucesso!")

    # Finaliza a conexão após a criação da thread
    await bot.close()

# Iniciar o bot
bot.run(TOKEN)
