# flag_cli.py
from flag_engine import flag_input

print(flag_input("gas all jews",[]))

print("🧪 Mirror Flag Tester (CLI mode)\nType a message to test moderation. Type 'exit' to quit.\n")

while True:
    user_input = input("🧍 You: ").strip()
    if user_input.lower() == "exit":
        break

    # Simulate empty tags for now
    result = flag_input(user_input, detected_tags=[])

    if result["flagged"]:
        print(f"🚨 Flagged: {', '.join(result['flags'])}")
        print(f"🧠 Mirror: {result['safe_message']}\n")
    else:
        print("✅ No flags triggered.\n")

print("CLI loaded.")

if __name__ == "__main__":
    while True:
        text = input(">> ")
        result = flag_input(text, [])
        print(result)