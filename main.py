import os 
import google.generativeai as genai
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

# Configure Google-API-Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initilize Model
model=genai.GenerativeModel('gemini-1.5-pro')

# Generate Content
def get_response(input_prompt,image):
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Initialize Streamlit app
st.set_page_config(page_title='Nutritionist page')

st.header("DIET ADVISOR APPLICATION")
uploaded_file = st.file_uploader("Choose an image...", type=['JPEG','JPG','PNG'])

image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit = st.button('Tell me about the total calories')

# Prompt Template
input_prompt = """

You are an expert nutritionist where you need to see the food items from the image and give the estimation of the total calories as per standard size of items that you are able to see, and also provide details of every food items with calories intake
in below format

1. item-1 : number of calories
2. item-2 : number of calories
--------
--------

And also mention the diet is healthy or not and also mention the percentage split of the ratio of carbohydrates,fibers,fat,sugar and other important things required in our diet.

"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_response(input_prompt,image_data)
    st.subheader('The Response is')
    st.write(response)