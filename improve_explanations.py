#!/usr/bin/env python3
"""Generate detailed explanations for English S1 questions."""
import json, re, random

fpath = '/Users/bruce/.openclaw/workspace/projects/project_03_bruce_institute_10000/uncle-bruce-10000/english/s1/questions.json'
with open(fpath) as f:
    d = json.load(f)
qs = d if isinstance(d, list) else d.get('questions', [])

def get_correct(q):
    opts = q.get('options_en', [])
    ans = q.get('answer', 0)
    return opts[ans] if ans < len(opts) else ''

def fill_blank_explanation(q):
    """Generate explanation for fill-in-the-blank questions."""
    en = q.get('question_en', '')
    correct = get_correct(q).lower().strip()
    en_lower = en.lower()
    
    explanations = []
    
    # Articles: a, an, the
    if correct in ['a', 'an', 'the']:
        if correct == 'the':
            explanations.append("'The' is used because it refers to a specific noun that is already known or identified.")
            explanations.append("We use 'the' when both speaker and listener know which thing is being talked about.")
        elif correct == 'an':
            explanations.append("'An' is used before words that begin with a vowel sound (a, e, i, o, u sounds).")
            if re.search(r'[aeiou]', correct[:1]):
                explanations.append(f"Since '{get_correct(q).strip()}' starts with a vowel sound, we use 'an'.")
        elif correct == 'a':
            explanations.append("'A' is used before words that begin with a consonant sound.")
            explanations.append("It refers to a non-specific, singular, countable noun.")
    
    # Prepositions
    prep_map = {
        'in': ("'In' is used for enclosed spaces, months, years, and longer periods.", "We say 'in the room', 'in January', 'in 2024'."),
        'on': ("'On' is used for surfaces and specific days/dates.", "We say 'on the table', 'on Monday', 'on January 1st'."),
        'at': ("'At' is used for specific points in time and locations.", "We say 'at 5pm', 'at the bus stop', 'at home'."),
        'to': ("'To' indicates direction or movement toward something.", "We say 'go to school', 'give it to me'."),
        'for': ("'For' indicates purpose, duration, or recipient.", "We say 'for three hours', 'for you'."),
        'with': ("'With' indicates accompaniment or using something.", "We say 'with my friend', 'with a knife'."),
        'of': ("'Of' indicates possession, origin, or relationship.", "We say 'the door of the house', 'a cup of tea'."),
        'by': ("'By' indicates the agent performing an action (passive voice) or means of transport.", "We say 'by car', 'written by Shakespeare'."),
        'from': ("'From' indicates origin or starting point.", "We say 'from Japan', 'from 9am to 5pm'."),
        'about': ("'About' indicates the topic or subject of something.", "We say 'talk about music', 'a book about history'."),
        'into': ("'Into' indicates movement from outside to inside.", "We say 'walk into the room', 'transform into'."),
        'about': ("'About' means regarding or concerning.", "We say 'think about it', 'a story about dragons'."),
    }
    
    if correct in prep_map:
        explanations.append(prep_map[correct][0])
        explanations.append(prep_map[correct][1])
    
    # Subject-verb agreement
    if correct in ['is', 'are', 'was', 'were', 'am']:
        subject = re.search(r'^(.+?)\s+___', en)
        if subject:
            subj = subject.group(1).strip()
            subj_words = subj.split()
            if subj_words:
                last_word = subj_words[-1].lower()
                if last_word in ['i']:
                    explanations.append(f"'{correct}' is correct because 'I' always uses '{correct}'.")
                elif last_word in ['he', 'she', 'it'] or (last_word not in ['they', 'we', 'you'] and not last_word.endswith('s')):
                    explanations.append(f"'{correct}' agrees with the singular subject '{subj}'.")
                else:
                    explanations.append(f"'{correct}' agrees with the plural subject '{subj}'.")
    
    # Verb forms (has/have/had + past participle)
    if correct.startswith('has ') or correct.startswith('have ') or correct.startswith('had '):
        tense = 'present perfect' if 'has ' in correct or 'have ' in correct else 'past perfect'
        explanations.append(f"This uses the {tense} tense: {'has/have' if 'present' in tense else 'had'} + past participle.")
        explanations.append(f"The {tense} is used to connect a past action to the present or another past time.")
    
    # Passive voice (is/are/was/were + past participle)
    if re.match(r'^(is|are|was|were|has been|have been|had been|will be)\s+\w+', correct):
        explanations.append("This sentence uses the passive voice.")
        explanations.append("Passive voice: subject + be verb + past participle (e.g., 'The cake was eaten').")
        explanations.append("We use passive when the action is more important than who does it.")
    
    # Comparative/Superlative
    if 'more' in correct or 'most' in correct or 'er' in correct[-3:] or 'est' in correct[-4:]:
        if 'most' in correct or 'est' in correct[-4:]:
            explanations.append("This is the superlative form, used to compare three or more things.")
            explanations.append("Superlative: 'the most + adjective' or 'adjective + est' (e.g., 'the tallest').")
        elif 'more' in correct or 'er' in correct[-3:]:
            explanations.append("This is the comparative form, used to compare two things.")
            explanations.append("Comparative: 'more + adjective' or 'adjective + er' (e.g., 'taller').")
    
    # Modals
    modals = {'can': 'ability', 'could': 'past ability or polite request', 'will': 'future intention',
              'would': 'conditional or polite request', 'should': 'advice or obligation',
              'must': 'strong obligation', 'might': 'possibility', 'may': 'permission or possibility'}
    if correct in modals:
        explanations.append(f"'{correct}' expresses {modals[correct]}.")
    
    # Default
    if not explanations:
        explanations.append(f"The correct answer is '{get_correct(q)}' because it fits the grammatical structure of the sentence.")
        explanations.append("Check the subject-verb agreement and the tense being used.")
    
    return ' '.join(explanations)

