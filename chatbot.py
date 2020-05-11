""" 
1) create a chatbot in teams via:
https://developer.webex.com/docs/bots

2) add the access token into messenger.py

3) place chatbot.py and messenger.py into the same directory on a public server

4) ammend "receiver_url" below to reflect your public URL, available on port 80

5) run with:
    $sudo python3 chatbot.py

"""
from flask import Flask, request, json
import requests
from messenger import Messenger

app = Flask(__name__)
port = 80
msg = Messenger()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Receive a notification from Webex Teams and handle it"""
    if request.method == 'GET':
        return f'Request received on local port {port}'
    elif request.method == 'POST':
        if 'application/json' in request.headers.get('Content-Type'):
            # Notification payload, received from Webex Teams webhook
            data = request.get_json()
            # Loop prevention, ignore messages which were posted by bot itself.
            # The bot_id attribute is collected from the Webex Teams API
            # at object instatiation.
            if msg.bot_id == data.get('data').get('personId'):
                return 'Message from self ignored'
            else:
                # Print the notification payload, received from the webhook
                print(json.dumps(data,indent=4))
                # Collect the roomId from the notification,
                # so you know where to post the response
                # Set the msg object attribute.
                msg.room_id = data.get('data').get('roomId')
                # Collect the message id from the notification, 
                # so you can fetch the message content
                message_id = data.get('data').get('id')
                # Get the contents of the received message. 
                msg.get_message(message_id)
                # If message starts with '/server', relay it to the web server.
                # If not, just post a confirmation that a message was received.
                msg.reply= f'Bot recieved message "{msg.message_text}"'
                msg.post_message(msg.room_id, msg.reply)
                return data
        else: 
            return ('Wrong data format', 400)
if __name__ == '__main__':

    def get_webhook_urls():
        webhook_urls = []
        webhooks_api = f'{msg.base_url}/webhooks'
        webhooks = requests.get(webhooks_api, headers=msg.headers)
        if webhooks.status_code != 200:
            webhooks.raise_for_status()
        else:
            for webhook in webhooks.json()['items']:
                webhook_urls.append(webhook['targetUrl'])
                print(webhook_urls)
        print("End of get_webhook_URLs \n")
        print(webhook_urls)
        return webhook_urls

    def create_webhook(url):
        print("entering create_webhook")
        webhooks_api = f'{msg.base_url}/webhooks'
        data = { 
            "name": "Webhook to ChatBot",
            "resource": "all",
            "event": "all",
            "targetUrl": f"{url}"
        }
        webhook = requests.post(webhooks_api, headers=msg.headers, data=json.dumps(data))
        if webhook.status_code != 200:
            webhook.raise_for_status()
        else:
            print(f'Webhook to {url} created')

    #this is the URL of the server the script is running on:
    receiver_url = "http://ec2-54-171-108-150.eu-west-1.compute.amazonaws.com"
    webhook_urls = get_webhook_urls()
    print(webhook_urls)
    
    if receiver_url in webhook_urls:
        print(f'Registered webhook {receiver_url}')
    else:
        create_webhook(receiver_url)

    app.run(host="0.0.0.0", port=port, debug=True)

                               