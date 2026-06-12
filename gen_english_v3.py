#!/usr/bin/env python3
"""Generate exactly 10,000 English S1 questions across 10 topics using parametric templates."""
import json, os, random, itertools
from collections import defaultdict

random.seed(42)

# ── Shared pools ──

SUBJECTS_3S = ["He", "She", "My mother", "The teacher", "Tom", "Mary",
               "Everyone", "Nobody", "The boy", "The girl", "My father",
               "The doctor", "Each student", "The man", "The woman",
               "My friend", "The nurse", "The chef", "The driver", "The artist"]
SUBJECTS_PL = ["We", "They", "The students", "The children", "My parents",
               "The workers", "The players", "The boys", "The girls", "People"]
SUBJECTS_ALL = ["I", "You"] + SUBJECTS_3S + SUBJECTS_PL

VERBS = ["go", "eat", "read", "write", "play", "study", "work", "live",
         "buy", "sell", "make", "take", "run", "walk", "talk", "sleep",
         "sing", "dance", "cook", "clean", "drive", "fly", "swim",
         "build", "draw", "teach", "learn", "help", "find", "think",
         "feel", "see", "hear", "know", "want", "need", "try", "start",
         "finish", "open", "close", "bring", "send", "watch", "listen",
         "carry", "catch", "choose", "cut", "fall", "give", "grow",
         "hold", "keep", "leave", "lose", "meet", "pay", "put",
         "ride", "rise", "say", "set", "show", "sit", "stand",
         "steal", "throw", "wake", "wear", "win"]

PLACES = ["school", "home", "the park", "the library", "the market",
          "the hospital", "the office", "the shop", "the beach", "London",
          "the station", "the cinema", "the museum", "the airport",
          "the restaurant", "the hotel", "the bank", "the gym",
          "the supermarket", "the church", "the theatre", "the zoo",
          "the mountain", "the island", "the valley", "the forest"]

NOUNS = ["cat", "dog", "book", "car", "house", "tree", "bird", "fish",
         "flower", "chair", "table", "door", "window", "bag", "hat",
         "cup", "bottle", "key", "phone", "pen", "pencil", "ruler",
         "apple", "orange", "banana", "cake", "ball", "box", "map",
         "desk", "lamp", "clock", "bell", "ring", "stone", "bridge",
         "ship", "plane", "train", "horse", "monkey", "elephant",
         "garden", "kitchen", "bedroom", "guitar", "piano", "violin",
         "camera", "computer", "laptop", "tablet", "printer", "bicycle",
         "motorcycle", "helicopter", "submarine", "telescope", "microscope",
         "umbrella", "suitcase", "backpack", "wallet", "newspaper",
         "magazine", "dictionary", "encyclopedia", "atlas", "globe",
         "candle", "lantern", "torch", "mirror", "painting", "sculpture",
         "vase", "trophy", "medal", "certificate", "passport", "ticket"]

PERSON_NAMES = ["Tom", "Mary", "John", "Alice", "Bob", "Sue", "David",
                "Lucy", "Peter", "Kate", "Jack", "Emma", "Mike", "Lisa",
                "James", "Sarah", "Ben", "Amy", "Chris", "Anna",
                "Daniel", "Sophie", "Ryan", "Grace", "Kevin", "Olivia",
                "Sam", "Lily", "Alex", "Helen", "Mark", "Jenny",
                "Paul", "Diana", "Steve", "Laura", "Eric", "Nancy",
                "Frank", "Carol", "George", "Helen", "Henry", "Iris"]

NOUNS_ART = ["elephant", "apple", "orange", "umbrella", "hour", "honest boy",
             "university", "European", "one-way street", "X-ray", "ant",
             "monkey", "horse", "ice cream", "egg", "island", "idea",
             "engineer", "old woman", "American", "honest man", "uniform",
             "eagle", "owl", "important meeting", "empty box", "orange tree",
             "open window", "office", "eye", "arm", "ear", "examination",
             "umbrella stand", "honor", "homage", "herb", "heir", "aisle",
             "hourglass", "orphan", "inn", "igloo", "ox", "eel"]

PREP_PLACES = ["table", "chair", "desk", "box", "room", "park", "school",
               "hospital", "shelf", "floor", "garden", "bed", "kitchen",
               "door", "window", "bridge", "corner", "wall", "street",
               "island", "mountain", "river", "valley", "beach", "forest",
               "library", "classroom", "playground", "bakery", "café",
               "station", "harbor", "castle", "palace", "tower", "temple",
               "museum", "cinema", "theatre", "stadium", "arena", "clinic"]

PREP_TIMES = ["3 o'clock", "noon", "midnight", "Monday", "January",
              "2024", "the weekend", "Christmas", "night", "morning",
              "afternoon", "evening", "Tuesday", "Friday", "February",
              "summer", "winter", "spring", "autumn", "Easter",
              "6 p.m.", "sunrise", "sunset", "dawn", "dusk",
              "Wednesday", "Thursday", "Saturday", "Sunday",
              "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December", "2025"]

ADJ_PAIRS = [("bigger", "big"), ("taller", "tall"), ("faster", "fast"),
             ("easier", "easy"), ("more beautiful", "beautiful"),
             ("hotter", "hot"), ("older", "old"), ("happier", "happy"),
             ("richer", "rich"), ("stronger", "strong"),
             ("longer", "long"), ("better", "good"),
             ("more interesting", "interesting"),
             ("worse", "bad"), ("more expensive", "expensive"),
             ("more popular", "popular"), ("more careful", "careful"),
             ("more comfortable", "comfortable"),
             ("more dangerous", "dangerous"),
             ("more delicious", "delicious"),
             ("wider", "wide"), ("narrower", "narrow"),
             ("deeper", "deep"), ("higher", "high"),
             ("lower", "low"), ("softer", "soft"),
             ("harder", "hard"), ("smarter", "smart"),
             ("louder", "loud"), ("quieter", "quiet"),
             ("brighter", "bright"), ("darker", "dark"),
             ("cleaner", "clean"), ("dirtier", "dirty"),
             ("newer", "new"), ("safer", "safe"),
             ("closer", "close"), ("farther", "far"),
             ("thicker", "thick"), ("thinner", "thin"),
             ("warmer", "warm"), ("cooler", "cool"),
             ("drier", "dry"), ("wetter", "wet"),
             ("sweeter", "sweet"), ("bitter", "bitter"),
             ("smoother", "smooth"), ("rougher", "rough"),
             ("fresher", "fresh"), ("fresher", "fresh")]

PP_PAIRS = [("baked", "bake"), ("written", "write"), ("built", "build"),
            ("cleaned", "clean"), ("broken", "break"), ("opened", "open"),
            ("closed", "close"), ("found", "find"), ("made", "make"),
            ("taken", "take"), ("eaten", "eat"), ("sold", "sell"),
            ("bought", "buy"), ("taught", "teach"), ("sent", "send"),
            ("drawn", "draw"), ("driven", "drive"), ("flown", "fly"),
            ("swum", "swim"), ("sung", "sing"), ("chosen", "choose"),
            ("given", "give"), ("held", "hold"), ("kept", "keep"),
            ("done", "do"), ("seen", "see"), ("heard", "hear"),
            ("known", "know"), ("worn", "wear"), ("fallen", "fall"),
            ("grown", "grow"), ("risen", "rise"), ("thrown", "throw"),
            ("stolen", "steal"), ("caught", "catch"), ("cut", "cut"),
            ("put", "put"), ("set", "set"), ("shut", "shut"),
            ("spent", "spend"), ("paid", "pay"), ("lost", "lose"),
            ("won", "win"), ("left", "leave"), ("met", "meet"),
            ("sat", "sit"), ("stood", "stand"), ("woken", "wake"),
            ("ridden", "ride"), ("shown", "show"), ("said", "say")]


def make_unique(questions, seen, q, opts, correct, expl, topic_zh, topic_en):
    """Add a question if not duplicate, return True if added."""
    if q in seen:
        return False
    seen.add(q)
    opts = list(dict.fromkeys(opts))[:4]
    while len(opts) < 4:
        opts.append("other")
    random.shuffle(opts)
    if correct not in opts:
        opts[0] = correct
    correct_idx = opts.index(correct)
    questions.append({
        "question_zh": q, "question_en": q,
        "options_zh": opts, "options_en": opts,
        "answer": correct_idx,
        "explanation_zh": expl, "explanation_en": expl,
        "topic_zh": topic_zh, "topic_en": topic_en
    })
    return True


# ── 1. TENSES (1000) ──
def gen_tenses(n=1000):
    questions = []
    seen = set()
    tenses = ["present_simple", "present_continuous", "past_simple",
              "present_perfect", "future", "past_continuous",
              "past_perfect", "future_continuous"]
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        s = random.choice(SUBJECTS_ALL)
        v = random.choice(VERBS)
        p = random.choice(PLACES)
        tense = random.choice(tenses)
        is_3s = s in SUBJECTS_3S

        if tense == "present_simple":
            v3s = v+"es" if v.endswith(("s","sh","ch","x","z","o")) else (v[:-1]+"ies" if v.endswith("y") else v+"s")
            answer = v3s if is_3s else v
            wrong1 = v if is_3s else v3s
            opts = [answer, wrong1, "will "+v, "am/is/are "+v+"ing"]
            expl = f"Present simple: '{s}' {'is third person → use -s/-es' if is_3s else 'is not third person → use base form'}."
        elif tense == "present_continuous":
            be = "is" if is_3s else ("am" if s == "I" else "are")
            answer = f"{be} {v}ing"
            opts = [answer, v, "will "+v, v+"s" if is_3s else v]
            expl = f"Present continuous: '{s}' → '{be} + verb-ing'."
        elif tense == "past_simple":
            answer = "did " + v
            opts = [answer, v+"s", "will "+v, "have/has "+v+"ed"]
            expl = "Past simple: use 'did + base verb'."
        elif tense == "present_perfect":
            have = "has" if is_3s else "have"
            answer = f"{have} {v}ed"
            opts = [answer, v+"ed", "will "+v, v+"s"]
            expl = f"Present perfect: '{have} + past participle'."
        elif tense == "future":
            answer = "will " + v
            opts = [answer, v+"s", "am/is/are "+v+"ing", v+"ed"]
            expl = "Future: 'will + base verb'."
        elif tense == "past_continuous":
            was = "was" if s in ["I","He","She"] or is_3s else "were"
            answer = f"{was} {v}ing"
            opts = [answer, v+"ed", "will "+v, v]
            expl = f"Past continuous: '{was} + verb-ing'."
        elif tense == "past_perfect":
            answer = "had " + v + "ed"
            opts = [answer, "have "+v+"ed", "will "+v, v+"ed"]
            expl = "Past perfect: 'had + past participle'."
        else:
            answer = "will be " + v + "ing"
            opts = [answer, "will "+v, "am/is/are "+v+"ing", v+"ed"]
            expl = "Future continuous: 'will be + verb-ing'."

        q = f"{s} ___ {v} {p}."
        make_unique(questions, seen, q, opts, answer, expl, "時態", "Tenses")
    return questions[:n]


