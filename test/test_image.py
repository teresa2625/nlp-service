import requests

def test_generate_image():
    # URL of the FastAPI endpoint
    url = "http://127.0.0.1:8000/generate-image/"

    # Example note (doctor's input)
    note = "Left shoulder muscle tight"

    # Send a GET request to the FastAPI endpoint
    response = requests.get(url, params={"note": note})

    # Check the response status and display the result
    if response.status_code == 200:
        print(f"✅ Test Passed: Image generated successfully")
        with open("output_test.png", "wb") as f:
            f.write(response.content)  # Save the image locally as output_test.png
        print("Image saved as output_test.png")
    else:
        print(f"❌ Test Failed: {response.status_code} - {response.json()}")

# Run the test
test_generate_image()
