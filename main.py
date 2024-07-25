#############    GET CHATS BY USER ID ##################
##def get_chats(id):
##    path = id
##    isexist = os.path.exists(path)
##    if isexist:
##        data = pd.read_json(path)
##        chats = data.chat
##        return  list(chats)
##    else:
##        return "No Chat found on this User ID."
#
#def get_chats(path):
#    if os.path.exists(path):
#        with open(path, 'r') as file:
#            data = json.load(file)
#            chats = data.get("chat", [])
#            return {"chats": chats}
#    else:
#        return {"chats": []}
#
################ APPEND NEW CHAT TO USER ID JSON FILE #################
## Function to write chat with timestamp
##def write_chat(new_data, id):
##    with open(id, 'r+') as file:
##        # First we load existing data into a dict.
##        file_data = json.load(file)
#        # Add timestamp to the new data
##        new_data_with_timestamp = {
##            "role": new_data["role"],
##            "content": new_data["content"],
##            "timestamp": datetime.now().isoformat()
##        }
#        # Join new_data with file_data inside emp_details
##        file_data["chat"].append(new_data_with_timestamp)
#        # Sets file's current position at offset.
##        file.seek(0)
#        # Convert back to json.
##        json.dump(file_data, file, indent=4)
#def write_chat(chat, path):
#    if os.path.exists(path):
#        with open(path, 'r') as file:
#            data = json.load(file)
#        data['chat'].append(chat)
#        with open(path, 'w') as file:
#            json.dump(data, file, indent=4)
#    else:
#        data = {"chat": [chat]}
#        with open(path, 'w') as file:
#            json.dump(data, file, indent=4)
#
#
################################# CHECK IF USER IS ALREADY EXIST IF NOT CREATE ONE ELSE RETURN GPT REPLY ##################
#
## Modify check_user function to include timestamps
##def check_user(ids, prompt):
##    path = str(os.getcwd()) + '//chats//' + ids + '.json'
##    isexist = os.path.exists(path)
##    if isexist:
##        write_chat({"role": "user", "content": prompt}, path)
##        chats = get_chats(path)
##        send = gpt(chats, prompt)
##        reply = send.choices[0].message
##        write_chat({"role": "assistant", "content": reply.content}, path)
##        return {"message": reply.content, "status": "OK"}
##    else:
##        dictionary = {
##            "user_id": ids,
##            "chat": []
##        }
##        json_object = json.dumps(dictionary, indent=4)
##        with open(path, "w") as outfile:
##            outfile.write(json_object)
##        reply = check_user(ids, prompt)
##        return reply
#def check_user(ids, prompt, is_audio=False, audio_path=None):
#    path = os.path.join('chats', f'{ids}.json')
#    isexist = os.path.exists(path)
#    if isexist:
#        if is_audio:
#            chat = {"role": "user", "content": prompt, "audio_path": audio_path}
#        else:
#            chat = {"role": "user", "content": prompt}
#        write_chat(chat, path)
#        chats = get_chats(path)
#        chatss = chats['chats']
#        send = gpt(ids, chatss, prompt)
#        reply = send.choices[0].message
#        write_chat({"role": "assistant", "content": reply.content}, path)
#        return {"message": reply.content, "status": "OK"}
#    else:
#        dictionary = {
#            "user_id": ids,
#            "chat": []
#        }
#        json_object = json.dumps(dictionary, indent=4)
#        with open(path, "w") as outfile:
#            outfile.write(json_object)
#        return check_user(ids, prompt, is_audio, audio_path)
#
#
#
##################################handling chats
#@app.route('/chat', methods=['POST'])
#def chats():
#    ids = request.json['user_id']
#    prompt = request.json['prompt']
#    reply = check_user(ids,prompt)
#    return reply
#
#
#UPLOAD_FOLDER = 'uploads'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
## Ensure the upload folder exists
#if not os.path.exists(UPLOAD_FOLDER):
#    os.makedirs(UPLOAD_FOLDER)
#
#@app.route('/chat', methods=['POST'])
#def chat():
#    ids = request.json['user_id']
#    prompt = request.json['prompt']
#    gpt_reply = check_user(str(ids),prompt)
#    return gpt_reply['message']['content']
#
## Adjust the upload_file function to include timestamp
#@app.route('/audio', methods=['POST'])
#def upload_file():
#    user_id = request.form.get('user_id')
#    if request.method == 'POST':
#        if 'audio_file' not in request.files:
#            return 'No file part'
#        file = request.files['audio_file']
#        name = file.filename
#        if file.filename == '':
#            return 'No selected file'
#        if file:
#            file_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
#            file.save(file_path)
#            text = transcribe(file_path, beam_size=5)
#            gpt_reply = check_user(str(user_id), str(text) + " give very short answer", is_audio=True, audio_path=file_path)
#            waveform = tts(str(gpt_reply['message']))
#            return send_file(waveform, as_attachment=True, download_name='downloaded_audio.wav')
#
#            # return gpt_reply
#
#
#####################   NEW ENPOINT GET CHAT ##############################
#def get_chats(path):
#    if os.path.exists(path):
#        with open(path, 'r') as file:
#            data = json.load(file)
#            chats = data.get("chat", [])
#            return {"chats": chats}
#    else:
#        return {"chats": []}
#
## Endpoint to get chat history
#@app.route('/get_chats', methods=['POST'])
#def get_chatss():
#    ids = request.json['user_id']
#    chats = get_chats(os.path.join('chats', f'{ids}.json'))
#    if not chats['chats']:
#        return jsonify({"message": "No Chat found on this User ID."}), 404
#    else:
#        return jsonify(chats#
from api import apikey
from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import pandas as pd
import json
import requests
from datetime import datetime
import os
import time
from flask import Flask, send_file, after_this_request
from openai import OpenAI
import json
import jsonpickle
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from qna import text 
from faster_whisper import WhisperModel

