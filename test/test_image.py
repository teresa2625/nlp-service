import requests

def test_generate_image():
    url = "http://127.0.0.1:8000/generate-image/"

    note = "Left shoulder muscle tight"

    response = requests.get(url, params={"note": note})

    if response.status_code == 200:
        print(f"✅ Test Passed: Image generated successfully")
        with open("output_test.png", "wb") as f:
            f.write(response.content)
        print("Image saved as output_test.png")
    else:
        print(f"❌ Test Failed: {response.status_code} - {response.json()}")

test_generate_image()
