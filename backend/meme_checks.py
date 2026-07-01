#meme_checks.py
#deadass had to type this shit
#m@vile.cx

MEME_KEYWORDS = [
    "lmao","lmfao","sigma","ligma","based","cringe","irl","cope","felt","💀","😭","✨","grindset","lol fr","kill me","i'm fine","🧍","🔫","gaslight","goblin","jpeg","vibes",
    "therapy","npc","deadass","ratio"
]

def tag_meme(msg):
    tags = []
    msg = msg.lower()

    if any(keyword in msg for keyword in MEME_KEYWORDS):
            tags.append("meme:shitpost")
    if "kill me" in msg or "i'm fine" in msg:
            tags.append("meme:ironic_crisis")
    if any(word in msg for word in ["gyatt","grip","grippy","goon","gooner","gooning","milkers","breed","daddy chill"]):
            tags.append("meme:hornycore")
    if any(word in msg for word in ["bro thinks","rizz","npc","main character"]):
            tags.append("meme:genz_meta")
    return tags
       
def interpret_meme(tags):
    notes = []

    if "meme:shitpost" in tags:
        notes.append("mirror may gently match the user's humour tone or offer playful reflection.")
    if "meme:ironic_crisis" in tags:
        notes.append("Possible dark humour or ironic expression of distress. mirror may respond with warmth and check-in subtly.")
    if "meme:hornycore" in tags:
        notes.append("mirror should gently acknowledge the user's sexual tone without feeding into it. If appropriate, steer back toward emotional context or consent language.")
    if "meme:genz_meta" in tags:
        notes.append("mirror may gently match the user's humour tone or offer playful reflection.")
    return "\n".join(notes)



