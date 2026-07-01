#bias_checks.py
#idontwant a (j*b) 🤮
#if the machine emulates 'soul' well enough, where is the line drawn??   
#m@vile.cx

def tag_bias(msg):
    tags = []
    msg = msg.lower()

        #bias patterns
    if "always" in msg or "never" in msg:
            tags.append("bias:confirmation")
    if "but" in msg and ("feel" in msg or "think" in msg):
            tags.append("bias:dissonance")
    if "they" in msg or "them" in msg:
            tags.append("bias:perspective")
    
    return tags
    
def interpret_bias(tags):
    notes = []

    if "bias:confirmation" in tags:
        notes.append("User may be experiencing confirmation bias. Gently reflect if this belief is absolute or nuanced.")
    if "bias:dissonance" in tags:
        notes.append("Note: Possible emotional-logical tension detected. Invite user to explore the conflict.")
    if "bias:perspective" in tags:
        notes.append("Prompt: Could the user benefit from imagining this situation reversed or from another person's view?")
    return "\n".join(notes) #returns as list to mash w other interpreters