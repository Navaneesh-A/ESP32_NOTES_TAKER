from flask import Flask, render_template_string, request, redirect
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import time
from dotenv import load_dotenv
import os
load_dotenv()
key_path = os.getenv('API_KEY')
db_url = os.getenv('DATABASE_URL')
private = os.getenv('FIREBASE_KEY')
# Initialize Firebase (Only if not already initialized)
if not firebase_admin._apps:
    cred = credentials.Certificate(private) # UPDATE THIS PATH
    firebase_admin.initialize_app(cred, {
        'databaseURL': db_url
    })

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>My Notes Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; padding: 30px; max-width: 900px; margin: auto; }
        h1 { color: #ffffff; text-align: center; }
        
        /* Category Form */
        .add-form { text-align: center; margin-bottom: 30px; }
        input[type="text"] { padding: 10px; border-radius: 5px; border: none; outline: none; background: #2a2a2a; color: white; width: 200px; }
        button { padding: 10px 15px; border-radius: 5px; border: none; background: #00a8ff; color: white; cursor: pointer; font-weight: bold; }
        button:hover { background: #0097e6; }

        /* Subject Cards */
        .subject-card { background: #1e1e1e; padding: 20px; margin-bottom: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h2 { margin-top: 0; color: #00a8ff; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .notification { background: #ff4757; color: white; padding: 4px 10px; border-radius: 12px; font-size: 12px; float: right; margin-top: 5px; }
        
        /* Hover & Scroll Logic */
        .notes-container { 
            max-height: 90px; /* Shows only top notes initially */
            overflow: hidden; 
            transition: max-height 0.4s ease-in-out; 
            padding-right: 5px;
        }
        .notes-container:hover { 
            max-height: 300px; /* Expands on hover */
            overflow-y: auto;  /* Enables scrolling */
        }
        
        /* Custom Scrollbar */
        .notes-container::-webkit-scrollbar { width: 6px; }
        .notes-container::-webkit-scrollbar-thumb { background: #444; border-radius: 4px; }

        /* Notes & Click-to-Complete */
        .note { border-left: 4px solid #444; background: #252525; padding: 12px; margin: 10px 0; border-radius: 0 5px 5px 0; cursor: pointer; transition: 0.2s; white-space: pre-wrap; }
        .note:hover { background: #2a2a2a; border-left-color: #00a8ff; }
        .date { font-size: 11px; color: #888; margin-bottom: 5px; }
        
        /* Completed State */
        .completed { background: #1b4332 !important; border-left-color: #2ecc71 !important; color: #95d5b2; text-decoration: line-through; }
    </style>
</head>
<body>
    <h1>Study Dashboard</h1>
    
    <div class="add-form">
        <form method="POST" action="/add_category">
            <input type="text" name="new_cat" placeholder="New Category Name" required>
            <button type="submit">+ Add Category</button>
        </form>
    </div>
    
    {% for subject, notes in data.items() %}
        <div class="subject-card">
            <h2>{{ subject }} 
                <span class="notification">{{ counts[subject] }} Added Today</span>
            </h2>
            
            <div class="notes-container">
                {% for timestamp, note in notes.items()|reverse %}
                    <!-- onclick toggles the 'completed' CSS class -->
                    <div class="note" onclick="this.classList.toggle('completed')">
                        <div class="date">{{ note.date }}</div>
                        <div>{{ note.text }}</div>
                    </div>
                {% endfor %}
            </div>
        </div>
    {% endfor %}
    
</body>
</html>
"""

@app.route('/')
def dashboard():
    all_notes = db.reference('/notes').get() or {}
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_counts = {}

    for subject, notes in all_notes.items():
        count = sum(1 for n in notes.values() if n.get('date') == today_str)
        today_counts[subject] = count

    return render_template_string(HTML_PAGE, data=all_notes, counts=today_counts)

@app.route('/add_category', methods=['POST'])
def add_category():
    new_category = request.form.get('new_cat')
    if new_category:
        # Create a dummy initialization note to force Firebase to create the category
        timestamp = str(int(time.time()))
        date_str = datetime.now().strftime("%Y-%m-%d")
        ref = db.reference(f'/notes/{new_category.strip()}/{timestamp}')
        ref.set({'text': 'Category initialized.', 'date': date_str})
        
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6060, debug=True)