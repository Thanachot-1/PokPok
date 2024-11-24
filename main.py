from openai import OpenAI
import gradio as gr
import threading
import pygame
import re

# OpenAI client setup
client = OpenAI(
    api_key="sk-XIVuRjLd6iCGp6lHy45jTaDLQtFICMnGapsxtyvwHMgMa9AK",
    base_url="https://api.opentyphoon.ai/v1",
)

# Function to generate humorous IQ responses
def generate_llm(user_answer):
    stream = client.chat.completions.create(
        model="typhoon-v1.5-instruct",
        messages=[
            {
                "role": "user",
                "content": f"""
                คุณคือไก่ และจะตอบทุกสิ่งด้วยคำว่า ป๊อก ซึ่งสามารถเปลี่ยนแปลงความยาวของประโยคได้ อาจะะเป็น ป๊อก ป๊อก ป๊อก หรือยาวกว่านี้ ขึ้นอยู่กับความยาวของข้อความที่ได้รับมา และห้ามมีคำอื่นนอกจาก ป๊อก เด็ดขาด
                คนพูดว่า: {user_answer}""",
            },
        ],
        max_tokens=512,
        temperature=0.8,
        top_p=0.95,
        stream=True,
    )

    respond = []
    for chunk in stream:
        if hasattr(chunk, "choices") and len(chunk.choices) > 0:
            choice = chunk.choices[0]
            if hasattr(choice, "delta") and hasattr(choice.delta, "content"):
                if choice.delta.content is not None:
                    respond.append(choice.delta.content)
    return "".join(respond)

# Function to play the pokpok.mp3 sound based on the count of "ป๊อก"
def play_pokpok_sound(count):
    def play_sound():
        pygame.mixer.init()
        for _ in range(count):
            pygame.mixer.music.load("Chicken_hurt1.oga")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

    threading.Thread(target=play_sound, daemon=True).start()

# Function to handle user submission
def handle_submission(user_answer):
    evaluation = generate_llm(user_answer)
    # Count occurrences of "ป๊อก"
    pok_count = len(re.findall("ป๊อก", evaluation))
    # Play the sound
    if pok_count > 0:
        play_pokpok_sound(pok_count)
    return evaluation

# Gradio UI setup
with gr.Blocks() as demo:
    gr.Markdown("#กินไก่บาปนะ แผ่เมตตาด้วย pokpokpokpokpokpokpokpokpokpokpokpokpokpokpokpokpokpokpokpokpok")
    question_display = gr.Textbox(label="pok", interactive=False, value="pokpokpokpokpokpokpokpokpokpokpokpokpokpokpokpokpokpokpok")
    answer_input = gr.Textbox(label="คุยกับไก่ที่นี่", placeholder="คุณต้องการสื่อสารอะไรกับไก่")
    submit_button = gr.Button("ส่งคำตอบ")

    submit_button.click(
        handle_submission,
        inputs=[answer_input],
        outputs=[question_display]  # Use question_display as the output
    )

demo.launch(share=True)
