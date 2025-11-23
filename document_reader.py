import pdfplumber
from docx import Document

def read_document(file_path):
    """
    Read text from PDF, Word, or TXT files
    """
    text = ""
    
    if file_path.endswith('.pdf'):
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            
    elif file_path.endswith('.docx'):
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading Word document: {e}")
            
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            print(f"Error reading text file: {e}")
    else:
        raise ValueError("Unsupported file format. Please use PDF, DOCX, or TXT.")
    
    return text

# Test the function
if __name__ == "__main__":
    print("Document reader is working!")