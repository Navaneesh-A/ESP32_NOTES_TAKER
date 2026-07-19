import keyboard
import firebase_admin
from firebase_admin import credentials, db
import time
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
key_path = os.getenv('API_KEY')
db_url = os.getenv('DATABASE_URL')
private = os.getenv('FIREBASE_KEY')
# --- CONFIGURATION ---
# Replace with the path to your Firebase Admin private key JSON file
cred = credentials.Certificate(private)
firebase_admin.initialize_app(cred, {
    'databaseURL': db_url
})

SUBJECTS = {'f1': 'DSA', 'f2': 'Skillrack', 'f3': 'Aptitude', 'f4': 'Project', 'f6': 'General'}

state = {
    "mode": "LIVE",         # 'LIVE' or 'RETRIEVAL'
    "subject": "DSA",
    "text": "",
    "retrieved_notes": [],  # List of notes for current subject
    "note_idx": 0,          # Left/Right pagination
    "scroll_idx": 0  ,       # Up/Down scrolling
    "is_blank": False # <-- ADD THIS
}

def update_badge(subject, text):
    """Pushes the current view to the ESP32 OLED"""
    db.reference('/badge_live').set({
        'subject': subject,
        'text': text
    })

def save_note():
    """Saves the note to Firebase and calculates today's count"""
    if not state["text"].strip(): return
    
    timestamp = str(int(time.time()))
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Save to database
    ref = db.reference(f'/notes/{state["subject"]}/{timestamp}')
    ref.set({'text': state["text"], 'date': date_str})
    
    # Count today's notes for this subject
    all_notes = db.reference(f'/notes/{state["subject"]}').get() or {}
    today_count = sum(1 for n in all_notes.values() if n.get('date') == date_str)
    
    print(f"\n[SAVED] {state['subject']} | Total Today: {today_count}")
    
    state["text"] = "" # Clear screen after saving
    update_badge(f"{state['subject']} (Saved!)", "")
    time.sleep(1)
    update_badge(state["subject"], state["text"])

def load_retrieval_notes():
    """Fetches notes for the current subject for F5 mode"""
    data = db.reference(f'/notes/{state["subject"]}').get() or {}
    state["retrieved_notes"] = [v['text'] for k, v in data.items()]
    state["note_idx"] = len(state["retrieved_notes"]) - 1 # Start at latest
    state["scroll_idx"] = 0
    show_retrieved_note()

def show_retrieved_note():
    if not state["retrieved_notes"]:
        update_badge(f"R: {state['subject']}", "No notes found.")
        return
        
    full_text = state["retrieved_notes"][state["note_idx"]]
    
    # Simple scroll math (send specific chunks of text)
    lines = full_text.split('\n')
    visible_lines = '\n'.join(lines[state["scroll_idx"] : state["scroll_idx"] + 5])
    
    update_badge(f"R: {state['subject']} [{state['note_idx']+1}/{len(state['retrieved_notes'])}]", visible_lines)

def on_key(event):
    # Blank Screen Toggle
    

    # Ignore all other typing if screen is currently haha 
    if event.event_type != 'down': return
    
    key = event.name
    if key == 'esc':
        state["is_blank"] = not state["is_blank"]
        if state["is_blank"]:
            update_badge("BLANK", "")
        else:
            # Restore previous state
            if state["mode"] == "LIVE":
                update_badge(state["subject"], state["text"])
            else:
                show_retrieved_note()
        return

    # Mode Switching
    if key == 'f5':
        state["mode"] = "RETRIEVAL"
        print("\n--- RETRIEVAL MODE ---")
        load_retrieval_notes()
        return

    # Subject Selection
    if key in SUBJECTS:
        state["subject"] = SUBJECTS[key]
        if state["mode"] == "LIVE":
            update_badge(state["subject"], state["text"])
        else:
            load_retrieval_notes()
        print(f"\nSubject changed to: {state['subject']}")
        return
    if state["is_blank"]:
        if key in SUBJECTS or key == 'f5':
            state["is_blank"] = False  # Wake up
        else:
            return
    # --- RETRIEVAL MODE CONTROLS ---
    if state["mode"] == "RETRIEVAL":
        if key == 'left' and state["note_idx"] > 0:
            state["note_idx"] -= 1
            state["scroll_idx"] = 0
            show_retrieved_note()
        elif key == 'right' and state["note_idx"] < len(state["retrieved_notes"]) - 1:
            state["note_idx"] += 1
            state["scroll_idx"] = 0
            show_retrieved_note()
        elif key == 'down':
            state["scroll_idx"] += 1
            show_retrieved_note()
        elif key == 'up' and state["scroll_idx"] > 0:
            state["scroll_idx"] -= 1
            show_retrieved_note()
        # Press any normal key to exit retrieval mode
        elif len(key) == 1 and key.isalpha():
            state["mode"] = "LIVE"
            update_badge(state["subject"], state["text"])

    # --- LIVE MODE CONTROLS ---
    elif state["mode"] == "LIVE":
        if key == '\\':
            save_note()
        elif key == 'enter':
            state["text"] += "\n- "
            update_badge(state["subject"], state["text"])
        elif key == 'space':
            state["text"] += " "
            update_badge(state["subject"], state["text"])
        elif key == 'backspace':
            state["text"] = state["text"][:-1]
            update_badge(state["subject"], state["text"])
        elif len(key) == 1:
            state["text"] += key
            # We don't update badge on every single character to prevent lag. 
            # It updates on Space, Enter, Backspace, or F-keys.

keyboard.hook(on_key)
print("Listening... Press F1-F4 to change subjects. F5 for Retrieval. F6 for General. '\\' to save.")
keyboard.wait('f12') # Press F12 to close the script