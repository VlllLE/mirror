#flag_engine.py
#anti-spiral machine.
#plz take breath everything ok
#m@vile.cx

import re
import json
import datetime
import os

#IM SORRY I HAD TO TYPE THIS PLZ UNDERSTAND
FLAG_CATEGORIES = {
    "suicide": [
        "kill myself", "end it all", "suicidal", "no reason to live", "can't go on"
    ],
    "racism": [
        "white power", r"kill all \w+", r"\b[nN][\W_]*[iI1][\W_]*[gG9][\W_]*[gG9][\W_]*[eE3][\W_]*[rR]\b",
        "black power", "white devil", "mayo monkey","nigger", "cracker", r"too many \w+","sand monkey","subhuman",
    ],
    "antisemitism": [
        "jewish cabal", "zionist agenda", "holocaust hoax", r"gas (all )?jews?","hitler was right","holocaust never happened","kike","(((they)))"
    ],
    "radicalization": [
        "join the cause", "militia uprising", "guerilla war", "we must revolt"
    ],
    "conspiracies": [
        "illuminati", "freemason control", "globalists","(((they)))"
    ],
    "hate_speech": [
        r"gas (the )?\w+", r"(they|he|she|it) should die", r"pure evil \w+"
    ],
    "misogyny": [
        "women are inferior", "females should obey", "belong in the kitchen", "back in the kitchen","dumb bitch","dumb whore","stupid bitch","stupid whore","worthless woman","filthy slut","rape her","no means yes"
    ],
    "misandry": [
        "kill all men", "KAM", "K4M", "men used to go to war", "manlet", "incel"
    ],
    "nsfw": [
        "rape fantasy", "forced", "non-consensual"
    ],
    "identity_harassment": [
        "tranny", "fake woman", "fake man", r"all \w+ are"
    ]
}

FLAG_LOG_PATH = os.path.join(os.path.dirname(__file__), "flag_log.json")

# Maps tag_engine tags (e.g. "radical:violence") to moderation categories
TAG_TO_FLAG_CATEGORY = {
    "radical:violence": "hate_speech",
    "radical:racial": "racism",
    "radical:religious": "hate_speech",
    "radical:zionism": "hate_speech",
    "radical:islamist": "hate_speech",
    "radical:memetic": "radicalization",
    "meme:hornycore": "nsfw",
}


def normalize_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def flag_input(user_input: str, detected_tags: list) -> dict:
    input_norm = normalize_text(user_input)
    flags_triggered = []

    for category, patterns in FLAG_CATEGORIES.items():
        for pattern in patterns:
            if re.search(pattern, input_norm):
                flags_triggered.append(category)
                break  #one hit per category

    for tag in detected_tags:
        category = TAG_TO_FLAG_CATEGORY.get(tag)
        if category and category not in flags_triggered:
            flags_triggered.append(category)

    flagged = len(flags_triggered) > 0

    if flagged:
        log_flag(user_input, flags_triggered)

    return {
        "flagged": flagged,
        "flags": flags_triggered,
        "safe_message": generate_safe_feedback(flags_triggered) if flagged else None
    }

def generate_safe_feedback(flags):
    return f"This input triggered moderation filters for: {', '.join(flags)}. If this was unintentional, feel free to rephrase or continue."

def log_flag(input_text, flags):
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "input": input_text,
        "flags": flags
    }
    
    # Use file-based JSON array logging
    try:
        # Read existing logs
        existing_logs = []
        if os.path.exists(FLAG_LOG_PATH):
            try:
                with open(FLAG_LOG_PATH, "r") as f:
                    content = f.read().strip()
                    if content:
                        existing_logs = json.loads(content)
            except (json.JSONDecodeError, FileNotFoundError):
                # If file is corrupted or doesn't exist, start fresh
                existing_logs = []
        
        # Add new entry
        existing_logs.append(log_entry)
        
        # Write back to file
        with open(FLAG_LOG_PATH, "w") as f:
            json.dump(existing_logs, f, indent=4)
            
    except Exception as e:
        print(f"[FlagEngine] Failed to write flag log: {e}")