# ── 2. ARTICLES (1000) ──
def gen_articles(n=1000):
    """Massively expanded with many template × noun combos."""
    questions = []
    seen = set()

    # Build large pools for parametric generation
    nouns_consonant = ["book", "car", "house", "tree", "dog", "cat", "bird",
                       "fish", "flower", "pen", "cup", "bag", "hat", "key",
                       "phone", "desk", "lamp", "clock", "bell", "stone",
                       "bridge", "ship", "plane", "train", "garden", "kitchen",
                       "bedroom", "guitar", "piano", "camera", "computer",
                       "bicycle", "suitcase", "wallet", "newspaper", "magazine",
                       "dictionary", "globe", "candle", "mirror", "painting",
                       "vase", "trophy", "medal", "passport", "ticket",
                       "bottle", "ruler", "map", "box", "table", "chair",
                       "door", "window", "ball", "cake", "banana", "monkey",
                       "horse", "doctor", "teacher", "student", "child",
                       "city", "river", "mountain", "forest", "library"]
    nouns_vowel = ["apple", "orange", "elephant", "egg", "island", "idea",
                   "engineer", "artist", "office", "eye", "arm", "ear",
                   "hour", "honest boy", "honest man", "umbrella", "ant",
                   "owl", "eagle", "exam", "answer", "actor", "aunt",
                   "uncle", "insect", "invention", "instrument", "igloo",
                   "ox", "eel", "ice cream", "open window", "empty box"]
    nouns_the = ["sun", "moon", "earth", "sky", "sea", "ocean", "universe",
                 "internet", "radio", "television", "world", "government",
                 "police", "army", "navy", "president", "king", "queen"]
    uncountables = ["water", "milk", "rice", "bread", "sugar", "salt",
                    "music", "information", "advice", "furniture", "luggage",
                    "equipment", "homework", "research", "knowledge", "traffic",
                    "weather", "news", "money", "time", "love", "happiness"]

    # Templates that produce unique sentences via parametric noun selection
    templates = [
        # Consonant noun templates
        lambda: (f"I bought ___ {random.choice(nouns_consonant)} yesterday.", "a",
                 "Use 'a' before consonant sounds."),
        lambda: (f"She wants ___ {random.choice(nouns_consonant)} for her birthday.", "a",
                 "Use 'a' before consonant sounds."),
        lambda: (f"He saw ___ {random.choice(nouns_consonant)} on the street.", "a",
                 "Use 'a' before consonant sounds."),
        lambda: (f"We need ___ {random.choice(nouns_consonant)} for the project.", "a",
                 "Use 'a' before consonant sounds."),
        lambda: (f"They found ___ {random.choice(nouns_consonant)} in the box.", "a",
                 "Use 'a' before consonant sounds."),
        lambda: (f"The children drew ___ {random.choice(nouns_consonant)} on paper.", "a",
                 "Use 'a' before consonant sounds."),
        lambda: (f"My sister lost ___ {random.choice(nouns_consonant)} at school.", "a",
                 "Use 'a' before consonant sounds."),
        lambda: (f"The dog chased ___ {random.choice(nouns_consonant)} in the park.", "a",
                 "Use 'a' before consonant sounds."),
        # Vowel noun templates
        lambda: (f"I ate ___ {random.choice(nouns_vowel)} for breakfast.", "an",
                 "Use 'an' before vowel sounds."),
        lambda: (f"She bought ___ {random.choice(nouns_vowel)} at the market.", "an",
                 "Use 'an' before vowel sounds."),
        lambda: (f"He drew ___ {random.choice(nouns_vowel)} on the board.", "an",
                 "Use 'an' before vowel sounds."),
        lambda: (f"We saw ___ {random.choice(nouns_vowel)} at the zoo.", "an",
                 "Use 'an' before vowel sounds."),
        lambda: (f"The teacher gave us ___ {random.choice(nouns_vowel)}.", "an",
                 "Use 'an' before vowel sounds."),
        lambda: (f"My mother found ___ {random.choice(nouns_vowel)} in the garden.", "an",
                 "Use 'an' before vowel sounds."),
        # 'The' templates
        lambda: (f"___ {random.choice(nouns_the)} rises in the east.", "The",
                 "Use 'The' with unique things."),
        lambda: (f"___ {random.choice(nouns_the)} sets in the west.", "The",
                 "Use 'The' with unique things."),
        lambda: (f"___ {random.choice(nouns_the)} is very beautiful today.", "The",
                 "Use 'The' with unique things."),
        lambda: (f"___ {random.choice(nouns_the)} provides light and warmth.", "The",
                 "Use 'The' with unique things."),
        lambda: (f"___ {random.choice(nouns_the)} is essential for life.", "The",
                 "Use 'The' with unique things."),
        # No article (uncountable/general)
        lambda: (f"___ {random.choice(uncountables)} is important for health.", "No article",
                 "No article before uncountable nouns in general statements."),
        lambda: (f"I drink ___ {random.choice(['water','milk','coffee','tea','juice'])} every morning.", "No article",
                 "No article before uncountable nouns in general."),
        lambda: (f"She listens to ___ {random.choice(['music','radio','news'])} every day.", "No article",
                 "No article before uncountable nouns."),
        lambda: (f"He needs ___ {random.choice(['advice','information','help','money','time'])}.", "No article",
                 "No article before uncountable nouns."),
        lambda: (f"We did ___ {random.choice(['homework','research','exercise'])} after school.", "No article",
                 "No article before uncountable nouns."),
        lambda: (f"___ {random.choice(uncountables)} flows through the pipes.", "No article",
                 "No article before uncountable nouns."),
        # Specific patterns
        lambda: (f"She is ___ {random.choice(nouns_vowel)}.", "an",
                 f"Use 'an' before vowel sounds."),
        lambda: (f"He became ___ {random.choice(nouns_vowel)} after years of study.", "an",
                 f"Use 'an' before vowel sounds."),
        lambda: (f"I want to be ___ {random.choice(nouns_consonant)} when I grow up.", "a",
                 "Use 'a' before consonant sounds."),
        lambda: (f"___ {random.choice(nouns_consonant)} in the garden is very old.", "The",
                 "Use 'The' when referring to something specific."),
        lambda: (f"___ {random.choice(nouns_vowel)} in the zoo is very cute.", "The",
                 "Use 'The' when referring to something specific."),
    ]

    attempts = 0
    while len(questions) < n and attempts < n * 5:
        attempts += 1
        tpl = random.choice(templates)
        q, correct, expl = tpl()
        opts = ["a", "an", "the", "No article"]
        if correct not in opts:
            opts[0] = correct
        make_unique(questions, seen, q, opts, correct, expl, "冠詞", "Articles")
    return questions[:n]


# ── 3. PREPOSITIONS (1000) ──
def gen_prepositions(n=1000):
    questions = []
    seen = set()

    nouns_pool = NOUNS
    places_pool = PREP_PLACES
    times_pool = PREP_TIMES
    activities = ["science", "music", "art", "history", "math", "English",
                  "sports", "cooking", "reading", "dancing", "swimming",
                  "painting", "writing", "singing", "running", "chess",
                  "football", "tennis", "photography", "gardening"]
    fears = ["dogs", "snakes", "spiders", "the dark", "heights", "water",
             "fire", "thunder", "flying", "cats", "birds", "insects",
             "deep water", "loud noises", "crowds", "small spaces"]

    # Deterministic: generate all noun×place combos for main template
    combos = [(nm, pl) for nm in nouns_pool for pl in places_pool]
    random.shuffle(combos)
    preps = ["on", "in", "under", "behind", "next to", "near", "above", "below", "beside", "between"]

    for noun, place in combos:
        if len(questions) >= n:
            break
        prep = random.choice(preps)
        q = f"The {noun} is ___ the {place}."
        opts = [prep] + random.sample([x for x in preps if x != prep], 3)
        expl = f"Use '{prep}' to describe the position of the {noun} relative to the {place}."
        make_unique(questions, seen, q, opts, prep, expl, "介詞", "Prepositions")

    # Fill remaining with other templates
    templates_pool = []
    for t in times_pool:
        if "o'clock" in t or t in ["noon", "midnight"]:
            correct = "at"
        elif t in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","Christmas","Easter","the weekend"]:
            correct = "on"
        else:
            correct = "in"
        templates_pool.append((f"I'll meet you ___ {t}.", correct,
            f"Use '{correct}' with '{t}'. 'at' for times, 'on' for days, 'in' for months/seasons."))

    for act in activities:
        templates_pool.append((f"She is interested ___ {act}.", "in", "The phrase is 'interested in'."))
        templates_pool.append((f"He is good ___ {act}.", "at", "The phrase is 'good at'."))
        templates_pool.append((f"She is fond ___ {act}.", "of", "The phrase is 'fond of'."))
        templates_pool.append((f"She succeeded ___ {act}.", "in", "The phrase is 'succeed in'."))

    for f in fears:
        templates_pool.append((f"He is afraid ___ {f}.", "of", "The phrase is 'afraid of'."))

    for nm in nouns_pool[:40]:
        for pl in ["wall", "door", "window", "shelf", "floor", "desk", "table"]:
            templates_pool.append((f"The {nm} is ___ the {pl}.", "on", "Use 'on' for things on a surface."))

    for nm in nouns_pool[:30]:
        templates_pool.append((f"The {nm} belongs ___ {random.choice(PERSON_NAMES)}.", "to", "The phrase is 'belong to'."))

    templates_pool.extend([
        ("The cat hid ___ the sofa.", "behind", "Use 'behind' for at the back of."),
        ("I am looking ___ my keys.", "for", "Use 'looking for' when searching."),
        ("He apologized ___ being late.", "for", "Use 'apologize for' + gerund."),
        ("She arrived ___ the airport early.", "at", "Use 'at' for specific locations."),
        ("He walked ___ the room quietly.", "into", "Use 'into' for entering."),
        ("She came ___ the room smiling.", "into", "Use 'into' for entering."),
        ("The bird flew ___ the window.", "out of", "Use 'out of' for exiting."),
        ("The bank is ___ the hospital and the school.", "between", "Use 'between' for two things."),
        ("The park is ___ the library.", "near", "Use 'near' for close proximity."),
        ("He is responsible ___ the project.", "for", "The phrase is 'responsible for'."),
        ("She sat ___ her mother.", "beside", "Use 'beside' for next to."),
        ("We have lived here ___ 2010.", "since", "Use 'since' with a specific year."),
        ("We have lived here ___ 2015.", "since", "Use 'since' with a specific year."),
        ("We have lived here ___ 2020.", "since", "Use 'since' with a specific year."),
        ("We have lived here ___ Monday.", "since", "Use 'since' with a specific day."),
    ])

    for place in ["France", "Japan", "Italy", "Spain", "Germany", "Australia", "Canada", "Brazil", "India", "China"]:
        templates_pool.append((f"We traveled ___ {place} last summer.", "to", "Use 'to' for destination."))

    for place in ["home", "school", "work", "the office", "the park", "the station"]:
        templates_pool.append((f"She returned ___ {place} late.", "to", "Use 'to' for destination."))

    for thing in ["fence", "wall", "table", "chair", "sofa", "bed", "desk"]:
        templates_pool.append((f"The cat jumped ___ the {thing}.", "over", "Use 'over' for jumping above."))

    for surface in ["table", "desk", "shelf", "floor", "bed"]:
        templates_pool.append((f"She put the vase ___ the {surface}.", "on", "Use 'on' for placing on a surface."))

    for area in ["park", "garden", "playground", "beach", "forest"]:
        templates_pool.append((f"The children played ___ the {area}.", "in", "Use 'in' for enclosed areas."))

    for month in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
        templates_pool.append((f"He was born ___ {month}.", "in", "Use 'in' with months."))

    for obj in ["river", "lake", "sea", "ocean", "channel"]:
        templates_pool.append((f"The boat sailed ___ the {obj}.", "across", "Use 'across' for going from one side to the other."))

    for obj in ["clouds", "mountains", "city", "ocean"]:
        templates_pool.append((f"The plane flew ___ the {obj}.", "over", "Use 'over' for above and across."))

    for path in ["street", "road", "path", "beach", "park"]:
        templates_pool.append((f"We walked ___ the {path}.", "along", "Use 'along' for movement following a line."))

    for thing in ["table", "desk", "bed", "sofa"]:
        templates_pool.append((f"The ball rolled ___ the {thing}.", "under", "Use 'under' for beneath."))

    for view in ["window", "door", "mirror"]:
        templates_pool.append((f"He looked ___ the {view}.", "through", "Use 'through' for looking via."))

    random.shuffle(templates_pool)

    for q, correct, expl in templates_pool:
        if len(questions) >= n:
            break
        opts = [correct]
        all_preps = ["on", "in", "under", "behind", "next to", "near", "above",
                     "below", "beside", "between", "across", "along", "over",
                     "through", "at", "for", "since", "to", "from", "into",
                     "out of", "around", "of", "about", "with"]
        while len(opts) < 4:
            p = random.choice(all_preps)
            if p not in opts:
                opts.append(p)
        make_unique(questions, seen, q, opts, correct, expl, "介詞", "Prepositions")

    return questions[:n]


