import streamlit as st
from datetime import datetime
import uuid
import re

# Minimalist styling
st.markdown("""
    <style>
    body, .main {
        background-color: #ffffff;
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
    }

    input, textarea {
        background-color: #f9f9f9;
        color: #000;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 6px;
    }

    button {
        background-color: #000;
        color: #fff;
        border-radius: 4px;
        padding: 6px 12px;
        border: none;
    }

    .stButton > button, .stTextInput > div > input {
        box-shadow: none !important;
    }

    .rtl {
        direction: rtl;
        text-align: right;
    }

    .ltr {
        direction: ltr;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize notes storage
if 'notes' not in st.session_state:
    st.session_state.notes = {}

st.title("NOts")

# Helper to detect URLs and convert to clickable HTML
def linkify(text):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.sub(r'<a href="\1" target="_blank" style="color:blue">\1</a>', text)

# Detect if text is Persian
def is_persian(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

# Create new blank note
if st.button("＋ New Note"):
    note_id = str(uuid.uuid4())
    st.session_state.notes[note_id] = {
        "text": "",
        "todos": [],
        "checklist": [],
        "images": [],
        "audio": [],
        "reminder": None,
        "created": datetime.now()
    }
    st.rerun()

# Display all notes
for note_id, note in list(st.session_state.notes.items()):
    with st.expander(f"Note created on {note['created'].strftime('%Y-%m-%d %H:%M:%S')}"):

        # Auto-save text area
        text_key = f"text_{note_id}"
        if text_key not in st.session_state:
            st.session_state[text_key] = note['text']
        st.text_area("✐ Edit Text", value=st.session_state[text_key], key=text_key,
                     on_change=lambda: note.update({"text": st.session_state[text_key]}))

        # Apply direction based on language
        direction_class = "rtl" if is_persian(note['text']) else "ltr"
        st.markdown(f"<div class='{direction_class}'>{linkify(note['text'])}</div>", unsafe_allow_html=True)

        # Add To-Do items
        with st.form(key=f"todo_form_{note_id}", clear_on_submit=True):
            new_todo = st.text_input("＋ Add To-Do", key=f"todo_input_{note_id}")
            submitted = st.form_submit_button("Add")
            if submitted and new_todo:
                note['todos'].append({"text": new_todo, "done": False})
                st.rerun()

        # Display To-Do list
        for i in range(len(note['todos'])):
            todo = note['todos'][i]
            col1, col2, col3 = st.columns([0.05, 0.85, 0.1])
            with col1:
                todo['done'] = st.checkbox("", value=todo['done'], key=f"todo_check_{note_id}_{i}")
            with col2:
                st.write(todo['text'])
            with col3:
                if st.button("⨯", key=f"del_todo_{note_id}_{i}"):
                    note['todos'].pop(i)
                    st.rerun()

        # Add Checklist items
        with st.form(key=f"check_form_{note_id}", clear_on_submit=True):
            new_check = st.text_input("＋ Add Checklist", key=f"check_input_{note_id}")
            submitted_check = st.form_submit_button("Add")
            if submitted_check and new_check:
                note['checklist'].append({"text": new_check, "done": False})
                st.rerun()

        # Display Checklist
        for i in range(len(note['checklist'])):
            item = note['checklist'][i]
            col1, col2, col3 = st.columns([0.05, 0.85, 0.1])
            with col1:
                item['done'] = st.checkbox("", value=item['done'], key=f"check_{note_id}_{i}")
            with col2:
                st.write(item['text'])
            with col3:
                if st.button("⨯", key=f"del_check_{note_id}_{i}"):
                    note['checklist'].pop(i)
                    st.rerun()

        # Add images
        uploaded_image = st.file_uploader("＋ Add Image", type=["png", "jpg", "jpeg"], key=f"img_{note_id}")
        if uploaded_image:
            note['images'].append(uploaded_image)
            st.rerun()
        for img in note['images']:
            st.image(img)

        # Add audio
        uploaded_audio = st.file_uploader("＋ Add Audio", type=["mp3", "wav"], key=f"audio_{note_id}")
        if uploaded_audio:
            note['audio'].append(uploaded_audio)
            st.rerun()
        for audio in note['audio']:
            st.audio(audio)

        # Add reminder
        reminder_date = st.date_input("⏰ Set Reminder", value=note['reminder'] or datetime.today(), key=f"reminder_{note_id}")
        note['reminder'] = reminder_date

        # Delete note
        if st.button("⨯ Delete Note", key=f"del_{note_id}"):
            del st.session_state.notes[note_id]
            st.rerun()
