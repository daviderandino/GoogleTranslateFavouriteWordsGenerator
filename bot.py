from typing import Final
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
import random
import os

token = os.environ.get('TOKEN')
words = {}

TOKEN: Final = token
BOT_USERNAME : Final = os.environ.get('BOT_USERNAME')
trad_wrapper = list()

# Commands
async def start_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    update_dict()
    await update.message.reply_text('Benvenuto/a! Digita il comando /genera')

async def help_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Benvenuto/a! Il bot genera una parola casuale dalla lista delle tue '+
                                    'parole preferite di google translate. Per caricare le parole avvia il bot con /start, e '
                                    'genera poi una parola con /genera'
                                    )

async def generation_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    if(len(words)==0):
        await update.message.reply_text("Devi prima caricare le parole con /start!")
    print(len(words))
    await update.message.reply_text("Sono presenti " + str(len(words)) + " parole tra le tue parole preferite di google translate!")
    chiavi = list(words.keys())
    r = random.randint(0, len(words))
    await update.message.reply_text("Qual è la traduzione di '" + chiavi[r].capitalize() + "'?")
    traduzione = words[chiavi[r]].lower()
    trad_wrapper.insert(0,traduzione)
    print(chiavi[r] + ':' + traduzione)
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    

def update_dict():
    words.clear()
    file_path = "words.csv"
    with open(file_path, mode='r', newline='') as csv_file:
        riga = csv_file.readline()

        while riga:
            parole = riga.split()
            if(len(parole)==4):
                if parole[0].lower() == 'italiano':
                    words[parole[2]] = parole[3]
                else:
                    words[parole[3]] = parole[2]
            riga = csv_file.readline()


# Responses

def handle_response(text: str) -> str:
    
    processed: str = text.lower()

    if processed == trad_wrapper[0].lower():
        return 'Traduzione corretta!'

    return 'Traduzione errata! \nCorretta: ' + trad_wrapper[0].capitalize()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_text)
        else:
            return     
    else:
        response: str = handle_response(text)

    print('Bot:',response)
    await update.message.reply_text(response)

async def error(update: Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'Update{update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot....')
    app = Application.builder().token(TOKEN).build()

    # Commands

    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('genera',generation_command))

    # Errors

    app.add_error_handler(error)

    # Polling

    print('Polling...')
    app.run_polling(poll_interval=3)
