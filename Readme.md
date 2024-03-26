

# Swiggy PDF Invoice Generation and Processing

This project is designed to automate the retrieval and processing of Swiggy invoice PDFs from Gmail, ensuring efficient management and analysis of food order expenses. It searches through the user's Gmail for emails from Swiggy containing PDF invoices, extracts these PDFs, and processes them to extract key information, such as invoice numbers and totals, while also checking for and eliminating duplicate invoices based on invoice numbers.

## Features

- **Email Search**: Automatically search your Gmail inbox for Swiggy invoice emails using specific criteria.
- **PDF Extraction**: Download PDF attachments directly from fetched emails.
- **Invoice Processing**: Extract critical information from each invoice, including invoice numbers and total amounts.
- **Duplicate Check**: Ensure that each processed invoice is unique by checking against previously processed invoice numbers.
- **PDF Merging**: Combine all unique invoices into a single PDF file for easy archiving and review.
- **Summarization**: Calculate the total amount spent on Swiggy orders based on the invoices processed.

## Prerequisites

- Python 3.8 or later
- Access to a Gmail account with Swiggy invoice emails
- Google Cloud project with the Gmail API enabled

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/vivekrunwal/Swiggy_Gmail_Client.git
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Gmail API Setup**

- Follow Google's guide to create a project in the Google Developer Console, enable the Gmail API, and obtain your `credentials.json` file. Place this file in the project root.

## Configuration

You can customize search criteria and other settings by editing the `config.py` file:

```python
# Example configuration
EMAIL_SEARCH_QUERY = 'from:swiggy.com subject:swiggy'
...
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, and suggest features.


## Acknowledgments

- This project is not affiliated with or endorsed by Swiggy.
- Thanks to the Gmail API for making email processing possible.

---

Remember to replace placeholder URLs and any specific instructions with your project's actual details. This README file provides a comprehensive guide to help users understand and use your project effectively.