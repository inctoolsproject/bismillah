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

line_bot_api = LineBotApi('cXqMLYM/XPK2nRFQgHw2UnT3KJGWUSHbA17EdnirXd4u7m4pM+tOZBgfn4AjLQftVOMvdm7R03S/BJ6vvsQRWgXfoJSdMyEn5X2Ba0Kw9FLE32Wy8PHwi620IEelX74uMVNE8K8RVpYwOEB+ivBqDQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('U8cc4e9dc84f73fa3e063b8162e6c09b7')


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
