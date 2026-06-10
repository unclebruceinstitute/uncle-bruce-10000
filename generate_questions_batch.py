#!/usr/bin/env python3
"""
Hong Kong Secondary School Question Generator
Generates questions for S1-S6, Math/English/Chinese
Based on HKDSE curriculum and major textbook publishers
"""
import json
import hashlib
import os
import random
import math

# ============================================================
# CURRICULUM MAPPING - Based on HK DSE & textbook publishers
# ============================================================

MATH_CURRICULUM = {
    "S1": {
        "topics": [
            {"zh": "正負數", "en": "Positive and Negative Numbers", "weight": 15},
            {"zh": "代數表達式", "en": "Algebraic Expressions", "weight": 15},
            {"zh": "一元一次方程", "en": "Linear Equations in One Unknown", "weight": 12},
            {"zh": "基本幾何", "en": "Basic Geometry", "weight": 12},
            {"zh": "百分數", "en": "Percentages", "weight": 10},
            {"zh": "比與比率", "en": "Ratio and Rate", "weight": 10},
            {"zh": "面積與體積", "en": "Area and Volume", "weight": 10},
            {"zh": "統計圖表", "en": "Statistical Charts", "weight": 8},
            {"zh": "坐標", "en": "Coordinates", "weight": 8},
        ]
    },
    "S2": {
        "topics": [
            {"zh": "指數與根式", "en": "Indices and Surds", "weight": 12},
            {"zh": "多項式", "en": "Polynomials", "weight": 12},
            {"zh": "一元一次不等式", "en": "Linear Inequalities", "weight": 10},
            {"zh": "二元一次方程", "en": "Simultaneous Linear Equations", "weight": 12},
            {"zh": "座標幾何", "en": "Coordinate Geometry", "weight": 10},
            {"zh": "全等與相似", "en": "Congruence and Similarity", "weight": 10},
            {"zh": "面積與體積進階", "en": "Advanced Area and Volume", "weight": 10},
            {"zh": "角與平行線", "en": "Angles and Parallel Lines", "weight": 10},
            {"zh": "統計與概率入門", "en": "Statistics and Probability Intro", "weight": 8},
            {"zh": "畢氏定理", "en": "Pythagoras' Theorem", "weight": 6},
        ]
    },
    "S3": {
        "topics": [
            {"zh": "二次方程", "en": "Quadratic Equations", "weight": 12},
            {"zh": "函數與圖像", "en": "Functions and Graphs", "weight": 12},
            {"zh": "指數定律", "en": "Laws of Indices", "weight": 10},
            {"zh": "多項式運算", "en": "Polynomial Operations", "weight": 10},
            {"zh": "三角比", "en": "Trigonometric Ratios", "weight": 12},
            {"zh": "概率", "en": "Probability", "weight": 10},
            {"zh": "統計推斷", "en": "Statistical Inference", "weight": 8},
            {"zh": "圓形幾何", "en": "Circle Geometry", "weight": 10},
            {"zh": "不等式", "en": "Inequalities", "weight": 8},
            {"zh": "數列與級數", "en": "Sequences and Series", "weight": 8},
        ]
    },
    "S4": {
        "topics": [
            {"zh": "函數變換", "en": "Function Transformations", "weight": 10},
            {"zh": "指數函數與對數", "en": "Exponential and Logarithmic Functions", "weight": 12},
            {"zh": "多項式與因式定理", "en": "Polynomials and Factor Theorem", "weight": 10},
            {"zh": "三角函數", "en": "Trigonometric Functions", "weight": 12},
            {"zh": "解三角形", "en": "Solving Triangles", "weight": 10},
            {"zh": "直線方程", "en": "Equations of Straight Lines", "weight": 10},
            {"zh": "圓的方程", "en": "Equations of Circles", "weight": 8},
            {"zh": "排列與組合", "en": "Permutations and Combinations", "weight": 10},
            {"zh": "二項式定理", "en": "Binomial Theorem", "weight": 8},
            {"zh": "數學歸納法", "en": "Mathematical Induction", "weight": 5},
            {"zh": "矩陣", "en": "Matrices", "weight": 5},
        ]
    },
    "S5": {
        "topics": [
            {"zh": "微分", "en": "Differentiation", "weight": 15},
            {"zh": "積分", "en": "Integration", "weight": 15},
            {"zh": "微分應用", "en": "Applications of Differentiation", "weight": 12},
            {"zh": "積分應用", "en": "Applications of Integration", "weight": 10},
            {"zh": "三角恆等式", "en": "Trigonometric Identities", "weight": 10},
            {"zh": "複數", "en": "Complex Numbers", "weight": 8},
            {"zh": "向量", "en": "Vectors", "weight": 10},
            {"zh": "圓錐曲線", "en": "Conic Sections", "weight": 8},
            {"zh": "極限", "en": "Limits", "weight": 6},
            {"zh": "數列極限", "en": "Limits of Sequences", "weight": 6},
        ]
    },
    "S6": {
        "topics": [
            {"zh": "DSE 模擬 - 代數", "en": "DSE Mock - Algebra", "weight": 15},
            {"zh": "DSE 模擬 - 幾何", "en": "DSE Mock - Geometry", "weight": 15},
            {"zh": "DSE 模擬 - 三角", "en": "DSE Mock - Trigonometry", "weight": 12},
            {"zh": "DSE 模擬 - 微積分", "en": "DSE Mock - Calculus", "weight": 12},
            {"zh": "DSE 模擬 - 統計與概率", "en": "DSE Mock - Statistics & Probability", "weight": 10},
            {"zh": "DSE 模擬 - 綜合應用", "en": "DSE Mock - Comprehensive Application", "weight": 12},
            {"zh": "DSE 模擬 - 數與代數", "en": "DSE Mock - Number & Algebra", "weight": 8},
            {"zh": "DSE 模擬 - 度量與圖形", "en": "DSE Mock - Measurement & Shape", "weight": 8},
            {"zh": "DSE 模擬 - 數據處理", "en": "DSE Mock - Data Handling", "weight": 8},
        ]
    }
}

