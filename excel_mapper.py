import pandas as pd
import os
from config import CATEGORY_TO_DOMAIN

def format_observations(obligations):
    """
    Format obligations as clean bullet points
    """
    # Get unique obligation texts (remove duplicates)
    unique_texts = list(set(obs['text'] for obs in obligations))
    
    # Clean and truncate long texts
    cleaned_texts = []
    for text in unique_texts:
        # Remove extra whitespace
        clean_text = ' '.join(text.split())
        # Truncate very long texts but keep meaning
        if len(clean_text) > 150:
            clean_text = clean_text[:147] + '...'
        cleaned_texts.append(clean_text)
    
    # Format as bullet points
    if len(cleaned_texts) == 1:
        return f"• {cleaned_texts[0]}"
    else:
        bullet_points = "\n".join([f"• {text}" for text in cleaned_texts])
        return bullet_points

def map_to_framework(obligations, framework_path, output_path):
    """
    Map extracted obligations to the existing Excel framework
    """
    try:
        # Check if input file exists
        if not os.path.exists(framework_path):
            print(f"❌ Error: Framework file '{framework_path}' not found!")
            return False
            
        # Check if output file is open in another program
        if os.path.exists(output_path):
            try:
                # Try to open the file to check if it's locked
                with open(output_path, 'a'):
                    pass
            except PermissionError:
                print(f"❌ Error: '{output_path}' is open in another program. Please close it and try again.")
                return False
        
        # Read the Excel file
        print("Reading Excel framework...")
        
        # DEBUG: Check available sheets
        all_sheets = pd.read_excel(framework_path, sheet_name=None)
        print(f"Available sheets: {list(all_sheets.keys())}")
        
        # Try to read the framework sheet
        try:
            df = pd.read_excel(framework_path, sheet_name='Data Protection Framework 1')
        except:
            # Try the first sheet if the specific name doesn't work
            first_sheet_name = list(all_sheets.keys())[0]
            print(f"Trying first sheet instead: {first_sheet_name}")
            df = all_sheets[first_sheet_name]
        
        print(f"✅ Loaded framework with {len(df)} rows")
        print(f"Columns in framework: {list(df.columns)}")
        
        # Initialize observations column if empty
        if 'Observation' not in df.columns:
            df['Observation'] = ''
        
        # Initialize Concise_Observation column if it doesn't exist
        if 'Concise_Observation' not in df.columns:
            df['Concise_Observation'] = ''
        
        # Create a set of found domains from obligations for faster lookup
        found_domains = set(obligation['domain'] for obligation in obligations)
        
        print(f"Found obligations in domains: {found_domains}")
        print(f"Total obligations to map: {len(obligations)}")
        
        # Map obligations to the framework
        updates_made = 0
        for index, row in df.iterrows():
            domain = str(row['Domain']) if pd.notna(row['Domain']) else ""
            current_observation = str(row['Observation']) if pd.notna(row['Observation']) else ""
            
            # Skip if domain is empty or already has content
            if not domain or current_observation:
                continue
            
            # Check if this domain has any obligations
            domain_obligations = [obs for obs in obligations if obs['domain'] == domain]
            
            if domain_obligations:
                # Format observations as clean bullet points
                new_observation = format_observations(domain_obligations)
                df.at[index, 'Observation'] = new_observation
                updates_made += 1
                print(f"✅ Updated row {index + 2} ({domain}): {len(domain_obligations)} clauses")
        
        # Save the updated framework
        print("Saving updated framework...")
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data Protection Framework 1', index=False)
        
        print(f"🎉 Success! Updated {updates_made} observations in '{output_path}'")
        print("Note: Rows without found obligations are left blank for cleaner look.")
        return True
        
    except PermissionError as e:
        print(f"❌ Permission denied: {e}")
        return False
    except Exception as e:
        print(f"❌ Error mapping to framework: {e}")
        import traceback
        print(f"Full error details: {traceback.format_exc()}")
        return False