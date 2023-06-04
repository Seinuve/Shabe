## built-in modules
import requests
import json
import os
import base64
import time

## third-party modules
import openai

from openai.error import APIConnectionError, APIError, AuthenticationError, ServiceUnavailableError, RateLimitError, Timeout


##-------------------start-of-Shabe---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Shabe:

    """
    
    Used for self-botting purposes

    """

##-------------------start-of-__init__()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):

        with open('C:\\Users\\Tetra\\Desktop\\ShabeSetupUrl.txt', 'r') as file:
            url = file.read()

        with open('C:\\Users\\Tetra\\Desktop\\ShabeSetupToken.txt', 'r') as file:
            token = file.read()

        self.auth = {
            'authorization': token
        }

        self.url = url

        if(os.name == 'nt'):  ## Windows
            self.config_dir = os.path.join(os.environ['USERPROFILE'],"ShabeConfig")
        else:  ## Linux
            self.config_dir = os.path.join(os.path.expanduser("~"), "ShabeConfig")


##-------------------start-of-get_pass_twenty_messages()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_past_five_messages(self):
        messages = requests.get(self.url, headers=self.auth)
        result = json.loads(messages.text)

        messages_to_return_content = []
        messages_to_return_user = []

        for i, key in enumerate(result):
            messages_to_return_content.append(key['content'])
            messages_to_return_user.append(key['author']['username'])

            if i >= 4:  # Check if 5 messages have been collected
                break

        return messages_to_return_content, messages_to_return_user

    
##-------------------start-of-post_message()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def post_message(self, message):
        msg = {
            'content': message
        }

        requests.post(self.url, headers=self.auth, data=msg)

##-------------------start-of-initialize_text()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def initialize(self) -> None:

        """

        Sets the open api key.\n
        
        Parameters:\n
        self (object - Shabe) : the Shabe object.\n

        Returns:\n
        None\n

        """

        try:
            with open(os.path.join(self.config_dir,'GPTApiKey.txt'), 'r', encoding='utf-8') as file:  ## get saved api key if exists
                api_key = base64.b64decode((file.read()).encode('utf-8')).decode('utf-8')

            openai.api_key = api_key
        
            print("Used saved api key in " + os.path.join(self.config_dir,'GPTApiKey.txt')) ## if valid save the api key
            time.sleep(.7)

        except (FileNotFoundError,AuthenticationError): ## else try to get api key manually
                
            if(os.path.isfile("C:\\ProgramData\\Kudasai\\GPTApiKey.txt") == True): ## if the api key is in the old location, delete it
                os.remove("C:\\ProgramData\\Kudasai\\GPTApiKey.txt")
                print("r'C:\\ProgramData\\Kudasai\\GPTApiKey.txt' was deleted due to Kudasai switching to user storage\n")
                
            api_key = input("DO NOT DELETE YOUR COPY OF THE API KEY\n\nPlease enter the openapi key you have : ")

            try: ## if valid save the api key

                openai.api_key = api_key

                if(os.path.isdir(self.config_dir) == False):
                    os.mkdir(self.config_dir, 0o666)
                    print(self.config_dir + " created due to lack of the folder")

                    time.sleep(.1)
                            
                if(os.path.isfile(os.path.join(self.config_dir,'GPTApiKey.txt')) == False):
                    print(os.path.join(self.config_dir,'GPTApiKey.txt') + " was created due to lack of the file")

                    with open(os.path.join(self.config_dir,'GPTApiKey.txt'), 'w+', encoding='utf-8') as key: 
                        key.write(base64.b64encode(api_key.encode('utf-8')).decode('utf-8'))

                    time.sleep(.1)
                
            except AuthenticationError: ## if invalid key exit
                    
                os.system('cls')
                        
                print("Authorization error with creating openai, please double check your api key as it appears to be incorrect.\n")
                os.system('pause')
                        
                exit()

            except Exception as e: ## other error, alert user and raise it

                os.system('cls')
                        
                print("Unknown error with connecting to openai, The error is as follows " + str(e)  + "\nThe exception will now be raised.\n")
                os.system('pause')

                raise e
                    
##-------------------start-of-main()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


client = Shabe()

messages, usernames = client.get_past_twenty_messages()

client.post_message("I'm just really bored")

for user, message in zip(usernames, messages):
    print(user + ": " + message + "\n")