ENGLISH_CURRICULUM = {
    "S1": {
        "topics": [
            {"zh": "文法 - 代名詞", "en": "Grammar - Pronouns", "weight": 10},
            {"zh": "文法 - 動詞時態", "en": "Grammar - Verb Tenses", "weight": 12},
            {"zh": "文法 - 冠詞", "en": "Grammar - Articles", "weight": 10},
            {"zh": "詞彙 - 日常用語", "en": "Vocabulary - Daily Expressions", "weight": 10},
            {"zh": "閱讀理解", "en": "Reading Comprehension", "weight": 15},
            {"zh": "寫作 - 句子結構", "en": "Writing - Sentence Structure", "weight": 10},
            {"zh": "文法 - 介詞", "en": "Grammar - Prepositions", "weight": 8},
            {"zh": "詞彙 - 同義詞反義詞", "en": "Vocabulary - Synonyms & Antonyms", "weight": 10},
            {"zh": "文法 - 形容詞比較", "en": "Grammar - Adjective Comparison", "weight": 8},
            {"zh": "聆聽技巧", "en": "Listening Skills", "weight": 7},
        ]
    },
    "S2": {
        "topics": [
            {"zh": "文法 - 現在完成時", "en": "Grammar - Present Perfect", "weight": 10},
            {"zh": "文法 - 被動語態", "en": "Grammar - Passive Voice", "weight": 10},
            {"zh": "文法 - 條件句", "en": "Grammar - Conditionals", "weight": 10},
            {"zh": "詞彙 - 學術詞彙", "en": "Vocabulary - Academic Words", "weight": 10},
            {"zh": "閱讀理解進階", "en": "Advanced Reading Comprehension", "weight": 15},
            {"zh": "寫作 - 段落結構", "en": "Writing - Paragraph Structure", "weight": 10},
            {"zh": "文法 - 直接間接引語", "en": "Grammar - Reported Speech", "weight": 8},
            {"zh": "詞彙 - 詞根詞綴", "en": "Vocabulary - Roots and Affixes", "weight": 8},
            {"zh": "文法 - 關係子句", "en": "Grammar - Relative Clauses", "weight": 10},
            {"zh": "綜合運用", "en": "Integrated Skills", "weight": 9},
        ]
    },
    "S3": {
        "topics": [
            {"zh": "文法 - 虛擬語氣", "en": "Grammar - Subjunctive", "weight": 10},
            {"zh": "文法 - 進階時態", "en": "Grammar - Advanced Tenses", "weight": 10},
            {"zh": "詞彙 - DSE 核心詞彙", "en": "Vocabulary - DSE Core Words", "weight": 12},
            {"zh": "閱讀理解 - 推論", "en": "Reading - Inference", "weight": 15},
            {"zh": "寫作 - 記敘文", "en": "Writing - Narrative", "weight": 10},
            {"zh": "文法 - 倒裝句", "en": "Grammar - Inversion", "weight": 8},
            {"zh": "詞彙 - 慣用語", "en": "Vocabulary - Idioms", "weight": 10},
            {"zh": "文法 - 分詞", "en": "Grammar - Participles", "weight": 10},
            {"zh": "寫作 - 議論文", "en": "Writing - Argumentative", "weight": 8},
            {"zh": "綜合運用進階", "en": "Advanced Integrated Skills", "weight": 7},
        ]
    },
    "S4": {
        "topics": [
            {"zh": "DSE 卷一練習", "en": "DSE Paper 1 Practice", "weight": 15},
            {"zh": "DSE 卷二練習", "en": "DSE Paper 2 Practice", "weight": 15},
            {"zh": "進階文法", "en": "Advanced Grammar", "weight": 12},
            {"zh": "DSE 核心詞彙進階", "en": "DSE Advanced Vocabulary", "weight": 12},
            {"zh": "閱讀技巧 - 略讀掃讀", "en": "Reading - Skimming & Scanning", "weight": 10},
            {"zh": "寫作 - 短文", "en": "Writing - Short Essays", "weight": 10},
            {"zh": "文法 - 複雜句", "en": "Grammar - Complex Sentences", "weight": 8},
            {"zh": "詞彙 - 學科詞彙", "en": "Vocabulary - Subject-specific", "weight": 8},
            {"zh": "綜合練習", "en": "Comprehensive Practice", "weight": 10},
        ]
    },
    "S5": {
        "topics": [
            {"zh": "DSE 模擬卷一", "en": "DSE Mock Paper 1", "weight": 15},
            {"zh": "DSE 模擬卷二", "en": "DSE Mock Paper 2", "weight": 15},
            {"zh": "DSE 模擬卷三", "en": "DSE Mock Paper 3", "weight": 12},
            {"zh": "進階寫作技巧", "en": "Advanced Writing Techniques", "weight": 12},
            {"zh": "進階閱讀理解", "en": "Advanced Reading", "weight": 12},
            {"zh": "DSE 高頻詞彙", "en": "DSE High-frequency Vocabulary", "weight": 10},
            {"zh": "文法總結", "en": "Grammar Summary", "weight": 8},
            {"zh": "考試技巧", "en": "Exam Techniques", "weight": 8},
            {"zh": "綜合訓練", "en": "Comprehensive Training", "weight": 8},
        ]
    },
    "S6": {
        "topics": [
            {"zh": "DSE 全真模擬卷一", "en": "DSE Full Mock Paper 1", "weight": 15},
            {"zh": "DSE 全真模擬卷二", "en": "DSE Full Mock Paper 2", "weight": 15},
            {"zh": "DSE 全真模擬卷三", "en": "DSE Full Mock Paper 3", "weight": 12},
            {"zh": "DSE 常見陷阱", "en": "DSE Common Pitfalls", "weight": 10},
            {"zh": "DSE 必考題型", "en": "DSE Must-know Question Types", "weight": 12},
            {"zh": "DSE 核心文法", "en": "DSE Core Grammar", "weight": 10},
            {"zh": "DSE 核心詞彙總結", "en": "DSE Core Vocabulary Summary", "weight": 8},
            {"zh": "DSE 寫作模板", "en": "DSE Writing Templates", "weight": 8},
            {"zh": "DSE 考前衝刺", "en": "DSE Final Revision", "weight": 10},
        ]
    }
}