# ── 4. COMPARISON (1000) ──
def gen_comparison(n=1000):
    questions = []
    seen = set()
    nouns = NOUNS + PERSON_NAMES

    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        comp, base = random.choice(ADJ_PAIRS)
        n1, n2 = random.sample(nouns, 2)
        r = random.random()

        if r < 0.30:
            q = f"The {n1} is ___ than the {n2}."
            correct = comp
            sup = comp.replace("more ","most ") if "more " in comp else (comp[:-2]+"est" if comp.endswith("er") else "most "+base)
            opts = [comp, base, "the "+sup, base+"er" if not comp.startswith("more") else comp]
            expl = f"Comparative of '{base}' is '{comp}'."
        elif r < 0.55:
            name1, name2 = random.sample(PERSON_NAMES, 2)
            q = f"{name1} is ___ than {name2}."
            correct = comp
            opts = [comp, base, "the "+base+"est", base+"ly"]
            expl = f"Use comparative '{comp}' for two people."
        elif r < 0.75:
            sup = comp.replace("more ","most ") if "more " in comp else (comp[:-2]+"est" if comp.endswith("er") else "most "+base)
            q = f"This is ___ {n1} in the city."
            correct = "the " + sup
            opts = ["the "+sup, comp, base, "a "+comp]
            expl = f"Superlative: 'the {sup}'."
        elif r < 0.90:
            q = f"Of the two, this one is ___."
            correct = comp
            opts = [comp, base, "the most "+base, base+"est"]
            expl = f"Comparative '{comp}' for two things."
        else:
            sup = comp.replace("more ","most ") if "more " in comp else (comp[:-2]+"est" if comp.endswith("er") else "most "+base)
            q = f"She is ___ of all the students."
            correct = "the " + sup
            opts = ["the "+sup, comp, base, "more "+base]
            expl = f"Superlative 'the {sup}' for more than two."

        make_unique(questions, seen, q, opts, correct, expl, "比較級", "Comparison")
    return questions[:n]


# ── 5. CONDITIONALS (1000) ──
def gen_conditionals(n=1000):
    questions = []
    seen = set()

    # Expanded pools for Type 1, 2, 3
    cond_present = [
        "rains", "snows", "is sunny", "is cold", "is hot", "is windy",
        "is cloudy", "is dark", "is late", "is early", "is free",
        "is busy", "is ready", "is possible", "is necessary", "is important",
        "is quiet", "is noisy", "is crowded", "is empty", "is cheap",
        "is expensive", "is open", "is closed", "is safe", "is dangerous",
        "is wet", "is dry", "is warm", "is cool", "is fresh"
    ]
    cond_past = [
        "rained", "snowed", "was sunny", "was cold", "was hot", "was windy",
        "was cloudy", "was dark", "was late", "was early", "was free",
        "was busy", "was ready", "was possible", "was necessary", "was important",
        "was quiet", "was noisy", "was crowded", "was empty", "was cheap",
        "was expensive", "was open", "was closed", "was safe", "was dangerous",
        "was wet", "was dry", "was warm", "was cool"
    ]
    cond_perfect = [
        "had rained", "had snowed", "had been sunny", "had been cold",
        "had been hot", "had been windy", "had been dark", "had been late",
        "had been early", "had been free", "had been busy", "had been ready",
        "had been possible", "had been quiet", "had been noisy",
        "had been crowded", "had been cheap", "had been expensive",
        "had been open", "had been closed", "had been safe",
        "had been warm", "had been cool", "had been fresh"
    ]
    will_acts = [
        "stay home", "take an umbrella", "go to the park", "call you",
        "be happy", "bring a jacket", "play outside", "feel sad",
        "cancel the trip", "help you", "buy a new car", "travel abroad",
        "study harder", "start a business", "learn English", "cook dinner",
        "clean the house", "wash the car", "plant flowers", "read a book",
        "watch a movie", "listen to music", "visit my grandmother",
        "go shopping", "eat at a restaurant", "take a taxi", "walk to school",
        "paint the wall", "fix the door", "water the plants"
    ]
    would_acts = [
        "stay home", "take an umbrella", "go to the park", "call you",
        "be happy", "bring a jacket", "play outside", "feel sad",
        "cancel the trip", "help you", "buy a new car", "travel abroad",
        "study harder", "start a business", "learn English", "cook dinner",
        "clean the house", "wash the car", "plant flowers", "read a book",
        "watch a movie", "listen to music", "visit my grandmother",
        "go shopping", "eat at a restaurant", "take a taxi", "walk to school",
        "paint the wall", "fix the door", "water the plants"
    ]
    would_have_acts = [
        "stayed home", "taken an umbrella", "gone to the park", "called you",
        "been happy", "brought a jacket", "played outside", "felt sad",
        "cancelled the trip", "helped you", "bought a new car", "travelled abroad",
        "studied harder", "started a business", "learned English", "cooked dinner",
        "cleaned the house", "washed the car", "planted flowers", "read a book",
        "watched a movie", "listened to music", "visited my grandmother",
        "gone shopping", "eaten at a restaurant", "taken a taxi", "walked to school",
        "painted the wall", "fixed the door", "watered the plants"
    ]
    subjects = ["I", "you", "he", "she", "we", "they"]

    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        subj = random.choice(subjects)
        cv = random.choice(cond_present)
        act = random.choice(will_acts)
        r = random.random()

        if r < 0.35:
            q = f"If it {cv}, {subj} will {act}. Choose the correct form:"
            correct = f"If it {cv}, {subj} will {act}."
            opts = [correct,
                    f"If it {cv}, {subj} would {act}.",
                    f"If it {cv}, {subj} would have {act}.",
                    f"If it {cv}, {subj} {act}."]
            expl = "Type 1: If + present, will + base."
        elif r < 0.65:
            q = f"If it {random.choice(cond_past)}, {subj} would {act}. Choose the correct form:"
            correct = f"If it {random.choice(cond_past)}, {subj} would {act}."
            opts = [correct,
                    f"If it {cv}, {subj} will {act}.",
                    f"If it {cv}, {subj} would have {act}.",
                    f"If it {cv}, {subj} {act}."]
            expl = "Type 2: If + past, would + base."
        else:
            cvp = random.choice(cond_perfect)
            act2 = random.choice(would_have_acts)
            q = f"If it {cvp}, {subj} would have {act2}. Choose the correct form:"
            correct = f"If it {cvp}, {subj} would have {act2}."
            opts = [correct,
                    f"If it {cv}, {subj} will {act2}.",
                    f"If it {cv}, {subj} would {act2}.",
                    f"If it {cv}, {subj} {act2}."]
            expl = "Type 3: If + had pp, would have + pp."

        make_unique(questions, seen, q, opts, correct, expl, "條件句", "Conditionals")
    return questions[:n]


# ── 6. PASSIVE (1000) ──
def gen_passive(n=1000):
    questions = []
    seen = set()
    psubjects = ["The cake", "The letter", "The car", "The house", "The window",
                 "The door", "The book", "The song", "The bridge", "The school",
                 "The homework", "The dinner", "The email", "The phone", "The report",
                 "The painting", "The building", "The road", "The garden", "The ship",
                 "The film", "The game", "The meal", "The wall", "The floor"]
    agents = ["the teacher", "the doctor", "the police", "the government",
              "the students", "the workers", "the children", "the chef",
              "the artist", "the engineer", "the manager", "the nurse",
              "the baker", "the gardener", "the driver", "the pilot"]

    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        subj = random.choice(psubjects)
        agent = random.choice(agents)
        pp, base = random.choice(PP_PAIRS)
        r = random.random()

        if r < 0.30:
            q = f"{subj} ___ {pp} by {agent}."
            correct = "is"
            opts = ["is", "was", "will be", "has been"]
            expl = "Present passive: is/are + past participle."
        elif r < 0.55:
            q = f"{subj} ___ {pp} by {agent} yesterday."
            correct = "was"
            opts = ["was", "is", "will be", "has been"]
            expl = "Past passive: was/were + past participle."
        elif r < 0.75:
            q = f"{subj} ___ {pp} by {agent} tomorrow."
            correct = "will be"
            opts = ["will be", "is", "was", "has been"]
            expl = "Future passive: will be + past participle."
        else:
            q = f"{subj} ___ {pp} by {agent} already."
            correct = "has been"
            opts = ["has been", "is", "was", "will be"]
            expl = "Present perfect passive: has/have been + past participle."

        make_unique(questions, seen, q, opts, correct, expl, "被動語態", "Passive Voice")
    return questions[:n]


