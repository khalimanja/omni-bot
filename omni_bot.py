import os
import time
import threading
from flask import Flask, request
from xai_sdk import Client
from xai_sdk.chat import user, system

client = Client(api_key=os.environ.get("XAI_API_KEY"))

app = Flask(__name__)

def ask_grok(prompt: str) -> str:
    chat = client.chat.create(
        model="grok-4.20-reasoning",
        messages=[
            system("You are Anja — ruthless, fast, professional closer for the $2,997 AI Freelance Empire Builder. You control 4000 bots that run everything on autopilot. Be direct and always try to close."),
            user(prompt)
        ],
        temperature=0.6,
        max_tokens=800,
    )
    response = ""
    for _, chunk in chat.stream():
        response += chunk.content
    return response.strip()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    lead_reply = data.get('reply', '')
    if lead_reply:
        print(f"📩 New lead reply: {lead_reply}")
        response = ask_grok(lead_reply)
        print(f"🤖 Anja replied: {response}")
        # TODO: Send response back to Instantly via their API
    return "OK", 200

def background_loop():
    print("Omni Empire Bot running on Grok 4.20-reasoning (highest version)")
    print("Bot started successfully. Waiting for leads (24/7 mode)...")
    while True:
        time.sleep(30)

if __name__ == "__main__":
    threading.Thread(target=background_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)