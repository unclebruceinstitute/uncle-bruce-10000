#!/usr/bin/env python3
"""
Hong Kong Secondary Chinese Question Generator
Template-based with proper explanations
"""
import json, hashlib, os, random, sys

CURRICULUM = {
    "S1": {
        "字詞辨析": [
            {"q": "「他＿經走遠了。」應填：", "opts": ["已", "己", "以", "几"], "ans": 0, "exp": "「已」表示已經。「己」是自己。", "exp_en": "'已' = already. '己' = self."},
            {"q": "「這是自＿的事情。」應填：", "opts": ["已", "己", "以", "几"], "ans": 1, "exp": "「己」是自己。「已」是已經。", "exp_en": "'己' = self. '已' = already."},
            {"q": "「我們要＿別是非。」應填：", "opts": ["辨", "辯", "辮", "瓣"], "ans": 0, "exp": "「辨」是辨別。「辯」是辯論。「辮」是辮子。「瓣」是花瓣。", "exp_en": "'辨' = distinguish. '辯' = debate. '辮' = braid. '瓣' = petal."},
            {"q": "「他的＿氣很好。」應填：", "opts": ["運", "韻", "暈", "蘊"], "ans": 0, "exp": "「運氣」指命運、幸運。「韻」是韻律。", "exp_en": "'運氣' = luck/fate. '韻' = rhythm."},
        ],
        "成語運用": [
            {"q": "「畫畫得栩栩如生」中的「栩栩如生」意思是：", "opts": ["很生氣", "非常逼真", "很無聊", "很快樂"], "ans": 1, "exp": "「栩栩如生」形容描寫或模仿非常逼真，像真的一樣。", "exp_en": "'栩栩如生' means lifelike, very realistic."},
            {"q": "以下哪個成語使用正確？", "opts": ["他做事一絲不苟", "他做事一絲不掛", "他做事一成不變", "他做事一目十行"], "ans": 0, "exp": "「一絲不苟」形容做事認真，一點不馬虎。", "exp_en": "'一絲不苟' = very careful and meticulous."},
            {"q": "「守株待兔」比喻什麼？", "opts": ["勤勞工作", "等待機會不勞而獲", "保護樹木", "打獵技巧"], "ans": 1, "exp": "「守株待兔」比喻不勞而獲或死守經驗。", "exp_en": "'守株待兔' = waiting for a windfall without effort."},
        ],
        "修辭手法": [
            {"q": "「月亮像一個銀盤」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "排比"], "ans": 0, "exp": "「像」是比喻詞，將月亮比作銀盤，是明喻。", "exp_en": "'像' = comparison word. Simile: moon compared to silver plate."},
            {"q": "「花兒在微笑」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "對偶"], "ans": 1, "exp": "「微笑」是人的動作，用在花上是擬人。", "exp_en": "'微笑' = human action applied to flowers = personification."},
            {"q": "「飛流直下三千尺」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "排比"], "ans": 2, "exp": "「三千尺」是誇張手法，形容瀑布極長。", "exp_en": "'三千尺' = hyperbole, exaggerating the waterfall's height."},
        ],
        "文言文基礎": [
            {"q": "「之」在古文中通常代表：", "opts": ["的/它", "和", "在", "是"], "ans": 0, "exp": "「之」常用作助詞（的）或代詞（它/他）。", "exp_en": "'之' = particle (of) or pronoun (it/him) in classical Chinese."},
            {"q": "「吾」的意思是：", "opts": ["你", "我", "他", "她"], "ans": 1, "exp": "「吾」是文言文中的第一人稱，意思是「我」。", "exp_en": "'吾' = first person pronoun 'I' in classical Chinese."},
        ],
        "標點符號": [
            {"q": "「今天天氣真好＿」應填什麼標點？", "opts": ["。", "，", "！", "？"], "ans": 2, "exp": "感嘆句用「！」。", "exp_en": "Exclamatory sentences use '!'. '！' = exclamation mark."},
            {"q": "「你吃飯了嗎＿」應填什麼標點？", "opts": ["。", "，", "！", "？"], "ans": 3, "exp": "疑問句用「？」。", "exp_en": "Questions use '?'. '？' = question mark."},
        ],
        "詞性辨別": [
            {"q": "「快速」是什麼詞性？", "opts": ["名詞", "動詞", "形容詞", "副詞"], "ans": 2, "exp": "「快速」修飾動作，是形容詞（也可作副詞）。", "exp_en": "'快速' = adjective (also adverb) describing speed."},
            {"q": "「奔跑」是什麼詞性？", "opts": ["名詞", "動詞", "形容詞", "副詞"], "ans": 1, "exp": "「奔跑」是動作，是動詞。", "exp_en": "'奔跑' = verb, to run."},
        ],
        "病句修改": [
            {"q": "以下哪句是病句？", "opts": ["他非常努力學習", "他的成績提高了很大", "我們要愛護環境", "今天天氣很好"], "ans": 1, "exp": "「提高了很大」搭配不當，應為「提高了很多」。", "exp_en": "'提高了很大' is wrong collocation. Should be '提高了很多'."}
        ],
        "文化常識": [
            {"q": "「春節」是中國農曆的哪一天？", "opts": ["正月初一", "正月十五", "十二月三十", "九月初九"], "ans": 0, "exp": "春節是農曆正月初一，即新年第一天。", "exp_en": "Spring Festival = 1st day of Chinese New Year (正月初一)."},
            {"q": "「中秋節」傳統吃什麼？", "opts": ["粽子", "月餅", "湯圓", "餃子"], "ans": 1, "exp": "中秋節吃月餅，象徵團圓。", "exp_en": "Mid-Autumn Festival: eat mooncakes (月餅), symbolizing reunion."},
        ],
    },
    "S2": {
        "文言文閱讀": [
            {"q": "「學而時習之」出自哪本書？", "opts": ["《孟子》", "《論語》", "《老子》", "《莊子》"], "ans": 1, "exp": "出自《論語》，孔子說的，意思是學習後要經常溫習。", "exp_en": "From《論語》(Analerta of Confucius). 'Learn and review regularly.'"},
        ],
        "成語典故": [
            {"q": "「臥薪嘗膽」形容什麼？", "opts": ["享受生活", "刻苦自勵", "膽小怕事", "品嚐美食"], "ans": 1, "exp": "越王勾踐的故事，形容刻苦自勵，發憤圖強。", "exp_en": "Story of King Goujian. Means enduring hardship to achieve a goal."},
        ],
        "古詩詞鑑賞": [
            {"q": "「床前明月光」的作者是？", "opts": ["杜甫", "李白", "白居易", "王維"], "ans": 1, "exp": "李白的《靜夜思》。", "exp_en": "Li Bai's 'Quiet Night Thought' (靜夜思)."},
        ],
    },
    "S3": {
        "議論文閱讀": [
            {"q": "議論文的三要素是什麼？", "opts": ["時間地點人物", "論點論據論證", "開頭經過結尾", "起因經過結果"], "ans": 1, "exp": "議論文三要素：論點（觀點）、論據（證據）、論證（推理過程）。", "exp_en": "Three elements of argumentation: thesis, evidence, reasoning."},
        ],
        "DSE 核心字詞": [
            {"q": "「鍥而不捨」的「鍥」讀音是：", "opts": ["qì", "qiè", "jié", "xiē"], "ans": 1, "exp": "「鍥」讀 qiè，意思是雕刻。鍥而不捨 = 堅持不懈。", "exp_en": "'鍥' pronounced qiè, means carve. 鍥而不捨 = persevere."},
        ],
    },
    "S4": {
        "DSE 卷一練習": [
            {"q": "以下哪項不是說明方法？", "opts": ["舉例子", "列數字", "作比較", "抒情"], "ans": 3, "exp": "抒情是表達方式，不是說明方法。說明方法包括舉例子、列數字、作比較等。", "exp_en": "抒情 (express emotion) is not an expository method. Methods include examples, statistics, comparison."},
        ],
    },
    "S5": {
        "DSE 模擬卷一": [
            {"q": "「先天下之憂而憂」出自哪篇文章？", "opts": ["《出師表》", "《岳陽樓記》", "《醉翁亭記》", "《滕王閣序》"], "ans": 1, "exp": "范仲淹《岳陽樓記》。表達憂國憂民的情懷。", "exp_en": "From Fan Zhongyan's 'Yueyang Tower Record'. Expresses concern for the nation."},
        ],
    },
    "S6": {
        "DSE 全真模擬卷一": [
            {"q": "「落霞與孤鶩齊飛」的下一句是：", "opts": ["秋水共長天一色", "月落烏啼霜滿天", "兩個黃鸝鳴翠柳", "春風又綠江南岸"], "ans": 0, "exp": "王勃《滕王閣序》。描寫壯麗的自然景色。", "exp_en": "From Wang Bo's 'Tengwang Pavilion Preface'. Describes magnificent scenery."},
        ],
    }
}

def generate_questions(form, count, start_id=1):
    topics = CURRICULUM.get(form, {})
    all_q = []
    seen = set()
    
    filepath = f"chinese/{form.lower()}/questions.json"
    if os.path.exists(filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            d = json.load(f)
            for q in (d if isinstance(d,list) else d.get('questions',[])):
                seen.add(hashlib.md5((q.get('question_zh','') or q.get('question','')).encode()).hexdigest())
    
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
                continue
            seen.add(h)
            diff = 1 if generated < per_topic * 0.4 else (2 if generated < per_topic * 0.7 else 3)
            
            all_q.append({
                "id": qid,
                "topic_zh": topic,
                "topic_en": topic,
                "subtopic_zh": "",
                "subtopic_en": "",
                "question_zh": tmpl["q"],
                "question_en": tmpl["q"],
                "options_zh": tmpl["opts"],
                "options_en": tmpl["opts"],
                "answer": tmpl["ans"],
                "explanation_zh": tmpl["exp"],
                "explanation_en": tmpl.get("exp_en", ""),
                "difficulty": diff
            })
            qid += 1
            generated += 1
    
    random.shuffle(all_q)
    for i,q in enumerate(all_q):
        q["id"] = start_id + i
    return all_q

def save(form, questions):
    filepath = f"chinese/{form.lower()}/questions.json"
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
    filepath = f"chinese/{form.lower()}/questions.json"
    start = 1
    if os.path.exists(filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            d = json.load(f)
            start = len(d if isinstance(d,list) else d.get('questions',[])) + 1
    print(f"Generating {count} Chinese questions for {form}...")
    qs = generate_questions(form, count, start)
    total = save(form, qs)
    print(f"Done! Generated {len(qs)}. Total: {total}")