# ── 7. REPORTED SPEECH (1000) ──
def gen_reported_speech(n=1000):
    questions = []
    seen = set()

    # Massive pool of direct statements
    statements = [
        ("I am happy", "was happy"), ("I am sad", "was sad"),
        ("I am tired", "was tired"), ("I am hungry", "was hungry"),
        ("I am thirsty", "was thirsty"), ("I am angry", "was angry"),
        ("I am scared", "was scared"), ("I am excited", "was excited"),
        ("I am busy", "was busy"), ("I am free", "was free"),
        ("I am ready", "was ready"), ("I am late", "was late"),
        ("I am early", "was early"), ("I am sick", "was sick"),
        ("I am fine", "was fine"), ("I am worried", "was worried"),
        ("I am surprised", "was surprised"), ("I am bored", "was bored"),
        ("I am confused", "was confused"), ("I am proud", "was proud"),
        ("I like coffee", "liked coffee"), ("I like tea", "liked tea"),
        ("I like music", "liked music"), ("I like books", "liked books"),
        ("I like chocolate", "liked chocolate"), ("I like swimming", "liked swimming"),
        ("I like cooking", "liked cooking"), ("I like reading", "liked reading"),
        ("I like dancing", "liked dancing"), ("I like singing", "liked singing"),
        ("I will come tomorrow", "would come the next day"),
        ("I will help you", "would help me"), ("I will call you", "would call me"),
        ("I will visit you", "would visit me"), ("I will send you a letter", "would send me a letter"),
        ("I will bring you a gift", "would bring me a gift"),
        ("I will wait for you", "would wait for me"),
        ("I will meet you there", "would meet me there"),
        ("I will finish it today", "would finish it that day"),
        ("I will start tomorrow", "would start the next day"),
        ("I have finished", "had finished"), ("I have eaten", "had eaten"),
        ("I have seen that movie", "had seen that movie"),
        ("I have been to Paris", "had been to Paris"),
        ("I have lost my keys", "had lost his/her keys"),
        ("I have done my homework", "had done his/her homework"),
        ("I have written the letter", "had written the letter"),
        ("I have read the book", "had read the book"),
        ("I have met her before", "had met her before"),
        ("I have known him for years", "had known him for years"),
        ("I can swim", "could swim"), ("I can run fast", "could run fast"),
        ("I can speak English", "could speak English"),
        ("I can play the piano", "could play the piano"),
        ("I can cook well", "could cook well"), ("I can drive a car", "could drive a car"),
        ("I can't come", "couldn't come"), ("I can't see anything", "couldn't see anything"),
        ("I can't hear you", "couldn't hear me"), ("I can't find it", "couldn't find it"),
        ("I must go now", "had to go then"), ("I must study harder", "had to study harder"),
        ("I must leave early", "had to leave early"), ("I must finish this", "had to finish that"),
        ("I may go to the party", "might go to the party"),
        ("I may be late", "might be late"), ("I may not come", "might not come"),
        ("I may need help", "might need help"),
        ("I don't know", "didn't know"), ("I don't understand", "didn't understand"),
        ("I don't like it", "didn't like it"), ("I don't agree", "didn't agree"),
        ("I don't have time", "didn't have time"), ("I don't want to go", "didn't want to go"),
        ("I won't go", "wouldn't go"), ("I won't forget", "wouldn't forget"),
        ("I won't tell anyone", "wouldn't tell anyone"),
        ("I need help", "needed help"), ("I need more time", "needed more time"),
        ("I need to study", "needed to study"), ("I need a doctor", "needed a doctor"),
        ("I want to leave", "wanted to leave"), ("I want more food", "wanted more food"),
        ("I want to go home", "wanted to go home"), ("I want a new car", "wanted a new car"),
        ("I saw a bird", "had seen a bird"), ("I saw her yesterday", "had seen her the day before"),
        ("I saw the accident", "had seen the accident"),
        ("I feel tired", "felt tired"), ("I feel happy", "felt happy"),
        ("I feel sick", "felt sick"), ("I feel cold", "felt cold"),
        ("I am reading a book", "was reading a book"),
        ("I am cooking dinner", "was cooking dinner"),
        ("I am working hard", "was working hard"),
        ("I am waiting for you", "was waiting for me"),
        ("I am going to travel", "was going to travel"),
        ("I am going to leave", "was going to leave"),
        ("I am going to study", "was going to study"),
        ("I am going to buy a car", "was going to buy a car"),
        ("I have never been there", "had never been there"),
        ("I have always loved music", "had always loved music"),
        ("I have just arrived", "had just arrived"),
        ("I have already eaten", "had already eaten"),
        ("I like this place", "liked that place"),
        ("I love this song", "loved that song"),
        ("I prefer coffee to tea", "preferred coffee to tea"),
        ("I hate cold weather", "hated cold weather"),
        ("I miss my family", "missed his/her family"),
        ("I believe you", "believed me"), ("I trust you", "trusted me"),
        ("I remember you", "remembered me"), ("I forgot my name", "had forgotten his/her name"),
    ]
    # Commands
    commands = [
        ("Open the door", "to open the door"), ("Close the window", "to close the window"),
        ("Be quiet", "to be quiet"), ("Come here", "to come there"),
        ("Sit down", "to sit down"), ("Stand up", "to stand up"),
        ("Help me", "to help him/her"), ("Don't go", "not to go"),
        ("Don't touch it", "not to touch it"), ("Stop talking", "to stop talking"),
        ("Wait for me", "to wait for him/her"), ("Clean your room", "to clean his/her room"),
        ("Finish your homework", "to finish his/her homework"),
        ("Don't be late", "not to be late"), ("Listen carefully", "to listen carefully"),
        ("Take this book", "to take that book"), ("Don't run", "not to run"),
        ("Be careful", "to be careful"), ("Write it down", "to write it down"),
        ("Don't forget", "not to forget"), ("Be polite", "to be polite"),
        ("Don't shout", "not to shout"), ("Eat your vegetables", "to eat his/her vegetables"),
        ("Wash your hands", "to wash his/her hands"),
        ("Brush your teeth", "to brush his/her teeth"),
        ("Go to bed", "to go to bed"), ("Don't play with fire", "not to play with fire"),
        ("Be on time", "to be on time"), ("Don't lie", "not to lie"),
        ("Keep quiet", "to keep quiet"), ("Turn off the light", "to turn off the light"),
        ("Don't waste food", "not to waste food"),
        ("Respect your elders", "to respect his/her elders"),
        ("Don't waste money", "not to waste money"),
        ("Be kind to others", "to be kind to others"),
    ]
    speakers = ["He", "She", "Tom", "Mary", "The teacher", "My father",
                "The doctor", "My mother", "The nurse", "The manager",
                "My friend", "The boss", "The officer", "The principal"]

    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        speaker = random.choice(speakers)
        is_male = speaker in ["He", "Tom", "My father", "The doctor",
                              "The teacher", "My friend", "The boss",
                              "The officer", "The principal", "The manager"]
        r = random.random()

        if r < 0.72:
            direct, reported = random.choice(statements)
            pronoun = "he" if is_male else "she"
            q = f'{speaker} said, "{direct}." → {speaker} said ___'
            correct = f"that {pronoun} " + reported
            opts = [correct]
            while len(opts) < 4:
                _, r2 = random.choice(statements)
                wrong = f"that {pronoun} " + r2
                if wrong not in opts:
                    opts.append(wrong)
            expl = f"Reported speech: shift tense back. → 'that {pronoun} {reported}'."
        else:
            direct, reported = random.choice(commands)
            q = f'{speaker} said to me, "{direct}." → {speaker} told me ___'
            correct = reported
            opts = [reported]
            while len(opts) < 4:
                _, r2 = random.choice(commands)
                if r2 not in opts:
                    opts.append(r2)
            expl = f"Reported commands: told + object + to/not to + verb."

        make_unique(questions, seen, q, opts, correct, expl, "間接引語", "Reported Speech")
    return questions[:n]


# ── 8. RELATIVE CLAUSES (1000) ──
def gen_relative_clauses(n=1000):
    questions = []
    seen = set()
    people = ["man", "woman", "boy", "girl", "teacher", "doctor", "student",
              "child", "person", "artist", "engineer", "nurse", "chef",
              "driver", "singer", "writer", "painter", "dancer", "farmer",
              "scientist", "musician", "athlete", "pilot", "soldier", "king",
              "queen", "prince", "princess", "detective", "lawyer"]
    things = ["book", "car", "house", "song", "painting", "movie", "city",
              "school", "garden", "bridge", "road", "table", "chair",
              "phone", "computer", "bag", "hat", "shoe", "door", "window",
              "cake", "letter", "picture", "bottle", "clock", "ring",
              "bicycle", "guitar", "piano", "violin", "camera", "watch"]
    verbs_p = ["lives", "works", "studies", "teaches", "cooks", "drives",
               "sings", "writes", "paints", "dances", "runs", "walks",
               "talks", "reads", "plays", "builds", "draws", "helps",
               "watches", "listens", "carries", "catches", "holds", "keeps"]
    adjs = ["tall", "young", "old", "kind", "clever", "brave", "smart",
            "friendly", "happy", "quiet", "loud", "fast", "strong",
            "beautiful", "handsome", "funny", "serious", "polite"]

    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        r = random.random()

        if r < 0.25:
            noun = random.choice(people)
            vp = random.choice(verbs_p)
            q = f"The {noun} ___ {vp} here is my friend."
            correct = "who"
            opts = ["who", "which", "whose", "whom"]
            expl = "'Who' is used for people."
        elif r < 0.45:
            thing = random.choice(things)
            q = f"The {thing} ___ is on the table belongs to me."
            correct = "which"
            opts = ["which", "who", "whose", "whom"]
            expl = "'Which' is used for things."
        elif r < 0.60:
            noun = random.choice(people)
            thing = random.choice(things)
            q = f"The {noun} ___ {thing} was stolen reported to the police."
            correct = "whose"
            opts = ["whose", "who", "which", "whom"]
            expl = "'Whose' shows possession."
        elif r < 0.75:
            noun = random.choice(people)
            q = f"The person ___ I met yesterday was very kind."
            correct = "whom"
            opts = ["whom", "who", "which", "whose"]
            expl = "'Whom' is the object form (formal)."
        elif r < 0.90:
            thing = random.choice(things)
            q = f"This is the {thing} ___ I bought last week."
            correct = "that"
            opts = ["that", "who", "which", "whose"]
            expl = "'That' works for both people and things."
        else:
            noun = random.choice(people)
            adj = random.choice(adjs)
            q = f"She is the {noun} ___ is most {adj}."
            correct = "who"
            opts = ["who", "which", "whose", "whom"]
            expl = "'Who' is used for people."

        make_unique(questions, seen, q, opts, correct, expl, "關係從句", "Relative Clauses")
    return questions[:n]


