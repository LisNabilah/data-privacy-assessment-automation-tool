# observation_summarizer.py
import pandas as pd
from comprehensive_summarizer import ComprehensiveObservationSummarizer  # The code I provided earlier

def summarize_observations(input_file, output_file):
    """
    Process your Excel/CSV file to add concise observations
    """
    # Read your data
    df = pd.read_excel(input_file)  # or pd.read_csv(input_file)
    
    # Initialize summarizer
    summarizer = ComprehensiveObservationSummarizer()
    
    # Add concise observations
    df['Concise_Observation'] = df.apply(
        lambda row: summarizer.generate_concise_observation(
            row['Observation'], 
            row['Keywords']
        ), 
        axis=1
    )
    
    # Save results
    df.to_excel(output_file, index=False)
    print(f"Processing complete! Output saved to {output_file}")

# Run it
if __name__ == "__main__":
    summarize_observations('your_input_file.xlsx', 'output_with_summaries.xlsx')