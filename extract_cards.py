import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
import os

def extract_and_save_cards(image_path, output_dir="output"):
    """
    Detects cards in an image, extracts them, and saves them as separate image files.

    Args:
        image_path (str): The path to the input image.
        output_dir (str): The directory to save the extracted card images.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the image
    try:
        original_image = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return

    # Load the model and processor
    model_id = "IDEA-Research/grounding-dino-base"
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id)

    # Prepare the text prompt
    text = "playing card."

    # Process the image and text
    inputs = processor(images=original_image, text=text, return_tensors="pt")

    # Get predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Process the results
    results = processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        threshold=0.2,
        text_threshold=0.2,
        target_sizes=[original_image.size[::-1]]
    )

    # Extract and save each card
    for i, (box, score, label) in enumerate(zip(results[0]["boxes"], results[0]["scores"], results[0]["labels"])):
        # Crop the image using the bounding box coordinates
        card_image = original_image.crop(box.tolist())

        # Save the cropped image
        output_path = os.path.join(output_dir, f"card_{i+1}.png")
        card_image.save(output_path)
        print(f"Saved card to {output_path}")

import requests

if __name__ == "__main__":
    # Example usage:
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Playing_cards_collage.jpg/250px-Playing_cards_collage.jpg"
    image_path = "downloaded_cards.jpg"

    # Download the image with a User-Agent header
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(image_url, headers=headers, stream=True)
        response.raise_for_status()
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Image downloaded to {image_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        exit()

    extract_and_save_cards(image_path)