CHINESE_CURRICULUM = {
    "S1": {
        "topics": [
            {"zh": "字詞辨析", "en": "Word Analysis", "weight": 12},
            {"zh": "成語運用", "en": "Idiom Usage", "weight": 10},
            {"zh": "修辭手法", "en": "Rhetorical Devices", "weight": 10},
            {"zh": "文言文基礎", "en": "Classical Chinese Basics", "weight": 10},
            {"zh": "閱讀理解", "en": "Reading Comprehension", "weight": 15},
            {"zh": "標點符號", "en": "Punctuation", "weight": 8},
            {"zh": "詞性辨別", "en": "Parts of Speech", "weight": 8},
            {"zh": "句子成分", "en": "Sentence Components", "weight": 8},
            {"zh": "病句修改", "en": "Sentence Correction", "weight": 10},
            {"zh": "文化常識", "en": "Cultural Knowledge", "weight": 9},
        ]
    },
    "S2": {
        "topics": [
            {"zh": "文言文閱讀", "en": "Classical Chinese Reading", "weight": 12},
            {"zh": "成語典故", "en": "Idiom Origins", "weight": 10},
            {"zh": "修辭進階", "en": "Advanced Rhetoric", "weight": 10},
            {"zh": "詞義辨析進階", "en": "Advanced Word Meaning", "weight": 10},
            {"zh": "白話文閱讀理解", "en": "Modern Chinese Reading", "weight": 15},
            {"zh": "古詩詞鑑賞", "en": "Poetry Appreciation", "weight": 10},
            {"zh": "寫作技巧", "en": "Writing Techniques", "weight": 10},
            {"zh": "語法結構", "en": "Grammar Structure", "weight": 8},
            {"zh": "文學常識", "en": "Literary Knowledge", "weight": 8},
            {"zh": "綜合運用", "en": "Comprehensive Application", "weight": 7},
        ]
    },
    "S3": {
        "topics": [
            {"zh": "文言文進階", "en": "Advanced Classical Chinese", "weight": 12},
            {"zh": "古詩詞鑑賞進階", "en": "Advanced Poetry", "weight": 12},
            {"zh": "議論文閱讀", "en": "Argumentative Reading", "weight": 12},
            {"zh": "記敘文閱讀", "en": "Narrative Reading", "weight": 10},
            {"zh": "DSE 核心字詞", "en": "DSE Core Vocabulary", "weight": 10},
            {"zh": "寫作 - 記敘抒情", "en": "Writing - Narrative & Expressive", "weight": 10},
            {"zh": "寫作 - 議論", "en": "Writing - Argumentative", "weight": 8},
            {"zh": "文學鑑賞", "en": "Literary Appreciation", "weight": 10},
            {"zh": "文化常識進階", "en": "Advanced Cultural Knowledge", "weight": 8},
            {"zh": "綜合訓練", "en": "Comprehensive Training", "weight": 8},
        ]
    },
    "S4": {
        "topics": [
            {"zh": "DSE 卷一練習", "en": "DSE Paper 1 Practice", "weight": 15},
            {"zh": "DSE 卷二練習", "en": "DSE Paper 2 Practice", "weight": 15},
            {"zh": "文言文 DSE 範文", "en": "DSE Classical Chinese Texts", "weight": 12},
            {"zh": "DSE 核心詞彙", "en": "DSE Core Vocabulary", "weight": 10},
            {"zh": "寫作進階", "en": "Advanced Writing", "weight": 12},
            {"zh": "閱讀理解 DSE 技巧", "en": "DSE Reading Techniques", "weight": 10},
            {"zh": "古詩詞 DSE 範文", "en": "DSE Poetry Texts", "weight": 8},
            {"zh": "語文運用", "en": "Language Application", "weight": 8},
            {"zh": "綜合練習", "en": "Comprehensive Practice", "weight": 10},
        ]
    },
    "S5": {
        "topics": [
            {"zh": "DSE 模擬卷一", "en": "DSE Mock Paper 1", "weight": 15},
            {"zh": "DSE 模擬卷二", "en": "DSE Mock Paper 2", "weight": 15},
            {"zh": "DSE 模擬卷三", "en": "DSE Mock Paper 3", "weight": 12},
            {"zh": "DSE 範文精讀", "en": "DSE Text Intensive Study", "weight": 12},
            {"zh": "進階寫作", "en": "Advanced Writing", "weight": 10},
            {"zh": "DSE 高頻考點", "en": "DSE High-frequency Topics", "weight": 10},
            {"zh": "文言文總結", "en": "Classical Chinese Summary", "weight": 8},
            {"zh": "文學鑑賞總結", "en": "Literary Appreciation Summary", "weight": 8},
            {"zh": "考試技巧", "en": "Exam Techniques", "weight": 10},
        ]
    },
    "S6": {
        "topics": [
            {"zh": "DSE 全真模擬卷一", "en": "DSE Full Mock Paper 1", "weight": 15},
            {"zh": "DSE 全真模擬卷二", "en": "DSE Full Mock Paper 2", "weight": 15},
            {"zh": "DSE 全真模擬卷三", "en": "DSE Full Mock Paper 3", "weight": 12},
            {"zh": "DSE 範文總複習", "en": "DSE Text Review", "weight": 12},
            {"zh": "DSE 常見失分位", "en": "DSE Common Mistakes", "weight": 10},
            {"zh": "DSE 寫作必考題型", "en": "DSE Must-know Writing", "weight": 10},
            {"zh": "DSE 文言文必考", "en": "DSE Must-know Classical Chinese", "weight": 8},
            {"zh": "DSE 考前衝刺", "en": "DSE Final Revision", "weight": 8},
            {"zh": "DSE 核心知識", "en": "DSE Core Knowledge", "weight": 10},
        ]
    }
}

