#!/usr/bin/env python3
"""Improve math S1 explanations with step-by-step working."""
import json
import re

with open('s1/questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data if isinstance(data, list) else data.get('questions', [])
improved = 0

for q in questions:
    expl = q.get('explanation_zh', '') or q.get('explanation', '')
    if len(expl) > 60:  # Already detailed enough
        continue
    
    question_text = q.get('question_zh', '') or q.get('question', '')
    opts = q.get('options_zh', []) or q.get('options', [])
    ans_idx = q.get('answer', 0)
    if isinstance(ans_idx, str):
        ans_idx = 'ABCD'.upper().find(ans_idx.upper())
    correct = opts[ans_idx] if ans_idx < len(opts) else ''
    topic = q.get('topic_zh', '') or q.get('topic', '')
    subtopic = q.get('subtopic_zh', '') or q.get('subtopic', '')
    
    new_expl = ''
    
    # Pattern: arithmetic calculation (計算 ...)
    if '計算' in question_text:
        # Extract the expression
        expr = question_text.replace('計算', '').strip()
        new_expl = f"題目要求計算：{expr}\n"
        
        # Try to explain step by step
        if '×' in expr or '÷' in expr:
            new_expl += "記住運算順序：先乘除，後加減（BODMAS 法則）。\n"
        if '-' in expr and ('×' in expr or '÷' in expr):
            new_expl += "注意負數的運算規則：\n"
            new_expl += "• 負 × 正 = 負\n• 負 × 負 = 正\n• 正 × 負 = 負\n"
        new_expl += f"答案是 {correct}。"
    
    # Pattern: fill in the blank (填入)
    elif '填入' in question_text or '填上' in question_text:
        new_expl = f"此題考查詞語運用。\n正確答案是「{correct}」。\n"
        if topic:
            new_expl += f"相關知識點：{topic}"
    
    # Pattern: which is correct/incorrect
    elif '正確' in question_text or '不正確' in question_text:
        new_expl = f"此題要求判斷正誤。\n正確答案是：{correct}\n"
        if topic:
            new_expl += f"考查範圍：{topic}"
    
    # Default improvement
    else:
        if topic and subtopic:
            new_expl = f"此題考查「{topic}」中的「{subtopic}」。\n正確答案是 {correct}。"
        elif topic:
            new_expl = f"此題考查「{topic}」。\n正確答案是 {correct}。"
        else:
            new_expl = f"正確答案是 {correct}。"
    
    if 'explanation_zh' in q:
        q['explanation_zh'] = new_expl
    else:
        q['explanation'] = new_expl
    
    # Add English explanation
    q['explanation_en'] = f"The correct answer is {correct}."
    if topic:
        q['explanation_en'] += f" Topic: {topic}."
    
    improved += 1

# Save
with open('s1/questions.json', 'w', encoding='utf-8') as f:
    if isinstance(data, list):
        json.dump(questions, f, ensure_ascii=False, indent=1)
    else:
        data['questions'] = questions
        json.dump(data, f, ensure_ascii=False, indent=1)

print(f"Improved {improved} explanations out of {len(questions)} questions")