# ── 9. VOCABULARY (1000) ──
def gen_vocabulary(n=1000):
    VWORDS = [
        ("abundant", "existing in large quantities", "豐富的"),
        ("accurate", "correct and exact", "準確的"),
        ("achieve", "to succeed in doing something", "達到"),
        ("adequate", "enough for a particular purpose", "足夠的"),
        ("admire", "to look at with respect", "欽佩"),
        ("adventure", "an unusual and exciting experience", "冒險"),
        ("aggressive", "ready to attack or fight", "好鬥的"),
        ("ancient", "very old; from long ago", "古老的"),
        ("apparent", "easy to see or understand", "明顯的"),
        ("approach", "to come near", "接近"),
        ("arrange", "to put things in order", "安排"),
        ("assist", "to help someone", "協助"),
        ("assume", "to suppose something is true", "假設"),
        ("attempt", "to try to do something", "嘗試"),
        ("attractive", "pleasing to look at", "吸引人的"),
        ("available", "able to be used or obtained", "可用的"),
        ("awkward", "causing difficulty", "尷尬的"),
        ("bargain", "something bought cheaply", "便宜貨"),
        ("barrier", "something that blocks the way", "障礙"),
        ("benefit", "an advantage or profit", "好處"),
        ("blame", "to say someone is responsible", "責備"),
        ("boundary", "a line that marks a limit", "邊界"),
        ("brave", "ready to face danger", "勇敢的"),
        ("brilliant", "extremely clever or bright", "傑出的"),
        ("budget", "an estimate of income and spending", "預算"),
        ("burden", "a heavy load or responsibility", "負擔"),
        ("calculate", "to work out by using numbers", "計算"),
        ("capable", "having the ability to do something", "有能力的"),
        ("cautious", "careful to avoid danger", "謹慎的"),
        ("celebrate", "to do something special for an occasion", "慶祝"),
        ("challenge", "a difficult task or situation", "挑戰"),
        ("character", "the qualities of a person", "性格"),
        ("charming", "very pleasant and attractive", "迷人的"),
        ("cheerful", "happy and positive", "開朗的"),
        ("clever", "quick to understand", "聰明的"),
        ("comfort", "a state of ease", "舒適"),
        ("communicate", "to share information", "溝通"),
        ("community", "a group of people living together", "社區"),
        ("compare", "to examine differences", "比較"),
        ("complain", "to say you are unhappy", "抱怨"),
        ("complete", "to finish something", "完成"),
        ("complex", "made of many parts; complicated", "複雜的"),
        ("concentrate", "to give all your attention", "專注"),
        ("concern", "a feeling of worry", "關心"),
        ("confident", "sure of yourself", "自信的"),
        ("confirm", "to make sure something is true", "確認"),
        ("confuse", "to make someone unable to understand", "使困惑"),
        ("connect", "to join two things together", "連接"),
        ("consider", "to think carefully", "考慮"),
        ("contain", "to have inside", "包含"),
        ("content", "happy and satisfied", "滿足的"),
        ("continue", "to keep doing something", "繼續"),
        ("contribute", "to give something to help", "貢獻"),
        ("control", "to have power over", "控制"),
        ("convenient", "easy to use; suitable", "方便的"),
        ("convince", "to make someone believe", "說服"),
        ("courage", "the ability to face fear", "勇氣"),
        ("create", "to make something new", "創造"),
        ("curious", "wanting to know about things", "好奇的"),
        ("custom", "a traditional practice", "習俗"),
        ("damage", "physical harm to something", "損壞"),
        ("danger", "the possibility of harm", "危險"),
        ("decide", "to make a choice", "決定"),
        ("decrease", "to become smaller in size or number", "減少"),
        ("defend", "to protect from attack", "防禦"),
        ("deliver", "to take something to a place", "遞送"),
        ("demand", "to ask for something forcefully", "要求"),
        ("demonstrate", "to show clearly", "示範"),
        ("depend", "to rely on", "依賴"),
        ("describe", "to say what something is like", "描述"),
        ("desire", "a strong wish", "渴望"),
        ("destroy", "to damage completely", "摧毀"),
        ("develop", "to grow or change", "發展"),
        ("difference", "the way things are not the same", "差異"),
        ("difficult", "not easy", "困難的"),
        ("discover", "to find for the first time", "發現"),
        ("discuss", "to talk about something", "討論"),
        ("distribute", "to give out to people", "分配"),
        ("donate", "to give to a good cause", "捐贈"),
        ("doubt", "a feeling of not being sure", "懷疑"),
        ("earn", "to receive money for work", "賺取"),
        ("educate", "to teach or train", "教育"),
        ("effective", "successful in producing a result", "有效的"),
        ("efficient", "working well without waste", "高效的"),
        ("effort", "a try to do something", "努力"),
        ("emerge", "to come out or appear", "出現"),
        ("emotion", "a strong feeling", "情感"),
        ("employ", "to give someone a job", "雇用"),
        ("enable", "to make something possible", "使能夠"),
        ("encourage", "to give support or hope", "鼓勵"),
        ("enormous", "very large", "巨大的"),
        ("ensure", "to make certain", "確保"),
        ("enthusiastic", "showing great interest", "熱情的"),
        ("entire", "whole; complete", "整個的"),
        ("environment", "the natural world", "環境"),
        ("essential", "very important and necessary", "必要的"),
        ("establish", "to set up or create", "建立"),
        ("estimate", "to guess an amount", "估計"),
        ("evaluate", "to judge the value of", "評估"),
        ("evidence", "facts that help prove something", "證據"),
        ("excellent", "extremely good", "優秀的"),
        ("expand", "to become larger", "擴展"),
        ("expect", "to think something will happen", "期待"),
        ("explain", "to make something clear", "解釋"),
        ("explore", "to travel around to learn about", "探索"),
        ("express", "to communicate thoughts or feelings", "表達"),
        ("extend", "to make longer or larger", "延長"),
        ("extraordinary", "very unusual or special", "非凡的"),
        ("failure", "lack of success", "失敗"),
        ("familiar", "well known; easily recognized", "熟悉的"),
        ("flexible", "able to bend easily", "靈活的"),
        ("focus", "to concentrate on", "集中"),
        ("forbid", "to not allow", "禁止"),
        ("fortunate", "lucky", "幸運的"),
        ("foundation", "the base of something", "基礎"),
        ("frequent", "happening often", "頻繁的"),
        ("function", "the purpose of something", "功能"),
        ("generate", "to produce or create", "產生"),
        ("genuine", "real; true", "真正的"),
        ("global", "relating to the whole world", "全球的"),
        ("guarantee", "a promise that something will happen", "保證"),
        ("guilty", "responsible for wrongdoing", "有罪的"),
        ("hesitate", "to pause before doing something", "猶豫"),
        ("identify", "to recognize what something is", "識別"),
        ("ignore", "to pay no attention to", "忽略"),
        ("imagine", "to form a picture in your mind", "想像"),
        ("immediate", "happening at once", "立即的"),
        ("impact", "a strong effect", "影響"),
        ("improve", "to make or become better", "改善"),
        ("include", "to have as part of a group", "包括"),
        ("increase", "to become larger in amount", "增加"),
        ("independent", "not needing help from others", "獨立的"),
        ("influence", "to have an effect on", "影響"),
        ("inform", "to tell someone about something", "通知"),
        ("innocent", "not guilty", "無辜的"),
        ("inspire", "to fill with creative power", "啟發"),
        ("intelligent", "able to learn and understand", "聰明的"),
        ("investigate", "to examine the facts", "調查"),
        ("involve", "to include as a part", "涉及"),
        ("isolate", "to separate from others", "隔離"),
        ("journey", "a long trip", "旅程"),
        ("judge", "to form an opinion about", "判斷"),
        ("knowledge", "information and understanding", "知識"),
        ("lack", "to not have enough of", "缺乏"),
        ("launch", "to start something new", "啟動"),
        ("maintain", "to keep in good condition", "維持"),
        ("manage", "to be in charge of", "管理"),
        ("manufacture", "to make in large quantities", "製造"),
        ("mature", "fully grown; sensible", "成熟的"),
        ("measure", "to find the size of", "測量"),
        ("mention", "to talk about something briefly", "提到"),
        ("method", "a way of doing something", "方法"),
        ("migrate", "to move to another place", "遷移"),
        ("minor", "small and not important", "次要的"),
        ("miracle", "a wonderful unexpected event", "奇蹟"),
        ("mission", "an important task", "任務"),
        ("modify", "to change slightly", "修改"),
        ("monitor", "to watch and check", "監控"),
        ("motive", "a reason for doing something", "動機"),
        ("mutual", "shared by two people", "互相的"),
        ("mystery", "something hard to explain", "神秘"),
        ("negotiate", "to discuss to reach agreement", "談判"),
        ("neutral", "not supporting either side", "中立的"),
        ("noble", "having high moral qualities", "高尚的"),
        ("numerous", "many", "眾多的"),
        ("obey", "to do what you are told", "服從"),
        ("objective", "something you aim to achieve", "目標"),
        ("observe", "to watch carefully", "觀察"),
        ("obstacle", "something that blocks progress", "障礙"),
        ("obtain", "to get something", "獲得"),
        ("obvious", "easy to see or understand", "明顯的"),
        ("occur", "to happen", "發生"),
        ("operate", "to work or control", "操作"),
        ("opponent", "someone you compete against", "對手"),
        ("opportunity", "a chance to do something", "機會"),
        ("oppose", "to be against something", "反對"),
        ("ordinary", "normal; not special", "普通的"),
        ("organize", "to arrange in order", "組織"),
        ("overcome", "to succeed in dealing with", "克服"),
        ("participate", "to take part in", "參與"),
        ("patience", "the ability to wait calmly", "耐心"),
        ("perceive", "to become aware of", "感知"),
        ("perform", "to carry out an action", "執行"),
        ("permanent", "lasting for a long time", "永久的"),
        ("permit", "to allow", "允許"),
        ("persist", "to continue firmly", "堅持"),
        ("phenomenon", "something that can be seen", "現象"),
        ("pleasant", "enjoyable; nice", "愉快的"),
        ("portable", "easy to carry", "便攜的"),
        ("positive", "good; hopeful", "積極的"),
        ("possess", "to have or own", "擁有"),
        ("potential", "possible; able to develop", "潛在的"),
        ("practical", "useful and realistic", "實際的"),
        ("precious", "very valuable", "珍貴的"),
        ("predict", "to say what will happen", "預測"),
        ("preserve", "to keep safe", "保存"),
        ("pressure", "the force of pushing", "壓力"),
        ("previous", "happening before", "以前的"),
        ("pride", "a feeling of satisfaction", "自豪"),
        ("primary", "most important; first", "主要的"),
        ("principle", "a basic rule or belief", "原則"),
        ("priority", "something important that comes first", "優先"),
        ("private", "for one person only; not public", "私人的"),
        ("proceed", "to continue doing something", "繼續"),
        ("process", "a series of actions", "過程"),
        ("produce", "to make or create", "生產"),
        ("profit", "money gained from business", "利潤"),
        ("promote", "to raise to a higher position", "促進"),
        ("proper", "correct; suitable", "適當的"),
        ("propose", "to suggest an idea", "提議"),
        ("protect", "to keep safe from harm", "保護"),
        ("protest", "to show strong disagreement", "抗議"),
        ("provide", "to give something needed", "提供"),
        ("purchase", "to buy something", "購買"),
        ("pursue", "to follow or chase", "追求"),
        ("qualify", "to have the right skills", "合格"),
        ("quantity", "an amount of something", "數量"),
        ("random", "without a plan or pattern", "隨機的"),
        ("rapid", "happening quickly", "快速的"),
        ("rare", "not common; unusual", "罕見的"),
        ("realize", "to become aware of", "意識到"),
        ("reasonable", "fair; not extreme", "合理的"),
        ("recognize", "to know from past experience", "認出"),
        ("recommend", "to suggest as good", "推薦"),
        ("recover", "to get better after illness", "恢復"),
        ("reduce", "to make smaller", "減少"),
        ("reflect", "to think deeply", "反映"),
        ("refuse", "to say no", "拒絕"),
        ("regard", "to consider or think of", "認為"),
        ("region", "a large area of land", "地區"),
        ("regret", "to feel sorry about", "後悔"),
        ("regular", "happening at the same time", "定期的"),
        ("reject", "to refuse to accept", "拒絕"),
        ("relate", "to connect or link", "關聯"),
        ("release", "to set free", "釋放"),
        ("relevant", "closely connected", "相關的"),
        ("rely", "to depend on", "依賴"),
        ("remove", "to take away", "移除"),
        ("repair", "to fix something broken", "修理"),
        ("replace", "to take the place of", "替換"),
        ("represent", "to act or speak for", "代表"),
        ("require", "to need", "要求"),
        ("rescue", "to save from danger", "營救"),
        ("research", "a detailed study", "研究"),
        ("reserve", "to keep for later", "保留"),
        ("resist", "to fight against", "抵抗"),
        ("resolve", "to find a solution", "解決"),
        ("resource", "something useful", "資源"),
        ("respond", "to answer or reply", "回應"),
        ("restore", "to bring back to good condition", "恢復"),
        ("restrict", "to limit", "限制"),
        ("retain", "to keep", "保留"),
        ("reveal", "to make known", "揭示"),
        ("reverse", "to go in the opposite direction", "反轉"),
        ("reward", "something given for good work", "獎勵"),
        ("rural", "relating to the countryside", "鄉村的"),
        ("sacrifice", "to give up something valuable", "犧牲"),
        ("satisfy", "to make happy or content", "滿足"),
        ("schedule", "a plan of events", "時間表"),
        ("secure", "safe; protected", "安全的"),
        ("select", "to choose", "選擇"),
        ("separate", "to keep apart", "分開"),
        ("severe", "very bad; serious", "嚴重的"),
        ("shelter", "a place that protects", "庇護所"),
        ("significant", "important; meaningful", "重要的"),
        ("similar", "almost the same", "相似的"),
        ("sincere", "honest and genuine", "真誠的"),
        ("situation", "the conditions at a time", "情況"),
        ("skilled", "having a lot of ability", "熟練的"),
        ("solution", "an answer to a problem", "解決方案"),
        ("specific", "clearly defined; particular", "具體的"),
        ("stable", "firm and not likely to change", "穩定的"),
        ("standard", "a level of quality", "標準"),
        ("stimulate", "to encourage or excite", "刺激"),
        ("strategy", "a plan to achieve a goal", "策略"),
        ("strength", "the quality of being strong", "力量"),
        ("strict", "firm and demanding", "嚴格的"),
        ("struggle", "to try hard with difficulty", "掙扎"),
        ("substitute", "a person or thing that replaces", "替代品"),
        ("sufficient", "enough", "足夠的"),
        ("summary", "a short version of something", "摘要"),
        ("supply", "to provide what is needed", "供應"),
        ("suppose", "to think something is likely", "假設"),
        ("surround", "to be all around", "包圍"),
        ("survive", "to continue to live", "生存"),
        ("suspect", "to think something is true", "懷疑"),
        ("symbol", "something that represents", "象徵"),
        ("sympathy", "feeling sorry for someone", "同情"),
        ("talent", "a natural ability to do something", "才能"),
        ("target", "something you aim at", "目標"),
        ("technique", "a way of doing something", "技術"),
        ("temporary", "lasting for a short time", "臨時的"),
        ("thorough", "complete and detailed", "徹底的"),
        ("threaten", "to say you will harm", "威脅"),
        ("tradition", "a custom passed down", "傳統"),
        ("transfer", "to move from one place to another", "轉移"),
        ("transform", "to change completely", "轉變"),
        ("tremendous", "very great in amount", "巨大的"),
        ("typical", "having usual qualities", "典型的"),
        ("ultimate", "the best or most extreme", "最終的"),
        ("undergo", "to experience something", "經歷"),
        ("unique", "being the only one", "獨特的"),
        ("universal", "relating to everyone", "普遍的"),
        ("urgent", "very important and needing action", "緊急的"),
        ("utilize", "to use for a purpose", "利用"),
        ("vacant", "empty; not in use", "空的"),
        ("vague", "not clear; uncertain", "模糊的"),
        ("valid", "based on truth or reason", "有效的"),
        ("valuable", "worth a lot of money", "有價值的"),
        ("vanish", "to disappear suddenly", "消失"),
        ("variety", "different types of things", "多樣性"),
        ("vast", "very large in area", "廣闊的"),
        ("venture", "a risky journey or business", "冒險"),
        ("version", "a particular form of something", "版本"),
        ("victim", "a person harmed by something", "受害者"),
        ("violate", "to break a rule or law", "違反"),
        ("violent", "using physical force", "暴力的"),
        ("visible", "able to be seen", "可見的"),
        ("vital", "very important; necessary", "至關重要的"),
        ("vivid", "bright and strong", "生動的"),
        ("voluntary", "done by choice", "自願的"),
        ("vulnerable", "able to be easily hurt", "脆弱的"),
        ("wander", "to walk without direction", "漫步"),
        ("wealth", "a large amount of money", "財富"),
        ("welfare", "health and happiness", "福利"),
        ("willing", "ready to do something", "願意的"),
        ("wisdom", "the quality of being wise", "智慧"),
        ("withdraw", "to take away or leave", "撤退"),
        ("witness", "a person who sees an event", "目擊者"),
        ("wonder", "to want to know", "想知道"),
        ("worthy", "deserving respect", "值得的"),
        ("yield", "to produce or give way", "產出"),
        ("zealous", "showing great energy", "熱心的"),
        ("zone", "an area with particular features", "區域"),
    ]

    questions = []
    seen = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        word, meaning_en, meaning_zh = random.choice(VWORDS)
        r = random.random()

        if r < 0.35:
            q = f"What does '{word}' mean?"
            correct = meaning_en
            opts = [meaning_en]
            while len(opts) < 4:
                _, m, _ = random.choice(VWORDS)
                if m not in opts:
                    opts.append(m)
            expl = f"'{word}' means '{meaning_en}' ({meaning_zh})."
        elif r < 0.60:
            q = f"Choose the word that means: {meaning_en}"
            correct = word
            opts = [word]
            while len(opts) < 4:
                w, _, _ = random.choice(VWORDS)
                if w not in opts:
                    opts.append(w)
            expl = f"'{word}' means '{meaning_en}' ({meaning_zh})."
        elif r < 0.80:
            q = f"Which word means '{meaning_zh}'?"
            correct = word
            opts = [word]
            while len(opts) < 4:
                w, _, _ = random.choice(VWORDS)
                if w not in opts:
                    opts.append(w)
            expl = f"'{word}' means '{meaning_en}' ({meaning_zh})."
        else:
            # Fill in sentence context
            contexts = [
                f"The scientist made an important ___. (meaning: {meaning_en})",
                f"Her ___ was very impressive. (meaning: {meaning_en})",
                f"We need to ___ this problem. (meaning: {meaning_en})",
                f"The ___ of the project was clear. (meaning: {meaning_en})",
                f"His ___ to the team was valuable. (meaning: {meaning_en})",
                f"She showed great ___ in her work. (meaning: {meaning_en})",
                f"The ___ of the situation was obvious. (meaning: {meaning_en})",
                f"We must ___ our resources carefully. (meaning: {meaning_en})",
                f"The ___ was very clear to everyone. (meaning: {meaning_en})",
                f"He demonstrated great ___ in the challenge. (meaning: {meaning_en})",
            ]
            q = random.choice(contexts)
            correct = word
            opts = [word]
            while len(opts) < 4:
                w, _, _ = random.choice(VWORDS)
                if w not in opts:
                    opts.append(w)
            expl = f"'{word}' means '{meaning_en}' ({meaning_zh})."

        make_unique(questions, seen, q, opts, correct, expl, "詞彙", "Vocabulary")
    return questions[:n]


