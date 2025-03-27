from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
import spacy
import io

app = FastAPI()

nlp = spacy.load("en_core_web_sm")

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
    
    text = text.lower()
    print(f"Debug: Normalized text for body part matching: '{text}'")
    
    for body_part in BODY_PARTS:
        if body_part in text:
            print(f"Debug: Found body part '{body_part}' in the note.")
            return body_part
    
    doc = nlp(text)
    print(f"Debug: Processed doc - {doc}")
    
    for token in doc:
        print(f"Debug: Token text '{token.text}', lemma '{token.lemma_}'")
        if token.text.lower() in BODY_PARTS:
            print(f"Debug: Found body part '{token.text.lower()}'")
            return token.text.lower()
    
    print("Debug: No body part found.")
    return None

@app.get("/generate-image/")
def generate_image(note: str):
    """ Generates a body image with marked location and note. """
    print(f"Debug: Generating image for note: '{note}'")
    
    body_part = find_body_part(note)
    
    if not body_part:
        print("Debug: Body part not recognized.")
        raise HTTPException(status_code=400, detail="Body part not recognized.")
    
    print(f"Debug: Body part recognized: '{body_part}'")

    try:
        body_image = Image.open("body.jpg")
        print("Debug: Loaded body image.")
    except Exception as e:
        print(f"Debug: Error loading image - {e}")
        raise HTTPException(status_code=500, detail="Error loading body image.")
    
    draw = ImageDraw.Draw(body_image)

    position = BODY_PARTS.get(body_part)
    if position:
        print(f"Debug: Drawing circle at position {position}")
        draw.ellipse((position[0]-20, position[1]-20, position[0]+20, position[1]+20), outline="red", width=5)

    font = ImageFont.load_default()
    text_position = (position[0] + 30, position[1])
    draw.text(text_position, note, font=font, fill="black")
    print("Debug: Text added to image.")

    img_byte_arr = io.BytesIO()
    body_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return Response(content=img_byte_arr.getvalue(), media_type="image/png")
