#!/usr/bin/env python3
"""
Bulk question generator using variation from existing S1 questions.
Takes S1 questions and creates S2-S6 variations with different contexts.
"""
import json, hashlib, os, random, sys, copy

NAMES_EN = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack",
            "Kate", "Leo", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Rose", "Sam", "Tina"]
NAMES_ZH = ["小明", "小紅", "小華", "小強", "小美", "小偉", "小玲", "小杰", "小芳", "小龍",
            "小雲", "小寶", "小鳳", "小豪", "小珊", "小文", "小玉", "小輝", "小蘭", "小德"]

PLACES_EN = ["school", "library", "park", "museum", "hospital", "station", "market", "zoo", "beach", "airport"]
PLACES_ZH = ["學校", "圖書館", "公園", "博物館", "醫院", "車站", "市場", "動物園", "海灘", "機場"]

ITEMS_EN = ["book", "pen", "apple", "chair", "table", "phone", "bag", "cup", "key", "hat"]
ITEMS_ZH = ["書本", "筆", "蘋果", "椅子", "桌子", "電話", "書包", "杯子", "鑰匙", "帽子"]

def load_questions(subject, form):
    filepath = f"{subject}/{form.lower()}/questions.json"
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        d = json.load(f)
        return d if isinstance(d, list) else d.get('questions', [])

def save_questions(subject, form, questions):
    filepath = f"{subject}/{form.lower()}/questions.json"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"total_questions": len(questions), "questions": questions}, f, ensure_ascii=False, indent=1)

def vary_english_question(q, new_id, target_form):
    """Create a variation of an English question."""
    new_q = copy.deepcopy(q)
    new_q["id"] = new_id
    
    # Replace names
    question = q.get("question", "")
    for name in ["Tom", "Mary", "John", "Jane"]:
        if name in question:
            new_name = random.choice(NAMES_EN)
            question = question.replace(name, new_name)
    
    # Replace places
    for place in ["school", "home", "park"]:
        if place in question:
            new_place = random.choice(PLACES_EN)
            question = question.replace(place, new_place)
    
    new_q["question"] = question
    
    # Adjust difficulty based on form
    form_diff = {"S2": 1, "S3": 2, "S4": 2, "S5": 3, "S6": 3}
    new_q["difficulty"] = form_diff.get(target_form, 2)
    
    return new_q

def vary_chinese_question(q, new_id, target_form):
    """Create a variation of a Chinese question."""
    new_q = copy.deepcopy(q)
    new_q["id"] = new_id
    
    question = q.get("question_zh", "") or q.get("question", "")
    
    # Replace names
    for name in ["小明", "小紅", "小華"]:
        if name in question:
            new_name = random.choice(NAMES_ZH)
            question = question.replace(name, new_name)
    
    new_q["question_zh"] = question
    new_q["question_en"] = question
    
    form_diff = {"S2": 1, "S3": 2, "S4": 2, "S5": 3, "S6": 3}
    new_q["difficulty"] = form_diff.get(target_form, 2)
    
    return new_q

def generate_variations(subject, target_form, target_count):
    """Generate questions for target_form by varying S1 questions."""
    # Load S1 as base
    s1_questions = load_questions(subject, "S1")
    if not s1_questions:
        print(f"No S1 {subject} questions found!")
        return []
    
    # Load existing target form questions
    existing = load_questions(subject, target_form)
    seen = set()
    for q in existing:
        key = q.get("question_zh", "") or q.get("question", "") or q.get("question", "")
        seen.add(hashlib.md5(key.encode()).hexdigest())
    
    vary_func = vary_chinese_question if subject == "chinese" else vary_english_question
    
    new_questions = []
    attempts = 0
    max_attempts = target_count * 5
    
    while len(new_questions) < target_count and attempts < max_attempts:
        attempts += 1
        base = random.choice(s1_questions)
        new_id = len(existing) + len(new_questions) + 1
        
        varied = vary_func(base, new_id, target_form)
        
        key = varied.get("question_zh", "") or varied.get("question", "")
        h = hashlib.md5(key.encode()).hexdigest()
        
        if h not in seen:
            seen.add(h)
            new_questions.append(varied)
    
    return new_questions

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 gen_variations.py <subject> <form> <count>")
        sys.exit(1)
    
    subject = sys.argv[1]
    form = sys.argv[2]
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 500
    
    print(f"Generating {count} {subject} variations for {form}...")
    new_qs = generate_variations(subject, form, count)
    
    existing = load_questions(subject, form)
    all_qs = existing + new_qs
    save_questions(subject, form, all_qs)
    
    print(f"Done! Generated {len(new_qs)} new. Total: {len(all_qs)}")
