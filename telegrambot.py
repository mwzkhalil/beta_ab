import telebot
from pydub import AudioSegment
import requests
import os
import json

TOKEN = '6860861824:AAFM0Ox2SJFUYOeT3OtkxnsXhMGMD8a7Y3E'
bot = telebot.TeleBot(TOKEN)

# Replace these with your actual API endpoints
TEXT_API_ENDPOINT = "http://localhost:5000/chat"
AUDIO_API_ENDPOINT = "http://localhost:5000/audio"
REGISTER_API_ENDPOINT = "http://localhost:5000/register"
LOGIN_API_ENDPOINT = "http://localhost:5000/login"
LOGOUT_API_ENDPOINT = "http://localhost:5000/logout"

# Handle text messages
@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    id = message.chat.id
    response = requests.post(TEXT_API_ENDPOINT, json={
        "prompt": message.text,
        'user_id': str(id)
    })
    reply = response.json()
    print(reply)
    reply = reply['message']
    if response.status_code == 200:
        bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, "Sorry, there was an error processing your request.")

# Handle voice messages
@bot.message_handler(content_types=['voice'])
def handle_voice_messages(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        user_id = message.chat.id

        ogg_file_path = 'voice_note.ogg'
        wav_file_path = 'voice_note.wav'

        with open(ogg_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        AudioSegment.from_file(ogg_file_path).export(wav_file_path, format="wav")

        files = {
            'audio_file': (wav_file_path, open(wav_file_path, 'rb'), 'audio/wav'),
        }
        data = {'user_id': json.dumps(user_id)}

        response = requests.post(AUDIO_API_ENDPOINT, files=files, data=data)

        if response.status_code == 200:
            response_audio_path = 'response_audio.wav'
            with open(response_audio_path, 'wb') as out_file:
                out_file.write(response.content)

            with open(response_audio_path, 'rb') as audio_response:
                bot.send_audio(message.chat.id, audio_response)
        else:
            bot.send_message(message.chat.id, "Sorry, there was an error processing your audio.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
    finally:
        cleanup_files()

def cleanup_files():
    if os.path.exists("voice_note.ogg"):
        os.remove("voice_note.ogg")
    if os.path.exists("voice_note.wav"):
        os.remove("voice_note.wav")
    if os.path.exists("response_audio.wav"):
        os.remove("response_audio.wav")

# Handle register command
def handle_register(message):
    try:
        args = message.text.split()
        if len(args) != 4:
            bot.send_message(message.chat.id, "Usage: /register <username> <password> <cnic>")
            return

        username, password, cnic = args[1], hash_password(args[2]), args[3]
        response = requests.post(REGISTER_API_ENDPOINT, data={
            "username": username,
            "password": password,
            "cnic": cnic
        })
        
        if response.status_code == 201:
            bot.send_message(message.chat.id, "Registration successful!")
        else:
            bot.send_message(message.chat.id, f"Registration failed: {response.json().get('error')}")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")


# Handle login command
@bot.message_handler(commands=['login'])
def handle_login(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "Usage: /login <username> <password>")
            return

        username, password = args[1], args[2]
        response = requests.post(LOGIN_API_ENDPOINT, data={
            "username": username,
            "password": password
        })
        
        if response.status_code == 200:
            bot.send_message(message.chat.id, "Login successful!")
        else:
            bot.send_message(message.chat.id, f"Login failed: {response.json().get('error')}")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

# Handle logout command
@bot.message_handler(commands=['logout'])
def handle_logout(message):
    try:
        response = requests.get(LOGOUT_API_ENDPOINT)
        
        if response.status_code == 200:
            bot.send_message(message.chat.id, "Logout successful!")
        else:
            bot.send_message(message.chat.id, "Logout failed.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

# Start polling for messages
bot.polling()
