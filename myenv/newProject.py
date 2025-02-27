import gradio as gr
import google.generativeai as genai
import os
import PyPDF2
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv

# Memory for file content and type
doc_memory = {"content": "", "type": ""}

def process_file(file):
    """Process uploaded file and store it in memory."""
    if not file:
        return "⚠️ Please upload a file."
    
    file_extension = os.path.splitext(file.name)[1].lower()
    text = ""
    
    try:
        if file_extension == ".pdf":
            with open(file.name, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif file_extension == ".txt":
            with open(file.name, "r", encoding="utf-8") as f:
                text = f.read()
        elif file_extension in [".mp3", ".wav"]:
            recognizer = sr.Recognizer()
            with sr.AudioFile(file.name) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="tr-TR")
        else:
            return "❌ Unsupported file type. Please upload a PDF, TXT, or audio file."
        
        if not text.strip():
            return f"❌ No text could be extracted from the {file_extension.upper()} file."
        
        doc_memory.update({"content": text, "type": file_extension[1:]})
        return f"✅ {file_extension.upper()} processed successfully! You can now ask questions."
    except Exception as e:
        return f"❌ Error processing file: {str(e)}"

def text_to_speech(text):
    """Convert text to speech."""
    try:
        tts = gTTS(text, lang="tr")
        audio_file = "output.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        return f"❌ Error creating audio file: {str(e)}"

# Load environment variables and configure API
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found! Please check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def ask_file_question(user_input):
    """Answer user questions based on file content or general knowledge."""
    try:
        if doc_memory["content"]:
            prompt = (
                f"If the question below relates to the following text, answer based on it. "
                f"Otherwise, respond using general knowledge:\n\n"
                f"{doc_memory['content']}\n\nQuestion: {user_input}"
            )
        else:
            prompt = user_input
        
        response = model.generate_content(prompt)
        
        if not response or not response.text.strip():
            return "❌ No valid response received from the model."
        
        return response.text
    except Exception as e:
        return f"❌ Error occurred: {str(e)}"

# Gradio Interface with updated layout
with gr.Blocks() as interface:
    gr.HTML("""
        <div style='padding: 30px 0; text-align: center;'>
            <h1>💎 File Converter by AI</h1>
            <p>Dive into your files with an AI-powered assistant.</p>
        </div>
    """)
    
    with gr.Row():
        # Left column for file upload and status
        with gr.Column(scale=4):
            file_input = gr.File(label="📂 Upload File", file_types=[".pdf", ".txt", ".mp3", ".wav"])
            file_process_button = gr.Button("📄 Process File")
            file_output = gr.Textbox(label="Status", interactive=False, lines=2)

        # Right column for chat and interaction
        with gr.Column(scale=6):
            chat_history = gr.Chatbot(label="Chat History")
            user_input = gr.Textbox(label="Your Question", placeholder="Ask something about the file...", lines=3)
            with gr.Row():
                submit_button = gr.Button("🚀 Submit")
                clear_button = gr.Button("🗑️ Clear Chat")
                tts_button = gr.Button("🔊 Convert to Speech")
            audio_output = gr.Audio(label="Listen to Response")

    # Event handlers
    file_process_button.click(process_file, inputs=[file_input], outputs=[file_output])
    
    def respond(message, history):
        reply = ask_file_question(message)
        history.append((message, reply))
        return history, ""
    
    submit_button.click(respond, inputs=[user_input, chat_history], outputs=[chat_history, user_input])
    clear_button.click(lambda: [], outputs=[chat_history])
    tts_button.click(text_to_speech, inputs=[user_input], outputs=[audio_output])

if __name__ == "__main__":
    interface.launch()
