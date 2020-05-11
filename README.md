1) create a chatbot in teams via:
https://developer.webex.com/docs/bots

2) add the access token into messenger.py

3) place chatbot.py and messenger.py into the same directory on a public server

4) ammend "receiver_url" below to reflect your public URL, available on port 80

5) run with:
    $sudo python3 chatbot.py