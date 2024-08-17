import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    transcript = ""

    # Iterate through each page in the PDF
    for page_number in range(document.page_count):
        page = document.load_page(page_number)
        text = page.get_text()
        transcript += text
    
    return transcript

# Path to your PDF file
pdf_path = "/Users/kabir/Desktop/IgnitionHacks/SuhaniMain/Meamifyy/material/history.pdf"

# Extract text from the PDF
transcript = extract_text_from_pdf(pdf_path)

# Print the transcript
print(transcript)