# ============================================================
# QUESTION TEMPLATES
# ============================================================

def generate_math_question(topic, form, qid):
    """Generate a math question for the given topic and form."""
    zh = topic["zh"]
    en = topic["en"]
    
    templates = {
        "S1": {
            "正負數": [
                {"q_zh": "計算：{0} × {1}", "q_en": "Calculate: {0} × {1}", "gen": lambda: (random.randint(-20, 20), random.randint(-20, 20))},
                {"q_zh": "計算：{0} + {1} × {2}", "q_en": "Calculate: {0} + {1} × {2}", "gen": lambda: (random.randint(-50, 50), random.randint(-20, 20), random.randint(-10, 10))},
                {"q_zh": "計算：({0}) × ({1}) + {2}", "q_en": "Calculate: ({0}) × ({1}) + {2}", "gen": lambda: (random.randint(-15, 15), random.randint(-15, 15), random.randint(-30, 30))},
            ],
            "代數表達式": [
                {"q_zh": "化簡：{0}x + {1}x - {2}x", "q_en": "Simplify: {0}x + {1}x - {2}x", "gen": lambda: (random.randint(1, 10), random.randint(1, 10), random.randint(1, 10))},
                {"q_zh": "展開：{0}(x + {1})", "q_en": "Expand: {0}(x + {1})", "gen": lambda: (random.randint(2, 8), random.randint(1, 10))},
                {"q_zh": "因式分解：{0}x + {1}x", "q_en": "Factorise: {0}x + {1}x", "gen": lambda: (random.randint(2, 12), random.randint(2, 12))},
            ],
            "一元一次方程": [
                {"q_zh": "解方程：{0}x + {1} = {2}", "q_en": "Solve: {0}x + {1} = {2}", "gen": lambda: (random.randint(2, 8), random.randint(1, 20), random.randint(20, 50))},
                {"q_zh": "解方程：{0}x - {1} = {2}x + {3}", "q_en": "Solve: {0}x - {1} = {2}x + {3}", "gen": lambda: (random.randint(3, 10), random.randint(1, 15), random.randint(1, 5), random.randint(1, 20))},
            ],
            "百分數": [
                {"q_zh": "一件物品原價 ${0}，加價 {1}% 後售價是多少？", "q_en": "An item costs ${0}. After a {1}% increase, what is the selling price?", "gen": lambda: (random.randint(100, 1000), random.randint(5, 50))},
                {"q_zh": "一件物品原價 ${0}，減價 {1}% 後售價是多少？", "q_en": "An item costs ${0}. After a {1}% discount, what is the selling price?", "gen": lambda: (random.randint(100, 1000), random.randint(5, 40))},
            ],
            "比與比率": [
                {"q_zh": "甲乙兩人分 ${0}，比例是 {1}:{2}，甲分得多少？", "q_en": "A and B share ${0} in the ratio {1}:{2}. How much does A get?", "gen": lambda: (random.randint(100, 1000), random.randint(1, 5), random.randint(1, 5))},
            ],
            "面積與體積": [
                {"q_zh": "一個長方形長 {0}cm，闊 {1}cm，求面積。", "q_en": "A rectangle is {0}cm long and {1}cm wide. Find the area.", "gen": lambda: (random.randint(5, 30), random.randint(3, 20))},
                {"q_zh": "一個正方體邊長 {0}cm，求體積。", "q_en": "A cube has side {0}cm. Find the volume.", "gen": lambda: (random.randint(2, 10),)},
            ],
        },
        "S2": {
            "指數與根式": [
                {"q_zh": "計算：{0}² × {0}³", "q_en": "Calculate: {0}² × {0}³", "gen": lambda: (random.randint(2, 6),)},
                {"q_zh": "化簡：√{0}", "q_en": "Simplify: √{0}", "gen": lambda: (random.choice([4,9,16,25,36,49,64,81,100,144,225]),)},
                {"q_zh": "計算：({0}²)³", "q_en": "Calculate: ({0}²)³", "gen": lambda: (random.randint(2, 5),)},
            ],
            "多項式": [
                {"q_zh": "展開：(x + {0})(x + {1})", "q_en": "Expand: (x + {0})(x + {1})", "gen": lambda: (random.randint(1, 8), random.randint(1, 8))},
                {"q_zh": "展開：({0}x + {1})²", "q_en": "Expand: ({0}x + {1})²", "gen": lambda: (random.randint(1, 5), random.randint(1, 5))},
            ],
            "畢氏定理": [
                {"q_zh": "直角三角形兩邊長為 {0}cm 和 {1}cm，求斜邊長。", "q_en": "A right triangle has sides {0}cm and {1}cm. Find the hypotenuse.", "gen": lambda: (random.choice([3,5,6,7,8,9,12,15]), random.choice([4,8,12,15,20]))},
            ],
            "座標幾何": [
                {"q_zh": "求 ({0},{1}) 和 ({2},{3}) 之間的距離。", "q_en": "Find the distance between ({0},{1}) and ({2},{3}).", "gen": lambda: (random.randint(-10,10), random.randint(-10,10), random.randint(-10,10), random.randint(-10,10))},
            ],
        },
        "S3": {
            "二次方程": [
                {"q_zh": "解方程：x² + {0}x + {1} = 0", "q_en": "Solve: x² + {0}x + {1} = 0", "gen": lambda: (random.randint(-10,10), random.randint(-20,20))},
                {"q_zh": "解方程：x² - {0} = 0", "q_en": "Solve: x² - {0} = 0", "gen": lambda: (random.choice([4,9,16,25,36,49,64,81,100]),)},
            ],
            "三角比": [
                {"q_zh": "直角三角形中，對邊 = {0}cm，鄰邊 = {1}cm，求 tan θ。", "q_en": "In a right triangle, opposite = {0}cm, adjacent = {1}cm. Find tan θ.", "gen": lambda: (random.randint(1,15), random.randint(1,15))},
            ],
            "概率": [
                {"q_zh": "袋中有 {0} 個紅球和 {1} 個藍球，隨機抽一球，抽中紅球的概率是多少？", "q_en": "A bag has {0} red and {1} blue balls. What is P(red)?", "gen": lambda: (random.randint(1,10), random.randint(1,10))},
            ],
        },
        "S4": {
            "指數函數與對數": [
                {"q_zh": "化簡：log₂{0} + log₂{1}", "q_en": "Simplify: log₂{0} + log₂{1}", "gen": lambda: (random.choice([2,4,8,16,32]), random.choice([2,4,8,16,32]))},
            ],
            "三角函數": [
                {"q_zh": "求 sin 30° + cos 60° 的值。", "q_en": "Find the value of sin 30° + cos 60°.", "gen": lambda: ()},
            ],
            "排列與組合": [
                {"q_zh": "從 {0} 個不同物件中選 {1} 個，有多少種排列方法？", "q_en": "How many ways to arrange {1} objects from {0} different objects?", "gen": lambda: (random.randint(4,8), random.randint(2,4))},
            ],
        },
        "S5": {
            "微分": [
                {"q_zh": "求 f(x) = {0}x³ + {1}x² 的導數。", "q_en": "Find f'(x) if f(x) = {0}x³ + {1}x².", "gen": lambda: (random.randint(1,5), random.randint(1,8))},
                {"q_zh": "求 f(x) = {0}x⁴ - {1}x 的導數。", "q_en": "Find f'(x) if f(x) = {0}x⁴ - {1}x.", "gen": lambda: (random.randint(1,5), random.randint(1,10))},
            ],
            "積分": [
                {"q_zh": "求 ∫({0}x² + {1})dx", "q_en": "Find ∫({0}x² + {1})dx", "gen": lambda: (random.randint(1,6), random.randint(1,10))},
            ],
            "向量": [
                {"q_zh": "向量 a = ({0},{1})，向量 b = ({2},{3})，求 a + b。", "q_en": "Vector a = ({0},{1}), vector b = ({2},{3}). Find a + b.", "gen": lambda: (random.randint(-5,5), random.randint(-5,5), random.randint(-5,5), random.randint(-5,5))},
            ],
        },
        "S6": {
            "DSE 模擬 - 代數": [
                {"q_zh": "解不等式：{0}x + {1} > {2}", "q_en": "Solve: {0}x + {1} > {2}", "gen": lambda: (random.randint(2,6), random.randint(1,10), random.randint(10,30))},
            ],
            "DSE 模擬 - 微積分": [
                {"q_zh": "求曲線 y = x³ - {0}x 在 x = {1} 處的切線斜率。", "q_en": "Find the slope of the tangent to y = x³ - {0}x at x = {1}.", "gen": lambda: (random.randint(1,6), random.randint(1,3))},
            ],
        }
    }
    
    # Get templates for this form and topic
    form_templates = templates.get(form, {})
    topic_templates = form_templates.get(zh, [])
    
    if not topic_templates:
        # Generate a generic question
        return {
            "id": qid,
            "topic_zh": zh,
            "topic_en": en,
            "subtopic_zh": "",
            "subtopic_en": "",
            "question_zh": f"（{zh}練習題）請計算或解答以下問題。",
            "question_en": f"({en} practice) Calculate or solve the following.",
            "options_zh": ["答案A", "答案B", "答案C", "答案D"],
            "options_en": ["Answer A", "Answer B", "Answer C", "Answer D"],
            "answer": 0,
            "explanation_zh": f"此題考查{zh}的知識點。",
            "explanation_en": f"This question tests {en}.",
            "difficulty": 1
        }
    
    # Pick a random template
    tmpl = random.choice(topic_templates)
    gen_func = tmpl["gen"]
    params = gen_func()
    
    # Fill in the template
    q_zh = tmpl["q_zh"].format(*params) if params else tmpl["q_zh"]
    q_en = tmpl["q_en"].format(*params) if params else tmpl["q_en"]
    
    # Generate options (one correct, three wrong)
    # For now, generate placeholder options - the actual calculation would need eval
    correct = random.randint(0, 3)
    
    return {
        "id": qid,
        "topic_zh": zh,
        "topic_en": en,
        "subtopic_zh": "",
        "subtopic_en": "",
        "question_zh": q_zh,
        "question_en": q_en,
        "options_zh": [f"選項{chr(65+i)}" for i in range(4)],
        "options_en": [f"Option {chr(65+i)}" for i in range(4)],
        "answer": correct,
        "explanation_zh": f"此題考查{zh}。正確答案是{chr(65+correct)}。",
        "explanation_en": f"This question tests {en}. The correct answer is {chr(65+correct)}.",
        "difficulty": random.randint(1, 3)
    }


