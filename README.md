# Note Tracker Class

A small Python project that helps me type quick study notes using a keyboard and display them on an OLED-style badge while also saving them in Firebase. The core idea was simple: make note-taking fast, visible, and organized by subject without needing a full app or a complicated interface.

This project is a practical learning experiment built by a curious 3rd-year student who wanted to combine coding, hardware thinking, and study productivity into one system.

## Why this project exists

As a student, I noticed that important ideas, revision points, and reminders were getting lost across notebooks, phones, and random text files. I wanted a system where I could:

- quickly type a note
- assign it to a subject
- save it instantly
- review it later
- see the current note on a display

The idea was not to build a polished product from day one, but to create something useful, lightweight, and fun to learn from.

## What it does

This project provides a small workflow for note tracking:

- subject-based note categories such as DSA, Skillrack, Aptitude, Project, and General
- keyboard-triggered input capture with Python
- live note display on an OLED-like badge
- retrieval mode to browse older notes
- Firebase-backed storage for saving and reading notes
- a simple web dashboard to view saved notes by category

## Project structure

```text
note_tracker_class/
├── app.py
├── app_start.py
├── main.py
├── .gitignore
├── README.md
└── .env (your local configuration file)
```

### Files overview

- `main.py`  
  Main application logic. Handles keyboard input, subject switching, saving notes, and updating the display.

- `app.py`  
  Flask dashboard that reads the notes from Firebase and displays them in a simple study dashboard.

- `app_start.py`  
  Earlier prototype version for a lightweight badge-style note sender using requests.

## Tech stack

- Python
- `keyboard` library for key detection
- Firebase Realtime Database
- Firebase Admin SDK
- Flask for the dashboard UI
- `python-dotenv` for environment variables

## How it works

The program listens for keyboard events using Python. When the user changes the active subject, the app updates the current context. In live mode, typed text is collected and kept in memory. Once the save action is triggered, the current note is written to Firebase under the selected subject.

The app also includes a retrieval mode, which lets the user move through past notes, scroll through them, and review older entries. This makes the system feel closer to a mini personal study assistant than just a note-taking script.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Navaneesh-A/note_tracker_class.git
cd note_tracker_class
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install the required dependencies:

```bash
pip install keyboard firebase-admin python-dotenv flask
```

4. Create a `.env` file with your Firebase and API information:

```env
API_KEY=your_api_key_or_endpoint
DATABASE_URL=https://your-project-default-rtdb.firebaseio.com
FIREBASE_KEY=./firebase-key.json
```

Make sure your Firebase service account JSON file is valid and accessible.

## Running the app

### Main tracker app

```bash
python main.py
```

This runs the keyboard-driven note tracker and syncs notes with Firebase.

### Dashboard

```bash
python app.py
```

Then open:

```text
http://localhost:6060
```

This serves a simple dashboard showing notes organized by subject.

## Typical usage

- Press `F1` to switch to `DSA`
- Press `F2` to switch to `Skillrack`
- Start typing your note
- Press `\` to save the note
- Press `F5` to enter retrieval mode and browse older notes
- Switch subjects anytime using the function keys

## Challenges and learning points

This project was built mostly as a learning experience, so it includes some rough edges and practical shortcuts.

A few challenges involved:

- capturing keyboard events correctly in Python
- managing subject state and note state across modes
- updating an OLED-like display without lagging the input
- syncing live notes into Firebase reliably
- keeping a simple UI working without overcomplicating the code

These challenges were valuable because they taught me how to think about state, event-driven programming, and integrating small hardware/software systems.

## Possible improvements

This is a project with room to grow. Some ideas for the future include:

- adding a proper GUI instead of keyboard-only interaction
- improving note editing and deletion
- adding search and tag filtering
- making the dashboard more visual and attractive
- adding support for more subjects and categories
- making the code more modular and easier to maintain

## Final note

This project is a beginner-friendly but genuinely useful idea: a student-friendly note tracker that blends keyboard input, real-time storage, and quick review. It is not just about saving notes; it is about building a tiny system that fits a student lifestyle and helps with daily revision.

It started as a simple problem-solving experiment and grew into a project that mixes software, productivity, and curiosity. That is what makes it interesting.

If you want to extend it, adjust it, or improve the interface, this is a great starting point for a more advanced smart study tool.

## License

This repository does not currently include a license file. If you plan to share or extend it publicly, adding a license is a good next step.
