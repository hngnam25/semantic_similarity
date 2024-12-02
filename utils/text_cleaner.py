import re

def clean_text(text):
# Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove non-ASCII characters if needed
    text = text.encode('ascii', 'ignore').decode()
    # Strip leading and trailing whitespace
    text = text.strip()
    return text