# Project Title: Booking system - NLP Body Part Annotation Service

## Overview

This FastAPI-based service extracts body parts from medical notes using NLP (spaCy) and generates an annotated image marking the identified body part.

## Features

- Extracts body parts from text using NLP (spaCy).
- Generates an image marking the identified body part.
- Returns the annotated image as a response.
- Supports multiple body parts like shoulders, knees, elbows, head, and

## Prerequisites

- Python 3.x
- `pip` package manager

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/nlp-service.git
cd nlp-service
```

2. Create a virtual environment (optional but recommended):

```
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Download the required NLP model:

```
python -m spacy download en_core_web_sm
```

5. Running the Service

## Start the FastAPI server:

```
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## API Endpoint

### GET /generate-image/

#### Request Parameters

- `note` (string): Doctor's note describing symptoms, e.g., `Left shoulder muscle tight`.

### Example Request

```
curl -X 'GET' \
 'http://127.0.0.1:8000/generate-image/?note=Left%20shoulder%20muscle%20tight' \
 -H 'accept: image/png' --output annotated_image.png
```

### Response

- Returns a PNG image with the detected body part marked.

## Debugging

- Debug logs are printed in the terminal while the service runs.
- If no body part is recognized, check the logs for tokenized words and NLP processing details.

## Repository Structure

```
nlp-service/
├── main.py # FastAPI service
├── requirements.txt # Dependencies
├── body.jpg # Body diagram image (replace with your own)
└── README.md # Documentation
```

## Troubleshooting

1. Body image not found

- Ensure `body.jpg` is present in the root directory.
- Try using a different image format like PNG.

2. PIL or FastAPI not found

- Run `pip install -r requirements.txt` to install missing dependencies.

3. spaCy model not installed

- Run `python -m spacy download en_core_web_sm`.
