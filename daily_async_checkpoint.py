import discord
import asyncio
from datetime import datetime, UTC
import os
import sys

# Somente para testes locais
# from dotenv import load_dotenv
# load_dotenv()

# Configura o loop de eventos correto no Windows (somente necessário para rodar os testes locais)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configurações do Bot
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("❌ ERRO: O token do Discord não foi carregado. Verifique o GitHub Secrets.")

# GUILD_ID = 1176999745043042355  # ID do servidor Discord (teste)
GUILD_ID = 689105567943360549  # ID do servidor Discord (produção)
# CHANNEL_ID = 1176999745043042358  # ID do canal onde a thread será criada (teste)
CHANNEL_ID = 1336416604900298823  # ID do canal onde a thread será criada (produção)
# ROLE_ID = 1337293749075709995   # ID do cargo (teste)
ROLE_ID = 809389784635277342    # ID do cargo (produção)

# Definir a data inicial para sextas alternadas (ajuste conforme necessário)
# START_DATE = datetime(2025, 2, 14, tzinfo=UTC)  # Primeira sexta desejada com timezone UTC
START_DATE = datetime(2025, 3, 21, tzinfo=UTC)  # Primeira sexta desejada com timezone UTC

def should_run_today():
    today = datetime.now(UTC)
    weekday = today.weekday()

    # Executa todas as terças (1) e quintas (3)
    if weekday in [1, 3]:  
        print("✅ Hoje é terça ou quinta. Dia de daily assíncrona. O bot será executado.")
        return True

    # Executa a cada duas sextas-feiras a partir da data inicial (checkpoint)
    if weekday == 4:
        delta_days = (today - START_DATE).days
        if delta_days >= 0 and delta_days % 14 == 0:
            print("✅ Hoje é uma sexta de checkpoint. O bot será executado.")
            return True
        else:
            print("⏳ Hoje NÃO é uma sexta de checkpoint.")

    print("⏳ Hoje NÃO é um dia de execução programado. O bot não rodará.")
    return False

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    # Verifica se o bot deve rodar hoje
    if not should_run_today():
        print("⏳ O bot não rodará hoje. Encerrando...")
        await bot.close()
        return

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

    thread_name = f"Daily - {datetime.now(UTC).strftime('%d/%m')}"
    message = await channel.send(f"Bom dia, <@&{ROLE_ID}>!\n\n**Hoje é dia de daily assíncrona!**\nSegue a thread da daily de hoje. **Por favor preencham até 10:30**. 😁💚\n\nBom trabalho para todos!✨")
    thread = await message.create_thread(name=thread_name)
    await thread.send("✅ Comente aqui suas atualizações.\n**Não esqueçam de atualizar os cards no ClickUp e de atualizar seus calendários.**")

    print(f"✅ Thread '{thread_name}' criada com sucesso!")

    # Finaliza a conexão após a criação da thread
    await bot.close()

# Iniciar o bot
bot.run(TOKEN)