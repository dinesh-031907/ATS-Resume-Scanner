from dotenv import load_dotenv
import os
import base64
import io
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ Google API Key not found. Please add it to your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Function to get Gemini response
def get_gemini_response(input_text, pdf_content, prompt):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        
        # New, simplified way to pass content to the model
        response = model.generate_content([input_text, pdf_content[0], prompt])
        
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Convert uploaded PDF to first page image in base64
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # The API expects content directly, not a base64 encoded string.
        # This function should be modified to return the image data as a dictionary.
        pdf_part = {
            "mime_type": "image/jpeg",
            "data": img_byte_arr
        }
        return [pdf_part]
    else:
        return None

# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("📄 ATS Tracking System")

input_text = st.text_area("💼 Job Description:", key="input")
uploaded_file = st.file_uploader("📤 Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF Uploaded Successfully")

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager(Dont include any dates). Review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
But provide the response in a concise manner, focusing on key points as if you were writing long bullet points.
"""

input_prompt2 = """
You are an experienced Technical Human Resource Manager(Dont include any dates). Review the provided resume against the job description. 
Provide suggestions on how the candidate can improve their skills and qualifications to better align with the job requirements.
Output a detailed list of skills that are missing or need improvement for this specific job, with justifications for each.
Also include a detailed explanation of areas to improve, including technical and soft skills, with actionable suggestions.
But provide the response in a concise manner, focusing on key points as if you were writing long bullet points.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with expertise in data science and ATS functionality.
Evaluate the resume against the provided job description.
First, output the match percentage, then list missing keywords, and finally provide your overall thoughts.
But provide the response in a concise manner, focusing on key points as if you were writing long bullet points.
"""

# Button handling
if st.button("📋 Tell Me About the Resume"):
    if uploaded_file and input_text.strip():
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("📝 Response")
        st.write(response)
    else:
        st.warning("⚠️ Please upload a resume and enter a job description.")

elif st.button("🛠 How Can I Improve My Skills"):
    if uploaded_file and input_text.strip():
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.subheader("📝 Response")
        st.write(response)
    else:
        st.warning("⚠️ Please upload a resume and enter a job description.")

elif st.button("📊 Percentage Match"):
    if uploaded_file and input_text.strip():
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("📝 Response")
        st.write(response)
    else:
        st.warning("⚠️ Please upload a resume and enter a job description.")








# from dotenv import load_dotenv

# load_dotenv()
# import base64
# import streamlit as st
# import os
# import io
# from PIL import Image 
# import pdf2image
# import google.generativeai as genai

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input,pdf_cotent,prompt):
#     model = genai.GenerativeModel("gemini-2.5-pro")
#     response=model.generate_content([input,pdf_content[0],prompt])
#     return response.text

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None:
#         ## Convert the PDF to image
#         images=pdf2image.convert_from_bytes(uploaded_file.read())

#         first_page=images[0]

#         # Convert to bytes
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_parts = [
#             {
#                 "mime_type": "image/jpeg",
#                 "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
#             }
#         ]
#         return pdf_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# ## Streamlit App

# st.set_page_config(page_title="ATS Resume EXpert")
# st.header("ATS Tracking System")
# input_text=st.text_area("Job Description: ",key="input")
# uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


# if uploaded_file is not None:
#     st.write("PDF Uploaded Successfully")


# submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("How Can I Improvise my Skills")

# submit3 = st.button("Percentage match")

# input_prompt1 = """
#  You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
#   Please share your professional evaluation on whether the candidate's profile aligns with the role. 
#  Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# """

# input_prompt2 = """
# You are an experienced Technical Human Resource Manager. Review the provided resume against the job description. 
# Provide suggestions on how the candidate can improve their skills and qualifications to better align with the job requirements.
# Output a detailed list of skills that are missing or need improvement for this specific job, with justifications for each.
# Also provide a detailed explanation of areas to improve, including technical and soft skills, with actionable suggestions.
# """

# input_prompt3 = """
# You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
# your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
# the job description. First the output should come as percentage and then keywords missing and last final thoughts.
# """

# if submit1:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt1,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")

# elif submit2:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt2,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")

# elif submit3:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt3,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")
