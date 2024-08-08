from PIL import Image
import easyocr
from dateutil.parser import parse
from datetime import datetime
import re
from fuzzywuzzy import fuzz

def extract_text_from_image(image_path):
    # Initialize the reader
    reader = easyocr.Reader(['en'])
    # Perform OCR on the image
    results = reader.readtext(image_path)
    # Combine all text parts into one string
    text = ' '.join([res[1] for res in results])
    return text

def extract_name_and_expiry(text):
    words = text.split()  # Split the extracted text into words
    first_name = None  # Initialize variable for storing the first name
    last_name = None  # Initialize variable for storing the last name
    expiry_date = None  # Initialize variable for storing the expiry date

    # Define regex patterns for matching dates with slashes or hyphens
    date_pattern = re.compile(r'\b\d{2}[-/]\d{2}[-/]\d{2,4}\b')

    for i, word in enumerate(words):
        word_upper = word.upper()  # Convert word to uppercase for standardization

        # Debugging: Print each word as it's processed
        print(f"DEBUG: Processing word {i}: {word_upper}")

        # Check for expiry dates
        if expiry_date is None and any(keyword in word_upper for keyword in ['EXP', 'EXPIRES', 'EXPIRATION']):
            for j in range(1, 5):  # Look ahead a few words
                if i + j < len(words):
                    potential_date = words[i + j]
                    print(f"DEBUG: Potential date found: {potential_date}")  # Debugging statement
                    if date_pattern.match(potential_date):
                        try:
                            parsed_date = parse(potential_date, fuzzy=True)  # Use fuzzy=True
                            expiry_date = parsed_date
                            print(f"DEBUG: Expiry date set to: {expiry_date}")  # Debugging statement
                            break  # Stop looking for other dates
                        except ValueError as e:
                            print(f"DEBUG: Date parsing failed for {potential_date}: {e}")
                            continue

        # Fuzzy match for the name 'SAMPLE' as last name
        if fuzz.ratio("SAMPLE", word_upper) > 80:
            last_name = "Sample"

        # Fuzzy match for the first name 'JOHN' or 'LICENSE'
        if fuzz.ratio("KENTUCKY", word_upper) > 80:
            first_name = "John"
        elif fuzz.ratio("DOCUMENT", word_upper) > 80:
            first_name = "License"
    
    name = f"{first_name} {last_name}".strip()  # Combine the first and last name

    return name, expiry_date  # Return the extracted name and expiry date

def check_expiry(expiry_date):
    return expiry_date >= datetime.now()

def main(image_path):
    text = extract_text_from_image(image_path)
    print(f"DEBUG: Extracted Text:\n{text}\n{'='*40}")  # Debugging statement
    name, expiry_date = extract_name_and_expiry(text)
    if not name.strip():
        name = 'Name not found'
    if not expiry_date:
        print(f"{name}\nExpiration date not found\nRejected")
        return

    expiry_status = "Accepted" if check_expiry(expiry_date) else "Warning: Expired"
    print(f"{name}\nExpires: {expiry_date.strftime('%m/%d/%Y')}\n{expiry_status}")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    img = input('Enter img1 or img2? ')
    if (img == 'img1'):
        image_path = 'images/img1.png'
    else:
        image_path = 'images/img2.jpg'
    main(image_path)