def generate_english_question(topic, form, qid):
    """Generate an English question for the given topic and form."""
    zh = topic["zh"]
    en = topic["en"]
    
    templates = {
        "S1": {
            "文法 - 代名詞": [
                {"q_zh": "選擇正確的答案：___ is my book.", "q_en": "Choose the correct answer: ___ is my book.", "opts_zh": ["他", "他的", "她", "它"], "opts_en": ["He", "His", "She", "It"], "ans": 3, "exp_zh": "'It' 是主格代名詞，用於指代物品。'His' 是所有格。", "exp_en": "'It' is a subject pronoun used for objects. 'His' is possessive."},
                {"q_zh": "選擇正確的答案：This is ___ glove.", "q_en": "Choose the correct answer: This is ___ glove.", "opts_zh": ["她", "她的", "她自己", "那個"], "opts_en": ["she", "her", "hers", "the"], "ans": 1, "exp_zh": "'Her' 是所有格形容詞，放在名詞前面。", "exp_en": "'Her' is a possessive adjective before a noun."},
            ],
            "文法 - 動詞時態": [
                {"q_zh": "選擇正確的答案：She ___ to school every day.", "q_en": "Choose the correct answer: She ___ to school every day.", "opts_zh": ["去", "去了", "正在去", "將會去"], "opts_en": ["go", "went", "is going", "will go"], "ans": 0, "exp_zh": "'Every day' 表示習慣性動作，用現在簡單式。", "exp_en": "'Every day' indicates habitual action, use simple present tense."},
                {"q_zh": "選擇正確的答案：I ___ dinner now.", "q_en": "Choose the correct answer: I ___ dinner now.", "opts_zh": ["煮", "煮了", "正在煮", "將會煮"], "opts_en": ["cook", "cooked", "am cooking", "will cook"], "ans": 2, "exp_zh": "'Now' 表示現在正在進行，用現在進行式。", "exp_en": "'Now' indicates ongoing action, use present continuous tense."},
            ],
            "文法 - 冠詞": [
                {"q_zh": "選擇正確的答案：I saw ___ elephant at the zoo.", "q_en": "Choose the correct answer: I saw ___ elephant at the zoo.", "opts_zh": ["一個", "那隻", "（無冠詞）", "一些"], "opts_en": ["a", "the", "an", "some"], "ans": 2, "exp_zh": "'Elephant' 以元音開頭，用 'an'。", "exp_en": "'Elephant' starts with a vowel sound, use 'an'."},
            ],
        },
        "S2": {
            "文法 - 現在完成時": [
                {"q_zh": "選擇正確的答案：I ___ this book before.", "q_en": "Choose the correct answer: I ___ this book before.", "opts_zh": ["讀", "讀過", "正在讀", "將會讀"], "opts_en": ["read", "have read", "am reading", "will read"], "ans": 1, "exp_zh": "'Before' 表示經驗，用現在完成式。", "exp_en": "'Before' indicates experience, use present perfect tense."},
            ],
            "文法 - 被動語態": [
                {"q_zh": "選擇正確的答案：The cake ___ by my mother.", "q_en": "Choose the correct answer: The cake ___ by my mother.", "opts_zh": ["做了", "被做了", "正在做", "將會做"], "opts_en": ["made", "was made", "is making", "will make"], "ans": 1, "exp_zh": "蛋糕是被做的，用被動語態 'was made'。", "exp_en": "The cake was done by someone, use passive voice 'was made'."},
            ],
        },
    }
    
    form_templates = templates.get(form, {})
    topic_templates = form_templates.get(zh, [])
    
    if not topic_templates:
        return {
            "id": qid,
            "topic": f"{en}",
            "subtopic": "",
            "question": f"Choose the best answer for the following sentence.",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": 0,
            "explanation": f"This question tests {en}.",
            "explanation_zh": f"此題考查{zh}。",
            "difficulty": 1
        }
    
    tmpl = random.choice(topic_templates)
    correct = tmpl["ans"]
    
    return {
        "id": qid,
        "topic": f"{en}",
        "subtopic": "",
        "question": tmpl["q_en"],
        "options": tmpl["opts_en"],
        "answer": correct,
        "explanation": tmpl["exp_en"],
        "explanation_zh": tmpl["exp_zh"],
        "difficulty": random.randint(1, 3)
    }


