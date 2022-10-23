import streamlit as st
from PIL import Image
from pathlib import Path

path = Path('streamlit/banner.jpeg')
st.title("Uncover")
image = Image.open(path)
st.image(image)

