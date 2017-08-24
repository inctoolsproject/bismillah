import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('MTn2latTZ4NmBnuah67007iRDPdliDVKkpxR1yb5IGpzTARdjzAqSnLmhkvew0EqfNs3wDSQuTc8j/DUfKCoPFpV3ECtur1KUxyiRd1jZjeS9JA7yJXlkuK6l6/WkCJEKDybBDiRMdFbYxtFlRYOmQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('adbb3952c8bc75b90664aa5ededbbbec')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
