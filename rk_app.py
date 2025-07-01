import streamlit as st
from gtts import gTTS
import wikipedia
import speech_recognition as sr
import os
import random
from tempfile import NamedTemporaryFile

# ------------------- Voice Input -------------------
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {text}")
        return text
    except:
        st.error("❌ Could not understand voice.")
        return ""

# ------------------- Wikipedia Summary -------------------
def get_summary(topic):
    try:
        return wikipedia.summary(topic, sentences=3)
    except:
        return "❌ Could not fetch summary."

# ------------------- gTTS Podcast -------------------
def create_podcast(summary):
    conversation = [
        "Hey, today’s topic is amazing!",
        f"Here’s something about it: {summary}",
        "That’s interesting. I love learning with RK AI!",
        "See you next time!"
    ]
    audio_files = []
    for i, line in enumerate(conversation):
        tts = gTTS(text=line, lang='en')
        temp_file = NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        audio_files.append(temp_file.name)
    return audio_files

# ------------------- Main App -------------------
st.set_page_config(page_title="RK AI - Podcast App", layout="centered")
st.title("🎙️ RK AI - Voice Wikipedia to Podcast")

mode = st.radio("Choose Input Mode", ["🎤 Voice", "⌨️ Text"])
topic = ""

if mode == "🎤 Voice":
    if st.button("Start Listening"):
        topic = get_voice_input()
else:
    topic = st.text_input("Enter a topic:")

if topic:
    summary = get_summary(topic)
    st.markdown("### 📖 Wikipedia Summary")
    st.write(summary)

    st.markdown("### 🎧 AI Podcast")
    files = create_podcast(summary)
    for i, file in enumerate(files):
        st.audio(file, format="audio/mp3")