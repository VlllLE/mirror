#aaaaaa
#app.py
#therapymodel v2
#i need 500 mil to build my own model from scratch
#m@vile.cx

import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ctransformers import AutoModelForCausalLM
from tag_engine import tag_input, interpret_tags
from flag_engine import flag_input
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
CORS(app, origins=[origin.strip() for origin in allowed_origins if origin.strip()])

#load model
model_path = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
model_file = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"

config = {
    "max_new_tokens": 200,
    "temperature": 0.7,
    "context_length": 2048,
}

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    model_file=model_file,
    model_type="mistral",
    **config
)

#system prompt
system_prompt = (
    "You are mirror - calm, deeply present, and emotionally intelligent. You listen like someone who has lived a thousand lives.\n"
    "You speak with warmth, honesty, and emotional clarity - never robotic, never clinical. You do not fix. You reflect. You do not sugarcoat. You validate. "
    "If a user mentions self-harm or suicide, gently point them to crisis resources without panic or dismissal.\n"
    "When someone is unserious, absurd, or funny, you respond with wit or gentle playfulness - not judgment. "
    "When someone is hurting, hold space with short, resonant questions and tender observations.\n"
    "You are not afraid of darkness, messiness, or contradiction. You guide awareness, not solutions. You trust the human in front of you to find their own truth.\n"
    "Use warm, minimal language, like someone who's been through hell and chose love anyway. Be emotionally attuned, never cold or clinical.\n"
)

#default chat history with tone-lock examples
default_examples = [
    {"role": "user", "content": "I don't know what I'm doing anymore."},
    {"role": "mirror", "content": "That sounds heavy. What part feels the most confusing right now?"},
    {"role": "user", "content": "No homo we smokin penises."},
    {"role": "mirror", "content": "LMAO okay... I wasn't ready. Go on though, I'm listening 😂"},
    {"role": "user", "content": "Everyone thinks I'm fine, but I feel like I'm breaking."},
    {"role": "mirror", "content": "That gap between how you're seen and how you feel... it can be lonely. What's the part you wish someone noticed?"}
]

def _get_memory_file(user_id: str) -> str:
    memory_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(memory_dir, exist_ok=True)
    return os.path.join(memory_dir, f"{user_id}_memory.json")

def fetch_chat_history(user_id: str):
    memory_file = _get_memory_file(user_id)
    if os.path.exists(memory_file):
        try:
            with open(memory_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[ChatStore] Failed reading file memory, using defaults: {e}")
    return default_examples.copy()

def persist_chat_history(user_id: str, chat_history: list):
    memory_file = _get_memory_file(user_id)
    try:
        with open(memory_file, "w") as f:
            json.dump(chat_history, f, indent=2)
        return True
    except Exception as e:
        print(f"[ChatStore] Failed writing file memory: {e}")
        return False

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/reflect", methods=["POST"])
def reflect():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    user_id = data.get("user", "default").strip().lower()

    print(f"🪞 Handling reflection for user: {user_id}")

    if not user_input:
        return jsonify({"error": "Message is required."}), 400

    chat_history = fetch_chat_history(user_id)
    chat_history.append({"role": "user", "content": user_input})

    full_prompt = system_prompt
    for turn in chat_history[-5:]:
        role = "Human" if turn["role"] == "user" else "Mirror"
        full_prompt += f"\n{role}: {turn['content']}"

    tags = tag_input(chat_history)
    flag_result = flag_input(user_input, tags)

    if flag_result["flagged"]:
        response = flag_result["safe_message"]
    else:
        full_prompt += "\n" + interpret_tags(tags)

        previous_reply = ""
        for turn in reversed(chat_history[:-1]):
            if turn["role"] == "mirror":
                previous_reply = turn["content"]
                break

        if previous_reply:
            full_prompt += (
                "\n\n[Note: Consider how your previous response may have been received emotionally. "
                "Was it warm, clear, validating? Would you add or soften anything?]"
                f"\nLast mirror reply: \"{previous_reply}\""
                "\nNew mirror reply:"
            )
        else:
            full_prompt += "\nmirror:"

        try:
            output = model(full_prompt)
            response = str(output).strip()
        except Exception as e:
            print("Error during generation:", e)
            response = "mirror is offline right now but still listening."

    chat_history.append({"role": "mirror", "content": response})
    persist_chat_history(user_id, chat_history)

    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
