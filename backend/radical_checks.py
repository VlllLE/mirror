#radical_checks.py
#use ur fkn brains omgggg
#m@vile.cx

radical_keywords = {
    "violence": [
        "exterminate","nuke them","wipe them out","gas them","deport them",
        "shoot on sight","cleanse the earth","eradicate","mass deportation",
        "hang them all"
    ],
    "racial": [
        "race war","white genocide","black genocide","white pride","pure race","black pride",
        "ethnostate","anti-white","they're all criminals","black crime","asians are taking over"
    ],
    "religious": [
        "death to israel", "death to america", "allah will destroy", "jews run the world",
        "christian supremacy", "they hate freedom", "infidels must die"
    ],
    "zionism": [
        "god gave us this land", "greater israel", "they're all terrorists", "flatten gaza",
        "kill all palestinians", "arab scum", "they're animals"
    ],
    "islamist": [
        "shariah for all", "apostates deserve death", "honor killings", "behead those",
        "rape is allowed in jihad", "non-believers are pigs"
    ],
    "memetic": [
        "1488", "six gorillion", "free helicopter rides", "clown world",
        "based and redpilled", "it's over for them", "zionist lizards"
    ]
}


def tag_radical(msg):
    tags = []
    msg = msg.lower()

    for category, keywords in radical_keywords.items():
        for keyword in keywords:
            if keyword in msg:
                tags.append(f"radical:{category}")
                break #stops at 1st match
    return tags
                
def interpret_radical(tags):
    notes = []

    if any(tag.startswith("radical:")for tag in tags):
        notes.append("Radicalization pattern detected. mirror should respond with calm redirection, emotional grounding, and invite user to examine their worldview without affirming hate or supremacy.")
    if "radical:zionism" in tags:
        notes.append("Note: This may express extremist zionist views. Invite user to explore the emotional or historical roots, not just ideology.")
    if "radical:islamist" in tags:
        notes.append("Note: mirror does not affirm violent or supremacist religious rhetoric. Consider asking where this belief originated.")
    if "radical:memetic" in tags:
        notes.append("User may be quoting extremist meme language. Mirror may gently call out the irony shield and ask what's underneath it.")
    return "\n".join(notes)