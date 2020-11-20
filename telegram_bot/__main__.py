import json
import logging
import random
import warnings

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

from telegram_bot import *
from telegram_bot import formatters as fm
from telegram_bot.regexs import *
from telegram_bot.scrapers import ProductScraper

warnings.filterwarnings("ignore")

# Enable logging
logging.basicConfig(
    filename='telegram_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOG_LEVEL
)

logger = logging.getLogger(__name__)

CHOOSING, UTM_CAMPAIGN = range(2)

YES, NO = "SI", "NO"


def start(update: Update, context: CallbackContext) -> None:
    logger.debug("start")

    update.message.reply_text("Envíame un enlace de producto de TU.com para empezar el proceso")
    return ConversationHandler.END


def help(update: Update, context: CallbackContext) -> None:
    logger.debug("help")

    message = f"/{start.__name__} - Te muestro el mensaje de bienvenida\n"
    message += f"/{help.__name__} - Te muestro este mensaje\n"
    message += f"/{cancel.__name__} - Aborta la conversación en curso\n"
    message += "\nTambién puedes mandarme un enlace de producto de TU.COM"

    update.message.reply_text(message)
    return ConversationHandler.END


def url(update: Update, context: CallbackContext) -> int:
    logger.debug("url")

    if update.message.chat_id not in VALID_IDS:
        return ConversationHandler.END

    product_url = TU_PRODUCT_REGEX.search(update.message.text).group(0)
    logger.info(f"URL Received: {product_url}")

    context.user_data.update({'product_url': product_url})
    update.message.reply_text("Dime el ID de campaña")
    return UTM_CAMPAIGN


def button(update: Update, context: CallbackContext) -> int:
    logger.debug("button")

    query = update.callback_query
    query.answer()
    answer = query.data
    query.message.edit_reply_markup(reply_markup=None)
    logger.debug(answer)

    chat_id = context.user_data.pop('chat_id')
    message_ids = context.user_data.pop('message_ids')

    if answer == YES:
        send(context)
    else:
        context.user_data.pop('details')

    for mid in message_ids:
        context.bot.delete_message(chat_id=chat_id, message_id=mid)

    context.bot.send_message(chat_id=chat_id,
                             text="Hecho!")

    return ConversationHandler.END


def campaign(update: Update, context: CallbackContext):
    logger.debug("campaign")

    campaign_id = update.message.text.strip()
    logger.info(f"CAMPAIGN ID: {campaign_id}")

    product_url = context.user_data.pop('product_url')
    logger.info(f"PRODUCT URL: {product_url}")

    chat_id = update.message.chat_id
    logger.debug(f"CHAT ID: {chat_id}")

    t_params = dict([tp.split("=") for tp in TRACKING_PARAMS.split("&")])
    t_params.update({'utm_campaign': campaign_id})
    logger.debug(f"TRACKING PARAMS: {json.dumps(t_params)}")

    details = ProductScraper(product_url, tracking_params=t_params).details
    if details:
        logger.debug(str(details))
        id1 = update.message.reply_text(text=fm.telegram_message(details),
                                        parse_mode=ParseMode.MARKDOWN_V2,
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(text=random.choice(
                                                OFFER_BUTTONS if details.before_price else NORMAL_BUTTONS),
                                                url=details.url_to_sent)]
                                        ]),
                                        timeout=10
                                        ).message_id
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(text=YES, callback_data=YES),
            InlineKeyboardButton(text=NO, callback_data=NO),
        ]])
        id2 = update.message.reply_text("Este es el mensaje que voy a enviar, OK?",
                                        reply_markup=reply_markup).message_id
        context.user_data.update({'details': details,
                                  'chat_id': chat_id,
                                  'message_ids': [id1, id2]})

    return CHOOSING


def send(context: CallbackContext):
    logger.debug("send")

    details = context.user_data.get('details', None)
    if details:
        logger.info(f"Sending message to {CHANNEL}")
        context.bot.send_message(chat_id=CHANNEL,
                                 text=fm.telegram_message(details),
                                 parse_mode=ParseMode.MARKDOWN_V2,
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton(
                                         text=random.choice(OFFER_BUTTONS if details.before_price else NORMAL_BUTTONS),
                                         url=details.url_to_sent)]
                                 ]),
                                 timeout=10
                                 )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> None:
    logger.debug("cancel")
    update.message.reply_text("Conversación cancelada")
    context.user_data = {}
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
                      CommandHandler(cancel.__name__, cancel),
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
        conversation_timeout=TIMEOUT,
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
