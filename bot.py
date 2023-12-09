# bot.py
import os
import discord
from dotenv import load_dotenv
import psutil
import subprocess
import logging
logging.basicConfig(filename='bot_commands.log', level=logging.INFO, format='%(asctime)s - %(message)s')
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
serverDirectory = os.getenv('SERVER_DIRECTORY')
serverCommand = os.getenv('SERVER_DIRECTORY') + 'run.bat'
bot = commands.Bot(command_prefix='!')


serverStatusList = {
    "online": "🟢",
    "offline": "🔴"
}
avaliableCommands = [
    "!help Comando para ver todos los comandos disponibles y sus funciones",
    "!status: Comando para consultar el estado del servidor de minecraft",
    "!start: Comando para iniciar el servidor (solo se ejecuta el servidor si no está en marcha)"
]

def get_server_status():
    # Replace 'your_server_command' with the actual command to start your Minecraft server
    server_command = "ServerForge\\run.bat"

    for process in psutil.process_iter(['cmdline']):
        try:
            cmdline = process.info['cmdline']
            if cmdline and server_command in " ".join(cmdline):
                return "online"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return "offline"

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!'):
        logging.info(f'{message.author} sent command: {message.content}')

    if message.content == '!help':
        msg_to_return = "Comandos disponibles actualmente:\n`"
        for command in avaliableCommands:
            msg_to_return += command + "\n"
        msg_to_return +="`"
        await message.channel.send(msg_to_return)
    if message.content == '!status':
        message_to_return = "Server Status: " + get_server_status() + "\t" + serverStatusList[get_server_status()]
        await message.channel.send(message_to_return)

    if message.content == '!start':
        if get_server_status() == "offline":
            subprocess.Popen([serverCommand],cwd=serverDirectory)
            await message.channel.send("Servidor en marcha")
        else:
            await message.channel.send("El servidor ya está en marcha")

client.run(TOKEN)