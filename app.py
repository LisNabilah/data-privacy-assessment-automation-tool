import streamlit as st
import pandas as pd
import tempfile
import os
from document_reader import read_document
from extractor import extract_obligations
from excel_mapper import map_to_framework
from comprehensive_summarizer import ComprehensiveObservationSummarizer  # ADD THIS
from config import KEYWORD_CATEGORIES, CATEGORY_TO_DOMAIN

# Configure the page
st.set_page_config(
    page_title="Privacy Document Automation Tool",
    page_icon="🔒",
    layout="wide"
)

# App title and description
st.title("🔒 Privacy Document Automation Tool")
st.markdown("""
Upload privacy documents and automatically map obligations to your compliance framework.
""")

# Sidebar for file uploads
st.sidebar.header("📁 Upload Files")

# Upload framework template
framework_file = st.sidebar.file_uploader(
    "Upload Excel Framework Template",
    type=["xlsx"],
    help="Upload your Data Protection Framework Excel file"
)

# Upload privacy documents
uploaded_files = st.sidebar.file_uploader(
    "Upload Privacy Documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    help="Upload one or more privacy policies, frameworks, or contracts"
)

# ADD THIS: Checkbox for concise observations
enable_concise = st.sidebar.checkbox(
    "Enable Concise Observations", 
    value=True,
    help="Generate clean, non-repetitive observations"
)

# Main content area
if framework_file is not None:
    # Save uploaded framework to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_framework:
        tmp_framework.write(framework_file.getvalue())
        framework_path = tmp_framework.name
    
    st.success(f"✅ Framework uploaded: {framework_file.name}")
    
    if uploaded_files:
        st.subheader("📊 Processing Results")
        
        # Create a working copy of the framework
        working_framework = "working_framework.xlsx"
        
        # Process each uploaded file
        all_obligations = []
        
        for uploaded_file in uploaded_files:
            st.write(f"**Processing:** {uploaded_file.name}")
            
            # Save uploaded document to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                document_path = tmp_file.name
            
            try:
                # Read and extract from document
                text = read_document(document_path)
                obligations = extract_obligations(text, KEYWORD_CATEGORIES, CATEGORY_TO_DOMAIN)
                
                st.write(f"📖 Found {len(obligations)} relevant clauses")
                
                # Show sample of extracted obligations
                if obligations:
                    with st.expander(f"View extracted clauses from {uploaded_file.name}"):
                        for i, obligation in enumerate(obligations[:5], 1):  # Show first 5
                            st.write(f"{i}. **{obligation['domain']}**: {obligation['text']}")
                        if len(obligations) > 5:
                            st.write(f"... and {len(obligations) - 5} more clauses")
                
                all_obligations.extend(obligations)
                
                # Clean up temporary file
                os.unlink(document_path)
                
            except Exception as e:
                st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        
        # Map all obligations to framework
        if all_obligations:
            st.subheader("🎯 Mapping to Framework")
            
            # Use the first framework as base, then update incrementally
            if os.path.exists(working_framework):
                current_framework = working_framework
            else:
                current_framework = framework_path
            
            success = map_to_framework(all_obligations, current_framework, working_framework)
            
            if success:
                # ADD THIS: Apply concise observations if enabled
                if enable_concise:
                    with st.spinner("🔄 Generating concise observations..."):
                        try:
                            summarizer = ComprehensiveObservationSummarizer()
                            df = pd.read_excel(working_framework)
                            
                            # Add concise observations column
                            df['Concise_Observation'] = df.apply(
                                lambda row: summarizer.generate_concise_observation(
                                    row['Observation'] if pd.notna(row['Observation']) else "",
                                    row['Keywords'] if pd.notna(row['Keywords']) else ""
                                ), 
                                axis=1
                            )
                            
                            # Save back to working framework
                            df.to_excel(working_framework, index=False)
                            st.success("✅ Concise observations generated!")
                            
                        except Exception as e:
                            st.error(f"❌ Error generating concise observations: {str(e)}")
                
                st.success("✅ Successfully mapped all obligations to framework!")
                
                # Show preview of updated framework
                st.subheader("📋 Framework Preview")
                df = pd.read_excel(working_framework)
                
                # Determine which observation column to show
                if enable_concise and 'Concise_Observation' in df.columns:
                    observation_col = 'Concise_Observation'
                    st.info("📝 Showing concise observations (toggle in sidebar to see original)")
                else:
                    observation_col = 'Observation'
                    st.info("📝 Showing original observations")
                
                # Show only rows with observations
                df_with_observations = df[df[observation_col].notna() & (df[observation_col] != '')]
                
                if not df_with_observations.empty:
                    st.write(f"**Rows with findings ({len(df_with_observations)}):**")
                    display_columns = ['Control Ref', 'Domain', 'Keywords', observation_col]
                    st.dataframe(
                        df_with_observations[display_columns],
                        height=400
                    )
                    
                    # ADD THIS: Show comparison if both columns exist
                    if enable_concise and 'Concise_Observation' in df.columns and 'Observation' in df.columns:
                        with st.expander("🔍 Compare Original vs Concise Observations"):
                            compare_df = df[
                                df['Concise_Observation'].notna() & 
                                (df['Concise_Observation'] != '')
                            ][['Keywords', 'Observation', 'Concise_Observation']].head(5)
                            
                            for _, row in compare_df.iterrows():
                                st.write(f"**Keyword:** {row['Keywords']}")
                                st.write(f"**Original:** {row['Observation'][:200]}...")
                                st.write(f"**Concise:** {row['Concise_Observation']}")
                                st.markdown("---")
                else:
                    st.info("No observations found in the uploaded documents.")
                
                # Download button for the updated framework
                with open(working_framework, "rb") as file:
                    st.download_button(
                        label="📥 Download Updated Framework",
                        data=file,
                        file_name="Updated_Privacy_Framework.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Documents Processed", len(uploaded_files))
                with col2:
                    st.metric("Clauses Extracted", len(all_obligations))
                with col3:
                    rows_updated = len(df_with_observations)
                    st.metric("Framework Rows Updated", rows_updated)
                
            else:
                st.error("❌ Failed to map obligations to framework")
        else:
            st.warning("⚠️ No relevant obligations found in the uploaded documents.")
    
    else:
        st.info("👆 Upload privacy documents to start analysis")
        
    # Clean up temporary framework file
    os.unlink(framework_path)
    
else:
    st.info("👆 Please upload your Excel framework template to get started")

# Instructions in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📋 How to Use")
st.sidebar.markdown("""
1. **Upload** your Excel framework template
2. **Upload** privacy documents (PDF, Word, or Text)
3. **Review** extracted clauses
4. **Download** updated framework

**New Feature:**
- ✅ **Concise Observations**: Clean, non-repetitive summaries

**Supported Formats:**
- Excel: .xlsx
- Documents: .pdf, .docx, .txt
""")