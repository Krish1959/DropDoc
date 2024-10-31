import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📄 BCA Submission Qns")

# Create two columns
col1, col2 = st.columns([1, 1])

# Place each checkbox in a separate column
with col1:
    show_popup1 = st.checkbox("API Key")
with col2:
    show_popup2 = st.checkbox("About")


#show_popup1 = st.checkbox("API Key")
#show_popup2 = st.checkbox("About Project")
# Display "popup" content
if show_popup1:
    st.code("Open AI API_Key is Set already", language="text")
# Display "popup" content
if show_popup2:
    st.code("This is the APP Developed\nas part of the GovTech\nAI Bootcamp by:\nUnni & Woon Wei (BCA)", language="text")

    
st.write("Upload a document below and ask a question about it– GPT will answer! ")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
#openai_api_key = st.text_input("OpenAI API Key", type="password")
openai_api_key = st.secrets["openai"]["secret_key"]

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
