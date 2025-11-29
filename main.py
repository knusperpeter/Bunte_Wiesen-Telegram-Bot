from typing import Final
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN: Final = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN not set")
BOT_USERNAME: Final = '@Bunte_Wiesen_Bot'

#Commands
async def start_command (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Summ summ! Die fleißige Bot-Biene meldet sich zur Stelle! Wie kann ich dir helfen?")

async def help_command (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bitte schreibe mir was ich für dich tun kann.")

async def custom_command (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Das ist ein Custom-Command!")

#Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    
    if 'wie geht es' in processed:
        return 'Mir geht es sehr gut!'
    
    return 'Mir ist unklar was du damit meinst.'



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            response: str = handle_response(text)

        print('Bot:', response)
        await update.message.reply_text(response)



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')



if __name__ == '__main__':
    print('Der Bot wird gestartet...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    #Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=5)