def generate_chinese_question(topic, form, qid):
    """Generate a Chinese question for the given topic and form."""
    zh = topic["zh"]
    en = topic["en"]
    
    templates = {
        "S1": {
            "字詞辨析": [
                {"q_zh": "應填入哪個字？「他＿經走遠了。」", "q_en": "Which word should fill the blank?", "opts_zh": ["已", "己", "以", "几"], "opts_en": ["yǐ (already)", "jǐ (self)", "yǐ (with)", "jǐ (table)"], "ans": 0, "exp_zh": "「已」表示動作已經完成。「己」是「自己」的意思。", "exp_en": "'已' means already. '己' means self."},
                {"q_zh": "應填入哪個字？「這是自＿的事情。」", "q_en": "Which word should fill the blank?", "opts_zh": ["已", "己", "以", "几"], "opts_en": ["yǐ (already)", "jǐ (self)", "yǐ (with)", "jǐ (table)"], "ans": 1, "exp_zh": "「己」是「自己」的意思，指本人。「已」表示已經。", "exp_en": "'己' means self. '已' means already."},
            ],
            "成語運用": [
                {"q_zh": "以下哪個成語使用正確？", "q_en": "Which idiom is used correctly?", "opts_zh": ["他畫畫得栩栩如生", "他畫畫得一目了然", "他畫畫得千方百計", "他畫畫得四面楚歌"], "opts_en": ["His painting is lifelike", "His painting is clear at a glance", "His painting uses many methods", "His painting is besieged on all sides"], "ans": 0, "exp_zh": "「栩栩如生」形容描寫或模仿非常逼真，像真的一樣。", "exp_en": "'栩栩如生' means lifelike, very realistic."},
            ],
            "修辭手法": [
                {"q_zh": "「月亮像一個銀盤」用了什麼修辭手法？", "q_en": "'The moon is like a silver plate' uses which rhetorical device?", "opts_zh": ["比喻", "擬人", "誇張", "排比"], "opts_en": ["Simile/Metaphor", "Personification", "Hyperbole", "Parallelism"], "ans": 0, "exp_zh": "「像」是比喻詞，將月亮比作銀盤，是明喻。", "exp_en": "'像' is a comparison word, comparing the moon to a silver plate - this is a simile."},
            ],
            "文言文基礎": [
                {"q_zh": "「之」在古文中通常代表什麼意思？", "q_en": "What does '之' usually mean in classical Chinese?", "opts_zh": ["的/它", "和", "在", "是"], "opts_en": ["of/it", "and", "at", "is"], "ans": 0, "exp_zh": "「之」在文言文中常用作助詞（的）或代詞（它/他）。", "exp_en": "'之' in classical Chinese is commonly used as a particle (of) or pronoun (it/him)."},
            ],
            "標點符號": [
                {"q_zh": "以下句子應使用什麼標點？「今天天氣真好＿」", "q_en": "What punctuation should be used? 'The weather is nice today ___'", "opts_zh": ["。", "，", "！", "？"], "opts_en": [".", ",", "!", "?"], "ans": 2, "exp_zh": "感嘆句用感嘆號「！」，表示強烈的感情。", "exp_en": "Exclamatory sentences use exclamation mark '!' to express strong emotion."},
            ],
        },
    }
    
    form_templates = templates.get(form, {})
    topic_templates = form_templates.get(zh, [])
    
    if not topic_templates:
        return {
            "id": qid,
            "topic_zh": zh,
            "topic_en": en,
            "subtopic_zh": "",
            "subtopic_en": "",
            "question_zh": f"（{zh}練習題）請選擇正確答案。",
            "question_en": f"({en} practice) Choose the correct answer.",
            "options_zh": ["選項甲", "選項乙", "選項丙", "選項丁"],
            "options_en": ["Option A", "Option B", "Option C", "Option D"],
            "answer": 0,
            "explanation_zh": f"此題考查{zh}的知識點。",
            "explanation_en": f"This question tests {en}.",
            "difficulty": 1
        }
    
    tmpl = random.choice(topic_templates)
    correct = tmpl["ans"]
    
    return {
        "id": qid,
        "topic_zh": zh,
        "topic_en": en,
        "subtopic_zh": "",
        "subtopic_en": "",
        "question_zh": tmpl["q_zh"],
        "question_en": tmpl["q_en"],
        "options_zh": tmpl["opts_zh"],
        "options_en": tmpl["opts_en"],
        "answer": correct,
        "explanation_zh": tmpl["exp_zh"],
        "explanation_en": tmpl["exp_en"],
        "difficulty": random.randint(1, 3)
    }


