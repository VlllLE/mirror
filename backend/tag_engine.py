#tag_engine.py
#the ethical implications of something like this are not lost on me
#i am obligated to continue
#m@vile.cx

from bias_checks import tag_bias, interpret_bias
from meme_checks import tag_meme, interpret_meme
from radical_checks import tag_radical, interpret_radical

def tag_input(history):
    tags = []
    for turn in history[-5:]:
        if turn["role"] != "user":
            continue
        msg = turn["content"].lower()

        tags.extend(tag_bias(msg))
        tags.extend(tag_meme(msg))
        tags.extend(tag_radical(msg))
        #can add more
    return tags

def interpret_tags(tags):
    notes = [
        interpret_bias(tags),
        interpret_meme(tags),
        interpret_radical(tags)
    ]
    return "\n".join(note for note in notes if isinstance(note,str)and note.strip())