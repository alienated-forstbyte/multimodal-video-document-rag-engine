import streamlit as st
from search import search_video
import os
from google import genai
from PIL import Image

GCP_API_KEY=os.environ["GCP_API_KEY"]

st.title("Multimodal Video RAG")
query = st.text_input("Ask a question about the video: ")

client = genai.Client(api_key=GCP_API_KEY)
context_text = ""
video_chunks = []
images = []
if query :
    with st.spinner("searching video and analyzing with gemini"):
        try:        
            video_chunks = search_video(query_text=query, top_k=3)
            images = [Image.open(video_chunk['frame_path']) for video_chunk in video_chunks]
            context_text = "\n".join([f"[{video_chunk['formatted_time']}] : [{video_chunk['text']}]" for video_chunk in video_chunks])

            prompt = f'''
            Answer the question using the provided video transcript and screenshot.
            Always cite the exact timestamp (eg [01:05]) for your answer

            Context:
            {context_text}

            Query:
            {query}'''

            response = client.models.generate_content(
                model = "gemini-3.8-flash",
                contents=[*images,prompt]
            )
            st.subheader("Answer")
            st.markdown(response.text)
            cols = st.columns(len(video_chunks))

            for col, video_chunk in zip(cols, video_chunks):
                with col:
                    st.image(video_chunk["frame_path"], caption=f"Time: {video_chunk['formatted_time']}")
        except Exception as e:
            st.error(e)