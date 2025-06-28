import pdfplumber
from PIL import Image
import pytesseract

# Set path to your tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\jaida\OneDrive\Desktop\Nyay_AI\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text
