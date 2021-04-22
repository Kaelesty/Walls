import argparse
import requests


"""
Скрипт, рассылающий всем собеседникам указанного пользователя указанный текст
"""

ADDRESS = "127.0.0.1:8080"



parser = argparse.ArgumentParser()
parser.add_argument("--login")
parser.add_argument("--password")
parser.add_argument("--text")
args = parser.parse_args()

text = args.text
req = f"http://{ADDRESS}/api/get/{args.login}&{args.password}/dialogues"
print("ASK CONTENT FROM ", req)
dialogues = requests.get(req).json()
print(dialogues)
user_id = dialogues["result"]["user_id"]
errors = 0
for elem in dialogues["result"]["content"]:
    req = requests.get(f"http://{ADDRESS}/api/post/{args.login}&{args.password}/message_l1/{elem['id']}&{text}").json()
    if req["result"]["content"] != ["SUCCESS"]:
        errors += 1
print(f"TRY TO SEND {len(dialogues['result']['content'])} MESSAGES")
print(f"GOT {errors} ERRORS")
