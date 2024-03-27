import fitz  # PyMuPDF
import os
import re
import PyPDF2
from datetime import datetime
import PyPDF2
import glob

store_dir = './attachments/taco'
merged_invoice_dir = './'

def delete_merged_invoices(directory):
    # Create a pattern to match all 'merged_invoice' PDF files
    pattern = os.path.join(directory, 'merged_invoice*.pdf')
    
    # Use glob to find all files matching the pattern
    merged_invoice_files = glob.glob(pattern)
    
    for file_path in merged_invoice_files:
        try:
            os.remove(file_path)
            print(f'Deleted {file_path}')
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Usage
delete_merged_invoices(merged_invoice_dir)

def extract_text_from_first_page(pdf_path):
    """
    Extract text from the first page of a PDF file.
    """
    # print(pdf_path)
    with fitz.open(pdf_path) as doc:
        page = doc.load_page(0)  # Assuming the relevant info is on the first page
        text = page.get_text()
        # print(text)
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
    print(f"Amount for {invoice_num} is {amounts} \n")
    
    if(invoice_num not in invoice_numbers_seen):
    # Assuming the last amount in the document is the total for simplicity
        if amounts:
            total_amount += float(amounts[-1])
    invoice_numbers_seen.add(invoice_num)

# 2945.16

# print(pdf_paths)

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
filename = f"merged_invoice_{formatted_time}.pdf"

pdf_writer = PyPDF2.PdfWriter()

print(f"Invoices capured: {invoice_numbers_seen}")

for pdf_path in pdf_paths:  # `pdf_paths` is a list of paths to your PDF files
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text = extract_text_from_first_page(pdf_path)
    invoice_num = find_invoice_num(text)
    # print(f"Invoice Num:{invoice_num}")
    
    if(invoice_num in invoice_numbers_seen):
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
        invoice_numbers_seen.remove(invoice_num)

with open(filename, 'wb') as out:
    pdf_writer.write(out)

print(f'Total Amount: {total_amount}')
