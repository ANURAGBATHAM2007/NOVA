import streamlit as st
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import base64
import os

# API Keys
newsapi = "<Your Key Here>"
client = OpenAI(api_key="<Your Key Here>")

# Function to play audio in Streamlit
def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")
    audio_file = open("temp.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
    os.remove("temp.mp3")

# AI response function
def aiProcess(command):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant. Give short responses."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

# Command processing
def processCommand(c):
    if "open google" in c.lower():
        st.write("Opening Google...")
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        st.write("Opening Facebook...")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        st.write("Opening YouTube...")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        st.write("Opening LinkedIn...")
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            st.write(f"Playing {song}...")
            webbrowser.open(link)
        else:
            st.write("Song not found in library.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # show only 5
                st.write("📰", article['title'])
                speak(article['title'])
    else:
        output = aiProcess(c)
        st.write("🤖 Jarvis:", output)
        speak(output)

# Streamlit App
st.title("🧠 Jarvis - Your Virtual Assistant")
st.write("Type your command below:")

user_input = st.text_input("Enter command (e.g., 'open google', 'play song', 'news', 'hello')")
if st.button("Run Command"):
    if user_input:
        processCommand(user_input)

