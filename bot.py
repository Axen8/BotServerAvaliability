# bot.py
import os
import discord
import platform
from dotenv import load_dotenv
import psutil
import subprocess
import logging
import bcrypt
logging.basicConfig(filename='bot_commands.log', level=logging.INFO, format='%(asctime)s - %(message)s')
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
serverDirectory = os.getenv('SERVER_DIRECTORY')
serverCommand = serverDirectory + os.getenv('SERVER_RUN')
system_platform = platform.system()

serverStatusList = {
    "online": "🟢",
    "offline": "🔴"
}
avaliableCommands = [
    "!help Comando para ver todos los comandos disponibles y sus funciones",
    "!status: Comando para consultar el estado del servidor de minecraft",
    "!start: Comando para iniciar el servidor (solo se ejecuta el servidor si no está en marcha)",
    "!stop password: Comando para cerrar el servidor (Necesita contraseña)"
]

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_passwd(passwd):
    if not isinstance(passwd, str): return False
    listinput = passwd.split()
    if len(listinput) != 2:
        return False
    else:
        return bcrypt.checkpw(listinput[1].encode('utf-8'), hash_password(os.getenv('CLOSING_PASSWD')))

def get_server_status():
    # Replace 'your_server_command' with the actual command to start your Minecraft server
    server_command = "minecraftforge/forge"
    for process in psutil.process_iter(['cmdline']):
        try:
            cmdline = process.info['cmdline']
            if cmdline and server_command in " ".join(cmdline):
                return "online"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return "offline"

def stop_minecraft_server_windows():
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'java.exe', '/T'], check=True)
        print("Minecraft server stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Unable to stop the Minecraft server.")

def stop_minecraft_server_unix():
    try:
        subprocess.run(['pkill', '-f', 'java'], check=True)
        print("Minecraft server stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Unable to stop the Minecraft server.")

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
    if message.content.startswith('!close '):
        if verify_passwd(message.content): 
            if system_platform == "Windows":
                stop_minecraft_server_windows()
            elif system_platform in ["Linux", "Darwin"]:  # "Darwin" is macOS
                stop_minecraft_server_unix()
            else:
                print(f"Unsupported operating system: {system_platform}")
            await message.channel.send("El servidor se esta cerrando")
        else:
            await message.channel.send("Contraseña incorrecta para esta acción")
client.run(TOKEN)