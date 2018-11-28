import sys
from flask import Flask, request
import telepot
import os
from telepot.loop import OrderedWebhook

"""
$ python2.7 webhook.py
Webhook path is '/webhook', therefore:
<webhook_url>: https://<base>/webhook
"""
def sendData(msg, bot, data):
    if bot != None:
        content_type, chat_type, chat_id = telepot.glance(msg)
        bot.sendMessage(chat_id, data)

def on_chat_message(msg):
    print("Inside on_chat_message")
    content_type, chat_type, chat_id = telepot.glance(msg)
    sendData(msg, bot, "This is the bot answering")
    print('Chat Message:', content_type, chat_type, chat_id)

def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)

# need `/setinline`
def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    print('Inline Query:', query_id, from_id, query_string)

    # Compose your own answers
    articles = [{'type': 'article',
                    'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]

    bot.answerInlineQuery(query_id, articles)

# need `/setinlinefeedback`
def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)


TOKEN = str(os.environ["telegram_token"])
TELEGRAM_PORT = str(os.environ["PORT"])
URL = str(os.environ["telegram_url"])
print(TELEGRAM_PORT)
app = Flask(__name__)
bot = telepot.Bot(TOKEN)
webhook = OrderedWebhook(bot, {'chat': on_chat_message,
                               'callback_query': on_callback_query,
                               'inline_query': on_inline_query,
                               'chosen_inline_result': on_chosen_inline_result})

@app.route('/webhook', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'

if __name__ == '__main__':
    print("Executing the stuff")
    app.run()
    print("After running app")
    try:
        print("Inside try")
        bot.setWebhook(URL)
        print("After setting webhook")
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