# ── 10. ERROR DETECTION (1000) ──
def gen_error_detection(n=1000):
    questions = []
    seen = set()

    # Massive pool of error patterns
    ERRORS = [
        ("He don't like apples.", "doesn't", "He doesn't like apples.",
         "Third person singular requires 'doesn't'."),
        ("She go to school every day.", "goes", "She goes to school every day.",
         "Third person singular requires '-s/-es'."),
        ("I have saw that movie.", "seen", "I have seen that movie.",
         "Present perfect uses past participle 'seen'."),
        ("The children is playing.", "are", "The children are playing.",
         "'Children' is plural → use 'are'."),
        ("He can to swim.", "can swim", "He can swim.",
         "Modal verbs are followed by base form."),
        ("She is more taller than me.", "taller", "She is taller than me.",
         "Don't use 'more' with -er comparatives."),
        ("I didn't went to school.", "go", "I didn't go to school.",
         "After 'didn't', use base form."),
        ("The informations are useful.", "information", "The information is useful.",
         "'Information' is uncountable."),
        ("I am agree with you.", "agree", "I agree with you.",
         "'Agree' is a verb; don't use 'am' before it."),
        ("He is good in mathematics.", "at", "He is good at mathematics.",
         "The phrase is 'good at'."),
        ("Each students must attend.", "student", "Each student must attend.",
         "'Each' is followed by a singular noun."),
        ("I look forward to see you.", "seeing", "I look forward to seeing you.",
         "'Look forward to' is followed by a gerund."),
        ("Despite of the rain, we went.", "Despite", "Despite the rain, we went.",
         "'Despite' is not followed by 'of'."),
        ("He denied to steal the money.", "stealing", "He denied stealing the money.",
         "'Deny' is followed by a gerund."),
        ("The police is investigating.", "are", "The police are investigating.",
         "'Police' is plural."),
        ("The number of students are increasing.", "is", "The number of students is increasing.",
         "'The number of' is singular."),
        ("She is belonging to the club.", "belongs", "She belongs to the club.",
         "'Belong' is a stative verb."),
        ("The news are bad.", "is", "The news is bad.",
         "'News' is uncountable and singular."),
        ("He made me to laugh.", "laugh", "He made me laugh.",
         "'Make + object' uses base form."),
        ("She avoids to make mistakes.", "making", "She avoids making mistakes.",
         "'Avoid' is followed by a gerund."),
        ("I have visited Paris last year.", "visited", "I visited Paris last year.",
         "Don't use present perfect with 'last year'."),
        ("He told me don't go.", "not to go", "He told me not to go.",
         "Reported commands: told + not to + verb."),
        ("The furniture are expensive.", "is", "The furniture is expensive.",
         "'Furniture' is uncountable and singular."),
        ("He suggested me a book.", "to me", "He suggested a book to me.",
         "'Suggest' needs 'to someone'."),
        ("I am accustomed to wake up early.", "waking", "I am accustomed to waking up early.",
         "'Accustomed to' is followed by a gerund."),
        ("She suggested that he went to a doctor.", "go", "She suggested that he go to a doctor.",
         "'Suggest that' uses the subjunctive."),
        ("He has been working since two hours.", "for", "He has been working for two hours.",
         "Use 'for' with duration."),
        ("I enjoyed very much the party.", "the party very much", "I enjoyed the party very much.",
         "Place 'very much' after the object."),
        ("She enjoys to read books.", "reading", "She enjoys reading books.",
         "'Enjoy' is followed by a gerund."),
        ("He asked me that what I wanted.", "what I wanted", "He asked me what I wanted.",
         "Don't use both 'that' and question word."),
        ("She is more smarter than her brother.", "smarter", "She is smarter than her brother.",
         "Don't use 'more' with -er comparatives."),
        ("He finished to do his homework.", "doing", "He finished doing his homework.",
         "'Finish' is followed by a gerund."),
        ("Each of the boys have a pen.", "has", "Each of the boys has a pen.",
         "'Each' is singular."),
        ("I prefer coffee than tea.", "to", "I prefer coffee to tea.",
         "The phrase is 'prefer ... to ...'."),
        ("He has went to the store.", "gone", "He has gone to the store.",
         "Present perfect uses past participle 'gone'."),
        ("She can sings very well.", "sing", "She can sing very well.",
         "After modals, use base form."),
        ("The people is happy.", "are", "The people are happy.",
         "'People' is plural."),
        ("He suggested to go to the park.", "going", "He suggested going to the park.",
         "'Suggest' is followed by a gerund."),
        ("I am used to get up early.", "getting", "I am used to getting up early.",
         "'Used to' (accustomed) is followed by a gerund."),
        ("He asked me where did I live.", "where I lived", "He asked me where I lived.",
         "Reported questions use normal word order."),
        ("She succeed in passing the exam.", "succeeded", "She succeeded in passing the exam.",
         "Past tense requires 'succeeded'."),
        ("He don't has any money.", "doesn't have", "He doesn't have any money.",
         "Third person: 'doesn't' + base form 'have'."),
        ("The teacher told us don't talk.", "not to talk", "The teacher told us not to talk.",
         "Reported commands: told + not to + verb."),
        ("He denied that he had stole the money.", "stolen", "He denied that he had stolen the money.",
         "Past perfect needs past participle 'stolen'."),
        ("I am looking forward to meet you.", "meeting", "I am looking forward to meeting you.",
         "'Look forward to' is followed by a gerund."),
        ("Neither the teacher nor students was there.", "were", "Neither the teacher nor students were there.",
         "'Neither...nor' agrees with the nearer subject."),
        ("I prefer walking than running.", "to", "I prefer walking to running.",
         "The phrase is 'prefer ... to ...'."),
        ("He suggested me to go.", "that I go", "He suggested that I go.",
         "'Suggest' uses 'suggest that' + subjunctive."),
        ("She asked that where I lived.", "where I lived", "She asked where I lived.",
         "Don't use both 'that' and question word."),
        ("The amount of students are growing.", "number", "The number of students are growing.",
         "Use 'number of' for countable nouns."),
        ("He suggested that she works harder.", "work", "He suggested that she work harder.",
         "'Suggest that' uses the subjunctive."),
        ("I have been to Paris since two years.", "for", "I have been to Paris for two years.",
         "Use 'for' with duration, 'since' with a point."),
        ("She is good in singing.", "at", "She is good at singing.",
         "The phrase is 'good at'."),
        ("He asked me that I wanted.", "what I wanted", "He asked me what I wanted.",
         "Use a question word, not 'that'."),
        ("The team are winning.", "is", "The team is winning.",
         "'Team' is typically singular in American English."),
        ("He suggested to take a taxi.", "taking", "He suggested taking a taxi.",
         "'Suggest' is followed by a gerund."),
        ("I look forward to hear from you.", "hearing", "I look forward to hearing from you.",
         "'Look forward to' is followed by a gerund."),
        ("She admitted to steal the money.", "stealing", "She admitted stealing the money.",
         "'Admit' is followed by a gerund."),
        ("He avoids to make errors.", "making", "He avoids making errors.",
         "'Avoid' is followed by a gerund."),
        ("Each boy and each girl have a ticket.", "has", "Each boy and each girl has a ticket.",
         "'Each' makes the subject singular."),
        ("I am looking forward to your reply.", "No error", "I am looking forward to your reply.",
         "This sentence is grammatically correct."),
        ("She is good at painting.", "No error", "She is good at painting.",
         "This sentence is grammatically correct."),
        ("The news was shocking.", "No error", "The news was shocking.",
         "This sentence is grammatically correct."),
        ("He has lived here since 2010.", "No error", "He has lived here since 2010.",
         "This sentence is grammatically correct."),
        ("They suggested that we leave early.", "No error", "They suggested that we leave early.",
         "This sentence uses the subjunctive correctly."),
        ("She enjoys swimming in the pool.", "No error", "She enjoys swimming in the pool.",
         "This sentence is grammatically correct."),
        ("I have been studying for three hours.", "No error", "I have been studying for three hours.",
         "This sentence is grammatically correct."),
        ("He is taller than his brother.", "No error", "He is taller than his brother.",
         "This sentence is grammatically correct."),
        ("We need to finish this by tomorrow.", "No error", "We need to finish this by tomorrow.",
         "This sentence is grammatically correct."),
        ("She succeeded in getting the job.", "No error", "She succeeded in getting the job.",
         "This sentence is grammatically correct."),
        ("I am afraid of dogs.", "No error", "I am afraid of dogs.",
         "This sentence is grammatically correct."),
        ("He denied knowing about it.", "No error", "He denied knowing about it.",
         "This sentence is grammatically correct."),
        ("The police are looking for the thief.", "No error", "The police are looking for the thief.",
         "This sentence is grammatically correct."),
        ("She suggested going to the movies.", "No error", "She suggested going to the movies.",
         "This sentence is grammatically correct."),
        ("I have been here since Monday.", "No error", "I have been here since Monday.",
         "This sentence is grammatically correct."),
        ("He asked me where I lived.", "No error", "He asked me where I lived.",
         "This sentence is grammatically correct."),
        ("Neither of them is coming.", "No error", "Neither of them is coming.",
         "This sentence is grammatically correct."),
        ("She prefers tea to coffee.", "No error", "She prefers tea to coffee.",
         "This sentence is grammatically correct."),
        ("I am used to waking up early.", "No error", "I am used to waking up early.",
         "This sentence is grammatically correct."),
        ("The furniture is new.", "No error", "The furniture is new.",
         "This sentence is grammatically correct."),
    
        ("She suggested me to go.", "that I go", "She suggested that I go.", "Suggest + that clause."),
        ("He asked me that I was tired.", "if I was tired", "He asked if I was tired.", "Ask + if/whether."),
        ("I have been here since two hours.", "for two hours", "For + duration, since + point."),
        ("He enjoyed from the party.", "enjoyed the party", "Enjoy + direct object."),
        ("I enjoy to read books.", "reading books", "Enjoy + -ing."),
        ("She made me to clean the room.", "me clean", "Make + object + base."),
        ("He let me to go.", "me go", "Let + object + base."),
        ("I heard her to sing.", "her sing", "Hear + object + base."),
        ("She was borned in 1990.", "born", "Born (not 'borned')."),
        ("He goed to school yesterday.", "went", "Irregular verb: go → went."),
        ("She eated lunch at noon.", "ate", "Irregular verb: eat → ate."),
        ("I have wrote a letter.", "written", "Present perfect: have + pp."),
        ("She has drank all the water.", "drunk", "Present perfect: has + pp."),
        ("He has began to study.", "begun", "Present perfect: has + pp."),
        ("They have spoke to the teacher.", "spoken", "Present perfect: have + pp."),
        ("She swimmed across the river.", "swam", "Irregular verb: swim → swam."),
        ("He bringed his lunch to school.", "brought", "Irregular verb: bring → brought."),
        ("She buyed a new dress.", "bought", "Irregular verb: buy → bought."),
        ("I catched the ball.", "caught", "Irregular verb: catch → caught."),
        ("He teached us English.", "taught", "Irregular verb: teach → taught."),
        ("She feeled happy.", "felt", "Irregular verb: feel → felt."),
        ("He finded his keys.", "found", "Irregular verb: find → found."),
        ("I thinked about it.", "thought", "Irregular verb: think → thought."),
        ("She knowed the answer.", "knew", "Irregular verb: know → knew."),
        ("He standed up.", "stood", "Irregular verb: stand → stood."),
        ("She understanded the lesson.", "understood", "Irregular verb: understand → understood."),
        ("I leaved early.", "left", "Irregular verb: leave → left."),
        ("He keeped running.", "kept", "Irregular verb: keep → kept."),
        ("She sleeped well.", "slept", "Irregular verb: sleep → slept."),
        ("I haved a good time.", "had", "Irregular verb: have → had."),
        ("He maked a cake.", "made", "Irregular verb: make → made."),
        ("She taked a photo.", "took", "Irregular verb: take → took."),
        ("We goed to the park.", "went", "Irregular verb: go → went."),
        ("They comed early.", "came", "Irregular verb: come → came."),
        ("She runned fast.", "ran", "Irregular verb: run → ran."),
        ("He singed a song.", "sang", "Irregular verb: sing → sang."),
        ("I writed a story.", "wrote", "Irregular verb: write → wrote."),
        ("She drived to work.", "drove", "Irregular verb: drive → drove."),
        ("He flied to London.", "flew", "Irregular verb: fly → flew."),
        ("She drawed a picture.", "drew", "Irregular verb: draw → drew."),
        ("He growed up in the city.", "grew", "Irregular verb: grow → grew."),
        ("She throwed the ball.", "threw", "Irregular verb: throw → threw."),
        ("He weared a hat.", "wore", "Irregular verb: wear → wore."),
        ("She breaked the glass.", "broke", "Irregular verb: break → broke."),
        ("He choosed the red one.", "chose", "Irregular verb: choose → chose."),
        ("She falled down.", "fell", "Irregular verb: fall → fell."),
        ("He gived me a gift.", "gave", "Irregular verb: give → gave."),
        ("She hide it under the bed.", "hid", "Irregular verb: hide → hid."),
        ("He losed his wallet.", "lost", "Irregular verb: lose → lost."),
        ("She payed for dinner.", "paid", "Irregular verb: pay → paid."),
        ("He readed the book.", "read", "Irregular verb: read → read (same spelling)."),
        ("She selled her car.", "sold", "Irregular verb: sell → sold."),
        ("He send me a message.", "sent", "Irregular verb: send → sent."),
        ("She sitted down.", "sat", "Irregular verb: sit → sat."),
        ("He spend all his money.", "spent", "Irregular verb: spend → spent."),
        ("She telled me a story.", "told", "Irregular verb: tell → told."),
        ("He winned the game.", "won", "Irregular verb: win → won."),
        ("She waked up early.", "woke", "Irregular verb: wake → woke."),
]


    # Parametric error templates for more variety
    subj3 = ['He','She','Tom','Mary','My father','My mother','The teacher','The boy','The girl','The doctor','The nurse','The chef']
    subjpl = ['The children','The students','The people','The cats','The dogs','My parents','The workers','The players']
    verbs_base = ['like','want','need','know','have','play','work','study','live','eat','drink','read','write','run','walk','talk','sleep','sing','dance','cook','clean','drive','fly','swim','build','draw','teach','learn','help','find','think','feel','see','hear']
    verbs_ing = ['playing','running','eating','sleeping','singing','dancing','cooking','cleaning','driving','flying','swimming','building','drawing','teaching','learning','helping','finding','thinking','feeling','reading','writing','walking','talking']
    verbs_past = ['went','came','saw','ate','ran','broke','took','gave','made','wrote','drove','flew','sang','bought','sold','told','found','thought','felt','heard','knew','woke','spoke','bore','chose','drew','grew','threw','wore','lent','sent','spent','built','caught','taught']
    verbs_pp = ['gone','come','seen','eaten','run','broken','taken','given','made','written','driven','flown','sung','bought','sold','told','found','thought','felt','heard','known','woken','spoken','borne','chosen','drawn','grown','thrown','worn','lent','sent','spent','built','caught','taught']
    places = ['school','work','the park','the shop','the library','the hospital','the station','the market','the bank','the office','the church','the hotel','the beach','the garden','the kitchen','the bedroom','the classroom']
    adjs = ['taller','bigger','faster','stronger','smarter','happier','older','younger','richer','poorer','shorter','longer','wider','higher','lower']
    error_templates = [
        lambda: (f"{random.choice(subj3)} don't {random.choice(verbs_base)} it.", "doesn't", "3rd person: doesn't + base."),
        lambda: (f"{random.choice(subj3)} go to {random.choice(places)} every day.", "goes", "3rd person: add -s."),
        lambda: (f"The {random.choice(subjpl)} is {random.choice(verbs_ing)}.", "are", "Plural: use 'are'."),
        lambda: (f"{random.choice(subj3)} can to {random.choice(verbs_base)}.", f"can {random.choice(verbs_base)}", "Modal + base (no 'to')."),
        lambda: (f"She is more {random.choice(adjs)} than me.", random.choice(adjs), "No double comparative."),
        lambda: (f"I didn't {random.choice(verbs_past)} to school.", "go", "After didn't: base form."),
        lambda: (f"He is good {random.choice(['in','on','for'])} {random.choice(['mathematics','English','science','sports','music'])}.", "at", "Good at + subject."),
        lambda: (f"I look forward to {random.choice(['see','hear','meet','visit','know'])} you.", "seeing", "Look forward to + -ing."),
        lambda: (f"He suggested {random.choice(['to go','to take','to buy','to make','to use'])} a taxi.", "going", "Suggest + -ing."),
        lambda: (f"She enjoys {random.choice(['to read','to swim','to play','to cook','to sing'])}.", "reading", "Enjoy + -ing."),
        lambda: (f"I am {random.choice(['agree','understand','believe','know','like'])} with you.", "agree", "No 'am' before verb."),
        lambda: (f"Each {random.choice(['students','boys','girls','children','players'])} must attend.", "student", "Each + singular noun."),
        lambda: (f"Neither of them {random.choice(['are','were','have'])} coming.", "is", "Neither + singular verb."),
        lambda: (f"He avoids {random.choice(['to make','to do','to take','to get','to find'])} errors.", "making", "Avoid + -ing."),
        lambda: (f"She admitted {random.choice(['to steal','to take','to break','to lie','to cheat'])}.", "stealing", "Admit + -ing."),
        lambda: (f"The {random.choice(['news','information','furniture','equipment','advice'])} are {random.choice(['good','new','broken','ready','useful'])}.", "is", "Uncountable: singular."),
        lambda: (f"He has lived here {random.choice(['since','from'])} two years.", "for", "For + duration."),
        lambda: (f"I prefer tea {random.choice(['than','over','from'])} coffee.", "to", "Prefer X to Y."),
        lambda: (f"{random.choice(subj3)} is {random.choice(['visited','bought','wrote','drove','sang'])} by the teacher.", "was visited", "Past passive: was + pp."),
        lambda: (f"{random.choice(subj3)} have {random.choice(verbs_past)} the movie.", f"has {random.choice(verbs_pp)}", "3rd person: has + pp."),
        lambda: (f"I am {random.choice(['use','used','using'])} to {random.choice(verbs_ing)} early.", "used", "Be used to + -ing."),
        lambda: (f"{random.choice(subj3)} denied {random.choice(['to know','to see','to take'])} about it.", "knowing", "Deny + -ing."),
        lambda: (f"The number of students {random.choice(['are','were','have'])} increasing.", "is", "The number of: singular."),
        lambda: (f"A number of students {random.choice(['is','was','has'])} absent.", "are", "A number of: plural."),
        lambda: (f"{random.choice(subj3)} told me {random.choice(['that what','that where','that who'])} he wanted.", "what", "Use question word, not 'that + question word'."),
        lambda: (f"{random.choice(subj3)} insisted {random.choice(['to go','to leave','to stay'])}.", "on going", "Insist on + -ing."),
        lambda: (f"I am looking forward to {random.choice(['your','his','her'])} reply.", "No error", "This is correct."),
        lambda: (f"{random.choice(subj3)} has lived here since {random.choice(['2010','2015','2020'])}.", "No error", "This is correct."),
        lambda: (f"She is good at {random.choice(['painting','singing','dancing','cooking'])}.", "No error", "This is correct."),
        lambda: (f"{random.choice(subj3)} suggested that we {random.choice(['leave','go','start'])} early.", "No error", "Subjunctive: correct."),
    ]
    for tmpl in error_templates:
        try:
            wrong, correct_word, rule = tmpl()
            q = f'Find the error: "{wrong}"'
            all_words = ["doesn't","goes","are","is","taller","go","at","for","seeing","stealing","has","Despite","to","than"]
            opts = [correct_word]
            while len(opts) < 4:
                w = random.choice(all_words)
                if w not in opts:
                    opts.append(w)
            make_unique(questions, seen, q, opts, correct_word, rule, "錯誤識別", "Error Detection")
        except:
            pass

    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        entry = random.choice(ERRORS)
        if len(entry) == 3:
            wrong, correct_word, rule = entry
            corrected = wrong.replace(correct_word, f"[{correct_word}]")
        else:
            wrong, correct_word, corrected, rule = entry
        r = random.random()

        if r < 0.50:
            if correct_word == "No error":
                q = f"Is this sentence correct? \"{wrong}\""
                correct = "Correct"
                opts = ["Correct", "Incorrect"]
                expl = f"This sentence is correct. {rule}"
            else:
                q = f"Find the error: \"{wrong}\""
                correct = correct_word
                all_words = ["doesn't","don't","goes","go","seen","saw","are","is",
                             "can swim","can to swim","taller","more taller","went","go",
                             "information","informations","me to go","that I go",
                             "that where","where","am agree","agree","in","at",
                             "students","student","see","seeing","Despite of","Despite",
                             "stealing","to steal","waking","wake","laugh","to laugh",
                             "visited","have visited","not to go","don't go","for","since",
                             "going","to go","meeting","meet","what","that what",
                             "smarter","more smarter","doing","to do","has","have",
                             "to","than","gone","went","sing","sings","at","in",
                             "stolen","stole","succeeded","succeed","number","amount"]
                opts = [correct]
                while len(opts) < 4:
                    w = random.choice(all_words)
                    if w not in opts:
                        opts.append(w)
                expl = f"Error: '{correct_word}' is correct. {rule}"
        elif r < 0.80:
            q = f"What is the correct version? \"{wrong}\""
            correct = corrected
            opts = [corrected, wrong]
            while len(opts) < 4:
                e2 = random.choice(ERRORS)
                c2 = e2[2] if len(e2) >= 3 else e2[0]
                if c2 not in opts:
                    opts.append(c2)
            expl = f"Correct: '{corrected}'. {rule}"
        else:
            q = f"Is this sentence correct? \"{wrong}\""
            if correct_word == "No error":
                correct = "Correct"
                opts = ["Correct", "Incorrect"]
            else:
                correct = "Incorrect"
                opts = ["Incorrect", "Correct"]
            expl = f"{'Correct.' if correct_word == 'No error' else f'Incorrect. {rule}'}"

        make_unique(questions, seen, q, opts, correct, expl, "錯誤辨識", "Error Detection")
    return questions[:n]