def error_detection_explanation(q):
    """Generate explanation for error detection questions."""
    en = q.get('question_en', '')
    correct = get_correct(q)
    opts = q.get('options_en', [])
    ans = q.get('answer', 0)
    
    # Extract the sentence from the question
    sent_match = re.search(r'["\u201c](.+?)["\u201d]', en)
    sentence = sent_match.group(1) if sent_match else ''
    
    explanations = []
    
    if 'correct' in correct.lower() or 'no error' in correct.lower() or 'no correction needed' in correct.lower():
        explanations.append(f"The sentence is grammatically correct as written.")
        explanations.append(f"All parts of the sentence follow standard English grammar rules.")
    else:
        # Find the error
        if 'in -> at' in correct.lower() or 'good at' in correct.lower():
            explanations.append("'Good at' is the correct collocation in English, not 'good in'.")
            explanations.append("We say 'good at English', 'good at math', 'good at sports'.")
        elif 'who' in correct.lower() and 'which' in sentence.lower():
            explanations.append("'Who' is used for people, 'which' is used for things.")
            explanations.append("Since we're referring to a person, 'who' is correct.")
        elif 'that' in correct.lower():
            explanations.append("'That' introduces a restrictive (defining) relative clause.")
        elif 'whom' in correct.lower():
            explanations.append("'Whom' is used as the object of a verb or preposition (formal English).")
        else:
            # General error explanation
            explanations.append(f"The error in the sentence should be corrected to: '{correct}'.")
            explanations.append("Look for subject-verb agreement, tense consistency, or word choice errors.")
    
    return ' '.join(explanations)

def tense_explanation(q):
    """Generate explanation for tense/type questions."""
    en = q.get('question_en', '').lower()
    correct = get_correct(q)
    
    tense_rules = {
        'present simple': "Present Simple is used for habits, facts, and general truths. Structure: subject + verb(s/es). Example: 'She plays tennis every day.'",
        'past simple': "Past Simple is used for completed actions in the past. Structure: subject + verb-ed (or irregular). Example: 'She played tennis yesterday.'",
        'present continuous': "Present Continuous is used for actions happening now or around now. Structure: subject + am/is/are + verb-ing. Example: 'She is playing tennis now.'",
        'past continuous': "Past Continuous was used for ongoing actions in the past. Structure: subject + was/were + verb-ing. Example: 'She was playing tennis when it rained.'",
        'present perfect': "Present Perfect connects past to present. Structure: subject + has/have + past participle. Example: 'She has played tennis since 2010.'",
        'past perfect': "Past Perfect shows an action completed before another past action. Structure: subject + had + past participle. Example: 'She had played tennis before she moved.'",
        'future': "Future tense is used for plans, predictions, and promises. Structure: subject + will + verb. Example: 'She will play tennis tomorrow.'",
        'first conditional': "First Conditional: If + present simple, will + verb. Used for real/likely future situations. Example: 'If it rains, I will stay home.'",
        'second conditional': "Second Conditional: If + past simple, would + verb. Used for unreal/hypothetical present situations. Example: 'If I were rich, I would travel.'",
        'third conditional': "Third Conditional: If + past perfect, would have + past participle. Used for unreal past situations. Example: 'If I had studied, I would have passed.'",
    }
    
    correct_lower = correct.lower().rstrip('.')
    for key, rule in tense_rules.items():
        if key in correct_lower:
            return rule
    
    return f"The correct answer is '{correct}'. Identify the time markers in the sentence to determine the appropriate tense."

def synonym_explanation(q):
    """Generate explanation for synonym questions."""
    correct = get_correct(q)
    en = q.get('question_en', '')
    word_match = re.search(r"['\u2018](.+?)['\u2019]", en)
    word = word_match.group(1) if word_match else 'the word'
    return f"'{correct}' has a similar meaning to '{word}'. Both words can be used interchangeably in this context."

def other_explanation(q):
    """Generate explanation for other question types."""
    correct = get_correct(q)
    return f"The correct answer is '{correct}'. Consider the context of the sentence and standard English usage."

# Process all questions
fixed = 0
for q in qs:
    expl = q.get('explanation_en', '')
    if len(expl) > 50:  # Already has good explanation
        continue
    
    en = q.get('question_en', '').lower()
    correct = get_correct(q).lower()
    
    if 'synonym' in en:
        new_expl = synonym_explanation(q)
    elif 'antonym' in en:
        new_expl = f"The antonym (opposite) of the word is '{get_correct(q)}'."
    elif 'error' in en or ('correct' in en and ('choose' in en or 'is this' in en or 'which' in en or 'find' in en)):
        new_expl = error_detection_explanation(q)
    elif 'tense' in en or 'what type' in en:
        new_expl = tense_explanation(q)
    elif '___' in en:
        new_expl = fill_blank_explanation(q)
    else:
        new_expl = other_explanation(q)
    
    q['explanation_en'] = new_expl
    # Also generate Chinese explanation
    q['explanation_zh'] = f"正確答案是「{get_correct(q)}」。" + new_expl
    fixed += 1

with open(fpath, 'w') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

# Also fix v2 copy
import shutil
shutil.copy2(fpath, '/Users/bruce/.openclaw/workspace/projects/project_03_bruce_institute_10000/uncle-bruce-10000/v2/english/s1/questions.json')

print(f"✅ Improved {fixed} explanations")

# Show samples
import random
for q in random.sample(qs, 5):
    print(f"\nQ: {q['question_en'][:60]}")
    print(f"A: {get_correct(q)[:40]}")
    print(f"Expl: {q['explanation_en'][:100]}")