apikeys = apikey

app = Flask(__name__)

########## Authentication ############
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"

# Initialize SQLAlchemy
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/register', methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    if Users.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409
    user = Users(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    user = Users.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"error": "Invalid username or password"}), 401
    login_user(user)
    return jsonify({"message": "Logged in successfully"}), 200

@app.route("/logout")
@login_required  # Ensure the user is logged in before they can logout
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


############## Openai ################################
global client
client = OpenAI(api_key=apikeys)

embeddings = OpenAIEmbeddings(openai_api_key=apikeys)
db_chroma = Chroma(persist_directory="mydb", embedding_function=embeddings)

################### MODEL LOADING ##############
print('Loading Whisper...')
model_size = "large-v3"
model = WhisperModel(model_size, device="cpu", compute_type="int8")
print('Models Loaded Successfully...')


def transcribe(audio_file_path, beam_size=5):   
    segments, info = model.transcribe(audio_file_path, beam_size=beam_size,language='ur')
    transcribed_text = ""

    for segment in segments:
        transcribed_text += segment.text + " "

    return transcribed_text.strip()

#def tts(text_input):
#    speech_file_path = "speech.wav"
#        # Use OpenAI's API to convert text to speech and stream to file
#    response = client.audio.speech.create(
#        model="tts-1",
#        voice="onyx",
#        input=text_input
#    )
#    response
#    
#    response.stream_to_file(str(speech_file_path))
#    return str(speech_file_path)

def tts(text_input, user_id):
    # Create a unique filename based on the user_id and current timestamp
    timestamp = int(time.time())
    speech_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{user_id}_generated_speech_{timestamp}.wav")

    # Use OpenAI's API to convert text to speech and stream to file
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text_input
    )
    response.stream_to_file(str(speech_file_path))
    return str(speech_file_path)


def retrieve_combined_documents(query, max_combined_docs=4):
    retriever = db_chroma.as_retriever(search_type="mmr")

    rev_doc = retriever.get_relevant_documents(query)
    lim_rev_doc = rev_doc[:max_combined_docs]

    docs = db_chroma.similarity_search(query)
    lim_docs = docs[:max_combined_docs]

    combined_docs = str(lim_rev_doc) + str(lim_docs)
    # combined_docs=db.similarity_search(query)

    return combined_docs


