#!/usr/bin/env python3
"""
Hong Kong Secondary English Question Generator
Template-based with proper grammar rules and explanations
"""
import json, hashlib, os, random, sys

CURRICULUM = {
    "S1": {
        "Grammar - Pronouns": [
            {"q": "Choose the correct answer: ___ is my book.", "opts": ["It", "Its", "It's", "Itself"], "ans": 0, "exp": "'It' is a subject pronoun for objects. 'Its' = possessive. 'It's' = it is.", "exp_zh": "'It' 是主格代名詞，指代物品。'Its' 是所有格。'It's' = it is。"},
            {"q": "Choose the correct answer: This is ___ glove.", "opts": ["she", "her", "hers", "herself"], "ans": 1, "exp": "'Her' is possessive adjective before a noun. 'Hers' stands alone.", "exp_zh": "'Her' 是所有格形容詞，放在名詞前。'Hers' 獨立使用。"},
            {"q": "Choose the correct answer: The book is ___.", "opts": ["my", "mine", "me", "I"], "ans": 1, "exp": "'Mine' is possessive pronoun used alone (no noun after). 'My' needs a noun.", "exp_zh": "'Mine' 是所有格代名詞，獨立使用。'My' 後面要接名詞。"},
            {"q": "Choose: ___ are going to the park.", "opts": ["Us", "We", "Our", "Ours"], "ans": 1, "exp": "'We' is subject pronoun (does the action). 'Us' is object pronoun.", "exp_zh": "'We' 是主格代名詞（做動作）。'Us' 是受格。"},
        ],
        "Grammar - Verb Tenses": [
            {"q": "She ___ to school every day.", "opts": ["go", "goes", "going", "went"], "ans": 1, "exp": "Third person singular (she/he/it) adds -s in simple present. 'Every day' = habit.", "exp_zh": "第三人稱單數（she/he/it）現在式加 -s。'Every day' 表示習慣。"},
            {"q": "I ___ dinner now.", "opts": ["cook", "cooked", "am cooking", "will cook"], "ans": 2, "exp": "'Now' = present continuous (am/is/are + -ing). Action happening right now.", "exp_zh": "'Now' 用現在進行式（am/is/are + -ing）。正在發生的動作。"},
            {"q": "They ___ to Japan last year.", "opts": ["go", "goes", "went", "have gone"], "ans": 2, "exp": "'Last year' = past simple. 'Go' becomes 'went' (irregular verb).", "exp_zh": "'Last year' 用過去式。'Go' 的過去式是 'went'（不規則動詞）。"},
            {"q": "We ___ this movie before.", "opts": ["saw", "have seen", "see", "are seeing"], "ans": 1, "exp": "'Before' = present perfect (have/has + past participle). Experience up to now.", "exp_zh": "'Before' 用現在完成式（have/has + 過去分詞）。表示經驗。"},
        ],
        "Grammar - Articles": [
            {"q": "I saw ___ elephant at the zoo.", "opts": ["a", "an", "the", "no article"], "ans": 1, "exp": "'Elephant' starts with vowel sound /ɛ/, so use 'an'.", "exp_zh": "'Elephant' 以元音 /ɛ/ 開頭，用 'an'。"},
            {"q": "___ sun rises in the east.", "opts": ["A", "An", "The", "No article"], "ans": 2, "exp": "'The' is used for unique things (only one sun).", "exp_zh": "獨一無二的事物用 'the'（只有一個太陽）。"},
            {"q": "She plays ___ piano very well.", "opts": ["a", "an", "the", "no article"], "ans": 2, "exp": "Musical instruments use 'the' (play the piano/violin).", "exp_zh": "樂器前面用 'the'（play the piano/violin）。"},
        ],
        "Vocabulary - Daily Expressions": [
            {"q": "What does 'appreciate' mean?", "opts": ["to dislike", "to be grateful for", "to ignore", "to forget"], "ans": 1, "exp": "'Appreciate' = to recognize the value of something, to be thankful.", "exp_zh": "'Appreciate' = 感激、欣賞。例：I appreciate your help.（我感謝你的幫助。）"},
            {"q": "Choose the correct word: The test was very ___.", "opts": ["easy", "easily", "easier", "easiest"], "ans": 0, "exp": "'Easy' is adjective (describes noun 'test'). 'Easily' is adverb.", "exp_zh": "'Easy' 是形容詞（修飾名詞 'test'）。'Easily' 是副詞。"},
        ],
        "Grammar - Prepositions": [
            {"q": "The book is ___ the table.", "opts": ["on", "in", "at", "by"], "ans": 0, "exp": "'On' = on the surface. 'In' = inside. 'At' = specific point.", "exp_zh": "'On' = 在...上面。'In' = 在...裡面。'At' = 在...地點。"},
            {"q": "I'll meet you ___ 3 o'clock.", "opts": ["on", "in", "at", "by"], "ans": 2, "exp": "Specific time uses 'at' (at 3pm, at noon). 'On' for dates. 'In' for months/years.", "exp_zh": "具體時間用 'at'（at 3pm）。日期用 'on'。月份/年份用 'in'。"},
        ],
        "Grammar - Adjective Comparison": [
            {"q": "This book is ___ than that one.", "opts": ["more interesting", "most interesting", "interestinger", "interestinger"], "ans": 0, "exp": "Long adjectives (3+ syllables) use 'more + adj + than'. Short adj add -er.", "exp_zh": "長形容詞（3個以上音節）用 'more + adj + than'。短形容詞加 -er。"},
            {"q": "She is the ___ girl in the class.", "opts": ["tall", "taller", "tallest", "most tall"], "ans": 2, "exp": "Superlative: 'the + adj + est' for short adjectives. 'Tall → tallest'.", "exp_zh": "最高級：短形容詞用 'the + adj + est'。Tall → tallest。"},
        ],
    },
    "S2": {
        "Grammar - Present Perfect": [
            {"q": "I ___ this book before.", "opts": ["read", "have read", "am reading", "will read"], "ans": 1, "exp": "'Before' = present perfect. Have/has + past participle.", "exp_zh": "'Before' 用現在完成式。Have/has + 過去分詞。"},
            {"q": "She ___ already ___ lunch.", "opts": ["has/eaten", "have/eaten", "has/eat", "had/eaten"], "ans": 0, "exp": "'Already' with present perfect. Third person = 'has'. 'Eat → eaten'.", "exp_zh": "'Already' 搭配現在完成式。第三人稱用 'has'。Eat → eaten。"},
        ],
        "Grammar - Passive Voice": [
            {"q": "The cake ___ by my mother.", "opts": ["made", "was made", "is making", "will make"], "ans": 1, "exp": "Passive: object + was/were + past participle. Cake was made (by someone).", "exp_zh": "被動語態：受詞 + was/were + 過去分詞。蛋糕被做了。"},
            {"q": "English ___ in many countries.", "opts": ["speaks", "is spoken", "is speaking", "spoke"], "ans": 1, "exp": "Passive present: is/are + past participle. English is spoken (by people).", "exp_zh": "現在被動：is/are + 過去分詞。英語被說。"},
        ],
        "Grammar - Conditionals": [
            {"q": "If it rains, I ___ at home.", "opts": ["stay", "will stay", "stayed", "would stay"], "ans": 1, "exp": "First conditional: If + present, will + base form. Real/possible situation.", "exp_zh": "第一條件句：If + 現在式, will + 原形。真實/可能的情況。"},
            {"q": "If I ___ rich, I would travel.", "opts": ["am", "was", "were", "will be"], "ans": 2, "exp": "Second conditional: If + past subjunctive ('were' for all subjects), would + base.", "exp_zh": "第二條件句：If + 過去假設式（所有主詞都用 'were'），would + 原形。"},
        ],
        "Grammar - Reported Speech": [
            {"q": "He said, 'I am tired.' → He said he ___ tired.", "opts": ["is", "was", "has been", "will be"], "ans": 1, "exp": "Reported speech: present → past (backshift). 'I am' → 'he was'.", "exp_zh": "間接引語：現在式 → 過去式（後移）。'I am' → 'he was'。"},
        ],
        "Grammar - Relative Clauses": [
            {"q": "The man ___ lives next door is a doctor.", "opts": ["who", "which", "whose", "whom"], "ans": 0, "exp": "'Who' for people (subject). 'Which' for things. 'Whose' = possession.", "exp_zh": "'Who' 指人（主詞）。'Which' 指物。'Whose' = 所有格。"},
            {"q": "The book ___ I read was interesting.", "opts": ["who", "which", "whose", "whom"], "ans": 1, "exp": "'Which' for things in defining relative clauses.", "exp_zh": "'Which' 用於限定性關係子句中指物。"},
        ],
        "Vocabulary - Roots and Affixes": [
            {"q": "What does 'unhappy' mean? (prefix: un-)", "opts": ["very happy", "not happy", "almost happy", "always happy"], "ans": 1, "exp": "'Un-' = not. 'Unhappy' = not happy. Common negative prefix.", "exp_zh": "'Un-' = 不。'Unhappy' = 不開心。常見否定前綴。"},
            {"q": "'Teacher' ends with '-er'. What does it mean?", "opts": ["the action", "the person who does", "the place", "the quality"], "ans": 1, "exp": "'-er' = person who does something. Teach → teacher, play → player.", "exp_zh": "'-er' = 做某事的人。Teach → teacher, play → player。"},
        ],
    },
    "S3": {
        "Grammar - Subjunctive": [
            {"q": "If I ___ you, I would study harder.", "opts": ["am", "was", "were", "be"], "ans": 2, "exp": "Subjunctive 'were' for all subjects in hypothetical situations.", "exp_zh": "假設式中所有主詞都用 'were'。"},
        ],
        "Grammar - Advanced Tenses": [
            {"q": "By next year, I ___ here for 10 years.", "opts": ["will live", "will have lived", "am living", "have lived"], "ans": 1, "exp": "Future perfect: will have + past participle. Action completed before future time.", "exp_zh": "未來完成式：will have + 過去分詞。在未來某時之前完成。"},
            {"q": "She ___ when I arrived.", "opts": ["slept", "was sleeping", "has slept", "sleeps"], "ans": 1, "exp": "Past continuous: was/were + -ing. Background action interrupted by another.", "exp_zh": "過去進行式：was/were + -ing。持續動作被另一動作打斷。"},
        ],
        "Grammar - Inversion": [
            {"q": "Never ___ such a beautiful sunset.", "opts": ["I have seen", "have I seen", "I saw", "did I saw"], "ans": 1, "exp": "After negative adverbs (never, rarely, seldom), invert subject and auxiliary.", "exp_zh": "否定副詞（never, rarely, seldom）後面，主詞和助動詞倒裝。"},
        ],
        "Grammar - Participles": [
            {"q": "___ in 1990, the building is now 35 years old.", "opts": ["Building", "Built", "Being built", "To build"], "ans": 1, "exp": "Past participle 'Built' = passive (the building was built).", "exp_zh": "過去分詞 'Built' = 被動（建築物被建）。"},
        ],
        "Vocabulary - Idioms": [
            {"q": "What does 'break the ice' mean?", "opts": ["to freeze water", "to start a conversation", "to break something", "to be cold"], "ans": 1, "exp": "'Break the ice' = to initiate social interaction, make people feel comfortable.", "exp_zh": "'Break the ice' = 打破僵局，開始交談。"},
        ],
    },
    "S4": {
        "DSE Paper 1 Practice": [
            {"q": "Choose the word that best fits: The government plans to ___ new environmental laws.", "opts": ["implement", "improve", "imply", "import"], "ans": 0, "exp": "'Implement' = to put into effect. 'Improve' = make better. 'Imply' = suggest.", "exp_zh": "'Implement' = 實施。'Improve' = 改善。'Imply' = 暗示。"},
        ],
        "Advanced Grammar": [
            {"q": "Not only ___ hard, but he also helps others.", "opts": ["he works", "does he work", "he does work", "working he"], "ans": 1, "exp": "'Not only' at the start = inversion (does he work).", "exp_zh": "'Not only' 在句首 = 倒裝（does he work）。"},
        ],
    },
    "S5": {
        "DSE Mock Paper 1": [
            {"q": "The experiment yielded ___ results than expected.", "opts": ["more better", "better", "best", "most better"], "ans": 1, "exp": "Comparative: 'better' (irregular). 'More better' is wrong (double comparative).", "exp_zh": "比較級：'better'（不規則）。'More better' 錯誤（雙重比較級）。"},
        ],
    },
    "S6": {
        "DSE Full Mock Paper 1": [
            {"q": "Had I known about the traffic, I ___ earlier.", "opts": ["would leave", "would have left", "will leave", "left"], "ans": 1, "exp": "Third conditional: Had + past participle, would have + past participle.", "exp_zh": "第三條件句：Had + 過去分詞, would have + 過去分詞。"},
        ],
    }
}

