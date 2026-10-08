import keyboard
import requests
import sys
from dotenv import load_dotenv
import os
load_dotenv()
key_path = os.getenv('API_KEY')
db_url = os.getenv('DATABASE_URL')
private = os.getenv('FIREBASE_KEY')
current_subject = "General"
current_line = ""

print(f"Active Subject: {current_subject}. Start typing...")

def send_to_badge(text, subject, is_status=True):
    data = {"text": text, "subject": subject, "isStatus": is_status}
    requests.put(f"{key_path}/badge_live.json", json=data)

def on_key_event(event):
    global current_subject, current_line
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'f1':
            current_subject = "Data_Structures"
            print(f"\n[Switched to {current_subject}]")
            send_to_badge("[Switched]", current_subject)
            return
        elif event.name == 'f2':
            current_subject = "Software_Engineering"
            print(f"\n[Switched to {current_subject}]")
            send_to_badge("[Switched]", current_subject)
            return
            
        if event.name == 'enter': 
            requests.post(f"{key_path}/notes/{current_subject}.json", json={"msg": current_line})
            print(f"\n[Saved to Firebase -> {current_subject}]")
            current_line = ""
            send_to_badge("", current_subject, is_status=False)
        elif event.name == 'space':
            current_line += " "
            send_to_badge(current_line, current_subject) # ONLY updates screen on Space
        elif event.name == 'backspace':
            current_line = current_line[:-1]
            send_to_badge(current_line, current_subject)
        elif len(event.name) == 1: 
            current_line += event.name
            # Removed the send_to_badge line here to stop per-letter blinking!
            
        sys.stdout.write(f"\rTyping: {current_line}          ")
        sys.stdout.flush()

keyboard.hook(on_key_event)
keyboard.wait()