import cv2
import numpy as np

def generate_body_image(output_path="body.png"):
    """ Generates a simple human body figure. """
    # Create a blank white canvas
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255

    # Draw head
    cv2.circle(img, (250, 80), 40, (0, 0, 0), 3)  # Head

    # Draw body
    cv2.line(img, (250, 120), (250, 300), (0, 0, 0), 3)  # Spine

    # Draw arms
    cv2.line(img, (250, 150), (150, 200), (0, 0, 0), 3)  # Left arm
    cv2.line(img, (250, 150), (350, 200), (0, 0, 0), 3)  # Right arm

    # Draw legs
    cv2.line(img, (250, 300), (180, 450), (0, 0, 0), 3)  # Left leg
    cv2.line(img, (250, 300), (320, 450), (0, 0, 0), 3)  # Right leg

    # Save image
    cv2.imwrite(output_path, img)
    print(f"✅ Body image generated and saved as {output_path}")

# Run the function
generate_body_image()
