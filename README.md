# Card Extractor

This project contains a Python script to detect and extract playing cards from an image and save each card as a separate file.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the script, execute the following command in your terminal:

```bash
python extract_cards.py
```

The script will download a sample image of playing cards, process it to detect the cards, and save the extracted card images in the `output/` directory. Each card will be saved as a separate PNG file (e.g., `card_1.png`, `card_2.png`, etc.).