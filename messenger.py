import json
import requests

# API Key / Chatop Access Token is obtained from the Webex Teams developers website.
# this is a dummy api-Key"
api_key = 'ccccMdA2MdEtsGM0sC00ZsZlLTd2ZDQtZWRkODdijncccfk0YzA545561NDktMDFssdfPF84_10985fdsdf643-417f-fds74-ad098ae0e10f'
# Webex Teams messages API endpoint
base_url = 'https://api.ciscospark.com/v1'

class Messenger():
    def __init__(self, base_url=base_url, api_key=api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.bot_id = requests.get(f'{self.base_url}/people/me', headers=self.headers).json().get('id')
    
    def get_message(self, message_id):
        print("get message")
        """ Retrieve a specific message, specified by message_id """
        received_message_url = f'{self.base_url}/messages/{message_id}'
        self.message_text = requests.get(received_message_url, headers=self.headers).json().get('text')
        self.message_personId = requests.get(received_message_url, headers=self.headers).json().get('personId')
        """ other value available inc message_personId, message_persionEmail,
        message_toPersonId. More details at
        https://developer.webex.com/docs/api/v1/messages/get-message-details
        """

    def post_message(self, room_id, message):
        """ Post message to a Webex Teams space, specified by room_id """
        print(f'room_id = {room_id} message = {message}')
        data = {
            "roomId" : room_id,
            "text" : message,
        }
        print(data)
        post_message_url = f'{self.base_url}/messages'
        post_message = requests.post(post_message_url,headers=self.headers,data = json.dumps(data))
        print(json.dumps(post_message.json(), indent=4))