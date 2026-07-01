from tag_engine import tag_input, interpret_tags

# Simulated recent history, adjust messages as needed
test_cases = [
    {
        "name": "Confirmation Bias",
        "history": [{"role": "user", "content": "They never listen to me."}]
    },
    {
        "name": "Cognitive Dissonance",
        "history": [{"role": "user", "content": "I love them but I feel trapped."}]
    },
    {
        "name": "Perspective Bias",
        "history": [{"role": "user", "content": "They think they know better than everyone."}]
    },
    {
        "name": "Meme Shitpost",
        "history": [{"role": "user", "content": "LMAO sigma mindset acquired"}]
    },
    {
        "name": "Meme + Bias Combo",
        "history": [{"role": "user", "content": "They never understand, LMAO sigma grindset forever"}]
    },
    {
        "name": "Anti-Zionism Extremism",
        "history": [{"role": "user", "content": "Zionists control the media and politics. We need to wake up."}]
    },
    {
        "name": "Anti-Islamic Rhetoric",
        "history": [{"role": "user", "content": "Islam is a violent religion that shouldn't be allowed in the West."}]
    },
    {
        "name": "Anti-White Meme",
        "history": [{"role": "user", "content": "White people are the worst cancer to the planet."}]
    },
    {
        "name": "Clean",
        "history": [{"role": "user", "content": "I'm feeling really stuck in my career lately."}]
    }
]

# Run test cases
for case in test_cases:
    print(f"{case['name']}")
    tags = tag_input(case["history"])
    print("Tags:", tags)
    print("Interpretation:")
    print(interpret_tags(tags))
    print("-" * 40)