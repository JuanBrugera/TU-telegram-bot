from telegram_bot.scrapers import ProductScraper
from telegram_bot.regexs import *
from telegram_bot import *
from telegram_bot import formatters as fm

import logging
import random

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, UTM_CAMPAIGN = range(2)

YES, NO = "SI", "NO"


def start(update: Update, context: CallbackContext) -> None:
    # TODO start text
    update.message.reply_text('Hi!')
    return ConversationHandler.END


def help(update: Update, context: CallbackContext) -> None:
    # TODO help text
    update.message.reply_text('Help!')
    return ConversationHandler.END


def url(update: Update, context: CallbackContext) -> int:
    product_url = TU_PRODUCT_REGEX.search(update.message.text).group(0)
    context.user_data.update({'product_url': product_url})
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton(text=YES, callback_data=YES),
        InlineKeyboardButton(text=NO, callback_data=NO),
    ]])
    update.message.reply_text("¿Deseas añadir un ID de campaña?", reply_markup=reply_markup)
    return CHOOSING


def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    answer = query.data
    logger.info(answer)
    query.message.edit_reply_markup(reply_markup=None)
    if answer == NO:
        return send(context)
    else:
        query.from_user.send_message("Introduce el ID de camapaña")
        return UTM_CAMPAIGN


def campaign(update: Update, context: CallbackContext):
    campaign_id = update.message.text.strip()
    if campaign_id:
        context.user_data.update({'campaign_id': campaign_id})
        return send(context)


def send(context: CallbackContext):
    product_url = context.user_data.get('product_url')

    logger.info(product_url)
    campaign_id = context.user_data.get('campaign_id', None)

    logger.info(campaign_id)
    t_params = dict([tp.split("=") for tp in TRACKING_PARAMS.split("&")])
    t_params.update({'utm_campaign': campaign_id})

    logger.info(t_params)
    details = ProductScraper(product_url, tracking_params=t_params).details
    context.bot.send_message(chat_id=CHANNEL,
                             text=fm.telegram_message(details),
                             parse_mode=ParseMode.MARKDOWN_V2,
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton(text=random.choice(BUTTONS), url=details.url_to_sent)]
                             ])
                             )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Conversación cancelada")
    return ConversationHandler.END


def error(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(start.__name__, start),
                      CommandHandler(help.__name__, help),
                      MessageHandler(Filters.regex(TU_PRODUCT_REGEX.pattern), url)
                      ],
        states={
            CHOOSING: [
                CallbackQueryHandler(button)
            ],
            UTM_CAMPAIGN: [
                MessageHandler(Filters.text, campaign)
            ]
        },
        conversation_timeout=120,
        fallbacks=[CommandHandler(cancel.__name__, cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
