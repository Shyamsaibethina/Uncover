import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
from yaml import load, SafeLoader
from PIL import Image
import base64
import numpy as np
import pandas as pd
import sounddevice as sd
import wavio
import glob
import os

if __name__ == '__main__':
    # ----------------- USER AUTHENTICATION ----
    with open('streamlit/credentials.yaml') as file:
        config = load(file, Loader=SafeLoader)
    alignment = 'vertical'
    st.set_page_config(layout='wide')
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    def img_to_bytes(img_path):
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded
    def img_to_htmlTitle(img_path):
        img_html = "<img src='data:image/png;base64,{}' class='img-fluid' width='750' style='vertical-align:middle;margin:0px -10px; margin-top: -100px'>".format(
        img_to_bytes(img_path)
        )
        return img_html
    def img_to_htmlWelcome(img_path):
        img_html = "<img src='data:image/png;base64,{}' class='img-fluid' width='750' style='horizontal-align:middle;margin:0px 330px; margin-top: -90px'>".format(
        img_to_bytes(img_path)
        )
        return img_html

    def record(duration=5, fs=48000):
        sd.default.samplerate = fs
        sd.default.channels = 1
        myrecording = sd.rec(int(duration * fs))
        sd.wait(duration)
        return myrecording

    def read_audio(file):
        with open(file, "rb") as audio_file:
            audio_bytes = audio_file.read()
        return audio_bytes

    def save_record(path_myrecording, myrecording, fs):
        wavio.write(path_myrecording, myrecording, fs, sampwidth=2)
        return None

    placeholder = st.empty()
    placeholder.markdown(img_to_htmlTitle('streamlit/title.jpeg'), unsafe_allow_html=True)

    name, authentication_status, username = authenticator.login("Login", "main")

    if st.session_state["authentication_status"]:
        placeholder.markdown(img_to_htmlWelcome('streamlit/saiProfile.png'), unsafe_allow_html=True)
        name = st.session_state["name"]

        filename = st.text_input("Choose a filename: ")
        st.markdown(f"<h4 style='text-align: left; color: black; margin-left: -3px'><FONT COLOR='#48064c'>Click button to record audio</h5>", unsafe_allow_html=True)
        if st.button("Click to record"):
            if filename == "":
                st.warning("Choose a filename.")
            else:
                record_state = st.text("Recording...")
                duration = 8
                fs = 48000
                myrecording = record(duration, fs)
                record_state.text(f"Saving sample as {filename}.mp3")

                path_myrecording = f"streamlit/samples/{filename}.mp3"

                save_record(path_myrecording, myrecording, fs)
                record_state.text(f"Done! Saved sample as {filename}.mp3")

                st.audio(read_audio(path_myrecording))

        audio_folder = "streamlit/samples"
        filenames = glob.glob(os.path.join(audio_folder, "*.mp3"))
        selected_filename = st.selectbox("Select a file", filenames)

        st.markdown(f"<h2 style='text-align: left; color: black; margin-left: -3px'><FONT COLOR='#48064c'>Team Acme:</h2>", unsafe_allow_html=True)
        chart_data = pd.DataFrame(
            np.random.randn(50, 3),
            columns=["a", "b", "c"])
        col1, col2 = st.columns(2)
        
        names = ['Chinar', 'Teja', 'Christian', 'Sai']
        for name in names:
            st.write(name)
            st.bar_chart(chart_data)
        authenticator.logout(button_name="Logout")

    elif st.session_state["authentication_status"] == False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] == None:
        st.warning('Please enter your username and password')