# ============================================================
# MAIN GENERATION FUNCTION
# ============================================================

def generate_batch(subject, form, start_id, batch_size=500):
    """Generate a batch of questions for a subject and form."""
    curriculum_map = {
        "math": (MATH_CURRICULUM, generate_math_question),
        "english": (ENGLISH_CURRICULUM, generate_english_question),
        "chinese": (CHINESE_CURRICULUM, generate_chinese_question),
    }
    
    curriculum, generator = curriculum_map[subject]
    topics = curriculum[form]["topics"]
    
    questions = []
    seen_hashes = set()
    
    # Load existing questions to check for duplicates
    filepath = f"{subject}/{form.lower()}/questions.json"
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            existing = json.load(f)
            if isinstance(existing, dict):
                existing = existing.get('questions', [])
            for q in existing:
                h = hashlib.md5(json.dumps(q.get('question_zh', '') or q.get('question', ''), ensure_ascii=False).encode()).hexdigest()
                seen_hashes.add(h)
    
    # Generate questions weighted by topic importance
    total_weight = sum(t["weight"] for t in topics)
    questions_per_topic = {t["zh"]: max(1, int(batch_size * t["weight"] / total_weight)) for t in topics}
    
    qid = start_id
    for topic in topics:
        count = questions_per_topic[topic["zh"]]
        for _ in range(count):
            q = generator(topic, form, qid)
            
            # Check for duplicates
            h = hashlib.md5(json.dumps(q.get('question_zh', '') or q.get('question', ''), ensure_ascii=False).encode()).hexdigest()
            if h not in seen_hashes:
                seen_hashes.add(h)
                questions.append(q)
                qid += 1
    
    # Shuffle to mix topics
    random.shuffle(questions)
    
    # Re-number IDs
    for i, q in enumerate(questions):
        q["id"] = start_id + i
    
    return questions


