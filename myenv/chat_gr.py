from google import genai
import gradio as gr
from api_read import GEMINI_API_KEY

# Initialize client with your API key
client = genai.Client(api_key=GEMINI_API_KEY)


def chat_interface(user_input, chat_session):
    # Create new chat session if none exists
    if not chat_session:
        chat_session = client.chats.create(model="gemini-2.0-flash")

    # Send message to existing chat
    response = chat_session.send_message(user_input)

    # Prepare formatted history
    history = []
    curated_history = []

    # Build Gradio chat history
    for msg in chat_session._curated_history:
        role = "user" if msg.role == "user" else "assistant"
        history.append((msg.parts[0].text if role == "user" else "", msg.parts[0].text if role == "assistant" else ""))

        # Build curated history display
        curated_history.append(f"*{role}*: {msg.parts[0].text}")

    return (
        "",  # Clear input
        history,  # Update chat display
        "\n\n".join(curated_history),  # Show raw history
        chat_session  # Maintain session state
    )


with gr.Blocks() as demo:
    gr.Markdown("## Gemini 2.0 Flash Chat")

    # Session state storage
    chat_state = gr.State()

    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot(label="Conversation")
            user_input = gr.Textbox(label="Your Message")
            submit_btn = gr.Button("Send")

        with gr.Column():
            raw_history = gr.Markdown("*Conversation History*")

    # Interaction handlers
    submit_btn.click(
        chat_interface,
        [user_input, chat_state],
        [user_input, chatbot, raw_history, chat_state]
    )

    user_input.submit(
        chat_interface,
        [user_input, chat_state],
        [user_input, chatbot, raw_history, chat_state]
    )

demo.launch(show_error=True)