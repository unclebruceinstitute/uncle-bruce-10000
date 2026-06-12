#!/usr/bin/env python3
"""
Reshuffle math S2-S6 questions to avoid consecutive same-topic.
Same round-robin approach as gen_math_v3.py.
"""
import json, os, random

def round_robin_shuffle(data, target=10000):
    """Round-robin shuffle: NO consecutive same topic."""
    # Group by topic_id
    by_topic = {}
    for q in data:
        tid = q.get('topic_id', '')
        if tid not in by_topic:
            by_topic[tid] = []
        by_topic[tid].append(q)
    
    for tid in by_topic:
        random.shuffle(by_topic[tid])
    
    topic_items = list(by_topic.items())
    if not topic_items:
        return data
    
    # Strict round-robin
    min_count = min(len(qs) for _, qs in topic_items)
    result = []
    for r in range(min_count):
        round_qs = [qs[r] for _, qs in topic_items]
        random.shuffle(round_qs)
        result.extend(round_qs)
    
    # Insert extras
    extras = []
    for tid, qs in topic_items:
        extras.extend(qs[min_count:])
    random.shuffle(extras)
    
    for q in extras:
        q_tid = q.get('topic_id', '')
        inserted = False
        step = max(1, len(result) // (len(extras) + 1))
        start = random.randint(0, min(step, len(result)))
        for pos in range(start, len(result) + 1, step):
            prev_ok = pos == 0 or result[pos - 1].get('topic_id', '') != q_tid
            next_ok = pos >= len(result) or result[pos].get('topic_id', '') != q_tid
            if prev_ok and next_ok:
                result.insert(pos, q)
                inserted = True
                break
        if not inserted:
            for pos in range(len(result) + 1):
                prev_ok = pos == 0 or result[pos - 1].get('topic_id', '') != q_tid
                next_ok = pos >= len(result) or result[pos].get('topic_id', '') != q_tid
                if prev_ok and next_ok:
                    result.insert(pos, q)
                    inserted = True
                    break
        if not inserted:
            result.append(q)
    
    # Fix remaining consecutive pairs
    for _ in range(500):
        fixed_all = True
        for i in range(1, len(result)):
            if result[i].get('topic_id', '') == result[i-1].get('topic_id', ''):
                fixed_all = False
                for j in range(i+1, min(i+500, len(result))):
                    jt = result[j].get('topic_id', '')
                    if jt == result[i-1].get('topic_id', ''):
                        continue
                    if j+1 < len(result) and jt == result[j+1].get('topic_id', ''):
                        continue
                    if j-1 >= 0 and result[j-1].get('topic_id', '') == result[i].get('topic_id', ''):
                        continue
                    result[i], result[j] = result[j], result[i]
                    break
                break
        if fixed_all:
            break
    
    # Trim and re-assign IDs
    result = result[:target]
    for i, q in enumerate(result):
        q['id'] = i + 1
    
    return result


def verify(data, name):
    """Print verification."""
    max_run = 0
    cur_topic = None
    cur_len = 0
    for q in data:
        t = q.get('topic_id', '')
        if t == cur_topic:
            cur_len += 1
        else:
            max_run = max(max_run, cur_len)
            cur_topic = t
            cur_len = 1
    max_run = max(max_run, cur_len)
    
    q_texts = [q.get('question_zh', '') for q in data]
    dupes = len(q_texts) - len(set(q_texts))
    
    from collections import Counter
    topics = Counter(q.get('topic_id', '') for q in data)
    
    print(f'\n=== {name} ===')
    print(f'Total: {len(data)}')
    print(f'Max consecutive same-topic: {max_run}')
    print(f'Duplicates: {dupes}')
    print(f'Topics: {len(topics)}')
    for t, c in topics.most_common():
        print(f'  {t}: {c}')


if __name__ == '__main__':
    for level in ['s2', 's3', 's4', 's5', 's6']:
        filepath = f'math/{level}/questions.json'
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        qs = data.get('questions', data) if isinstance(data, dict) else data
        
        print(f'\nReshuffling math/{level} ({len(qs)} questions)...')
        reshuffled = round_robin_shuffle(qs)
        verify(reshuffled, f'math/{level}')
        
        # Save (overwrite as array)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(reshuffled, f, ensure_ascii=False, indent=1)
        
        # Also save to v2 if exists
        v2_path = f'v2/{filepath}'
        if os.path.exists(v2_path):
            with open(v2_path, 'w', encoding='utf-8') as f:
                json.dump(reshuffled, f, ensure_ascii=False, indent=1)
        
        print(f'  Saved to {filepath}')
    
    print('\nDone!')
