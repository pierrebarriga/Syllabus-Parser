import streamlit as st
import pdfplumber
import json
from google import genai
from google.genai import types  
from pydantic import BaseModel
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# --- FRONTEND SETUP ---
st.set_page_config(page_title="Syllabus Parser", page_icon="📅", layout="wide")

st.title("Extract Assignment Dates from Your Syllabus")

# --- AUTHENTICATION SECTION (Moved from Sidebar) ---
st.header("Step 1: Upload your API Key")

col1, col2 = st.columns([2, 1])

with col1:
    user_api_key = st.text_input(
        "Enter Gemini API Key", 
        type="password", 
        help="Get a free key from Google AI Studio!"
    )

with col2:
    st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)    
    if user_api_key:
        st.success("API Key detected!")
    else:
        st.info("Key required to activate parser.")

st.divider() 

st.header("Step 2: Upload your Course's Syllabus")

# MAIN INTERFACE WORKFLOW 
uploaded_file = st.file_uploader("Upload your Course's PDF Syllabus Here!", type=["pdf"])

# DATA STRUCTURE SPECIFICATION
class DeadlineItem(BaseModel): 
    course_name: str
    task_title: str
    due_date: str          
    weight_percentage: float | None = None 

class SyllabusData(BaseModel):
    assignments: list[DeadlineItem]

# CORE PRODUCT LOGIC FUNCTION
def extract_text_from_pdf(pdf_file):
    output = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for t in tables:
                for row in t:
                    output.append(" | ".join([str(c).replace('\n', ' ') for c in row if c]))
            
            # Then get all text (including the messy table text)
            output.append(page.extract_text() or "")
            
    return "\n".join(output)    
    
def parse_syllabus_with_ai(cleaned_text, api_key):
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an agent helping graduate students stay organized. Analyze the following syllabus text. 
    Extract all readings, assignments, quizzes, exams, projects, and deadlines.
    
    INSTRUCTIONS:
    1. Standardize all due dates to the format YYYY-MM-DD. Use MM-DD if the year is not given. 
    2. Extract the grade weight as a number out of 100. Leave Null if not available. 
    3. If a specific date isn't clear but a week is mentioned, estimate it or leave it blank.
    
    Syllabus Text:
    {cleaned_text}
    """
    
    response = client.models.generate_content(
        model='gemini-3-flash-preview', #Alternatively - Replace with LLM of Choice
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SyllabusData,
            temperature=0.1 
        ),
    )
    return response.text

if uploaded_file is not None:
    if not user_api_key:
        st.error("Action Required: Please enter your Gemini API Key in the sidebar.")
    else:
        with st.spinner("Step 1: Extracting text from PDF..."):
            cleaned_text = extract_text_from_pdf(uploaded_file)
            st.info(f"Successfully extracted {len(cleaned_text)} characters.")
            
        with st.spinner("Step 2: AI is analyzing structure..."):
            try:
                json_raw_output = parse_syllabus_with_ai(cleaned_text, user_api_key)
                parsed_json = json.loads(json_raw_output)
                
                st.success("Parsing complete! 🎉")
                st.subheader("Your Upcoming Assignments 📅")
                st.dataframe(parsed_json['assignments'], use_container_width=True)
                
            except Exception as e:
                st.error(f"Error details: {e}")