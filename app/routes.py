from flask import request, Response
from app import app, db, telegram_bot
from app.show import exchange_rate_text, graph_chart
from app.models import TelegramUser
from app import messages
from datetime import datetime, timedelta
from telebot import types
import requests
import re


# getting messages via webhook
@app.route('/' + app.config['BOT_TOKEN'], methods=['POST'])
def get_message():
    telegram_bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return Response("Ok", 200)


# setting webhook
@app.route("/")
def webhook():
    telegram_bot.remove_webhook()
    telegram_bot.set_webhook(url=app.config['APP_URL'] + app.config['BOT_TOKEN'])
    return Response("Webhook has been set", 200)


@telegram_bot.message_handler(commands=['start'])
def auth_telegram_user(message):
    user = TelegramUser.query.filter_by(id=message.from_user.id).first()
    if not user:
        user = TelegramUser(id=message.from_user.id)
        db.session.add(user)
        db.session.commit()
    telegram_bot.send_message(chat_id=message.chat.id, text=messages.start_command)


@telegram_bot.message_handler(commands=['list', 'lst'])
def get_available_rates(message):
    try:
        user = TelegramUser.query.filter_by(id=message.from_user.id).first()
        rates = user.exchange_rates()
        if rates:
            telegram_bot.send_message(chat_id=message.chat.id, text=exchange_rate_text(rates))
        else:
            raise Exception()
    except Exception as e:
        telegram_bot.send_message(message.chat.id, text=str(e))


@telegram_bot.message_handler(regexp=r'/exchange[ ]{1,}(\d*[.,]?\d*[ ]{1,}[A-Z]{3}|\$\d*[.,]?\d*)[ ]{1,}to[ ]{1,}([A-Z]{3})')
def handle_usd_exchange(message):
    try:
        user = TelegramUser.query.filter_by(id=message.from_user.id).first()
        curr_search = re.search(r'[ ]{1,}(\d*[.,]?\d*[ ]{1,}[A-Z]{3}|\$\d*[.,]?\d*)[ ]{1,}to[ ]{1,}([A-Z]{3})', message.text)
        if not curr_search:
            raise Exception()

        value = float(re.findall(r'\d*[.,]?\d+', curr_search.group(1))[0].replace(',', '.'))
        if '$' in curr_search.group(1):
            base = 'USD'
        else:
            base = re.findall(r'([A-Z]{3})', curr_search.group(1))[0]

        curr = curr_search.group(2)

        response = requests.get(url="https://api.exchangeratesapi.io/latest", params={'base': base, 'symbols': curr})
        if response:
            result = response.json().get('rates').get(curr)*value
            telegram_bot.send_message(chat_id=message.chat.id, text='{:.2f} {}'.format(result, curr))
        else:
            raise Exception()
    except Exception as e:
        send_exchange_command_info(message)


@telegram_bot.message_handler(commands=['exchange'])
def send_exchange_command_info(message):
    text = messages.exchange_command
    telegram_bot.send_message(message.chat.id,  text=text)


@telegram_bot.message_handler(regexp=r'\/history[ ]{1,}([A-Z]{3})\/([A-Z]{3})[ ]{1,}for[ ]{1,}([1-9]\d*)[ ]{1,}days')
def send_graph_chart(message):
    try:
        curr_search = re.search(r'\/history[ ]{1,}([A-Z]{3})\/([A-Z]{3})[ ]{1,}for[ ]{1,}([1-9]\d*)[ ]{1,}days',
                                message.text)
        if not curr_search:
            raise Exception('Something went wrong')

        base = curr_search.group(1)
        curr = curr_search.group(2)
        days = int(curr_search.group(3))
        if days > 90:
            raise Exception('You are able to see result for the past 3 months')
        end_at = datetime.utcnow()
        start_at = end_at - timedelta(days=days)

        response = requests.get(url='https://api.exchangeratesapi.io/history',
                                params={'start_at': start_at.strftime('%Y-%m-%d'),
                                        'end_at':  end_at.strftime('%Y-%m-%d'),
                                        'base': base,
                                        'symbols': curr})
        if not response:
            raise Exception('Please, enter correct data')
        rates = response.json().get('rates')
        if len(rates) == 0:
            raise Exception('No exchange rate data is available for the selected currency')

        telegram_bot.send_photo(message.chat.id, graph_chart(rates, base=base, curr=curr))
    except Exception as e:
        telegram_bot.send_message(chat_id=message.chat.id, text=str(e))


@telegram_bot.message_handler(commands=['history'])
def send_exchange_command_info(message):
    text = messages.history_command
    telegram_bot.send_message(message.chat.id,  text=text)


@telegram_bot.message_handler(commands=['help'])
def send_exchange_command_info(message):
    text = messages.help_commnad
    telegram_bot.send_message(message.chat.id,  text=text)


