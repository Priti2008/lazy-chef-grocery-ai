import base64
import os
import requests
import streamlit as st
from PIL import Image

# Page Config
st.set_page_config(
    page_title="Lazy Chef: Fridge to Grocery List", page_icon="🛒", layout="centered"
)

st.title("🛒 Lazy Chef: Fridge Photo to Grocery List")
st.markdown(
    "*Channel your inner sloth! Let open-source AI inspect your fridge so you"
    " don't have to think about what's missing.*"
)

# Sidebar for configuration
st.sidebar.header("Configuration")
model_choice = st.sidebar.selectbox(
    "Choose Open-Weight Vision Model",
    ["llama3.2-vision", "minicpm-v", "llava"],
)
ollama_url = st.sidebar.text_input(
    "Ollama API Endpoint", value="http://localhost:11434/api/chat"
)

# Image Upload
uploaded_file = st.file_uploader(
    "Upload a photo of your fridge or pantry...", type=["jpg", "jpeg", "png"]
)


def encode_image(image_file):
  return base64.b64encode(image_file.read()).decode("utf-8")


if uploaded_file is not None:
  # Display uploaded image
  image = Image.open(uploaded_file)
  st.image(image, caption="Your Fridge State", use_container_width=True)

  if st.button("Generate Grocery List (The Lazy Way) 🦥"):
    with st.spinner("Analyzing your fridge locally... Please wait."):
      # Reset file pointer for encoding
      uploaded_file.seek(0)
      base64_image = encode_image(uploaded_file)

      prompt = (
          "Analyze this fridge/pantry photo. Identify what items are running"
          " low or missing, and generate a clean, categorized grocery shopping"
          " list (e.g., Dairy, Vegetables, Snacks, Beverages). Keep it brief"
          " and practical."
      )

      payload = {
          "model": model_choice,
          "messages": [{
              "role": "user",
              "content": prompt,
              "images": [base64_image],
          }],
          "stream": False,
      }

      try:
        response = requests.post(ollama_url, json=payload)
        if response.status_code == 200:
          result = response.json()
          ai_response = result.get("message", {}).get(
              "content", "No response generated."
          )

          st.success("Grocery List Generated Successfully!")
          st.markdown("### 📝 Your Smart Shopping List:")
          st.markdown(ai_response)
        else:
          st.error(
              f"Error from Ollama local server: {response.status_code} -"
              f" {response.text}"
          )
      except Exception as e:
        st.error(
            f"Failed to connect to local Ollama instance. Is it running? Error:"
            f" {e}"
        )

# Footer info on Open Innovation
st.markdown("---")
st.markdown("### 💡 Why Open-Source AI Matters Here:")
st.markdown(
    "- **Total Data Privacy:** Your personal fridge contents and home photos"
    " never leave your local machine or get uploaded to third-party cloud"
    " servers.\n- **Zero Cost:** Running inference locally via Ollama means no"
    " API token costs or paid subscriptions.\n- **Offline Capability:** Works"
    " even without an active internet connection."
)