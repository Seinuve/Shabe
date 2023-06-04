import requests
import json

class Shabe:
    def __init__(self):

        with open('C:\\Users\\Tetra\\Desktop\\ShabeSetupUrl.txt', 'r') as file:
            url = file.read()

        with open('C:\\Users\\Tetra\\Desktop\\ShabeSetupToken.txt', 'r') as file:
            token = file.read()

        self.auth = {
            'authorization': token
        }

        self.url = url

    def get_past_five_messages(self):
        messages = requests.get(self.url, headers=self.auth)
        result = json.loads(messages.text)

        messages_to_return = []

        i = 0

        for key in result:
            messages_to_return.append(key['content'])
            i += 1

            if i <= 5:
                break

        return messages_to_return

    def post_message(self):
        msg = {
            'content': 'Bleh2'
        }

        requests.post(self.url, headers=self.auth, data=msg)


client = Shabe()

client.post_message()

print(client.get_past_five_messages())
