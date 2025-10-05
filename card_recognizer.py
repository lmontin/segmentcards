import requests
import json
import time
import random

# --- SETUP ---
API_ENDPOINT = "https://api.ximilar.com/recognition/v2/recognize"
TASK_ID = "889f207c-953b-4204-a698-10e30d7c222c"
AUTH_TOKEN = "Token 4026605e54b6797a7806de6f83733075677a28e9"
IMAGE_PATH = "path/to/your/card_image.jpg" # <-- IMPORTANT: CHANGE THIS

# --- ABUSE PREVENTION SETUP ---

# 1. A list of realistic User-Agent strings to rotate through
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
]

# 2. Settings for exponential backoff retry mechanism
MAX_RETRIES = 5
INITIAL_BACKOFF = 1 # Start with a 1-second wait

# 3. (Optional) Proxy configuration
# To use, you need a proxy service. Example format:
# PROXIES = {
#    "http": "http://user:pass@host:port",
#    "https": "http://user:pass@host:port",
# }


def recognize_card(image_path):
    """
    Uploads a card image for recognition with abuse-handling techniques.
    """
    retries = 0
    backoff_time = INITIAL_BACKOFF

    while retries < MAX_RETRIES:
        try:
            # --- Prepare the request for each attempt ---
            headers = {
                "Authorization": AUTH_TOKEN,
                "User-Agent": random.choice(USER_AGENTS) # Rotate User-Agent
            }
            data = {"task_id": TASK_ID}

            with open(image_path, "rb") as image_file:
                files = {'records': (image_path, image_file, 'image/jpeg')}

                print(f"\nAttempt {retries + 1}/{MAX_RETRIES}: Uploading image...")
                response = requests.post(
                    API_ENDPOINT,
                    headers=headers,
                    data=data,
                    files=files,
                    # proxies=PROXIES # Uncomment to use proxies
                    timeout=15 # Add a timeout
                )

                # --- Process the response ---
                if response.status_code == 200:
                    print("✅ Success! Recognition Results:")
                    print(json.dumps(response.json(), indent=2))
                    return # Exit the function on success

                elif response.status_code == 429: # Rate limit hit!
                    print(f"⚠️ Rate limit hit (429). Backing off for {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    backoff_time *= 2 # Double the wait time for the next attempt
                    retries += 1

                else: # Handle other potential errors
                    print(f"❌ Error: Received status code {response.status_code}")
                    print(f"Response: {response.text}")
                    # For other server errors, you might want to retry after a short delay
                    time.sleep(2)
                    retries += 1

            # Add a small, polite delay between retries even if not rate-limited
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"❌ Network Error: {e}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
            backoff_time *= 2
            retries += 1

    print("\n❌ Failed to get a successful response after all retries.")


# --- Main execution ---
if __name__ == "__main__":
    try:
        # This will run the function for your specified image
        recognize_card(IMAGE_PATH)

        # If you were processing multiple images, you'd add a polite delay here
        # print("\n--- Waiting before next image ---")
        # time.sleep(2) # Wait 2 seconds before processing the next file in a loop

    except FileNotFoundError:
        print(f"❌ FATAL ERROR: The file was not found at '{IMAGE_PATH}'")