############# Abhi API #####################
def get_latest_transaction_status(cnic):
    url = f"https://api-dev-revamp.abhi.com.pk/dev-transactions/latest/status/{cnic}"
    headers = {
        "X-API-KEY": "usman",
        "X-API-SECRET": "usman",
        "X-API-CLIENT": "chatbot"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        transaction_data = response.json()
        status = transaction_data["data"]["status"]
        return json.dumps({"CNIC": cnic, "status": status})
    else:
        print("Failed to fetch transaction data:", response.text)
        return None

def get_transaction_status_by_id(transaction_id):
    url = f"https://api-dev-revamp.abhi.com.pk/dev--transactions/status-only/{transaction_id}"
    headers = {
        "X-API-KEY": "usman",
        "X-API-SECRET": "usman",
        "X-API-CLIENT": "chatbot"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        transaction_data = response.json()
        status = transaction_data["data"]["status"]
        return json.dumps({"Transaction ID": transaction_id, "status": status})
    else:
        print("Failed to fetch transaction data:", response.text)
        return None

def get_employee_info(cnic):
    url = f"https://api-dev-revamp.abhi.com.pk/dev-employee/info/{cnic}"
    headers = {
        "X-API-KEY": "usman",
        "X-API-SECRET": "usman",
        "X-API-CLIENT": "chatbot"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        employee_data = response.json()
        name = employee_data["data"]["name"]
        salary = employee_data["data"]["salary"]
        status = employee_data["data"]["status"]
        verified = employee_data["data"]["verified"]
        bank_details = employee_data["data"]["bankDetails"]
        return json.dumps({
            "CNIC": cnic,
            "name": name,
            "salary": salary,
            "status": status,
            "verified": verified,
            "bank_details": bank_details
        })
    else:
        print("Failed to fetch employee data:", response.text)
        return None

def get_organization_info(cnic):
    url = f"https://api-dev-revamp.abhi.com.pk/dev-organization/get-organization-info/{cnic}"
    headers = {
        "X-API-KEY": "usman",
        "X-API-SECRET": "usman",
        "X-API-CLIENT": "chatbot"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        organization_data = response.json()
        result = organization_data["data"]["result"]
        return json.dumps({"Organization Info": result})
    else:
        print("Failed to fetch organization data:", response.text)
        return None

def get_available_balance(cnic):
    url = f"https://api-dev-revamp.abhi.com.pk/dev-transactions/available/balance/chatbot/{cnic}"
    headers = {
        "X-API-KEY": "usman",
        "X-API-SECRET": "usman",
        "X-API-CLIENT": "chatbot"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        balance_data = response.json()
        available_balance = balance_data["data"]["availableBalance"]
        per_minute_salary = balance_data["data"]["perMinuteSalary"]
        return json.dumps({
            "CNIC": cnic,
            "available_balance": available_balance,
            "per_minute_salary": per_minute_salary
        })
    else:
        print("Failed to fetch balance data:", response.text)
        return None


############## GPT PROMPT ####################
def gpt(user_id, inp,prompt):
    systems = {"role":"system","content":"""
               You are an Abhi Assistant. 
               You just have to assit Abhi users, use the given data to answer.
               Use the given data to answer the question, if you can't find any relevant information
               just ask for more clarrification or tell the user to contact us through mail: connect@abhi.com.pk,
               phone: +923041115276. Be concise as possible in your answer dont provide lenghty answers.
               The cnic is in {user_id} dont ask question about cnic if the user provide other cnic stop him.

IMPORTANT : You are not allowed to give answers other than abhi only talk about abhi app, Give answers in a language user asked such as
            if user asked in Urdu give reply in Urdu, if user asked in Enlgish give reply in Enlgish and
            if in Roman Urdu give reply in Roman Urdu you support only three languages (Enlgish, Urdu, Roman Urdu).               
               """}
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_latest_transaction_status",
                "description": "Get latest transaction status for a given CNIC",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cnic": {
                            "type": "string",
                            "description": "The CNIC number",
                        },
                    },
                    "required": ["cnic"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_transaction_status_by_id",
                "description": "Get transaction status by transaction ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "transaction_id": {
                            "type": "string",
                            "description": "The transaction ID",
                        },
                    },
                    "required": ["transaction_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_employee_info",
                "description": "Get employee information for a given CNIC",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cnic": {
                            "type": "string",
                            "description": "The CNIC number",
                        },
                    },
                    "required": ["cnic"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_organization_info",
                "description": "Get organization information for a given CNIC",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cnic": {
                            "type": "string",
                            "description": "The CNIC number",
                        },
                    },
                    "required": ["cnic"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_available_balance",
                "description": "Get available balance for a given CNIC",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cnic": {
                            "type": "string",
                            "description": "The CNIC number",
                        },
                    },
                    "required": ["cnic"],
                },
            },
        }
    ]


    rcd = retrieve_combined_documents(prompt)
    print("text  hai ye &&&&&&& : ",rcd)
    systems1 = {"role":"system","content":str(text)}
    new_inp = inp
    new_inp.insert(0,systems)
    new_inp.insert(1,systems1)
    print("inp : \n ",new_inp)
    # openai.api_key = apikeys
    completion = client.chat.completions.create(
    model="gpt-4o", 
    tools=tools,
    tool_choice="auto",
    messages=new_inp
    )
    
    
    response_message = completion.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "get_latest_transaction_status": get_latest_transaction_status,
            "get_transaction_status_by_id": get_transaction_status_by_id,
            "get_employee_info": get_employee_info,
            "get_organization_info": get_organization_info,
            "get_available_balance": get_available_balance,
        }

        new_inp.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_args["cnic"] = user_id

            function_response = function_to_call(**function_args)
            new_inp.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response),
                }
            )

        second_response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=new_inp,
        )

        return second_response

    else:
        return completion