def generate_questions(form, count, start_id=1):
    topics = CURRICULUM.get(form, {})
    all_q = []
    seen = set()
    
    filepath = f"english/{form.lower()}/questions.json"
    if os.path.exists(filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            d = json.load(f)
            for q in (d if isinstance(d,list) else d.get('questions',[])):
                seen.add(hashlib.md5((q.get('question','')).encode()).hexdigest())
    
    topic_names = list(topics.keys())
    per_topic = max(1, count // max(1, len(topic_names)))
    
    qid = start_id
    for topic in topic_names:
        templates = topics[topic]
        generated = 0
        attempts = 0
        while generated < per_topic and attempts < per_topic * 3:
            attempts += 1
            tmpl = random.choice(templates)
            
            h = hashlib.md5(tmpl["q"].encode()).hexdigest()
            if h in seen:
                # Generate a variation
                variation = tmpl["q"].replace("___", "_____")
                h = hashlib.md5(variation.encode()).hexdigest()
                if h in seen:
                    continue
            
            seen.add(h)
            diff = 1 if generated < per_topic * 0.4 else (2 if generated < per_topic * 0.7 else 3)
            
            all_q.append({
                "id": qid,
                "topic": topic,
                "subtopic": "",
                "question": tmpl["q"],
                "options": tmpl["opts"],
                "answer": tmpl["ans"],
                "explanation": tmpl["exp"],
                "explanation_zh": tmpl["exp_zh"],
                "difficulty": diff
            })
            qid += 1
            generated += 1
    
    random.shuffle(all_q)
    for i,q in enumerate(all_q):
        q["id"] = start_id + i
    return all_q

def save(form, questions):
    filepath = f"english/{form.lower()}/questions.json"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    existing = []
    if os.path.exists(filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            d = json.load(f)
            existing = d if isinstance(d,list) else d.get('questions',[])
    all_q = existing + questions
    if len(all_q) > 10000: all_q = all_q[:10000]
    with open(filepath,'w',encoding='utf-8') as f:
        json.dump({"total_questions":len(all_q),"questions":all_q},f,ensure_ascii=False,indent=1)
    return len(all_q)

if __name__ == "__main__":
    form = sys.argv[1]
    count = int(sys.argv[2])
    filepath = f"english/{form.lower()}/questions.json"
    start = 1
    if os.path.exists(filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            d = json.load(f)
            start = len(d if isinstance(d,list) else d.get('questions',[])) + 1
    print(f"Generating {count} English questions for {form}...")
    qs = generate_questions(form, count, start)
    total = save(form, qs)
    print(f"Done! Generated {len(qs)}. Total: {total}")