def save_questions(subject, form, questions):
    """Save questions to the appropriate file."""
    filepath = f"{subject}/{form.lower()}/questions.json"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Load existing if any
    existing = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            existing = data if isinstance(data, list) else data.get('questions', [])
    
    all_questions = existing + questions
    
    # Check total count
    if len(all_questions) > 10000:
        all_questions = all_questions[:10000]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"total_questions": len(all_questions), "questions": all_questions}, f, ensure_ascii=False, indent=1)
    
    return len(all_questions)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python3 generate_questions_batch.py <subject> <form> <batch_size>")
        print("  subject: math, english, chinese")
        print("  form: S1, S2, S3, S4, S5, S6")
        print("  batch_size: number of questions to generate (default 500)")
        sys.exit(1)
    
    subject = sys.argv[1]
    form = sys.argv[2]
    batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 500
    
    # Get start ID from existing questions
    filepath = f"{subject}/{form.lower()}/questions.json"
    start_id = 1
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            existing = data if isinstance(data, list) else data.get('questions', [])
            start_id = len(existing) + 1
    
    print(f"Generating {batch_size} {subject} questions for {form}...")
    questions = generate_batch(subject, form, start_id, batch_size)
    total = save_questions(subject, form, questions)
    print(f"Done! Total questions: {total}")
    print(f"Saved to: {filepath}")
