import streamlit as st
from PIL import Image, ImageDraw
import pytesseract
import numpy as np

# Function to load the image and cache the result
@st.cache_resource
def load_image(uploaded_file):
    return Image.open(uploaded_file)

# Function to perform OCR and cache the extracted text
@st.cache_data
def perform_ocr(image_np):
    ocr_data = pytesseract.image_to_data(image_np, lang='eng+hin', output_type=pytesseract.Output.DICT)
    extracted_text = " ".join(ocr_data['text'])
    return ocr_data, extracted_text

# Streamlit UI layout
st.title("OCR: Extract Hindi & English Text from Images")
st.write("Upload an image and search for keywords in the extracted text (both Hindi and English are supported).")

# Upload image
uploaded_file = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load image with caching
    image = load_image(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert the uploaded image to a NumPy array
    image_np = np.array(image)

    # Perform OCR with caching
    st.write("Extracting text...")
    ocr_data, extracted_text = perform_ocr(image_np)
    st.write("Extracted Text:", extracted_text)

    # Keyword search within the extracted text (Hindi and English)
    search_query = st.text_input("Enter keyword to search (supports Hindi and English):")

    if search_query:
        # Make a copy of the original image to draw on
        image_with_boxes = image.copy()
        draw = ImageDraw.Draw(image_with_boxes)

        # Loop through the OCR data to find occurrences of the search query
        for i, word in enumerate(ocr_data['text']):
            if search_query.lower() in word.lower():
                # Get the bounding box coordinates for the word
                (x, y, w, h) = (ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i])
                # Draw a rectangle around the word
                draw.rectangle([(x, y), (x + w, y + h)], outline="red", width=2)

        # Display the image with boxes
        st.image(image_with_boxes, caption='Image with keyword highlighted', use_column_width=True)

        # Highlight the search results in the extracted text
        highlighted_text = extracted_text.replace(search_query, f"**{search_query}**")
        st.markdown(f"Search Results:\n{highlighted_text}")
