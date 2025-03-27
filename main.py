from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import spacy
import io

app = FastAPI()

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Define body part positions (you can adjust these based on your body image)
BODY_PARTS = {
    "left shoulder": (150, 100),
    "right shoulder": (350, 100),
    "left knee": (180, 400),
    "right knee": (320, 400),
    "left elbow": (100, 250),
    "right elbow": (400, 250),
    "head": (250, 50),
    "torso": (250, 200)
}

def find_body_part(text):
    """ Extracts body part from doctor notes using NLP. """
    print(f"Debug: Processing note - '{text}'")
    
    # Normalize text to lowercase for matching
    text = text.lower()
    print(f"Debug: Normalized text for body part matching: '{text}'")
    
    # Check for multi-word body part directly
    for body_part in BODY_PARTS:
        if body_part in text:
            print(f"Debug: Found body part '{body_part}' in the note.")
            return body_part
    
    # Process the note using spaCy
    doc = nlp(text)
    print(f"Debug: Processed doc - {doc}")
    
    # Check each token in the note and match with body parts
    for token in doc:
        print(f"Debug: Token text '{token.text}', lemma '{token.lemma_}'")
        if token.text.lower() in BODY_PARTS:
            print(f"Debug: Found body part '{token.text.lower()}'")
            return token.text.lower()
    
    # If no body part is found
    print("Debug: No body part found.")
    return None

@app.get("/generate-image/")
def generate_image(note: str):
    """ Generates a body image with marked location and note. """
    print(f"Debug: Generating image for note: '{note}'")
    
    # Find the body part from the note
    body_part = find_body_part(note)
    
    if not body_part:
        print("Debug: Body part not recognized.")
        raise HTTPException(status_code=400, detail="Body part not recognized.")
    
    print(f"Debug: Body part recognized: '{body_part}'")

    # Load body image (ensure 'body.jpg' is in your backend folder)
    try:
        body_image = Image.open("body.jpg")
        print("Debug: Loaded body image.")
    except Exception as e:
        print(f"Debug: Error loading image - {e}")
        raise HTTPException(status_code=500, detail="Error loading body image.")
    
    draw = ImageDraw.Draw(body_image)

    # Circle position based on body part
    position = BODY_PARTS.get(body_part)
    if position:
        print(f"Debug: Drawing circle at position {position}")
        draw.ellipse((position[0]-20, position[1]-20, position[0]+20, position[1]+20), outline="red", width=5)

    # Add text next to the circle
    font = ImageFont.load_default()
    text_position = (position[0] + 30, position[1])
    draw.text(text_position, note, font=font, fill="black")
    print("Debug: Text added to image.")

    # Save the output image to a BytesIO object to return as a response
    img_byte_arr = io.BytesIO()
    body_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return Response(content=img_byte_arr.getvalue(), media_type="image/png")
