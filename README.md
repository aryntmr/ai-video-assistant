# Video-based AI Assistant

## Overview
This project is a Streamlit-based AI-powered video assistant that processes user-uploaded videos to extract audio and frames, transcribe speech, and provide AI-generated responses. The assistant can also suggest product purchase links based on user queries.

## Features
- Upload video files and process them in a to-and-fro manner.
- Extract audio and images from the video.
- Transcribe audio to text using OpenAI Whisper.
- Generate responses based on video content using GPT models.
- Provide product recommendations if requested.
- Convert AI responses into speech for playback.

## Technologies Used
- **Python** (Core language)
- **Streamlit** (Web application framework)
- **OpenAI API** (Whisper for speech-to-text and GPT for response generation)
- **MoviePy** (Video processing)
- **PIL (Pillow)** (Image processing)
- **Pygame** (Audio playback)
- **DuckDuckGo Search API** (Product search functionality)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/video-ai-assistant.git
   cd video-ai-assistant
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variable by creating a `.env` file and adding your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Upload a video file through the web interface.

3. The application will:
   - Extract audio and frames.
   - Transcribe speech to text.
   - Analyze the content and provide a response.
   - Convert the response into speech.

4. If the user expresses interest in purchasing a product, the assistant will return URLs of top online stores.

## Project Structure
```
.
├── streamlit_app.py      # Main application script
├── requirements.txt     # Dependencies
└── README.md             # Project documentation
```
