import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# API anahtarı kontrolü
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY bulunamadı! Lütfen .env dosyanı kontrol et.")

# Gemini API'yi yapılandır
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def chat_with_ai(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

# Gradio Arayüzü
with gr.Blocks(theme=gr.themes.Default()) as interface:
    gr.Markdown("<h1 style='text-align: center; color: #4CAF50;'>💬 Gemini AI Chatbot</h1>")
    gr.Markdown("<p style='text-align: center;'>Google Gemini API ile geliştirilmiş gelişmiş sohbet arayüzü.</p>")

    with gr.Row():
        with gr.Column(scale=4):
            chat_history = gr.Chatbot(label="Sohbet Geçmişi", height=400)
        with gr.Column(scale=1):
            clear_button = gr.Button("🗑️ Temizle")

    user_input = gr.Textbox(
        label="Mesajınızı girin",
        placeholder="Merhaba, sana bir soru sorabilir miyim?",
        lines=2,
        interactive=True
    )
    
    submit_button = gr.Button("🚀 Gönder")

    def respond(message, history):
        reply = chat_with_ai(message)
        history.append((message, reply))
        return history, ""

    submit_button.click(respond, inputs=[user_input, chat_history], outputs=[chat_history, user_input])
    clear_button.click(lambda: [], outputs=[chat_history])

# Çalıştırma
if __name__ == "__main__":
    interface.launch()