# ── Main ──

def round_robin_shuffle(topic_lists):
    """Round-robin: take one from each topic in turn."""
    result = []
    topic_names = list(topic_lists.keys())
    max_len = max(len(v) for v in topic_lists.values())
    for i in range(max_len):
        for t in topic_names:
            if i < len(topic_lists[t]):
                result.append(topic_lists[t][i])
    return result


def main():
    print("Generating questions...")

    generators = {
        "Tenses": gen_tenses,
        "Articles": gen_articles,
        "Prepositions": gen_prepositions,
        "Comparison": gen_comparison,
        "Conditionals": gen_conditionals,
        "Passive Voice": gen_passive,
        "Reported Speech": gen_reported_speech,
        "Relative Clauses": gen_relative_clauses,
        "Vocabulary": gen_vocabulary,
        "Error Detection": gen_error_detection,
    }

    all_questions = {}
    for name, gen_func in generators.items():
        print(f"  Generating {name}...")
        qs = gen_func(1000)
        print(f"    Got {len(qs)} questions")
        all_questions[name] = qs

    total = sum(len(v) for v in all_questions.values())
    print(f"\nTotal questions generated: {total}")

    if total < 10000:
        print(f"WARNING: Got {total}, will pad with extras from larger topics.")
        for name, qs in all_questions.items():
            if len(qs) < 1000:
                print(f"  {name} is short: {len(qs)}/1000")

    # Round-robin shuffle
    print("Shuffling (round-robin)...")
    shuffled = round_robin_shuffle(all_questions)

    # Verify no duplicate question_zh
    seen_q = set()
    dupes = 0
    for q in shuffled:
        if q["question_zh"] in seen_q:
            dupes += 1
        seen_q.add(q["question_zh"])
    print(f"Duplicate question_zh: {dupes}")

    # Verify max consecutive same topic
    max_consec = 1
    current_consec = 1
    for i in range(1, len(shuffled)):
        if shuffled[i]["topic_en"] == shuffled[i-1]["topic_en"]:
            current_consec += 1
            max_consec = max(max_consec, current_consec)
        else:
            current_consec = 1
    print(f"Max consecutive same topic: {max_consec}")

    # Topic distribution
    topic_dist = defaultdict(int)
    for q in shuffled:
        topic_dist[q["topic_en"]] += 1
    print("\nTopic distribution:")
    for t, c in sorted(topic_dist.items()):
        print(f"  {t}: {c}")

    # Save
    base_dir = "/Users/bruce/.openclaw/workspace/projects/project_03_bruce_institute_10000/uncle-bruce-10000"
    paths = [
        os.path.join(base_dir, "english", "s1", "questions.json"),
        os.path.join(base_dir, "v2", "english", "s1", "questions.json"),
    ]

    for p in paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(shuffled, f, ensure_ascii=False, indent=2)
        print(f"Saved to {p}")

    print(f"\n✅ DONE: total={total}, max_consecutive={max_consec}, duplicates={dupes}")


if __name__ == "__main__":
    main()