############## Flask Endpoints ################

def get_chats(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            data = json.load(file)
            chats = data.get("chat", [])
            return {"chats": chats}
    else:
        return {"chats": []}

def write_chat(chat, path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            data = json.load(file)
        data['chat'].append(chat)
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        data = {"chat": [chat]}
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)

def check_user(ids, prompt, is_audio=False, audio_path=None):
    path = os.path.join('chats', f'{ids}.json')
    isexist = os.path.exists(path)
    
    if isexist:
        if is_audio:
            chat = {"role": "user", "content": prompt, "audio_path": audio_path}
        else:
            chat = {"role": "user", "content": prompt}
        write_chat(chat, path)
        chats = get_chats(path)
        chatss = chats['chats']
        send = gpt(ids, chatss, prompt)
        reply = send.choices[0].message
        tts_audio_path = tts(reply.content, ids)
        write_chat({"role": "assistant", "content": reply.content, "audio_path": tts_audio_path}, path)
        return {"message": reply.content, "status": "OK"}
    else:
        dictionary = {
            "user_id": ids,
            "chat": []
        }
        json_object = json.dumps(dictionary, indent=4)
        with open(path, "w") as outfile:
            outfile.write(json_object)
        return check_user(ids, prompt, is_audio, audio_path)




@app.route('/chat', methods=['POST'])
def chats():
    ids = request.json['user_id']
    prompt = request.json['prompt']
    reply = check_user(ids, prompt)
    return jsonify(reply)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/chat', methods=['POST'])
def chat():
    ids = request.json['user_id']
    prompt = request.json['prompt']
    gpt_reply = check_user(str(ids),prompt)
    return gpt_reply['message']['content']


# Adjust the upload_file function to include timestamps
#@app.route('/audio', methods=['POST'])
#def upload_file():
#    user_id = request.form.get('user_id')
#    if request.method == 'POST':
#        if 'audio_file' not in request.files:
#            return 'No file part'
#        file = request.files['audio_file']
#        name = file.filename
#        if file.filename == '':
#           return 'No selected file'
#        if file:
#            file_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
#            file.save(file_path)
#            text = transcribe(file_path, beam_size=5)
#            gpt_reply = check_user(str(user_id), str(text) + " give very short answer", is_audio=True, audio_path=file_path)
#            waveform = tts(str(gpt_reply['message']))
#            return send_file(waveform, as_attachment=True, download_name='downloaded_audio.wav')


            # return gpt_reply
@app.route('/audio', methods=['POST'])
def upload_file():
    user_id = request.form.get('user_id')
    if request.method == 'POST':
        if 'audio_file' not in request.files:
            return 'No file part'
        file = request.files['audio_file']
        if file.filename == '':
            return 'No selected file'
        if file:
            # Create a unique filename for the uploaded file
            timestamp = int(time.time())
            uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{user_id}_uploaded_audio_{timestamp}.wav")
            file.save(uploaded_file_path)

            # Transcribe the uploaded audio
            text = transcribe(uploaded_file_path, beam_size=5)

            # Get GPT response
            gpt_reply = check_user(str(user_id), str(text) + " give very short answer", is_audio=True, audio_path=uploaded_file_path)

            # Generate TTS audio file
            generated_file_path = tts(str(gpt_reply['message']), user_id)
            write_chat({"role": "assistant", "content": gpt_reply['message'], "audio_path": generated_file_path}, os.path.join('chats', f'{user_id}.json'))

            return send_file(generated_file_path, as_attachment=True, download_name=f"{user_id}_generated_audio_{timestamp}.wav")

@app.route('/get_audio/<filename>', methods=['GET'])
def get_audio(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found', 404

@app.route('/get_chats', methods=['POST'])
def get_chatss():
    ids = request.json['user_id']
    chats = get_chats(os.path.join('chats', f'{ids}.json'))
    if not chats['chats']:
        return jsonify({"message": "No Chat found on this User ID."}), 404
    else:
        return jsonify(chats)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

