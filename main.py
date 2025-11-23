from document_reader import read_document
from extractor import extract_obligations
from excel_mapper import map_to_framework
from config import KEYWORD_CATEGORIES, CATEGORY_TO_DOMAIN
import os

def main():
    print("=== Privacy Document Automation Tool ===")
    print("This tool maps privacy obligations directly to your Excel framework.")
    
    # File paths
    original_framework = "Data Protection Framework_PDPA_Malaysia.xlsx"
    working_framework = "Working_Framework.xlsx"
    
    # Check if we have a working copy, otherwise start with original
    if os.path.exists(working_framework):
        current_framework = working_framework
        print("📖 Continuing with existing working framework...")
    else:
        current_framework = original_framework
        print("📖 Starting with original framework...")
    
    # Get document path from user
    file_path = input("Enter the path to your privacy document: ").strip()
    
    try:
        # 1. Read the document
        print("Reading document...")
        text = read_document(file_path)
        print(f"Document read successfully! ({len(text)} characters)")
        
        # 2. Extract obligations with domain mapping
        print("Extracting obligations and mapping to domains...")
        obligations = extract_obligations(text, KEYWORD_CATEGORIES, CATEGORY_TO_DOMAIN)
        print(f"Found {len(obligations)} relevant clauses!")
        
        # 3. Display what was found
        if obligations:
            print("\n--- EXTRACTED OBLIGATIONS ---")
            for i, obligation in enumerate(obligations, 1):
                print(f"{i}. [{obligation['domain']}] {obligation['text']}")
            
            # 4. Map to Excel framework (incrementally)
            print(f"\nMapping to framework: {current_framework}")
            
            success = map_to_framework(obligations, current_framework, working_framework)
            
            if success:
                print(f"✅ Success! Framework updated with new findings.")
                print(f"📊 Total documents processed: {count_processed_documents(working_framework)}")
                
                # Ask if user wants to process another document
                another = input("\nProcess another document? (y/n): ").lower()
                if another == 'y':
                    main()  # Restart the process
                else:
                    print(f"🎉 Final updated framework saved as: {working_framework}")
            else:
                print("❌ Failed to update the framework.")
        else:
            print("No relevant obligations found.")
            
    except Exception as e:
        print(f"Error: {e}")

def count_processed_documents(framework_path):
    """Count how many documents have been processed"""
    try:
        import pandas as pd
        df = pd.read_excel(framework_path, sheet_name='Data Protection Framework 1')
        # Count rows with observations
        return df['Observation'].notna().sum()
    except:
        return 0

if __name__ == "__main__":
    main()
    