from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = 'fetopia123'  # Change this to your custom token
PAGE_ACCESS_TOKEN = 'EAAObedByszABO1nehH0zhghA1UKjU4fMCilif2jXTuFwjAZAEZCkllTCsw8z8uDxZCYZCITUekBptEYOLTzrPwvjkG59Y3LfLfesOVk7WGb0qlsIrQAvbpPf2zZCBZBMZAt8nrnHk93AeUU9pGdiOzttaaddWjZAdZBJ8Up8DqcqEflVke2T5QtIiICIvNBZABsAiNAz3pTKx0QXRvz8jQ'  # Your page access token from Facebook

# Function to send messages
def send_message(recipient_id, text):
    url = 'https://graph.facebook.com/v17.0/me/messages'
    params = {'access_token': PAGE_ACCESS_TOKEN}
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': text}
    }
    response = requests.post(url, params=params, json=data)
    print("Sent message:", response.json())

# Webhook verification (Facebook requires this to verify the URL)
@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Invalid verification token'

# Webhook to handle incoming messages
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Iterate through the incoming messages
    for entry in data['entry']:
        for msg in entry['messaging']:
            sender_id = msg['sender']['id']  # Get the sender's ID
            if 'message' in msg and 'text' in msg['message']:
                message_text = msg['message']['text']  # Get the message text
                send_message(sender_id, f"Your message: {message_text}")  # Send a reply

    return 'ok'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
