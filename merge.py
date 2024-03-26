import fitz  # PyMuPDF
import os
import re
import PyPDF2


store_dir = './attachments/taco'

def extract_text_from_first_page(pdf_path):
    """
    Extract text from the first page of a PDF file.
    """
    print(pdf_path)
    with fitz.open(pdf_path) as doc:
        page = doc.load_page(0)  # Assuming the relevant info is on the first page
        text = page.get_text()
        print(text)
    return text

def find_invoice_amounts(text):
    """
    Find invoice amounts in the extracted text using a regular expression.
    """
    # This is a simple regex that looks for patterns resembling currency amounts
    regex_pattern =  r"Invoice Total\s*\n*(\d+\.\d{2})"
    amounts = re.findall(regex_pattern, text)
    return amounts

def find_invoice_num(text):
    regex_pattern =  r"Invoice No:\s*(\d+)"

    invoice_num = re.findall(regex_pattern, text)
    return invoice_num[-1]


pdf_paths = [os.path.join(store_dir, f) for f in os.listdir(store_dir) if f.endswith('.pdf')]
total_amount = 0.0

invoice_numbers_seen = set()

for pdf_path in pdf_paths:
    text = extract_text_from_first_page(pdf_path)
    amounts = find_invoice_amounts(text)
    invoice_num = find_invoice_num(text)
    print(text, invoice_num)
    
    if(invoice_num not in invoice_numbers_seen):
    # Assuming the last amount in the document is the total for simplicity
        if amounts:
            total_amount += float(amounts[-1])
    invoice_numbers_seen.add(invoice_num)

# 2945.16

print(pdf_paths)
print(f'Total Amount: {total_amount}')


pdf_writer = PyPDF2.PdfWriter()

for pdf_path in pdf_paths:  # `pdf_paths` is a list of paths to your PDF files
    pdf_reader = PyPDF2.PdfReader(pdf_path)

    invoice_num = find_invoice_num(text)
    
    if(invoice_num in invoice_numbers_seen):
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
        invoice_numbers_seen.remove(invoice_num)

with open('merged_invoices.pdf', 'wb') as out:
    pdf_writer.write(out)
