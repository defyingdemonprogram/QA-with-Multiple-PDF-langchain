import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Configure the Streamlit page
st.set_page_config(page_title="🥣FOOD MANAGER", page_icon="🩺")
st.title("🥣Your Diet Manager")

def get_gemini_response(input_prompt, image_data, system_prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image_data[0], system_prompt])
    return response.text

def process_image(uploaded_file):
    # Check if file is uploaded
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        # print("Data type:", uploaded_file.type)
        return image_parts
    else:
        raise FileNotFoundError("No file is uploaded")

# User input prompt
user_input = st.text_input("Input Prompt: ", "Is this Food Healthy?",key="input")

# Upload the image
with st.sidebar:
    uploaded_file = st.file_uploader("Upload the image of food you want...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
submit = st.button("Tell me the total calories")

# System prompt
system_prompt = """You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food item in the format as:

1. Item 1 - no of calories
2. Item 2 - no of calories

------
------
"""

# If submit button is clicked
if submit:
    image_data = process_image(uploaded_file)
    response = get_gemini_response(user_input, image_data, system_prompt)
    with st.chat_message("assistant"):
        st.write(response)
