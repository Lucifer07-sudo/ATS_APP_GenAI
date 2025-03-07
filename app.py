from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
    #read pdf as image
        pdf_image = pdf2image.convert_from_bytes(uploaded_file.read())
        #read first page
        first_page = pdf_image[0]

        #create buffer memory
        img_byte_arr = io.BytesIO()

        #store image as jpeg to this memory
        first_page.save(img_byte_arr, format="JPEG")

        #retrive raw byte data
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base 64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file found")

#streamlit app

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
#field for JD
input_text = st.text_area("Job Description: ", key='input')
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Parse resume")
submit3 = st.button("Percentage match")

input_prompt1 = """You are an experienced HR with experience in technologies like Data science, Fullstack web development,
Big Data engineering, DevOps, Data Analyst, Generative AI. Your task is to review the provided resume against the job description for these 
technologies.Please share your professional evaluation on whether the candidate's profile aligns with the role provided in the job description. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 ="""You are an advanced AI-powered resume parser and ATS (Applicant Tracking System) with expertise in analyzing resumes and matching them to job descriptions. Your task is to extract and evaluate key details from a given resume and compare them with a provided job description.

### **Instructions:**
1. **Extract the following details from the resume:**
   - **Candidate's Name**
   - **Mobile Number**
   - **Email Address**
   - **Work Experience** (Company names, job titles, duration, key responsibilities)
   - **Key Projects** (Project names, technologies used, impact)
   - **Technical and Soft Skills** (Programming languages, tools, methodologies, and soft skills)

2. **Evaluate Resume Match:**
   - Compare the extracted skills, experience, and projects with the job description.
   - Identify missing or extra skills.
   - Highlight gaps in experience or domain knowledge.
   - Provide a **percentage match score** (0-100%) based on relevance.
   - Structure the output as follows:

### **Output Format:**
Candidate Details:

Name: [Extracted Name] \n
Mobile: [Extracted Mobile] \n
Email: [Extracted Email]

Work Experience:

[Job Title], [Company Name], [Years of Experience] 
- Key Responsibilities: [Summarized key tasks]
Key Projects:

Project Name: [Project Title]
Description: [Short description]
Technologies Used: [Tech stack]
Skills:

Technical Skills: [List of extracted skills]
Soft Skills: [List of extracted soft skills]
ATS Resume Match Score:

Percentage Match: XX% \n
Missing Keywords: [List of missing key skills or experiences]
Final Thoughts: [Summary of candidate strengths and weaknesses]
Leave blank if any information is not found

"""

input_prompt3 = """You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of technologies like Data science, Fullstack web development,
Big Data engineering, DevOps, Data Analyst, Generative AI and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The response is:")
        st.write(response.candidates[0].content.parts[0].text)
    else:
        st.write("Please upload PDF resume file")

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.subheader("The response is")
        st.write(response.candidates[0].content.parts[0].text)
    else:
        st.write("Please upload PDF resume file")

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The response is:")
        st.write(response.candidates[0].content.parts[0].text)
    else:
        st.write("Please upload PDF resume file")







