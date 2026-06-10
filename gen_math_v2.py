#!/usr/bin/env python3
"""
Hong Kong Secondary Math Question Generator v2
Generates questions with ACTUAL calculated answers and plausible distractors
"""
import json, hashlib, os, random, sys, math

CURRICULUM = {
    "S1": {
        "正負數": [
            {"type": "calc", "zh": "計算：{0} × {1} + {2}", "en": "Calculate: {0} × {1} + {2}",
             "gen": lambda: (random.randint(-12,12), random.randint(-12,12), random.randint(-30,30)),
             "calc": lambda p: p[0]*p[1]+p[2], "distractor": lambda p,v: [v+1, v-1, -v, v+random.choice([2,3,5])]},
            {"type": "calc", "zh": "計算：({0}) × ({1})", "en": "Calculate: ({0}) × ({1})",
             "gen": lambda: (random.randint(-15,15), random.randint(-15,15)),
             "calc": lambda p: p[0]*p[1], "distractor": lambda p,v: [v+1, v-1, -v, abs(v)]},
            {"type": "calc", "zh": "計算：{0} ÷ {1} - {2}", "en": "Calculate: {0} ÷ {1} - {2}",
             "gen": lambda: (random.choice([i*j for i in range(-10,11) for j in range(2,8) if j!=0]), random.randint(2,7), random.randint(-15,15)),
             "calc": lambda p: p[0]//p[1]-p[2], "distractor": lambda p,v: [v+1, v-1, p[0]//p[1]+p[2], -v]},
        ],
        "代數表達式": [
            {"type": "expr", "zh": "化簡：{0}x + {1}x", "en": "Simplify: {0}x + {1}x",
             "gen": lambda: (random.randint(2,15), random.randint(2,15)),
             "ans": lambda p: f"{p[0]+p[1]}x", "opts": lambda p: [f"{p[0]+p[1]}x", f"{p[0]-p[1]}x", f"{p[0]*p[1]}x", f"{abs(p[0]-p[1])}x"]},
            {"type": "expr", "zh": "展開：{0}(x + {1})", "en": "Expand: {0}(x + {1})",
             "gen": lambda: (random.randint(2,8), random.randint(1,12)),
             "ans": lambda p: f"{p[0]}x + {p[0]*p[1]}", "opts": lambda p: [f"{p[0]}x + {p[0]*p[1]}", f"{p[0]}x + {p[1]}", f"x + {p[0]*p[1]}", f"{p[0]}x - {p[0]*p[1]}"]},
        ],
        "一元一次方程": [
            {"type": "eq", "zh": "解方程：{0}x + {1} = {2}", "en": "Solve: {0}x + {1} = {2}",
             "gen": lambda: (random.randint(2,8), random.randint(1,20), None),
             "setup": lambda p: (p[0], p[1], p[0]*random.randint(1,10)+p[1]),
             "calc": lambda p: (p[2]-p[1])/p[0], "distractor": lambda p,v: [v+1, v-1, (p[2]+p[1])/p[0], v*2]},
        ],
        "百分數": [
            {"type": "pct", "zh": "{0} 的 {1}% 是多少？", "en": "What is {1}% of {0}?",
             "gen": lambda: (random.choice([50,100,200,250,400,500,800,1000]), random.choice([5,10,15,20,25,30,40,50])),
             "calc": lambda p: p[0]*p[1]/100, "distractor": lambda p,v: [v*10, v/10, p[0]-v, p[0]+v]},
            {"type": "pct", "zh": "一件物品原價 ${0}，加價 {1}% 後售價是多少？", "en": "An item costs ${0}. After {1}% increase, what is the price?",
             "gen": lambda: (random.choice([100,200,300,400,500,800]), random.choice([5,10,15,20,25,30])),
             "calc": lambda p: p[0]*(1+p[1]/100), "distractor": lambda p,v: [p[0]*p[1]/100, p[0]*(1-p[1]/100), v+p[0], v-p[0]]},
        ],
        "比與比率": [
            {"type": "ratio", "zh": "甲乙分 ${0}，比例 {1}:{2}，甲分得多少？", "en": "A and B share ${0} in ratio {1}:{2}. How much does A get?",
             "gen": lambda: (random.choice([120,150,180,200,240,300,360,450,600]), random.randint(1,5), random.randint(1,5)),
             "calc": lambda p: p[0]*p[1]/(p[1]+p[2]), "distractor": lambda p,v: [p[0]*p[2]/(p[1]+p[2]), p[0]/(p[1]+p[2]), v*2, p[0]-v]},
        ],
        "面積與體積": [
            {"type": "area", "zh": "長方形長 {0}cm，闊 {1}cm，求面積。", "en": "Rectangle: {0}cm × {1}cm. Find area.",
             "gen": lambda: (random.randint(5,30), random.randint(3,20)),
             "calc": lambda p: p[0]*p[1], "distractor": lambda p,v: [2*(p[0]+p[1]), p[0]+p[1], p[0]*p[1]+1, p[0]*p[1]-1]},
            {"type": "vol", "zh": "正方體邊長 {0}cm，求體積。", "en": "Cube side = {0}cm. Find volume.",
             "gen": lambda: (random.randint(2,8),),
             "calc": lambda p: p[0]**3, "distractor": lambda p,v: [p[0]**2, 3*p[0], 6*p[0]**2, v+1]},
            {"type": "area", "zh": "圓形半徑 {0}cm，求面積（取 π = 3.14）。", "en": "Circle radius = {0}cm. Find area (π = 3.14).",
             "gen": lambda: (random.choice([3,4,5,6,7,8,10]),),
             "calc": lambda p: round(3.14*p[0]**2,2), "distractor": lambda p,v: [round(2*3.14*p[0],2), round(3.14*p[0],2), round(3.14*p[0]**3,2), round(v/2,2)]},
        ],
        "統計圖表": [
            {"type": "stat", "zh": "五個數：{0},{1},{2},{3},{4}，求平均數。", "en": "Five numbers: {0},{1},{2},{3},{4}. Find mean.",
             "gen": lambda: tuple(random.sample(range(10,60),5)),
             "calc": lambda p: sum(p)/5, "distractor": lambda p,v: [sorted(p)[2], min(p), max(p), v+5]},
        ],
        "坐標": [
            {"type": "coord", "zh": "求點 ({0},{1}) 和原點的距離。", "en": "Find distance from ({0},{1}) to origin.",
             "gen": lambda: (random.choice([3,5,6,8,9,12]), random.choice([4,5,12,15])),
             "calc": lambda p: round((p[0]**2+p[1]**2)**0.5,2), "distractor": lambda p,v: [p[0]+p[1], abs(p[0]-p[1]), p[0]*p[1], round(v+1,2)]},
        ],
        "規律與數列": [
            {"type": "seq", "zh": "等差數列首項 {0}，公差 {1}，第5項是多少？", "en": "AP: first term {0}, common diff {1}. Find 5th term.",
             "gen": lambda: (random.randint(1,20), random.randint(2,10)),
             "calc": lambda p: p[0]+4*p[1], "distractor": lambda p,v: [p[0]+5*p[1], p[0]+3*p[1], p[0]*4*p[1], v+1]},
        ],
    },
    "S2": {
        "指數與根式": [
            {"type": "idx", "zh": "化簡：{0}² × {0}³", "en": "Simplify: {0}² × {0}³",
             "gen": lambda: (random.randint(2,6),),
             "calc": lambda p: p[0]**5, "distractor": lambda p,v: [p[0]**6, p[0]**4, p[0]**2+p[0]**3, v*p[0]]},
            {"type": "surd", "zh": "化簡：√{0}", "en": "Simplify: √{0}",
             "gen": lambda: (random.choice([4,9,16,25,36,49,64,81,100,144,225]),),
             "calc": lambda p: int(p[0]**0.5), "distractor": lambda p,v: [v*2, v+1, p[0]//2, v-1]},
        ],
        "多項式": [
            {"type": "poly", "zh": "展開：(x + {0})(x + {1})", "en": "Expand: (x + {0})(x + {1})",
             "gen": lambda: (random.randint(1,8), random.randint(1,8)),
             "ans": lambda p: f"x² + {p[0]+p[1]}x + {p[0]*p[1]}", "opts": lambda p: [f"x² + {p[0]+p[1]}x + {p[0]*p[1]}", f"x² + {p[0]*p[1]}x + {p[0]+p[1]}", f"x² - {p[0]+p[1]}x + {p[0]*p[1]}", f"x² + {p[0]+p[1]}x - {p[0]*p[1]}"]},
        ],
        "畢氏定理": [
            {"type": "pyth", "zh": "直角三角形兩邊 {0}cm 和 {1}cm，求斜邊。", "en": "Right triangle sides {0}cm and {1}cm. Find hypotenuse.",
             "gen": lambda: (random.choice([(3,4),(5,12),(6,8),(8,15),(9,12),(12,16),(7,24),(15,20)])),
             "calc": lambda p: (p[0]**2+p[1]**2)**0.5, "distractor": lambda p,v: [p[0]+p[1], abs(p[0]-p[1]), p[0]*p[1], round(v+2,1)]},
        ],
        "座標幾何": [
            {"type": "dist", "zh": "求 ({0},{1}) 和 ({2},{3}) 的距離。", "en": "Distance between ({0},{1}) and ({2},{3}).",
             "gen": lambda: tuple(random.sample(range(-8,9),4)),
             "calc": lambda p: round(((p[0]-p[2])**2+(p[1]-p[3])**2)**0.5,2),
             "distractor": lambda p,v: [abs(p[0]-p[2])+abs(p[1]-p[3]), round(v+2,2), round(v-2,2), round(v*2,2)]},
        ],
        "一元一次不等式": [
            {"type": "ineq", "zh": "解不等式：{0}x + {1} > {2}", "en": "Solve: {0}x + {1} > {2}",
             "gen": lambda: (random.randint(2,6), random.randint(1,15), random.randint(20,50)),
             "calc": lambda p: (p[2]-p[1])/p[0],
             "distractor": lambda p,v: [v+1, v-1, (p[2]+p[1])/p[0], v/2]},
        ],
        "角與平行線": [
            {"type": "angle", "zh": "兩平行線被截線所截，一角為 {0}°，其同位角是多少度？", "en": "Parallel lines cut by transversal. One angle = {0}°. Find corresponding angle.",
             "gen": lambda: (random.choice([30,35,40,45,50,55,60,65,70,75,80,100,110,120,130,135,140,150]),),
             "calc": lambda p: p[0], "distractor": lambda p,v: [180-p[0], 360-p[0], 90-p[0], p[0]+90]},
        ],
    },
    "S3": {
        "二次方程": [
            {"type": "quad", "zh": "解方程：x² + {0}x + {1} = 0", "en": "Solve: x² + {0}x + {1} = 0",
             "gen": lambda: (random.randint(-10,10), random.randint(-20,20)),
             "disc": lambda p: p[0]**2-4*p[1],
             "calc": lambda p: (-p[0]+(p[0]**2-4*p[1])**0.5)/2 if p[0]**2-4*p[1]>=0 else None,
             "distractor": lambda p,v: [v+1, v-1, -v, (-p[0]-(p[0]**2-4*p[1])**0.5)/2 if p[0]**2-4*p[1]>=0 else v+2]},
        ],
        "三角比": [
            {"type": "trig", "zh": "直角三角形，對邊 {0}cm，鄰邊 {1}cm，求 tan θ。", "en": "Right triangle: opposite={0}cm, adjacent={1}cm. Find tan θ.",
             "gen": lambda: (random.randint(1,15), random.randint(1,15)),
             "calc": lambda p: round(p[0]/p[1],2), "distractor": lambda p,v: [round(p[1]/p[0],2), round((p[0]**2+p[1]**2)**0.5,2), round(v+0.5,2), round(v-0.5,2)]},
        ],
        "概率": [
            {"type": "prob", "zh": "袋中 {0} 個紅球和 {1} 個藍球，抽中紅球的概率？", "en": "Bag: {0} red, {1} blue. P(red)?",
             "gen": lambda: (random.randint(1,8), random.randint(1,8)),
             "calc": lambda p: round(p[0]/(p[0]+p[1]),4), "distractor": lambda p,v: [round(p[1]/(p[0]+p[1]),4), round(1-v,4), round(v/2,4), round(v*2,4)]},
        ],
    },
    "S4": {
        "三角函數": [
            {"type": "trig", "zh": "求 sin 30° 的值。", "en": "Find sin 30°.", "gen": lambda: (),
             "calc": lambda p: 0.5, "distractor": lambda p,v: [0.866, 1, 0, 0.707]},
            {"type": "trig", "zh": "求 cos 60° 的值。", "en": "Find cos 60°.", "gen": lambda: (),
             "calc": lambda p: 0.5, "distractor": lambda p,v: [0.866, 1, 0, 0.707]},
        ],
        "指數函數與對數": [
            {"type": "log", "zh": "化簡：log₂32", "en": "Simplify: log₂32", "gen": lambda: (),
             "calc": lambda p: 5, "distractor": lambda p,v: [4, 6, 32, 16]},
            {"type": "log", "zh": "化簡：log₁₀1000", "en": "Simplify: log₁₀1000", "gen": lambda: (),
             "calc": lambda p: 3, "distractor": lambda p,v: [2, 4, 100, 10]},
        ],
        "排列與組合": [
            {"type": "perm", "zh": "P({0},{1}) = ?", "en": "P({0},{1}) = ?",
             "gen": lambda: (random.randint(4,8), random.randint(2,4)),
             "calc": lambda p: math.perm(p[0],p[1]), "distractor": lambda p,v: [v+1, v-1, math.comb(p[0],p[1]), v*2]},
        ],
    },
    "S5": {
        "微分": [
            {"type": "diff", "zh": "求 f(x) = {0}x³ + {1}x² 的 f'(x)。", "en": "Find f'(x) if f(x) = {0}x³ + {1}x².",
             "gen": lambda: (random.randint(1,5), random.randint(1,8)),
             "ans": lambda p: f"{3*p[0]}x² + {2*p[1]}x",
             "opts": lambda p: [f"{3*p[0]}x² + {2*p[1]}x", f"{p[0]}x² + {p[1]}x", f"{3*p[0]}x³ + {2*p[1]}x²", f"{3*p[0]}x + {2*p[1]}"]},
        ],
        "積分": [
            {"type": "int", "zh": "求 ∫({0}x² + {1})dx", "en": "Find ∫({0}x² + {1})dx",
             "gen": lambda: (random.randint(1,6), random.randint(1,10)),
             "ans": lambda p: f"{p[0]}x³/3 + {p[1]}x + C",
             "opts": lambda p: [f"{p[0]}x³/3 + {p[1]}x + C", f"{p[0]}x² + {p[1]}x + C", f"{p[0]}x³ + {p[1]}x + C", f"{2*p[0]}x³/3 + {p[1]}x + C"]},
        ],
        "向量": [
            {"type": "vec", "zh": "a=({0},{1}), b=({2},{3}), 求 a+b。", "en": "a=({0},{1}), b=({2},{3}), find a+b.",
             "gen": lambda: tuple(random.randint(-5,5) for _ in range(4)),
             "ans": lambda p: f"({p[0]+p[2]},{p[1]+p[3]})",
             "opts": lambda p: [f"({p[0]+p[2]},{p[1]+p[3]})", f"({p[0]-p[2]},{p[1]-p[3]})", f"({p[0]*p[2]},{p[1]*p[3]})", f"({p[2]-p[0]},{p[3]-p[1]})"]},
        ],
    },
    "S6": {
        "DSE 模擬 - 代數": [
            {"type": "alg", "zh": "若 f(x) = {0}x² - {1}x + {2}，求 f({3})。", "en": "If f(x) = {0}x² - {1}x + {2}, find f({3}).",
             "gen": lambda: (random.randint(1,4), random.randint(1,8), random.randint(0,5), random.randint(1,5)),
             "calc": lambda p: p[0]*p[3]**2-p[1]*p[3]+p[2],
             "distractor": lambda p,v: [v+1, v-1, -v, v*2]},
        ],
        "DSE 模擬 - 微積分": [
            {"type": "calc", "zh": "曲線 y=x³-{0}x 在 x={1} 處的切線斜率？", "en": "Slope of tangent to y=x³-{0}x at x={1}?",
             "gen": lambda: (random.randint(1,6), random.randint(1,3)),
             "calc": lambda p: 3*p[1]**2-p[0],
             "distractor": lambda p,v: [v+1, v-1, p[1]**3-p[0]*p[1], 3*p[1]**2+p[0]]},
        ],
        "DSE 模擬 - 統計與概率": [
            {"type": "stat", "zh": "數據 {0},{1},{2},{3},{4} 的標準差約為？", "en": "Find std dev of {0},{1},{2},{3},{4}.",
             "gen": lambda: tuple(random.sample(range(10,50),5)),
             "calc": lambda p: round((sum((x-sum(p)/5)**2 for x in p)/5)**0.5,2),
             "distractor": lambda p,v: [round(v+2,2), round(v-2,2), round(v*2,2), round(max(p)-min(p),2)]},
        ],
    }
}

def generate_questions(subject, form, count, start_id=1):
    """Generate questions with real answers."""
    topics = CURRICULUM.get(form, {})
    all_q = []
    seen = set()
    
    # Load existing to avoid dupes
    filepath = f"math/{form.lower()}/questions.json"
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            d = json.load(f)
            for q in (d if isinstance(d,list) else d.get('questions',[])):
                seen.add(hashlib.md5((q.get('question_zh','') or q.get('question','')).encode()).hexdigest())
    
    # Weight distribution
    total_templates = sum(len(v) for v in topics.values())
    per_topic = {k: max(1, count*len(v)//total_templates) for k,v in topics.items()}
    
    qid = start_id
    for topic_name, templates in topics.items():
        target = per_topic[topic_name]
        generated = 0
        attempts = 0
        while generated < target and attempts < target*3:
            attempts += 1
            tmpl = random.choice(templates)
            
            try:
                params = tmpl["gen"]()
                
                # For templates with setup (like equations)
                if "setup" in tmpl:
                    params = tmpl["setup"](params)
                
                q_zh = tmpl["zh"].format(*params)
                q_en = tmpl["en"].format(*params)
                
                # Calculate answer
                if "calc" in tmpl:
                    val = tmpl["calc"](params)
                    if val is None: continue
                    if isinstance(val, float):
                        val = round(val, 2)
                    correct = str(val)
                    distractors = tmpl["distractor"](params, val)
                    opts = [correct] + [str(round(d,2) if isinstance(d,float) else d) for d in distractors[:3]]
                elif "ans" in tmpl:
                    correct = tmpl["ans"](params)
                    opts = tmpl["opts"](params)
                else:
                    continue
                
                # Shuffle options
                correct_idx = 0
                combined = list(zip(range(4), opts))
                random.shuffle(combined)
                correct_idx = next(i for i,(orig,_) in enumerate(combined) if orig==0)
                opts_shuffled = [o for _,o in combined]
                
                h = hashlib.md5(q_zh.encode()).hexdigest()
                if h in seen: continue
                seen.add(h)
                
                diff = 1 if generated < target*0.4 else (2 if generated < target*0.7 else 3)
                
                all_q.append({
                    "id": qid,
                    "topic_zh": topic_name,
                    "topic_en": topic_name,
                    "subtopic_zh": "",
                    "subtopic_en": "",
                    "question_zh": q_zh,
                    "question_en": q_en,
                    "options_zh": opts_shuffled,
                    "options_en": opts_shuffled,
                    "answer": correct_idx,
                    "explanation_zh": f"此題考查「{topic_name}」。正確答案是 {correct}。",
                    "explanation_en": f"This tests '{topic_name}'. The correct answer is {correct}.",
                    "difficulty": diff
                })
                qid += 1
                generated += 1
            except Exception:
                continue
    
    random.shuffle(all_q)
    for i,q in enumerate(all_q):
        q["id"] = start_id + i
    return all_q


def save(subject, form, questions):
    filepath = f"math/{form.lower()}/questions.json"
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
    if len(sys.argv) < 3:
        print("Usage: python3 gen_math_v2.py <form> <count>")
        sys.exit(1)
    form = sys.argv[1]
    count = int(sys.argv[2])
    
    filepath = f"math/{form.lower()}/questions.json"
    start = 1
    if os.path.exists(filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            d = json.load(f)
            start = len(d if isinstance(d,list) else d.get('questions',[])) + 1
    
    print(f"Generating {count} math questions for {form} (from #{start})...")
    qs = generate_questions("math", form, count, start)
    total = save("math", form, qs)
    print(f"Done! Generated {len(qs)} questions. Total: {total}")
