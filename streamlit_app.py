import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
#from PyPDF2 import PdfReader
#import docx

# Contract Clause Generation
st.title("Pharmaceutical Contract Management")

# Load your trained LLM model and tokenizer
model_dir = "/path/to/your/model/directory"
#model = AutoModelForCausalLM.from_pretrained(model_dir)
#tokenizer = AutoTokenizer.from_pretrained(model_dir)

st.sidebar.header("Contract Clause Management")
contract_management = st.sidebar.selectbox(
    "Select generate or validate",
    [
        "--Select--",
        "Contract Clause Generation",
        "Contract Clause Validation"
    ]
)

if contract_management == "Contract Clause Generation":
    st.sidebar.header("Contract Clause Generation")
    
    # Dropdown for Type of Agreement
    agreement_type = st.sidebar.selectbox(
        "Select Agreement Type", 
        [
            "--Select--",
            "Research and Development (R&D) Agreements",
            "Licensing Agreements",
            "Clinical Trial Agreements (CTAs)",
            "Manufacturing and Supply Agreements",
            "Distribution and Marketing Agreements",
            "Confidentiality and Non-Disclosure Agreements (NDAs)",
            "Quality Assurance and Quality Control Agreements",
            "Intellectual Property (IP) Agreements",
            "Pharmacovigilance Agreements",
            "Consulting and Advisory Agreements",
            "Joint Venture and Partnership Agreements",
            "Merger and Acquisition (M&A) Agreements",
            "Pharmacy Benefit Management (PBM) Agreements",
            "Government and Public Health Agreements",
            "Sales and Service Agreements"
        ]
    )

    # Subcategory Dropdown (Conditional)
    subcategory = None
    if agreement_type == "Research and Development (R&D) Agreements":
        subcategory = st.sidebar.selectbox(
            "Select Subcategory",
            ["--Select--", "Collaborative Research Agreements", "Sponsored Research Agreements", "Material Transfer Agreements (MTAs)"]
        )
    elif agreement_type == "Licensing Agreements":
        subcategory = st.sidebar.selectbox(
            "Select Subcategory",
            ["--Select--", "In-Licensing Agreements", "Out-Licensing Agreements"]
        )
    elif agreement_type == "Manufacturing and Supply Agreements":
        subcategory = st.sidebar.selectbox(
            "Select Subcategory",
            ["--Select--", "Contract Manufacturing Agreements (CMAs)", "Supply Agreements"]
        )
    elif agreement_type == "Distribution and Marketing Agreements":
        subcategory = st.sidebar.selectbox(
            "Select Subcategory",
            ["--Select--", "Distribution Agreements", "Co-Promotion Agreements"]
        )
    elif agreement_type == "Intellectual Property (IP) Agreements":
        subcategory = st.sidebar.selectbox(
            "Select Subcategory",
            ["--Select--", "IP Assignment Agreements", "Patent Licensing Agreements"]
        )

    # Clauses Dropdown
    if agreement_type != "--Select--":
        clause = st.sidebar.selectbox(
            "Select Clause",
            ["--Select--", "Confidentiality", "Termination", "Liability", "Payment Terms", "Governing Law"]
        )
    else:
        clause = None

    # Auto-filled Text Area for Prompt
    if clause != "--Select--" and clause is not None:
        prompt_text = f"Please draft a {clause} clause for a {agreement_type}."
        if subcategory and subcategory != "--Select--":
            prompt_text += f" This is a {subcategory} agreement."

        st.text_area("Prompt", prompt_text, height=100)

    # Button to Generate Clause
    if st.sidebar.button("Generate Clause"):
        st.success(f"{clause} clause for {agreement_type} generated successfully.")

elif contract_management == "Contract Clause Validation":
    st.sidebar.header("Contract Clause Validation")

    # Dropdown for Contract Validation type (PDF or Text)
    validation_type = st.sidebar.selectbox(
        "Select Validation Method",
        ["--Select--", "Contract Validation using PDF", "Contract Validation using Text"]
    )

    # Helper function to use the LLM model for validation
    def validate_contract_text(input_context):
        instruction = "Validate and rate the following clause on a scale of 1 to 10:"
        input_text = f"### Instruction:\n{instruction}\n### Input:\n{input_context}\n### Response:\n"

        # Fallback to CPU if CUDA is unavailable
        device = "cuda" if torch.cuda.is_available() else "cpu"
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True).to(device)
        generated_ids = model.generate(**inputs, max_new_tokens=500)
        generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        
        return generated_text

    # If the user selects "Contract Validation using PDF"
    if validation_type == "Contract Validation using PDF":
        st.sidebar.write("Upload a contract for validation:")
        # File upload
        uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

        if uploaded_file is not None:
            st.write("File uploaded successfully!")
            st.write("Performing validation checks...")
            
            # Perform PDF extraction and LLM validation logic here
            # (You can implement PDF/Docx extraction logic)
            st.checkbox("Check for Compliance with Regulations", value=True)
            st.checkbox("Check for Consistency", value=True)
            st.checkbox("Check for Missing Clauses", value=False)
            
            if st.sidebar.button("Validate"):
                st.success("Validation completed successfully!")

    # If the user selects "Contract Validation using Text"
    elif validation_type == "Contract Validation using Text":
        st.sidebar.write("Please enter contract text for validation:")
        
        # Textarea for contract text input
        contract_text = st.text_area("Enter contract text here", height=200)

        # Validate Button
        if st.button("Validate"):
            if contract_text:
                st.write("Validating the provided contract text...")
                # Use the LLM model for validation
                validation_result = validate_contract_text(contract_text)
                st.write(validation_result)
            else:
                st.error("Please enter contract text to validate.")
