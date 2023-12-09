**BOT PARA OBTENER INFORMACIÓN DEL SERVIDOR DE MINECRAFT, PARA DISCORD**
how to setup:

- Create a .env file with the following information:
```bash
DISCORD_TOKEN="Paste your discord bot token here"
SERVER_DIRECTORY="Paste the directory path to the location where the server is stored here."
SERVER_RUN="Provide the run file with the appropriate extension. If you're using a Windows OS, paste the .bat file; if you're on Linux, paste the .sh file here."
```
- Execute the following command to install the dependencies (it is advisable to do this within a virtual environment):

`pip install -r requirements.txt`

- Run `python bot.py` on Windows or `python3 bot.py` on Linux to ensure the proper functioning of the bot.

- The bot should be working now!
