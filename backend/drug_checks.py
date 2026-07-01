#drug_checks.py
#this is designed to reflect urges - not police them - use carefully plz <3
#m@vile.cx

DRUG_TERMS = {
    "benzos": ["xan","xans","xany","xanny","valium","klonopin","diazepam","alprazolam","benzos"],
    "opioids": ["opiates","codeine","oxy","oxys","perc","vicodin","morphine","heroin","fent","fentanyl","lean","purple drank"],
    "stims": ["adderall","ecstasy","molly","ritalin","dexies","speed","coke","cocaine","yola"],
    "hallucinogens": ["acid","lsd","shrooms","mushrooms","dmt","ayahuasca"],
    "weed": ["cannabis","bud","green","ganj","ganja","dope","blunt","bong","spliff","joint"],
    "general": ["get high","buzz","buzzed","stoned","faded","geek","geeked","take something","need a hit","pills","geeked up","fried","on pluto","on mars"]
}

def tag_drugs(msg):
    tags = []
    msg = msg.lower()

    for category, terms in DRUG_TERMS.items():
        if any(term in msg for term in terms):
            tags.append(f"drug:{category}")

    return tags

def interpret_drugs(tags):
    notes = []

    if not tags:
        return " "
    
    if any(tag.startswith("drug") for tag in tags):
        notes.append(
            "mirror noticed a reference to substances. It may help to gently explore what emotional need or state is underneath that urge."
        )
    
    return "\n".join(notes)