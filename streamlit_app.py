import streamlit as st
from moviepy import VideoFileClip
import openai
import os
from dotenv import load_dotenv
import base64
from phi.agent import Agent, RunResponse
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from PIL import Image
from io import BytesIO
import tempfile
import pygame

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to extract audio from video
def extract_audio(video_path):
    video = VideoFileClip(video_path)
    audio_path = tempfile.mktemp(suffix=".mp3")
    video.audio.write_audiofile(audio_path, codec='mp3')
    return audio_path

# Function to transcribe speech to text
def speech_to_text(audio_path):
    with open(audio_path, "rb") as audio:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            language="en"
        )
    return response.text

# Function to extract frames from the video
def extract_images(video_path, interval=2):
    video = VideoFileClip(video_path)
    duration = video.duration
    frames = []
    for t in range(0, int(duration), interval):
        frame = video.get_frame(t)
        frames.append(frame)
    return frames

# Function to encode images to base64
def encode_images_to_base64(frames):
    encoded_images = []
    for frame in frames:
        img = Image.fromarray(frame)
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        encoded_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
        encoded_images.append(f"data:image/jpeg;base64,{encoded_string}")
    return encoded_images

# Function to convert text to speech
def text_to_speech(text):
    response = openai.audio.speech.create(
        model="tts-1",
        input=text,
        voice="alloy"
    )
    temp_audio_path = tempfile.mktemp(suffix=".mp3")
    with open(temp_audio_path, "wb") as audio_file:
        audio_file.write(response.content)
    
    return temp_audio_path  # Return the path to the generated audio file

# Streamlit UI
st.title("Video-based AI Assistant")
st.write("Upload a video and receive AI-powered responses.")

# File uploader for video input
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    with st.spinner("Processing video..."):
        # Save uploaded video to a temporary location
        temp_video_path = tempfile.mktemp(suffix=".mp4")
        with open(temp_video_path, "wb") as f:
            f.write(uploaded_file.read())

        # Extract audio and transcribe to text
        audio_path = extract_audio(temp_video_path)
        user_text = speech_to_text(audio_path)

        # Extract and encode images
        images = extract_images(temp_video_path)
        encoded_images = encode_images_to_base64(images)

        # Initialize the AI agent
        agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            tools=[DuckDuckGo()],
            description="You are a video assistant.",
            instructions=[
                "Address the user with their name, if they give it. Greet them.",
                "If the user mentions buying a product, respond with 4 URLs to buy the product.",
                "Search for 10 websites to buy that item and select the top 4 unique websites.",
                "Otherwise, just give the description of the product."
            ],
            markdown=True,
        )

        # Get response from the AI assistant
        response: RunResponse = agent.run(
            message=user_text,
            images=encoded_images,
            stream=False
        )

        # Display response in the UI
        st.subheader("AI Response")
        st.write(response.content)

        # Play audio response
        audio_path = text_to_speech(response.content)
        st.audio(audio_path, format="audio/mp3")
        # After getting the AI response
        
        #text_to_speech(response.content)

        # Provide option for another input (to-and-fro interaction)
        st.success("Upload another video for further interaction.")
